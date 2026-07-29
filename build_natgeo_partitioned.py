import os
import glob
import base64
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
from datetime import datetime

print("Building Partitioned National Geographic ZIM files...")

natgeo_dir = "natgeo_collection"
pdfs = sorted(glob.glob(f'{natgeo_dir}/pdfs/*.pdf'))

# Split into two parts to avoid 2GB limit
part1_pdfs = pdfs[:20]
part2_pdfs = pdfs[20:]

def get_aid(path):
    return os.path.splitext(os.path.basename(path))[0]

part1_aids = set(get_aid(p) for p in part1_pdfs)
part2_aids = set(get_aid(p) for p in part2_pdfs)

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

def generate_index_html(aids_subset, part_name):
    cards_html = ""
    for p in pdfs:
        aid = get_aid(p)
        if aid not in aids_subset:
            continue
            
        title = f'National Geographic ({aid})'
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
    <title>National Geographic Archive {part_name}</title>
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
            line-height: 1.3;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color: var(--accent); margin:0;">National Geographic Magazine Archive ({part_name})</h1>
        <p style="color: #94a3b8; margin-top:0.5rem;">Exclusive Appalachian Collection & Full Photo Issues</p>
    </div>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>"""

def build_zim_part(aids_subset, part_num):
    zim_filename = os.path.join("zim_downloads", f"National_Geographic_Appalachian_Collection_Part{part_num}_v8.zim")
    print(f"Building {zim_filename} with {len(aids_subset)} magazines...")
    
    index_html = generate_index_html(aids_subset, f"Part {part_num}")
    
    with Creator(zim_filename) as creator:
        creator.add_metadata("Title", f"Nat Geo Collection Part {part_num}")
        creator.add_metadata("Language", "eng")
        creator.add_metadata("Creator", "Custom ZIM Builder")
        creator.add_metadata("Publisher", "Hickory Search")
        creator.add_metadata("Description", f"National Geographic Magazine Archive Part {part_num}")
        creator.add_metadata("Name", f"national_geographic_collection_part{part_num}_v8")
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
                    
                # Skip PDFs and their HTML wrappers if they don't belong in this part!
                if root.endswith("pdfs"):
                    aid = os.path.splitext(file)[0]
                    if aid not in aids_subset:
                        continue
                    
                local_path = os.path.join(root, file)
                zim_path = os.path.relpath(local_path, natgeo_dir).replace("\\", "/")
                
                ext = os.path.splitext(file)[1].lower()
                mimetype = mimetype_map.get(ext, "application/octet-stream")
                    
                creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
                item_count += 1
                
    print(f"ZIM file {zim_filename} created successfully with {item_count} items.")

# Build Part 1
build_zim_part(part1_aids, 1)

# Build Part 2
build_zim_part(part2_aids, 2)
