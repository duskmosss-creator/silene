import os
import re
import base64

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

decoder_js = """const binStr = atob(b64Data);
        const bytes = new Uint8Array(binStr.length);
        for (let i = 0; i < binStr.length; i++) { bytes[i] = binStr.charCodeAt(i); }
        const decodedText = new TextDecoder('utf-8').decode(bytes);"""

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace old decodeURIComponent(escape(atob(b64Data))) if present
                old_decoder = "const decodedText = decodeURIComponent(escape(atob(b64Data)));"
                if old_decoder in content:
                    content = content.replace(old_decoder, decoder_js)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated decoder in {filepath}")
                
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
        {decoder_js}
        document.getElementById('mdContent').innerHTML = renderMarkdown(decodedText);"""
                        
                        fetch_pattern = re.compile(r"fetch\('[^']+'\).*?\.catch\([^\n]+\);", re.MULTILINE | re.DOTALL)
                        
                        new_content = fetch_pattern.sub(replacement, content)
                        
                        if new_content != content:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            print(f"Fixed fetch in {filepath}")

print("Updated Base64 decoding logic to robust TextDecoder across all files.")
