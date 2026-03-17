import urllib.request
import re
import os

pages = [
    "web-design",
    "app-development",
    "portofoliu-web-design",
    "echipa",
    "parteneri",
    "blog",
    "politica-de-confidentialitate",
    "termeni-si-conditii",
    "marca-inregistrata",
    "compania-magic5",
    "declaratie-de-accesabilitate"
]

# Create mapping dictionary mapping exact URL to local file
mapping = {
    "https://magic5.ro": "index.html",
    "https://magic5.ro/": "index.html",
    "https://magic5.ro/acasa": "index.html",
}
for p in pages:
    mapping[f"https://magic5.ro/{p}"] = f"{p}.html"
    mapping[f"https://magic5.ro/{p}/"] = f"{p}.html"

scripts_to_inject = """<script src="translations.js"></script>
<script src="i18n.js"></script>
<script src="clock.js"></script>
</body>"""

def process_html(html):
    # fix asset links (CSS, JS, uploads, fonts) to be local absolute or relative
    # e.g. https://magic5.ro/css/ -> css/
    html = html.replace('href="https://magic5.ro/css/', 'href="css/')
    html = html.replace('href="https://magic5.ro/css/', 'href="css/')
    html = html.replace('src="https://magic5.ro/js/', 'src="js/')
    
    # Hotlink all images back to live server so we don't have broken missing assets on inner pages
    # Replace absolute-to-local with nothing (let absolute stay absolute), 
    # and replace root-relative with absolute live.
    html = html.replace('src="/uploads/', 'src="https://magic5.ro/uploads/')
    html = html.replace('srcset="/uploads/', 'srcset="https://magic5.ro/uploads/')
    html = html.replace('href="/uploads/', 'href="https://magic5.ro/uploads/')
    html = html.replace('src="/images/', 'src="https://magic5.ro/images/')
    
    # Also fix relative like "uploads/" just in case
    html = html.replace('src="uploads/', 'src="https://magic5.ro/uploads/')
    html = html.replace('srcset="uploads/', 'srcset="https://magic5.ro/uploads/')
    html = html.replace('href="uploads/', 'href="https://magic5.ro/uploads/')

    # Replace specific page links
    for full_link, local_link in mapping.items():
        html = html.replace(f'href="{full_link}"', f'href="{local_link}"')
        html = html.replace(f"href='{full_link}'", f"href='{local_link}'")

    # Inject scripts
    if "</body>" in html:
        html = html.replace("</body>", scripts_to_inject)
    
    # We might need to fix Vite unexpected char attribute (the ""> bug on google reviews)
    html = html.replace('class="icon-wrapper d-flex flex-column gap-2 align-items-center""', 'class="icon-wrapper d-flex flex-column gap-2 align-items-center"')

    return html

# Download and process all pages
for p in pages:
    print(f"Downloading {p}...")
    try:
        req = urllib.request.Request(f"https://magic5.ro/{p}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            processed_html = process_html(html)
            
            with open(f"{p}.html", "w", encoding="utf-8") as f:
                f.write(processed_html)
    except Exception as e:
        print(f"Failed to process {p}: {e}")

# Process index.html separately to replace links but NOT inject scripts blindly again
try:
    with open("index.html", "r", encoding="utf-8") as f:
        idx_html = f.read()
    
    # Replace specific page links in index.html as well
    for full_link, local_link in mapping.items():
        idx_html = idx_html.replace(f'href="{full_link}"', f'href="{local_link}"')
        idx_html = idx_html.replace(f"href='{full_link}'", f"href='{local_link}'")
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(idx_html)
    print("Processed index.html successfully.")
except Exception as e:
    print(f"Failed to process index.html: {e}")
