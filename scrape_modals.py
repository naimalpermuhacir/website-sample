import os
import glob
from bs4 import BeautifulSoup
import requests
import time

html_files = glob.glob('*.html')
project_ids = set()

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        triggers = soup.find_all(class_='project-modal-trigger')
        for t in triggers:
            if t.has_attr('data-id'):
                project_ids.add(t['data-id'])

print(f"Found {len(project_ids)} unique project IDs.")

if not os.path.exists('project-modals'):
    os.makedirs('project-modals')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for pid in project_ids:
    url = f"https://magic5.ro/get-project-content?project_id={pid}"
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            html = req.text
            # We also need to fix image paths in the downloaded modal HTML!
            # Replace /uploads/ with https://magic5.ro/uploads/
            html = html.replace('"/uploads/', '"https://magic5.ro/uploads/')
            html = html.replace("'//uploads/", "'https://magic5.ro/uploads/")
            html = html.replace('src="/uploads/', 'src="https://magic5.ro/uploads/')
            html = html.replace('src="uploads/', 'src="https://magic5.ro/uploads/')
            html = html.replace('href="/uploads/', 'href="https://magic5.ro/uploads/')
            
            with open(f'project-modals/{pid}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Downloaded project {pid}")
        else:
            print(f"Failed to download {pid}: status {req.status_code}")
    except Exception as e:
        print(f"Error downloading {pid}: {e}")
    time.sleep(0.5)

print("Done.")
