import os
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint

print("Building ZIM file...")

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

with Creator("Appalachian_Corridor.zim") as creator:
    creator.set_mainpath("index.html")
    
    # Add index
    with open("content/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    creator.add_item(ZimItem("index.html", html_content, "text/html", is_file=False))
    
    # Add files
    for root, dirs, files in os.walk("content"):
        for file in files:
            if file == "index.html":
                continue
                
            local_path = os.path.join(root, file)
            # Make the ZIM path relative to content/
            zim_path = os.path.relpath(local_path, "content").replace("\\", "/")
            
            mimetype = "application/octet-stream"
            if file.endswith(".txt"):
                mimetype = "text/plain"
            elif file.endswith(".json"):
                mimetype = "application/json"
            elif file.endswith(".html"):
                mimetype = "text/html"
            elif file.endswith(".mp3"):
                mimetype = "audio/mpeg"
                
            creator.add_item(ZimItem(zim_path, local_path, mimetype, is_file=True))

print("ZIM file Appalachian_Corridor.zim created successfully.")
