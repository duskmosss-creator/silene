import os
import glob
import base64
import re
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
from datetime import datetime

print("Building UNIFIED National Geographic ZIM file...")

natgeo_dir = "natgeo_collection"
pdfs = sorted(glob.glob(f'{natgeo_dir}/pdfs/*.pdf'))

def get_aid(path):
    return os.path.splitext(os.path.basename(path))[0]

def parse_date(filename):
    if filename == '194701to12.pdf': return (1947, 1)
    if filename == '194905.pdf': return (1949, 5)
    if filename == '195011.pdf': return (1950, 11)
    if filename == '195105.pdf': return (1951, 5)
    if filename == '195204.pdf': return (1952, 4)
    if filename == '195304.pdf': return (1953, 4)
    
    if filename.startswith('20'):
        m = re.search(r'^(20\d\d)(\d\d)', filename)
        if m: 
            month = int(m.group(2))
            if month > 12: month = 1
            return (int(m.group(1)), month)
            
    m = re.search(r'NG(20\d\d)(\d\d)', filename)
    if m: return (int(m.group(1)), int(m.group(2)))
    
    m = re.search(r'(20\d\d)', filename)
    if m:
        year = int(m.group(1))
        month = 1
        name = filename.lower()
        if 'january' in name or 'jan' in name: month = 1
        elif 'february' in name or 'feb' in name: month = 2
        elif 'march' in name or 'mar' in name: month = 3
        elif 'april' in name or 'apr' in name: month = 4
        elif 'may' in name: month = 5
        elif 'june' in name or 'jun' in name: month = 6
        elif 'july' in name or 'jul' in name: month = 7
        elif 'august' in name or 'aug' in name: month = 8
        elif 'september' in name or 'sep' in name: month = 9
        elif 'october' in name or 'oct' in name: month = 10
        elif 'november' in name or 'nov' in name: month = 11
        elif 'december' in name or 'dec' in name: month = 12
        return (year, month)
        
    m = re.search(r'1888_1_1', filename)
    if m: return (1888, 1)
    
    m = re.search(r'(18\d\d|19\d\d)', filename)
    if m: return (int(m.group(1)), 1)
    
    return (9999, 1)

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class ZimItem(Item):
    def __init__(self, path, content_or_path, mimetype, is_file=True):
        super().__init__()
        self.path = path
        self.content_or_path = content_or_path
        self.mimetype = mimetype
        self.is_file = is_file
        
    def get_path(self):
        return self.path
    
    def get_title(self):
        return self.path
        
    def get_mimetype(self):
        return self.mimetype
        
    def get_contentprovider(self):
        if self.is_file:
            return FileProvider(self.content_or_path)
        else:
            return StringProvider(self.content_or_path)
            
    def get_hints(self):
        return {Hint.FRONT_ARTICLE: True} if self.path == "C/index.html" else {}

mimetype_map = {
    ".html": "text/html",
    ".txt": "text/plain",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".js": "application/javascript",
    ".css": "text/css"
}

favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
favicon_bytes = base64.b64decode(favicon_b64)

def generate_index_html():
    parsed_pdfs = []
    for p in pdfs:
        filename = os.path.basename(p)
        y, m = parse_date(filename)
        parsed_pdfs.append((p, y, m))
        
    # Sort chronologically
    parsed_pdfs.sort(key=lambda x: (x[1], x[2]))
    
    cards_html = ""
    for p, y, m in parsed_pdfs:
        aid = get_aid(p)
        
        if y == 9999:
            title = f'National Geographic (Archival)'
        else:
            title = f'National Geographic<br/>{MONTHS[m]} {y}'
            
        cover_path = f'../images/{aid}_cover.jpg'
        local_cover = f'natgeo_collection/images/{aid}_cover.jpg'
        if not os.path.exists(local_cover):
            cover_path = '../images/nationalgeograph11889nati_cover.jpg'
            
        cards_html += f'''
            <a class="card" href="pdfs/{aid}.html">
                <div>
                    <img src="{cover_path.replace('../', '')}" class="card-cover" alt="Cover" loading="lazy">
                    <div class="card-title">{title}</div>
                    <div style="margin-top: 0.5rem; color: var(--accent); font-weight: 600; font-size: 0.85rem;">📄 Open PDF Magazine →</div>
                </div>
            </a>
    '''
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>National Geographic Unified Archive</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #fbbf24;
            --text-main: #f8fafc;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 0;
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 1.5rem 1rem;
            text-align: center;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            border: 1px solid #334155;
        }}
        .card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}
        .card-cover {{
            width: 100%;
            height: 320px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            background: #000;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.4;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color: var(--accent); margin:0;">National Geographic Complete Archive</h1>
        <p style="color: #94a3b8; margin-top:0.5rem;">Chronological Unified Collection</p>
    </div>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>"""

def build_zim_unified():
    zim_filename = os.path.join("zim_downloads", "National_Geographic_Complete_Collection_v10.zim")
    print(f"Building {zim_filename} with {len(pdfs)} magazines...")
    
    index_html = generate_index_html()
    
    with Creator(zim_filename) as creator:
        creator.add_metadata("Title", "National Geographic Complete Archive")
        creator.add_metadata("Language", "eng")
        creator.add_metadata("Creator", "Custom ZIM Builder")
        creator.add_metadata("Publisher", "Hickory Search")
        creator.add_metadata("Description", "National Geographic Magazine Unified Chronological Archive")
        creator.add_metadata("Name", "national_geographic_complete_collection_v10")
        creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
        
        creator.add_illustration(48, favicon_bytes)
        creator.set_mainpath("C/index.html")
        creator.add_item(ZimItem("C/index.html", index_html, "text/html", is_file=False))
        
        item_count = 0
        for root, dirs, files in os.walk(natgeo_dir):
            if "texts" in root.split(os.sep):
                continue
                
            for file in files:
                if file == "index.html" and root == natgeo_dir:
                    continue
                    
                local_path = os.path.join(root, file)
                zim_path = os.path.relpath(local_path, natgeo_dir).replace("\\", "/")
                
                ext = os.path.splitext(file)[1].lower()
                mimetype = mimetype_map.get(ext, "application/octet-stream")
                    
                creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
                item_count += 1
                
    print(f"ZIM file {zim_filename} created successfully with {item_count} items.")

build_zim_unified()
