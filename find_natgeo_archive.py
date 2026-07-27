import urllib.request
import json
import urllib.parse

url = "https://archive.org/advancedsearch.php?q=title%3A%28%22National+Geographic%22%29+AND+mediatype%3A%28texts%29&fl[]=identifier,title,date,year,description&sort[]=downloads+desc&rows=15&page=1&output=json"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        docs = data.get('response', {}).get('docs', [])
        print("=== Internet Archive NatGeo Results ===")
        for d in docs:
            print(f"ID: {d.get('identifier')} | Title: {d.get('title')} | Year: {d.get('year')}")
except Exception as e:
    print(f"Error: {e}")
