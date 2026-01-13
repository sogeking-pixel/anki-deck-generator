import genanki

MODEL_ID = 1607392319 

STYLE = """
.card {
 font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
 font-size: 20px;
 text-align: center;
 color: #e0e0e0;
 background-color: #2d2d2d;
 padding: 20px;
}

.word-box {
 background-color: #383838;
 border-radius: 12px;
 padding: 20px;
 box-shadow: 0 4px 6px rgba(0,0,0,0.3);
 margin-bottom: 20px;
 border-left: 5px solid #61dafb; /* Color React Blue para estilo tech */
}

.word {
 font-size: 36px;
 font-weight: bold;
 color: #ffffff;
 margin-bottom: 5px;
}

.ipa {
 font-family: 'Lucida Sans Unicode', sans-serif;
 color: #aaaaaa;
 font-size: 18px;
}

.pos-tag {
 display: inline-block;
 background-color: #444;
 color: #61dafb;
 padding: 2px 8px;
 border-radius: 4px;
 font-size: 14px;
 text-transform: uppercase;
 font-weight: bold;
 margin-top: 5px;
 vertical-align: middle;
}

/* Sección de definición */
.def-box {
 text-align: left;
 margin-top: 15px;
 border-top: 1px solid #555;
 padding-top: 15px;
}

.definition {
 font-size: 18px;
 line-height: 1.5;
 color: #ddd;
}


.example-box {
 margin-top: 20px;
 background-color: #252526;
 border-left: 4px solid #98c379; /* Verde sutil */
 padding: 10px 15px;
 text-align: left;
 font-style: italic;
 color: #abb2bf;
 border-radius: 0 8px 8px 0;
}

.collocation-box {
 margin-top: 15px;
 font-size: 16px;
 color: #e5c07b; /* Amarillo suave */
 font-weight: bold;
}

.label {
 font-size: 12px;
 color: #666;
 text-transform: uppercase;
 letter-spacing: 1px;
 display: block;
 margin-bottom: 4px;
}
"""

my_model = genanki.Model(
    MODEL_ID,
    'Tech English Pro Model',
    fields=[
        {'name': 'Word'},
        {'name': 'IPA'},
        {'name': 'Audio'},
        {'name': 'Definition'},
        {'name': 'Example'},
        {'name': 'Type'}, 
        {'name': 'Collocation'},
    ],
    templates=[
        {
            'name': 'Tech Card',
            'qfmt': '''
                <div class="word-box">
                    <div class="word">{{Word}}</div>
                    <div class="ipa">/{{IPA}}/</div>
                    <div class="pos-tag">{{Type}}</div>
                </div>
                {{Audio}}
            ''',
            'afmt': '''
                {{FrontSide}}
                
                <div class="def-box">
                    <span class="label">Definition</span>
                    <div class="definition">{{Definition}}</div>
                </div>

                <div class="collocation-box">
                    {{Collocation}}
                </div>

                <div class="example-box">
                    <span class="label">Context</span>
                    "{{Example}}"
                </div>
            ''',
        },
    ],
    css=STYLE
)