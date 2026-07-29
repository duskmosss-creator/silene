import os
import re
import base64
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
from datetime import datetime

print("Building National Geographic ZIM file (static cards, active gallery only)...")

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
        return {Hint.FRONT_ARTICLE: True} if self.path == "index.html" else {}


natgeo_dir = "natgeo_collection"
# Write directly to root ZIM (the one Kiwix loads)
zim_filename = "National_Geographic_Appalachian_Collection.zim"

mimetype_map = {
    ".html": "text/html",
    ".txt": "text/plain",
    ".json": "application/json",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".js": "application/javascript",
    ".css": "text/css",
    ".pdf": "application/pdf"
}

with open(f"{natgeo_dir}/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Collect active stems from static card hrefs in index.html (can be pdfs/ or texts/)
active_pdf_stems = set()
for stem in re.findall(r'href="(?:pdfs|texts)/([^"]+)\.html"', html_content):
    active_pdf_stems.add(stem)

print(f"Active magazine items in index: {len(active_pdf_stems)}")
for stem in sorted(active_pdf_stems):
    print(f"  - {stem}")

with Creator(zim_filename) as creator:
    creator.add_metadata("Title", "National Geographic Appalachian Collection")
    creator.add_metadata("Language", "eng")
    creator.add_metadata("Creator", "Custom ZIM Builder")
    creator.add_metadata("Publisher", "Hickory Search")
    creator.add_metadata("Description", "National Geographic Appalachian magazines collection for Kiwix and iOS")
    creator.add_metadata("Name", "national_geographic_appalachian_collection_v7")
    creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
    
    favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
    favicon_bytes = base64.b64decode(favicon_b64)
    creator.add_illustration(48, favicon_bytes)
    
    # Set main path for Kiwix
    creator.set_mainpath("C/index.html")
    creator.add_item(ZimItem("C/index.html", html_content, "text/html", is_file=False))
    
    item_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(natgeo_dir):
        for file in files:
            if file == "index.html":
                continue
                
            local_path = os.path.join(root, file)
            zim_path = os.path.relpath(local_path, natgeo_dir).replace("\\", "/")
            
            ext = os.path.splitext(file)[1].lower()
            stem = os.path.splitext(file)[0]
            
            # STRICT: Only include PDFs whose stem is an active gallery item
            if ext == ".pdf":
                if stem not in active_pdf_stems:
                    skipped_count += 1
                    continue

            # STRICT: Only include PDF viewer HTMLs for active gallery items
            if ext == ".html" and zim_path.startswith("pdfs/"):
                if stem not in active_pdf_stems:
                    skipped_count += 1
                    continue

            # STRICT: Only include text HTMLs/txts for active gallery items  
            if ext in (".txt", ".html") and zim_path.startswith("texts/"):
                if stem not in active_pdf_stems:
                    skipped_count += 1
                    continue

            # STRICT: Only include cover images for active gallery items
            if ext in (".jpg", ".jpeg", ".png", ".webp") and zim_path.startswith("images/"):
                img_stem = stem.replace("_cover", "")
                if img_stem not in active_pdf_stems:
                    skipped_count += 1
                    continue

            # STRICT: Only include .json metadata for active gallery items
            if ext == ".json":
                if stem not in active_pdf_stems:
                    skipped_count += 1
                    continue

            mimetype = mimetype_map.get(ext, "application/octet-stream")
            # Prepend C/ to the zim_path
            creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
            item_count += 1
            if item_count % 10 == 0:
                print(f"  Added {item_count} items...")

print(f"\nZIM '{zim_filename}' built: {item_count} items included, {skipped_count} orphan items skipped.")
