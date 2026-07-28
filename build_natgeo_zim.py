import os
import re
import base64
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint

print("Building National Geographic ZIM file (bundling active gallery magazine issues)...")

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

from datetime import datetime

natgeo_dir = "natgeo_collection"
zim_filename = os.path.join("zim_downloads", "National_Geographic_Appalachian_Collection_v2.zim")

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

# Collect all referenced paths from index.html
referenced_paths = set(re.findall(r'["\']((?:images|pdfs|texts|js)/[^"\']+)["\']', html_content))

with Creator(zim_filename) as creator:
    creator.add_metadata("Title", "NatGeo Appalachia Col v2")
    creator.add_metadata("Language", "eng")
    creator.add_metadata("Creator", "Custom ZIM Builder")
    creator.add_metadata("Publisher", "Hickory Search")
    creator.add_metadata("Description", "National Geographic Appalachian magazines collection for iOS and Kiwix")
    creator.add_metadata("Name", "national_geographic_appalachian_collection_v2")
    creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
    
    favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
    favicon_bytes = base64.b64decode(favicon_b64)
    creator.add_illustration(48, favicon_bytes)
    
    creator.set_mainpath("C/index.html")
    creator.add_item(ZimItem("C/index.html", html_content, "text/html", is_file=False))
    
    # set_mainpath handles main article entry cleanly
    pass
    
    item_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(natgeo_dir):
        for file in files:
            if file == "index.html":
                continue
                
            local_path = os.path.join(root, file)
            zim_path = os.path.relpath(local_path, natgeo_dir).replace("\\", "/")
            
            ext = os.path.splitext(file)[1].lower()
            
            # If it's a PDF, only include it if it's referenced in index.html or has a matching .html viewer
            if ext == ".pdf":
                stem = os.path.splitext(file)[0]
                matching_html = os.path.join(natgeo_dir, "pdfs", f"{stem}.html")
                if not os.path.exists(matching_html) and zim_path not in referenced_paths:
                    print(f"  [SKIP ORPHAN PDF] {zim_path}")
                    skipped_count += 1
                    continue

            mimetype = mimetype_map.get(ext, "application/octet-stream")
            creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
            item_count += 1

print(f"ZIM file {zim_filename} created successfully with {item_count} bundled items ({skipped_count} orphan PDFs skipped).")
