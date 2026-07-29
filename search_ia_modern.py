import urllib.request, json
import time

def search_ia(year):
    url = f'https://archive.org/advancedsearch.php?q=title%3A(%22National+Geographic%22)+AND+date%3A{year}&fl%5B%5D=identifier,title,mediatype,format&rows=100&output=json'
    print(f'Searching {year}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            docs = data.get('response', {}).get('docs', [])
            for d in docs:
                formats = d.get('format', [])
                if isinstance(formats, str): formats = [formats]
                has_pdf = any('PDF' in f.upper() or 'pdf' in f.lower() for f in formats)
                if has_pdf and d.get('mediatype') == 'texts':
                    print(f"  FOUND PDF: {d.get('identifier')} - {d.get('title')}")
    except Exception as e:
        print('Error:', e)
    time.sleep(1)

for y in range(2016, 2020):
    search_ia(y)
