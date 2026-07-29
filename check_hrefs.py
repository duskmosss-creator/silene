import re

with open('natgeo_collection/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'window.location' in content: print('Has window.location')
if 'replace(' in content: print('Has replace(')

print("Hrefs found:")
for href in re.findall(r'href="([^"]+)"', content):
    print("  -", href)
