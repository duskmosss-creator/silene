import sys
sys.stdout.reconfigure(encoding='utf-8')
from libzim.reader import Archive
import re

# Check the actual ZIM index.html directly for the "40" near top right UI
a = Archive('zim_downloads/Appalachian_Corridor.zim')
e = a.get_entry_by_path('index.html')
item = e.get_item()
raw = bytes(item.content).decode('utf-8', errors='ignore')

# Find the header/nav area  
header_idx = raw.find('<header')
if header_idx == -1:
    header_idx = raw.find('<nav')
print("=== Header/Nav area ===")
print(raw[header_idx:header_idx+800])
print()

# Also find "XL" in context — the font button at top right
xl_idx = raw.find('>XL<')
print("=== XL button context ===")
print(raw[max(0,xl_idx-300):xl_idx+50])
print()

# Count total items
match = re.search(r'const searchData\s*=\s*(\[.*?\]);', raw, re.DOTALL)
if match:
    import json
    data = json.loads(match.group(1))
    print(f"Total searchData items: {len(data)}")
    # Check for overflow on body
    
# Look in the HTML for overflow hidden
body_idx = raw.find('<body')
print("=== Body tag ===")
print(raw[body_idx:body_idx+100])
