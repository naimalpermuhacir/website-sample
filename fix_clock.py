import glob
import re

html_files = glob.glob('*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The HTML segment we want to replace
    # <p class="text-secondary fw-semibold text-xs">Ploiești, România <span class="header-time text-white">02:12</span></p>
    
    # We will replace 'Ploiești, România' with '<span id="user-location"></span>'
    # And we will ensure the time span has id="user-time"
    new_content = re.sub(
        r'<p class="text-secondary fw-semibold text-xs">Ploiești, România <span class="header-time text-white">\d{2}:\d{2}</span></p>',
        r'<p class="text-secondary fw-semibold text-xs"><span id="user-location"></span> <span id="user-time" class="header-time text-white"></span></p>',
        content
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

print("Done replacing hardcoded location and time.")
