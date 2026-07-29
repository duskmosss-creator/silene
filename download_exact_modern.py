import urllib.request
import json
import os
import urllib.parse

issues = [
  '2017011',
  '201704_201905',
  '201612_201905',
  '201709_201905',
  '201608_201905',
  '201603_201905',
  '201703_201905',
  '201610_201905'
]

natgeo_dir = 'natgeo_collection'
os.makedirs(f'{natgeo_dir}/pdfs', exist_ok=True)
os.makedirs(f'{natgeo_dir}/images', exist_ok=True)

for identifier in issues:
    print(f'Fetching {identifier}...')
    pdf_out = f'{natgeo_dir}/pdfs/{identifier}.pdf'
    cover_out = f'{natgeo_dir}/images/{identifier}_cover.jpg'
    
    if not os.path.exists(cover_out):
        try:
            thumb_url = f'https://archive.org/services/img/{identifier}'
            t_req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(t_req, timeout=15) as t_resp:
                t_data = t_resp.read()
                if len(t_data) > 1000:
                    with open(cover_out, 'wb') as cf:
                        cf.write(t_data)
        except Exception as e:
            print('Cover err:', e)
            
    if not os.path.exists(pdf_out):
        meta_url = f'https://archive.org/metadata/{identifier}'
        try:
            req = urllib.request.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                files = data.get('files', [])
                pdf_files = [f for f in files if f.get('name', '').lower().endswith('.pdf')]
                pdf_files.sort(key=lambda x: int(x.get('size', 0)), reverse=True)
                
                if pdf_files:
                    best_pdf = pdf_files[0]
                    pdf_name = best_pdf['name']
                    download_url = f"https://archive.org/download/{identifier}/{urllib.parse.quote(pdf_name)}"
                    size_mb = int(best_pdf.get('size', 0)) / 1024 / 1024
                    print(f'  Downloading PDF ({size_mb:.1f} MB)...')
                    
                    pdf_req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(pdf_req, timeout=120) as pdf_resp:
                        with open(pdf_out, 'wb') as f:
                            f.write(pdf_resp.read())
                    print('  Success!')
        except Exception as e:
            print('PDF err:', e)

print("Done downloading exact modern issues!")
