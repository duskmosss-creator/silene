import urllib.request
import json
import os

items = [
    'nationalgeograph11889nati',
    'nationalgeograph37natiuoft',
    '194701to12',
    '194905',
    '195011',
    '195105',
    '195204',
    '195304',
    'jishankhan_hotmail_1954'
]

os.makedirs("natgeo_collection/pdfs", exist_ok=True)

print("Resolving exact full-size PDF files from Internet Archive API...")
for identifier in items:
    pdf_out = f"natgeo_collection/pdfs/{identifier}.pdf"
    if os.path.exists(pdf_out) and os.path.getsize(pdf_out) > 500000:
        print(f"Verified {identifier}.pdf ({os.path.getsize(pdf_out)/1024/1024:.2f} MB)")
        continue

    meta_url = f"https://archive.org/metadata/{identifier}"
    try:
        req = urllib.request.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            files = data.get('files', [])
            pdf_files = [f for f in files if f.get('name', '').endswith('.pdf') and not f.get('name', '').endswith('_bw.pdf')]
            
            # Sort by file size descending to get the full-resolution PDF volume
            pdf_files.sort(key=lambda x: int(x.get('size', 0)), reverse=True)
            
            if pdf_files:
                target_file = pdf_files[0]['name']
                download_url = f"https://archive.org/download/{identifier}/{target_file}"
                print(f"Found PDF for {identifier}: {target_file} ({int(pdf_files[0].get('size', 0))/1024/1024:.2f} MB)")
                print(f"Downloading from {download_url}...")
                
                req_dl = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_dl, timeout=120) as dl_resp:
                    pdf_bytes = dl_resp.read()
                    if len(pdf_bytes) > 100000:
                        with open(pdf_out, 'wb') as pf:
                            pf.write(pdf_bytes)
                        print(f"Saved {pdf_out} ({len(pdf_bytes)/1024/1024:.2f} MB)")
            else:
                print(f"No PDF file listed for {identifier}")
    except Exception as e:
        print(f"Error fetching {identifier}: {e}")

print("Exact PDF resolution and download complete.")
