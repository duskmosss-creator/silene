import os
import glob
import base64
import re
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
from datetime import datetime

print("Building two properly-split National Geographic ZIM volumes...")

natgeo_dir = "natgeo_collection"
all_pdfs = sorted(glob.glob(f'{natgeo_dir}/pdfs/*.pdf'))

def get_aid(path):
    return os.path.splitext(os.path.basename(path))[0]

def parse_date(filename):
    fn = os.path.basename(filename)
    if fn == '194701to12.pdf': return (1947, 1)
    if fn == '194905.pdf': return (1949, 5)
    if fn == '195011.pdf': return (1950, 11)
    if fn == '195105.pdf': return (1951, 5)
    if fn == '195204.pdf': return (1952, 4)
    if fn == '195304.pdf': return (1953, 4)
    if fn.startswith('20'):
        m = re.search(r'^(20\d\d)(\d\d)', fn)
        if m:
            month = int(m.group(2))
            if month > 12: month = 1
            return (int(m.group(1)), month)
    m = re.search(r'NG(20\d\d)(\d\d)', fn)
    if m: return (int(m.group(1)), int(m.group(2)))
    m = re.search(r'(20\d\d)', fn)
    if m:
        year = int(m.group(1))
        month = 1
        name = fn.lower()
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        for i, mo in enumerate(months):
            if mo in name or mo[:3] in name:
                month = i + 1
                break
        return (year, month)
    m = re.search(r'1888_1_1', fn)
    if m: return (1888, 1)
    m = re.search(r'(18\d\d|19\d\d)', fn)
    if m: return (int(m.group(1)), 1)
    return (9999, 1)

def is_classic(path):
    y, _ = parse_date(path)
    return y < 2000

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Split
classic_pdfs = sorted([p for p in all_pdfs if is_classic(p)], key=lambda p: parse_date(p))
modern_pdfs  = sorted([p for p in all_pdfs if not is_classic(p)], key=lambda p: parse_date(p))

print(f"Classic PDFs: {len(classic_pdfs)}")
print(f"Modern PDFs:  {len(modern_pdfs)}")

classic_sz = sum(os.path.getsize(p) for p in classic_pdfs)
modern_sz  = sum(os.path.getsize(p) for p in modern_pdfs)
print(f"Classic size: {classic_sz/1024/1024:.0f} MB")
print(f"Modern size:  {modern_sz/1024/1024:.0f} MB")

class ZimItem(Item):
    def __init__(self, path, content_or_path, mimetype, is_file=True, front=False):
        super().__init__()
        self._path = path
        self._content = content_or_path
        self._mime = mimetype
        self._is_file = is_file
        self._front = front
    def get_path(self): return self._path
    def get_title(self): return self._path
    def get_mimetype(self): return self._mime
    def get_contentprovider(self):
        if self._is_file: return FileProvider(self._content)
        return StringProvider(self._content)
    def get_hints(self): return {Hint.FRONT_ARTICLE: True} if self._front else {}

mimetype_map = {
    ".html": "text/html", ".pdf": "application/pdf",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".js": "application/javascript",
    ".css": "text/css", ".json": "application/json",
    ".webp": "image/webp", ".txt": "text/plain",
}

favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
favicon_bytes = base64.b64decode(favicon_b64)

def make_card_title(aid):
    y, m = parse_date(aid + '.pdf')
    if y == 9999: return 'National Geographic<br/>(Archival)'
    return f'National Geographic<br/>{MONTHS[m]} {y}'

def make_index_html(pdf_list, title, subtitle):
    cards = ""
    for p in pdf_list:
        aid = get_aid(p)
        cover = f'images/{aid}_cover.jpg'
        if not os.path.exists(f'{natgeo_dir}/{cover}'):
            cover = 'images/nationalgeograph11889nati_cover.jpg'
        card_title = make_card_title(aid)
        cards += f'''
        <a class="card" href="pdfs/{aid}.html">
            <img src="{cover}" class="cover" alt="cover" loading="lazy">
            <div class="card-title">{card_title}</div>
            <div class="open-label">&#128196; Open Magazine</div>
        </a>'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root{{--bg:#0f172a;--card:#1e293b;--accent:#fbbf24;--text:#f8fafc;--muted:#94a3b8;--border:#334155;}}
*{{box-sizing:border-box;}}
body{{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}}
.header{{background:var(--card);border-bottom:2px solid var(--accent);padding:1.25rem 1rem;text-align:center;}}
h1{{color:var(--accent);margin:0;font-size:1.6rem;}}
.sub{{color:var(--muted);margin:0.25rem 0 0;font-size:0.9rem;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1.25rem;padding:1.5rem;max-width:1200px;margin:0 auto;}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:0.75rem;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:border-color 0.2s,transform 0.2s;}}
.card:hover{{border-color:var(--accent);transform:translateY(-3px);}}
.cover{{width:100%;height:280px;object-fit:cover;border-radius:8px;margin-bottom:0.75rem;background:#000;}}
.card-title{{font-size:0.95rem;font-weight:700;line-height:1.4;word-wrap:break-word;overflow-wrap:break-word;}}
.open-label{{margin-top:0.5rem;color:var(--accent);font-size:0.8rem;font-weight:600;}}
</style>
</head>
<body>
<div class="header">
    <h1>{title}</h1>
    <p class="sub">{subtitle}</p>
</div>
<div class="grid">{cards}</div>
</body>
</html>"""

def build_vol(pdf_list, vol_num, title, subtitle, name_meta):
    zim_out = f"zim_downloads/National_Geographic_Vol{vol_num}_v11.zim"
    aids = {get_aid(p) for p in pdf_list}
    index_html = make_index_html(pdf_list, title, subtitle)
    print(f"\nBuilding {zim_out} ({len(pdf_list)} magazines)...")

    with Creator(zim_out) as creator:
        creator.add_metadata("Title", title[:30])
        creator.add_metadata("Language", "eng")
        creator.add_metadata("Creator", "Custom ZIM Builder")
        creator.add_metadata("Publisher", "Hickory Search")
        creator.add_metadata("Description", subtitle[:80])
        creator.add_metadata("Name", name_meta)
        creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
        creator.add_illustration(48, favicon_bytes)
        creator.set_mainpath("C/index.html")
        creator.add_item(ZimItem("C/index.html", index_html, "text/html", is_file=False, front=True))

        count = 0
        for root, dirs, files in os.walk(natgeo_dir):
            if "texts" in root.split(os.sep):
                continue
            if "pdfs_original" in root.split(os.sep):
                continue
            for file in files:
                local_path = os.path.join(root, file)
                zim_path = os.path.relpath(local_path, natgeo_dir).replace("\\", "/")
                # Skip root index.html — already added as the main page
                if zim_path == "index.html":
                    continue
                ext = os.path.splitext(file)[1].lower()
                mimetype = mimetype_map.get(ext, "application/octet-stream")

                # If it's in the pdfs folder, only include files belonging to this volume
                if "pdfs" in root.split(os.sep):
                    aid = os.path.splitext(file)[0]
                    if aid not in aids:
                        continue

                creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
                count += 1

    print(f"Done: {zim_out} ({count} items)")

build_vol(
    classic_pdfs, 1,
    "Nat Geo Vol 1: Classic",
    "National Geographic Classic Collection 1888-1953",
    "nat_geo_vol1_classic_v11"
)

build_vol(
    modern_pdfs, 2,
    "Nat Geo Vol 2: Modern",
    "National Geographic Modern Collection 2009-2019",
    "nat_geo_vol2_modern_v11"
)

print("\nAll done!")
