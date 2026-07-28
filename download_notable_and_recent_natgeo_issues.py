import urllib.request
import json
import os

natgeo_dir = "natgeo_collection"
os.makedirs(f"{natgeo_dir}/pdfs", exist_ok=True)
os.makedirs(f"{natgeo_dir}/images", exist_ok=True)
os.makedirs(f"{natgeo_dir}/texts", exist_ok=True)

notable_issues = [
    {
        'id': 'sim_national-geographic_1969-12_136_6',
        'search': 'national geographic 1969 moon',
        'title': 'National Geographic (Dec 1969 - Man on the Moon Historic Issue)',
        'year': 1969,
        'era': '1950s-1970s',
        'desc': 'Iconic Apollo 11 moon landing special issue featuring Apollo lunar photography.'
    },
    {
        'id': 'sim_national-geographic_1985-06_167_6',
        'search': 'national geographic june 1985',
        'title': 'National Geographic (June 1985 - Iconic Afghan Girl Issue)',
        'year': 1985,
        'era': '1980s-1990s',
        'desc': 'World-famous cover photo by Steve McCurry and global refugee report.'
    },
    {
        'id': 'sim_national-geographic_1985-12_168_6',
        'search': 'national geographic titanic 1985',
        'title': 'National Geographic (Dec 1985 - Discovery of RMS Titanic)',
        'year': 1985,
        'era': '1980s-1990s',
        'desc': 'Dr. Robert Ballard historic underwater discovery of the RMS Titanic.'
    },
    {
        'id': 'sim_national-geographic_1999-12_196_6',
        'search': 'national geographic december 1999 millennium',
        'title': 'National Geographic (Dec 1999 - Millennium Special Collector Issue)',
        'year': 1999,
        'era': '1980s-1990s',
        'desc': 'Turn-of-the-century special issue on global exploration and Earth mapping.'
    },
    {
        'id': 'sim_national-geographic_2016-05_229_5',
        'search': 'national geographic may 2016 national parks',
        'title': 'National Geographic (May 2016 - National Parks Centennial Issue)',
        'year': 2016,
        'era': '2000s-2010s',
        'desc': '100th Anniversary of America National Parks featuring Great Smoky Mountains.'
    },
    {
        'id': 'sim_national-geographic_2020-04_237_4',
        'search': 'national geographic april 2020 earth day',
        'title': 'National Geographic (April 2020 - Earth Day 50th Anniversary Issue)',
        'year': 2020,
        'era': '2020s-Present',
        'desc': '50 Years of Earth Day special issue on global climate resilience and mountain conservation.'
    },
    {
        'id': 'sim_national-geographic_2023-01_243_1',
        'search': 'national geographic january 2023',
        'title': 'National Geographic (Jan 2023 - Wild Rewilding & Conservation Issue)',
        'year': 2023,
        'era': '2020s-Present',
        'desc': 'Modern rewilding features, elk species recovery, and Appalachian forest protection.'
    }
]

print("Searching and downloading notable & recent National Geographic issues from Internet Archive...")
for item in notable_issues:
    identifier = item['id']
    pdf_out = f"{natgeo_dir}/pdfs/{identifier}.pdf"
    cover_out = f"{natgeo_dir}/images/{identifier}_cover.jpg"
    
    # 1. Fetch cover image
    if not os.path.exists(cover_out):
        try:
            thumb_url = f"https://archive.org/services/img/{identifier}"
            t_req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(t_req, timeout=15) as t_resp:
                t_data = t_resp.read()
                if len(t_data) > 1000:
                    with open(cover_out, 'wb') as cf:
                        cf.write(t_data)
                    print(f"Downloaded cover for notable issue: {cover_out}")
        except Exception as e:
            pass
            
    # 2. Query IA API for PDF
    if not os.path.exists(pdf_out) or os.path.getsize(pdf_out) < 50000:
        meta_url = f"https://archive.org/metadata/{identifier}"
        try:
            req = urllib.request.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                files = data.get('files', [])
                pdf_files = [f for f in files if f.get('name', '').endswith('.pdf') and not f.get('name', '').endswith('_bw.pdf')]
                pdf_files.sort(key=lambda x: int(x.get('size', 0)), reverse=True)
                
                if pdf_files:
                    target_file = pdf_files[0]['name']
                    dl_url = f"https://archive.org/download/{identifier}/{target_file}"
                    print(f"Downloading notable issue {identifier} ({item['year']}): {target_file} ({int(pdf_files[0].get('size',0))/1024/1024:.1f} MB)...")
                    
                    d_req = urllib.request.Request(dl_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(d_req, timeout=120) as d_resp:
                        pdf_bytes = d_resp.read()
                        if len(pdf_bytes) > 50000:
                            with open(pdf_out, 'wb') as pf:
                                pf.write(pdf_bytes)
                            print(f"Saved notable issue PDF: {pdf_out} ({len(pdf_bytes)/1024/1024:.1f} MB)")
        except Exception as e:
            print(f"Notice fetching notable issue {identifier}: {e}")

print("Notable & recent National Geographic acquisition complete.")
