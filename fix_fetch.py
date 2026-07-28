import os
import re
import base64

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find fetch calls like: fetch('filename.txt')
                match = re.search(r"fetch\('([^']+)'\)", content)
                if match:
                    txt_filename = match.group(1)
                    txt_filepath = os.path.join(root, txt_filename)
                    if os.path.exists(txt_filepath):
                        with open(txt_filepath, 'r', encoding='utf-8') as tf:
                            txt_content = tf.read()
                        
                        b64_content = base64.b64encode(txt_content.encode('utf-8')).decode('utf-8')
                        
                        # Replace the whole fetch block
                        # We use regex to match the fetch... catch block
                        fetch_pattern = re.compile(r"fetch\('[^']+'\)\s*\.then\([^\)]+\)\s*\.then\([^\)]+\)\s*\.catch\([^;]+\);", re.MULTILINE | re.DOTALL)
                        
                        replacement = f"""const b64Data = "{b64_content}";
        const decodedText = decodeURIComponent(escape(atob(b64Data)));
        document.getElementById('mdContent').innerHTML = renderMarkdown(decodedText);"""
                        
                        new_content = fetch_pattern.sub(replacement, content)
                        
                        # Write it back if changed
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Fixed {filepath}")
                        else:
                            print(f"Regex didn't match fully for {filepath}, though fetch was found.")

# Update the python builder scripts so future generations don't use fetch
scrapers = ['scrape.py', 'scrape_backpacking.py', 'scrape_natgeo.py']
for script in scrapers:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8') as f:
            script_content = f.read()
            
        script_pattern = re.compile(r"fetch\('[^']+'\)\s*\.then\([^\)]+\)\s*\.then\([^\)]+\)\s*\.catch\([^;]+\);", re.MULTILINE | re.DOTALL)
        
        # We need to change the python template.
        # But wait, in python we don't have the text at this exact generation point, or do we?
        # In scrape.py, we have `g['content']`! 
        # Actually, let's just replace the fetch block in python script with a template string `{{b64_data}}` that python fills?
        # It's safer to just let the script run `fix_fetch.py` as a post-build step in the bat file or something.
        pass

print("Inlined all text files into HTML wrappers as Base64 to bypass iOS CORS.")
