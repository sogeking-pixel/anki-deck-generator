# Anki Deck Generator

## Overview

This project is a Python-based automation tool designed to streamline the creation of language learning materials. Instead of manual data entry, this script acts as an **ETL (Extract, Transform, Load)** pipeline:

1. **Extract:** Reads a list of raw words from a text file.
2. **Transform:**
    * Fetches IPA phonetics from Dictionary API.
    * Uses **Google Gemini AI** (Batch Processing) to generate technical definitions, context sentences, part-of-speech tags, and common collocations.
    * Generates high-fidelity audio using **Microsoft Edge Neural TTS**.
3. **Load:** Packages everything into an `.apkg` file ready to be imported into Anki/AnkiDroid with a custom "Dark Mode" CSS design.

## Features

* **Asynchronous:** Built with `asyncio` and `aiohttp` to handle I/O-bound tasks (API requests & audio downloading) concurrently.
* **AI-Powered Enrichment:** Uses Gemini 2.5 Flash to understand the *context* of words.
* **JSON-Based Configuration:** All project settings (language, deck name, input/output files, voice, etc.) are defined in a single JSON file, making the pipeline easy to customize without modifying the source code.
* **Neural TTS:** Integrates `edge-tts` to generate natural-sounding audio (e.g. Christopher – US English).
* **Batch Processing:** Implements smart batching (N words per request) to respect API Rate Limits and optimize throughput.
* **Custom UI:** Includes a pre-styled Anki Note Type with CSS for a modern, app-like experience (Dark Mode friendly).

## Tech Stack

* **Python 3.13+**
* **Asyncio:** Concurrency management.
* **Google GenAI SDK:** For semantic data generation.
* **Edge-TTS:** For audio generation.
* **Genanki:** For `.apkg` file construction.

## Installation

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/sogeking-pixel/anki-deck-generator](https://github.com/sogeking-pixel/anki-deck-generator)
    cd anki-deck-generator
    ```

2. **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(If you don't have a requirements.txt, install manually: `pip install google-genai edge-tts genanki aiohttp python-dotenv`)*

4. **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your Google Gemini API Key:

    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

## Configuration (JSON)

All runtime configuration is handled through a JSON settings file.
This allows easy customization without touching the Python code.

Example `settings.json`:

```json
    {
    "language": "English",
    "deck_name": "English Vocabulary Deck",
    "file_out_name": "output_deck.apkg",
    "deck_id": 2059400110,
    "file_input": "week1.txt",
    "voice": "en-US-ChristopherNeural"
}
```

### Parameters

* **language:** Target language of the deck
* **deck_name:** Name displayed in Anki
* **file_out_name:** Output `.apkg` filename
* **deck_id:** Unique Anki deck ID
* **file_input:** Input text file containing the vocabulary
* **voice:** Neural TTS voice (Edge-TTS)

Available voices: [https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

## Usage

1. **Prepare your input:**
    Create a text file (e.g. `words.txt`) with one word per line:

    ```text
    Hello
    Word
    ```

2. **Run the pipeline:**

    ```bash
    python main.py
    ```

3. **Import to Anki:**
    * Locate the generated `output_deck.apkg` file.
    * Open it with Anki Desktop or AnkiDroid.
    * Enjoy your new cards!
