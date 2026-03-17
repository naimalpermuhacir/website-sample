import re

with open('translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix missing commas between properties: `} \n "KEY"` -> `}, \n "KEY"`
content = re.sub(r'\}\s+"', '},\n  "', content)

with open('translations.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed missing commas.")
