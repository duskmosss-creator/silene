import os
import urllib.request

natgeo_pdf_dir = "natgeo_collection/pdfs"
os.makedirs(natgeo_pdf_dir, exist_ok=True)

items = [
    {
        'id': 'nationalgeograph11889nati',
        'url': 'https://archive.org/download/nationalgeograph11889nati/nationalgeograph11889nati.pdf',
        'filename': 'nationalgeograph11889nati.pdf'
    },
    {
        'id': 'nationalgeograph37natiuoft',
        'url': 'https://archive.org/download/nationalgeograph37natiuoft/nationalgeograph37natiuoft.pdf',
        'filename': 'nationalgeograph37natiuoft.pdf'
    },
    {
        'id': '194701to12',
        'url': 'https://archive.org/download/194701to12/194701to12_text.pdf',
        'filename': '194701to12.pdf'
    },
    {
        'id': '194905',
        'url': 'https://archive.org/download/194905/194905_text.pdf',
        'filename': '194905.pdf'
    },
    {
        'id': '195011',
        'url': 'https://archive.org/download/195011/195011_text.pdf',
        'filename': '195011.pdf'
    },
    {
        'id': '195105',
        'url': 'https://archive.org/download/195105/195105_text.pdf',
        'filename': '195105.pdf'
    },
    {
        'id': '195204',
        'url': 'https://archive.org/download/195204/195204_text.pdf',
        'filename': '195204.pdf'
    },
    {
        'id': '195304',
        'url': 'https://archive.org/download/195304/195304_text.pdf',
        'filename': '195304.pdf'
    },
    {
        'id': 'jishankhan_hotmail_1954',
        'url': 'https://archive.org/download/jishankhan_hotmail_1954/jishankhan_hotmail_1954_text.pdf',
        'filename': 'jishankhan_hotmail_1954.pdf'
    }
]

print("Downloading full multi-megabyte National Geographic magazine PDFs from Internet Archive...")
for item in items:
    filepath = f"{natgeo_pdf_dir}/{item['filename']}"
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100000:
        print(f"Already exists: {filepath} ({os.path.getsize(filepath)/1024/1024:.2f} MB)")
        continue
        
    print(f"Downloading {item['id']} from {item['url']}...")
    try:
        req = urllib.request.Request(item['url'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            if len(data) > 50000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                print(f"Successfully downloaded {filepath} ({len(data)/1024/1024:.2f} MB)")
            else:
                # Try direct pdf fallback
                fallback_url = f"https://archive.org/download/{item['id']}/{item['id']}.pdf"
                print(f"Trying fallback: {fallback_url}")
                req2 = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2, timeout=60) as resp2:
                    data2 = resp2.read()
                    if len(data2) > 50000:
                        with open(filepath, 'wb') as f:
                            f.write(data2)
                        print(f"Successfully downloaded fallback {filepath} ({len(data2)/1024/1024:.2f} MB)")
    except Exception as e:
        print(f"Download notice for {item['id']}: {e}")

print("NatGeo PDF download process completed.")
