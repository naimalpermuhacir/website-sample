import os
import glob
from bs4 import BeautifulSoup
import json
import re

html_files = glob.glob('*.html') + glob.glob('project-modals/*.html')
texts = set()

class MyHTMLParser:
    def __init__(self):
        self.texts = set()

    def parse(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        for script in soup(["script", "style", "noscript", "svg", "path", "circle"]):
            script.extract()
            
        for element in soup.find_all(string=True):
            text = element.strip()
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            if self._is_valid_text(text):
                self.texts.add(text)
                
        # Also grab placeholder attributes
        for element in soup.find_all(attrs={"placeholder": True}):
             text = element['placeholder'].strip()
             text = re.sub(r'\s+', ' ', text)
             if self._is_valid_text(text):
                 self.texts.add(text)

    def _is_valid_text(self, text):
        if not text:
            return False
        if len(text) < 2:
            return False
        if text.isdigit():
            return False
        if re.match(r'^[\W_]+$', text): # Only punctuation
            return False
        if "{" in text or "}" in text: # JS code or CSS
            return False
        return True

parser = MyHTMLParser()
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            parser.parse(f.read())
    except Exception as e:
        print(f"Error parsing {file}: {e}")

# Load existing translations to avoid duplicates
existing_keys = set()
try:
    with open('translations.js', 'r', encoding='utf-8') as f:
        content = f.read()
        # Very basic regex to find keys in translations.js
        matches = re.findall(r'"([^"]+)":\s*\{', content)
        for match in matches:
            existing_keys.add(match)
except FileNotFoundError:
    pass

new_texts = [t for t in parser.texts if t not in existing_keys]

with open('inner_texts.json', 'w', encoding='utf-8') as f:
    json.dump(new_texts, f, ensure_ascii=False, indent=2)

print(f"Found {len(new_texts)} NEW extractable text phrases.")
