import os
import base64
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint

print("Building GSMNP Backpacking Field Guide ZIM file...")

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

b_dir = "backpacking_guide"
zim_filename = os.path.join("zim_downloads", "GSMNP_Backpacking_Field_Guide.zim")

with Creator(zim_filename) as creator:
    creator.add_metadata("Title", "GSMNP Field Guide")
    creator.add_metadata("Language", "eng")
    creator.add_metadata("Creator", "Custom ZIM Builder")
    creator.add_metadata("Publisher", "Hickory Search")
    creator.add_metadata("Description", "GSMNP & DuPont Backpacking Field Manual for iOS and Kiwix")
    creator.add_metadata("Name", "gsmnp_backpacking_field_guide")
    creator.add_metadata("Date", datetime.now().strftime("%Y-%m-%d"))
    
    favicon_b64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAcSURBVGhD7cExAQAAAMKg9U9tCy8gAAAAAAA8Bw1AAAEVv+wMAAAAAElFTkSuQmCC"
    favicon_bytes = base64.b64decode(favicon_b64)
    creator.add_illustration(48, favicon_bytes)
    
    creator.set_mainpath("C/index.html")
    
    with open(f"{b_dir}/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    creator.add_item(ZimItem("C/index.html", html_content, "text/html", is_file=False))
    
    # set_mainpath handles main article entry cleanly
    pass
    
    for root, dirs, files in os.walk(b_dir):
        for file in files:
            if file == "index.html":
                continue
                
            local_path = os.path.join(root, file)
            zim_path = os.path.relpath(local_path, b_dir).replace("\\", "/")
            
            ext = os.path.splitext(file)[1].lower()
            mimetype_map = {
                ".html": "text/html",
                ".txt": "text/plain",
                ".json": "application/json",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".css": "text/css",
                ".js": "application/javascript"
            }
            mimetype = mimetype_map.get(ext, "application/octet-stream")
            creator.add_item(ZimItem(f"C/{zim_path}", local_path, mimetype, is_file=True))

print(f"ZIM file {zim_filename} created successfully.")
