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
                        
                        replacement = f"""const b64Data = "{b64_content}";
        const decodedText = decodeURIComponent(escape(atob(b64Data)));
        document.getElementById('mdContent').innerHTML = renderMarkdown(decodedText);"""
                        
                        # Use a simpler regex that matches everything from fetch('...') to the ending catch(...);
                        fetch_pattern = re.compile(r"fetch\('[^']+'\).*?\.catch\([^\n]+\);", re.MULTILINE | re.DOTALL)
                        
                        new_content = fetch_pattern.sub(replacement, content)
                        
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Fixed {filepath}")
                        else:
                            print(f"Regex didn't match fully for {filepath}")

print("Inlined all text files into HTML wrappers as Base64 to bypass iOS CORS.")
