import os
import re

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

# Fix the HTML files
for d in directories:
    texts_dir = os.path.join(d, 'texts')
    if not os.path.exists(texts_dir):
        continue
    for file in os.listdir(texts_dir):
        if file.endswith('.html'):
            filepath = os.path.join(texts_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the literal newline bug
            bad_string = "const lines = md.split('\n');"
            good_string = "const lines = md.split('\\n');"
            
            if bad_string in content:
                content = content.replace(bad_string, good_string)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed JS syntax bug in {filepath}")

# Fix the Python scrapers
scrapers = ['scrape.py', 'scrape_backpacking.py', 'scrape_natgeo.py', 'scrape_appalachia_regional.py']
for script in scrapers:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8') as f:
            content = f.read()
            
        bad_python_string = "const lines = md.split('\\n');"
        good_python_string = "const lines = md.split('\\\\n');"
        
        # Wait, if it's already `const lines = md.split('\n');` in python file:
        if "const lines = md.split('\\n');" in content:
             content = content.replace("const lines = md.split('\\n');", "const lines = md.split('\\\\n');")
             with open(script, 'w', encoding='utf-8') as f:
                 f.write(content)
             print(f"Fixed python template bug in {script}")

print("Syntax bugs fixed!")
