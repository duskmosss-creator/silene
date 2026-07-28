import urllib.request
import json
import os

natgeo_dir = "natgeo_collection"
os.makedirs(f"{natgeo_dir}/pdfs", exist_ok=True)
os.makedirs(f"{natgeo_dir}/images", exist_ok=True)
os.makedirs(f"{natgeo_dir}/texts", exist_ok=True)

# Search Internet Archive API for National Geographic full magazine texts
search_url = "https://archive.org/advancedsearch.php?q=title%3A%28%22National+Geographic%22%29+AND+mediatype%3A%28texts%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&sort%5B%5D=year+asc&rows=40&page=1&output=json"

print("Searching Internet Archive for full National Geographic magazine issues...")
try:
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        search_data = json.loads(resp.read().decode('utf-8'))
        docs = search_data.get('response', {}).get('docs', [])
        print(f"Found {len(docs)} National Geographic full issues on Internet Archive.")
        
        for doc in docs:
            identifier = doc.get('identifier')
            title = doc.get('title', identifier)
            year = doc.get('year', 'Unknown')
            
            pdf_out = f"{natgeo_dir}/pdfs/{identifier}.pdf"
            cover_out = f"{natgeo_dir}/images/{identifier}_cover.jpg"
            
            # Fetch cover image
            if not os.path.exists(cover_out):
                try:
                    thumb_url = f"https://archive.org/services/img/{identifier}"
                    t_req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(t_req, timeout=15) as t_resp:
                        t_data = t_resp.read()
                        if len(t_data) > 1000:
                            with open(cover_out, 'wb') as cf:
                                cf.write(t_data)
                except Exception as e:
                    pass
            
            # Fetch Metadata to get largest PDF file
            if not os.path.exists(pdf_out) or os.path.getsize(pdf_out) < 100000:
                meta_url = f"https://archive.org/metadata/{identifier}"
                try:
                    m_req = urllib.request.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(m_req, timeout=20) as m_resp:
                        m_data = json.loads(m_resp.read().decode('utf-8'))
                        files = m_data.get('files', [])
                        pdf_files = [f for f in files if f.get('name', '').endswith('.pdf') and not f.get('name', '').endswith('_bw.pdf')]
                        pdf_files.sort(key=lambda x: int(x.get('size', 0)), reverse=True)
                        
                        if pdf_files:
                            target_pdf = pdf_files[0]['name']
                            dl_url = f"https://archive.org/download/{identifier}/{target_pdf}"
                            print(f"Downloading full issue {identifier} ({year}): {target_pdf} ({int(pdf_files[0].get('size',0))/1024/1024:.1f} MB)...")
                            
                            d_req = urllib.request.Request(dl_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(d_req, timeout=120) as d_resp:
                                p_data = d_resp.read()
                                if len(p_data) > 100000:
                                    with open(pdf_out, 'wb') as pf:
                                        pf.write(p_data)
                                    print(f"Saved full issue PDF: {pdf_out} ({len(p_data)/1024/1024:.1f} MB)")
                except Exception as e:
                    print(f"Notice downloading {identifier}: {e}")
except Exception as e:
    print(f"Error querying Internet Archive search: {e}")

print("Internet Archive full issue acquisition complete.")
