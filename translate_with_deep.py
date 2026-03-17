import json
import time
import sys
from deep_translator import GoogleTranslator

# Initialize translators
en_translator = GoogleTranslator(source='ro', target='en')
tr_translator = GoogleTranslator(source='ro', target='tr')

try:
    with open('inner_texts.json', 'r', encoding='utf-8') as f:
        texts = json.load(f)
except Exception as e:
    print(f"Error reading texts: {e}")
    sys.exit(1)

print(f"Starting translation of {len(texts)} phrases using deep-translator...")

try:
    with open('translations.js', 'r', encoding='utf-8') as f:
        existing_content = f.read()
except Exception as e:
    print(f"Error reading translations.js: {e}")
    sys.exit(1)

existing_content = existing_content.replace('};\n', ',').replace('};', ',')

appended_obj = ""

for i, text in enumerate(texts):
    try:
        # Use deep-translator
        en = en_translator.translate(text)
        tr = tr_translator.translate(text)
        
        # Fallback to original text if translation fails
        if not en: en = text
        if not tr: tr = text
        
        # Escape quotes and formatting for valid JS object
        key = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_val = en.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        tr_val = tr.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        appended_obj += f'\n  "{key}": {{ "en": "{en_val}", "tr": "{tr_val}" }}'
        if i != len(texts) - 1:
            appended_obj += ','
            
        if i % 20 == 0:
            print(f"Progress: {i}/{len(texts)}")
            
            # Save incrementally
            with open('translations.js', 'w', encoding='utf-8') as f:
                f.write(existing_content + appended_obj + '\n};\n')
                
            # Reload for next batch
            with open('translations.js', 'r', encoding='utf-8') as f:
                existing_content = f.read().replace('};\n', ',').replace('};', ',')
            appended_obj = ""
            
    except Exception as e:
        print(f"Failed at index {i}: {str(e)[:50]}...")
        time.sleep(1) # Backoff if banned

if appended_obj:
    with open('translations.js', 'w', encoding='utf-8') as f:
        f.write(existing_content + appended_obj + '\n};\n')

print("Finished successfully!")
