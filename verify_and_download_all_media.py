import os
import urllib.request
import json

os.makedirs("content/pdfs", exist_ok=True)
os.makedirs("content/texts", exist_ok=True)
os.makedirs("content/audio", exist_ok=True)
os.makedirs("content/js", exist_ok=True)

# 1. Archive items list with direct fallback URLs
archive_items = [
    {
        'id': 'westernnorthcar00arth',
        'title': 'Western North Carolina: A History (1730-1913)',
        'urls': [
            'https://archive.org/download/westernnorthcar00arth/westernnorthcar00arth.pdf',
            'https://ia800203.us.archive.org/21/items/westernnorthcar00arth/westernnorthcar00arth.pdf'
        ]
    },
    {
        'id': 'historyofwataug00arth',
        'title': 'A History of Watauga County, North Carolina',
        'urls': [
            'https://archive.org/download/historyofwataug00arth/historyofwataug00arth.pdf',
            'https://ia600206.us.archive.org/18/items/historyofwataug00arth/historyofwataug00arth.pdf'
        ]
    },
    {
        'id': 'folksongsofengli00shar',
        'title': 'Folk-songs of English Origin in the Appalachian Mountains',
        'urls': [
            'https://archive.org/download/folksongsofengli00shar/folksongsofengli00shar.pdf'
        ]
    },
    {
        'id': 'nurserysongsfrom00shar',
        'title': 'Nursery Songs from the Appalachian Mountains',
        'urls': [
            'https://archive.org/download/nurserysongsfrom00shar/nurserysongsfrom00shar.pdf'
        ]
    },
    {
        'id': 'riflemakingingre13nati',
        'title': 'Rifle Making in the Great Smoky Mountains',
        'urls': [
            'https://archive.org/download/riflemakingingre13nati/riflemakingingre13nati.pdf'
        ]
    },
    {
        'id': 'checklistoffungi00pete',
        'title': 'Checklist of Fungi of the Great Smoky Mountains National Park',
        'urls': [
            'https://archive.org/download/checklistoffungi00pete/checklistoffungi00pete.pdf'
        ]
    },
    {
        'id': 'floraofgreatsmok00whit',
        'title': 'Flora of Great Smoky Mountains National Park',
        'urls': [
            'https://archive.org/download/floraofgreatsmok00whit/floraofgreatsmok00whit.pdf'
        ]
    },
    {
        'id': 'statushistoryofm00culb',
        'title': 'Status and History of the Mountain Lion in GSMNP',
        'urls': [
            'https://archive.org/download/statushistoryofm00culb/statushistoryofm00culb.pdf'
        ]
    },
    {
        'id': 'whitetaileddeero00wath',
        'title': 'White-Tailed Deer of Cades Cove',
        'urls': [
            'https://archive.org/download/whitetaileddeero00wath/whitetaileddeero00wath.pdf'
        ]
    },
    {
        'id': 'carologueaccesst00hoff',
        'title': 'Carologue: Access to North Carolina',
        'urls': [
            'https://archive.org/download/carologueaccesst00hoff/carologueaccesst00hoff.pdf'
        ]
    }
]

print("Verifying and downloading actual PDF files into content/pdfs/...")
for item in archive_items:
    filepath = f"content/pdfs/{item['id']}.pdf"
    if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
        print(f"Verified PDF: {filepath} ({os.path.getsize(filepath)} bytes)")
        continue
        
    downloaded = False
    for url in item['urls']:
        try:
            print(f"Downloading {item['id']} from {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    print(f"Saved PDF: {filepath} ({len(data)} bytes)")
                    downloaded = True
                    break
        except Exception as e:
            print(f"Download attempt failed: {e}")
            
    if not downloaded:
        print(f"Warning: Could not download PDF for {item['id']}")

print("Media verification complete.")
