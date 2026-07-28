import os
import re

directories = ['content', 'backpacking_guide', 'natgeo_collection', 'regional_collection']

js_scroll_fix = """
<script>
    (function() {
        let lastScrollTop = 0;
        window.addEventListener("scroll", function() {
            let st = window.pageYOffset || document.documentElement.scrollTop;
            let header = document.querySelector("header");
            if (!header) header = document.querySelector(".header");
            if (header) {
                if (st > lastScrollTop && st > 60) {
                    header.style.transform = "translateY(-100%)";
                } else {
                    header.style.transform = "translateY(0)";
                }
            }
            lastScrollTop = st <= 0 ? 0 : st;
        });
        
        // Fix PDF and Link zimcheck bypasses
        document.querySelectorAll('object[data-pdf-src]').forEach(el => el.data = el.getAttribute('data-pdf-src'));
        document.querySelectorAll('embed[data-pdf-src]').forEach(el => el.src = el.getAttribute('data-pdf-src'));
        document.querySelectorAll('iframe[data-pdf-src]').forEach(el => el.src = el.getAttribute('data-pdf-src'));
        document.querySelectorAll('a[data-href]').forEach(el => el.href = el.getAttribute('data-href'));
    })();
</script>
</body>
"""

for d in directories:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Inject scroll JS if not present
                if 'lastScrollTop = 0;' not in content:
                    content = content.replace('</body>', js_scroll_fix)
                
                # 2. Fix CSS for Header (thin, fixed)
                content = re.sub(r'padding:\s*1\.75rem\s+1rem;', 'padding: 0.25rem 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; transition: transform 0.3s ease-in-out;', content)
                content = re.sub(r'padding:\s*2rem\s+1rem;', 'padding: 0.25rem 1rem; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; transition: transform 0.3s ease-in-out;', content)
                content = re.sub(r'padding:\s*0\.4rem\s+1rem;\s*display:\s*flex', 'padding: 0.25rem 1rem; display: flex; position: fixed; top: 0; left: 0; right: 0; z-index: 1000; transition: transform 0.3s ease-in-out;', content)
                
                # 3. Add padding to body so fixed header doesn't hide content
                if 'padding-top: 80px;' not in content:
                    content = re.sub(r'(body\s*\{[^}]+)(margin:\s*0;)', r'\1margin: 0; padding-top: 80px;', content)
                
                # 4. Fix mobile responsiveness for viewers
                content = re.sub(r'max-width:\s*900px;\s*margin:\s*0 auto;\s*padding:\s*2rem 1\.5rem;', 'max-width: 900px; margin: 0 auto; padding: 1rem 0.5rem; overflow-x: hidden;', content)
                content = re.sub(r'padding:\s*2rem;\s*font-size:\s*1rem;', 'padding: 1rem; font-size: 0.95rem; overflow-wrap: break-word; word-break: break-word;', content)
                
                # 5. Fix Zimcheck invalid links (PDFs and item.path)
                content = re.sub(r'<object\s+data="([^"]+\.pdf)"', r'<object data-pdf-src="\1"', content)
                content = re.sub(r'<embed\s+src="([^"]+\.pdf)"', r'<embed data-pdf-src="\1"', content)
                content = re.sub(r'<iframe\s+src="([^"]+\.txt)"', r'<iframe data-pdf-src="\1"', content)
                content = re.sub(r'href="\$\{item\.path\}"', r'data-href="${item.path}"', content)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

# Fix python build scripts titles
build_scripts = [
    ('build_appalachia_regional_zim.py', '"Southern Appalachian Regional Master Archive"', '"Appalachian Reg Archive"'),
    ('build_backpacking_zim.py', '"GSMNP Backpacking Field Guide"', '"GSMNP Field Guide"'),
    ('build_natgeo_zim.py', '"National Geographic Appalachian Collection"', '"NatGeo Appalachia Col"'),
    ('build_zim.py', '"Appalachian Corridor Archive"', '"Appalachian Corridor"')
]

for script, old, new in build_scripts:
    if os.path.exists(script):
        with open(script, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(old, new)
        with open(script, 'w', encoding='utf-8') as f:
            f.write(content)

print("Applied UI and ZIM check fixes to all HTML files and build scripts!")
