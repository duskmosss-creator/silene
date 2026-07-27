import os
from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint

print("Building Appalachian Corridor ZIM file with PDF.js and offline WAV audio...")

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

content_dir = "content"
zim_filename = "Appalachian_Corridor.zim"

with Creator(zim_filename) as creator:
    creator.set_mainpath("index.html")
    
    with open(f"{content_dir}/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    creator.add_item(ZimItem("index.html", html_content, "text/html", is_file=False))
    
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file == "index.html":
                continue
                
            local_path = os.path.join(root, file)
            zim_path = os.path.relpath(local_path, content_dir).replace("\\", "/")
            
            mimetype = "text/plain"
            if file.endswith(".json"):
                mimetype = "application/json"
            elif file.endswith(".html"):
                mimetype = "text/html"
            elif file.endswith(".pdf"):
                mimetype = "application/pdf"
            elif file.endswith(".wav"):
                mimetype = "audio/wav"
            elif file.endswith(".mp3"):
                mimetype = "audio/mpeg"
            elif file.endswith(".js"):
                mimetype = "application/javascript"
            elif file.endswith(".css"):
                mimetype = "text/css"
                
            creator.add_item(ZimItem(zim_path, local_path, mimetype, is_file=True))

print(f"ZIM file {zim_filename} created successfully.")
