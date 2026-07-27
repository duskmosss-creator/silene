import urllib.request
import json
import urllib.parse

def search_internet_archive(query):
    url = f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(query)}&fl[]=identifier,title,creator,mediatype&sort[]=downloads+desc&rows=10&page=1&output=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('response', {}).get('docs', [])
    except Exception as e:
        print(f"Error searching Internet Archive for {query}: {e}")
        return []

def search_librivox(query):
    url = f"https://librivox.org/api/feed/audiobooks?title=^{urllib.parse.quote(query)}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('books', [])
    except Exception as e:
        # Librivox API returns 404 if no results
        return []

if __name__ == "__main__":
    queries = [
        "Great Smoky Mountains",
        "Dupont State Forest",
        "Appalachian Mountains",
        "Cades Cove",
        "Elkmont"
    ]
    
    print("=== Internet Archive Results ===")
    for q in queries:
        print(f"\nSearching for: {q}")
        results = search_internet_archive(f'title:("{q}") AND mediatype:(texts OR audio)')
        for r in results:
            print(f"- {r.get('title', 'Unknown')} by {r.get('creator', 'Unknown')} [{r.get('mediatype', 'unknown')}] (ID: {r.get('identifier')})")

    print("\n=== LibriVox Results ===")
    for q in queries:
        print(f"\nSearching for: {q}")
        results = search_librivox(q)
        if isinstance(results, list):
            for r in results:
                print(f"- {r.get('title')} by {r.get('authors')} (ID: {r.get('id')})")
        elif isinstance(results, dict) and 'books' in results:
            for r in results['books']:
                print(f"- {r.get('title')} by {r.get('authors')} (ID: {r.get('id')})")
