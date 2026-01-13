import asyncio
import edge_tts
import aiohttp
import genanki
import os
import json
import hashlib
import re
from google import genai
from google.genai import types
from config import my_model
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Error: GOOGLE_API_KEY environment variable not set.")

settings = None
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
if not settings:
    raise ValueError("Error: settings.json not found or invalid.")


client = genai.Client(api_key=GOOGLE_API_KEY)

def get_stable_filename(word: str) -> str:
    hash_object = hashlib.md5(word.lower().encode())
    return f"anki_{hash_object.hexdigest()}.mp3"

def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def clean_json_string(text: str) -> str:
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text


async def fetch_ipa(session, word: str) -> str:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return "" 
            data = await response.json()
            for phon in data[0].get('phonetics', []):
                if phon.get('text'):
                    return phon.get('text')
            return ""
    except Exception as e:
        print(f"Error fetching IPA for {word}: {e}")
        return ""

async def fetch_batch_ai_content(words: list[str]) -> dict[str, any]:

    prompt = f"""
    Act as a {settings["language"]} Dictionary API. I will give you a list of words.
    Words: {json.dumps(words)}
    
    Return a JSON Object where keys are the words (in lowercase).
    
    For each word provide:
    1. definition: A concise definition of the word.
    2. example: A sentence using the word in context.
    3. type: The part of speech (e.g., noun, verb, adj).
    4. collocation: A short 2-3 word common phrase using the word.
    
    Example Output format:
    {{
        "cloud": {{ "definition": "...", "example": "...", "type": "...", "collocation": "..." }},
        "hello": {{ "definition": "...", "example": "...", "type": "...", "collocation": "..." }}
    }}
    """
    
    try:

        response = await asyncio.to_thread(
            client.models.generate_content,
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        clean_text = response.text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3]
            
        data = json.loads(clean_text)
        return {k.lower(): v for k, v in data.items()}

    except Exception as e:
        print(f"Error : {e}")
        return {}

async def generate_audio(word: str, output_filename: str) -> str:
    communicate = edge_tts.Communicate(word, settings["voice"])
    await communicate.save(output_filename)
    return output_filename

async def process_single_card(session, word: str, ai_data: dict, media_files: list) -> genanki.Note:
    word_key = word.lower()
    if word_key not in ai_data:
        print(f"Gemini did not return data for '{word}'")
        return None
    
    definition = ai_data[word_key].get('definition', 'N/A')
    example = ai_data[word_key].get('example', 'N/A')
    word_type = ai_data[word_key].get('type', '')
    collocation = ai_data[word_key].get('collocation', '')

    filename = get_stable_filename(word)
    
    ipa_task = asyncio.create_task(fetch_ipa(session, word))
    audio_task = asyncio.create_task(generate_audio(word, filename))
    
    ipa_result, _ = await asyncio.gather(ipa_task, audio_task)
    
    media_files.append(filename)

    return genanki.Note(
        model=my_model,
        fields=[word, ipa_result,f"[sound:{filename}]", definition, example, word_type, collocation]
    )


def get_words_from_file(filepath: str) -> list:
    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words


async def main():
    
    words = get_words_from_file(settings["file_input"])
    all_notes = []
    media_files = []
    
    BATCH_SIZE = 6
    
    async with aiohttp.ClientSession() as session:
        
        for chunk in chunk_list(words, BATCH_SIZE):
            start_time = asyncio.get_running_loop().time()
            
            ai_results = await fetch_batch_ai_content(chunk)
            
            if not ai_results:
                print("Skipping batch due to AI fetch error.")
                continue
            
            tasks = [process_single_card(session, word, ai_results, media_files) for word in chunk]
            batch_notes = await asyncio.gather(*tasks)
            
            valid_notes = [n for n in batch_notes if n]
            all_notes.extend(valid_notes)
            
            elapsed = asyncio.get_running_loop().time() - start_time
            wait_time = max(0, 20 - elapsed) # Rate limit: 3 requests per minute, Can be adjusted, for me 20s works well.
            
            if wait_time > 0 and chunk != list(chunk_list(words, BATCH_SIZE))[-1]: 
                print(f"Waiting {wait_time:.2f}s to respect rate limits...")
                await asyncio.sleep(wait_time)

    if not all_notes:
        print("Done. No cards were created.")
        return

    my_deck = genanki.Deck(settings["deck_id"], settings["deck_name"])
    for note in all_notes:
        my_deck.add_note(note)

    package = genanki.Package(my_deck)
    package.media_files = media_files
    package.write_to_file(settings["file_out_name"])

    print(f"\n Finished {len(all_notes)} cards.")
    print(f"File: {settings['file_out_name']}")
    
    for f in media_files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    asyncio.run(main())