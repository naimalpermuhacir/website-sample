import os
import re
import requests
import glob

# Extensions typical for assets
ASSET_EXTENSIONS = {'.webp', '.png', '.jpg', '.jpeg', '.svg', '.mp4', '.mov', '.woff2', '.woff', '.ttf', '.json', '.pdf'}

files_to_process = []
for ext in ['*.html', '*.js', '*.css', '*.json', 'project-modals/*.html']:
    files_to_process.extend(glob.glob(ext))

downloaded_urls = set()
files_updated = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Regex to find https://magic5.ro/...
pattern = re.compile(r'https://magic5.ro/([a-zA-Z0-9_\-/\.]+)')

def should_download(path):
    _, ext = os.path.splitext(path)
    if ext.lower() in ASSET_EXTENSIONS:
        return True
    if path.startswith('uploads/') or path.startswith('fonts/') or path.startswith('img/'):
        return True
    return False

for filepath in files_to_process:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue

    new_content = content
    matches = pattern.findall(content)
    
    for path in set(matches):
        if should_download(path):
            url = f"https://magic5.ro/{path}"
            
            # Vite best practice: serve absolute path static assets from the `public/` folder
            local_save_path = os.path.join('public', path)
            
            if url not in downloaded_urls:
                downloaded_urls.add(url)
                if not os.path.exists(local_save_path):
                    os.makedirs(os.path.dirname(local_save_path), exist_ok=True)
                    print(f"Downloading: {url}")
                    try:
                        with requests.get(url, stream=True, headers=headers, timeout=30) as r:
                            if r.status_code == 200:
                                with open(local_save_path, 'wb') as out_f:
                                    for chunk in r.iter_content(chunk_size=8192):
                                        out_f.write(chunk)
                            else:
                                print(f"Failed {r.status_code}: {url}")
                    except Exception as e:
                        print(f"Error downloading {url}: {e}")
            
            # Rewrite URL to be local absolute root (e.g. /uploads/...)
            new_content = new_content.replace(f"https://magic5.ro/{path}", f"/{path}")

    # Also strip absolute domain from inner links
    new_content = new_content.replace('"https://magic5.ro/"', '"/"')
    new_content = new_content.replace('"https://magic5.ro"', '"/"')
    new_content = new_content.replace("'https://magic5.ro/'", "'/'")
    new_content = new_content.replace("'https://magic5.ro'", "'/'")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        files_updated += 1

print(f"Finished processing. Downloaded {len(downloaded_urls)} assets. Updated {files_updated} source files to point locally.")
