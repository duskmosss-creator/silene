import urllib.request
import re

try:
    html = urllib.request.urlopen('https://download.openzim.org/release/zim-tools/').read().decode('utf-8')
    links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
    for link in links:
        if "win" in link.lower() or ".zip" in link.lower() or ".exe" in link.lower():
            print(link)
except Exception as e:
    print(f"Error: {e}")
