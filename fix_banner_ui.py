import os
import re

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

def clean_header_css(content):
    # Regex to find .header { ... } and replace it
    pattern = re.compile(r'\.header\s*\{[^}]+\}', re.MULTILINE | re.DOTALL)
    replacement = """.header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 0.4rem 1rem;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            transition: transform 0.3s ease-in-out;
        }}"""
    return pattern.sub(replacement, content)

def clean_header_html(content):
    # Find the title inside the existing header
    title_match = re.search(r'<div class="header">.*?<h1>(.*?)</h1>', content, re.MULTILINE | re.DOTALL)
    title = title_match.group(1) if title_match else "Document Viewer"
    
    # We want to replace the whole <div class="header"> block.
    # The header block usually ends before <div class="container"> or <div class="scroll-container">
    # We can match from <div class="header"> to the div right before <div class="container"
    pattern = re.compile(r'<div class="header">.*?(?=<div class="(?:container|scroll-container)")', re.MULTILINE | re.DOTALL)
    
    new_header = f"""<div class="header">
        <div style="max-width: 950px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <h1 style="font-size: 0.95rem; margin: 0; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 75%;">{title}</h1>
            <a href="../index.html" onclick="if(window.history.length>1){{window.history.back();return false;}}else{{location.href='../index.html';return false;}}" style="font-size: 0.85rem; white-space: nowrap; color: var(--accent); text-decoration: none; font-weight: 600;">← Back</a>
        </div>
    </div>
    
    """
    
    return pattern.sub(new_header, content)


for d in directories:
    for folder in ['texts', 'pdfs']:
        target_dir = os.path.join(d, folder)
        if not os.path.exists(target_dir):
            continue
            
        for file in os.listdir(target_dir):
            if file.endswith('.html'):
                filepath = os.path.join(target_dir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = clean_header_css(content)
                content = clean_header_html(content)
                
                # Make sure the scroll JS logic points to .header properly
                # My previous script added window.addEventListener("scroll", ...) which uses document.querySelector(".header")
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched header in {filepath}")

# We should also patch the python scraper files so if we regenerate them they have the clean banner.
# Actually I will just replace the template manually in the python files using regex.
scrapers = ['scrape.py', 'scrape_backpacking.py', 'scrape_natgeo.py']
for script in scrapers:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace .header CSS in py templates
        content = re.sub(r'\.header\s*\{[^}]+\}', """.header {
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 0.4rem 1rem;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            transition: transform 0.3s ease-in-out;
        }""", content)
        
        with open(script, 'w', encoding='utf-8') as f:
            f.write(content)

print("Banner UI fixed and S/M/L buttons removed.")
