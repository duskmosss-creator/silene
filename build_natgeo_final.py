import os
import base64
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint
from datetime import datetime

print("Building National Geographic Collection ZIM file (bundling PDFs and HTML)...")

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

content_dir = "natgeo_collection"
zim_filename = os.path.join("zim_downloads", "National_Geographic_Appalachian_Collection_v8.zim")

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

with Creator(zim_filename) as creator:
    creator.add_metadata("Title", "Nat Geo Collection")
    creator.add_metadata("Language", "eng")
    creator.add_metadata("Creator", "Custom ZIM Builder")
    creator.add_metadata("Publisher", "Hickory Search")
    creator.add_metadata("Description", "National Geographic Magazine Archive for iOS and Kiwix")
    creator.add_metadata("Name", "national_geographic_collection_v8")
    creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
    
    # Generic base64 favicon for the ZIM
    favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
    favicon_bytes = base64.b64decode(favicon_b64)
    creator.add_illustration(48, favicon_bytes)
    
    creator.set_mainpath("C/index.html")
    
    with open(f"{content_dir}/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    creator.add_item(ZimItem("C/index.html", html_content, "text/html", is_file=False))
    
    item_count = 0
    for root, dirs, files in os.walk(content_dir):
        # Exclude texts directory entirely to prevent orphaned items or confusion
        if "texts" in root.split(os.sep):
            continue
            
        for file in files:
            if file == "index.html" and root == content_dir:
                continue # Already added as C/index.html
                
            local_path = os.path.join(root, file)
            zim_path = os.path.relpath(local_path, content_dir).replace("\\", "/")
            
            ext = os.path.splitext(file)[1].lower()
            mimetype = mimetype_map.get(ext, "application/octet-stream")
                
            creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))
            item_count += 1

print(f"ZIM file {zim_filename} created successfully with {item_count} bundled items.")
