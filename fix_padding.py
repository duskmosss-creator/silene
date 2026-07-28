import os
import re

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

# Fix HTML files
for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = re.sub(r'padding:\s*1\.25rem\s+1\.5rem;', 'padding: 0.25rem 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; transition: transform 0.3s ease-in-out;', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

# Fix Python scrapers too
scrapers = ['scrape.py', 'scrape_backpacking.py', 'scrape_natgeo.py']
for script in scrapers:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'padding:\s*1\.25rem\s+1\.5rem;', 'padding: 0.25rem 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; transition: transform 0.3s ease-in-out;', content)
        with open(script, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed missed paddings!")
