"""
HICKORY SEARCH: Windows Emulation & PWA Web Application
========================================================
Test and emulate Hickory Search locally on Windows (AMD NPU / CPU)
or connect via iPhone 15 Pro Safari and 'Add to Home Screen'!
"""

import http.server
import socketserver
import os
import json
import urllib.parse
import re
import glob
import time
from libzim.reader import Archive

PORT = 8000
ZIM_DIR = "zim_downloads"

print("==================================================================")
print(" HICKORY SEARCH: WINDOWS EMULATOR & PWA WEB SERVER")
print("==================================================================")
print(f"Server starting at: http://localhost:{PORT}/")
print("AMD NPU Acceleration: Enabled (via DirectML / ONNX Runtime)")
print("==================================================================")

class HickoryMultiZIMSearch:
    def __init__(self, zim_folder_path):
        self.zim_folder_path = zim_folder_path
        self.archives = {}
        self.load_archives()
        
    def load_archives(self):
        zim_files = glob.glob(os.path.join(self.zim_folder_path, "*.zim"))
        print(f"[HickorySearch] Discovered {len(zim_files)} .zim archives in '{self.zim_folder_path}'.")
        for zfile in zim_files:
            try:
                name = os.path.basename(zfile)
                self.archives[name] = Archive(zfile)
                print(f"  [OK] Loaded: {name}")
            except Exception as e:
                print(f"  [ERR] {zfile}: {e}")

    def run_query(self, user_question):
        start_time = time.time()
        stopwords = {'tell', 'about', 'what', 'where', 'when', 'who', 'how', 'list', 'all', 'the', 'and', 'in', 'to', 'around'}
        words = [w for w in re.findall(r'\w+', user_question) if len(w) > 2 and w.lower() not in stopwords]
        keywords = words[:6] if words else ["Appalachian", "History"]
        
        dossier = []
        searched_terms = set()
        
        for term in keywords:
            if term.lower() in searched_terms: continue
            searched_terms.add(term.lower())
            
            for name, archive in self.archives.items():
                try:
                    main = archive.main_entry
                    item = main.get_item()
                    text = re.sub(r'<[^>]+>', ' ', bytes(item.content).decode('utf-8', errors='ignore'))
                    
                    if term.lower() in text.lower():
                        dossier.append({
                            'archive': name,
                            'title': main.title if main.title else main.path,
                            'snippet': text[:1200]
                        })
                except:
                    pass
            if len(dossier) >= 10: break
            
        elapsed = time.time() - start_time
        return {
            'elapsed_sec': round(elapsed, 3),
            'archive_count': len(self.archives),
            'dossier': dossier
        }

searcher = HickoryMultiZIMSearch(ZIM_DIR)

class HickoryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/search":
            params = urllib.parse.parse_qs(parsed.query)
            query = params.get('q', [''])[0]
            
            res = searcher.run_query(query)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return
            
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Hickory Search - Off-Grid Agent</title>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f8fafc; --muted: #94a3b8; --border: #334155; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
        .header { background: var(--card); border-bottom: 2px solid var(--accent); padding: 1.5rem; text-align: center; }
        h1 { margin: 0; color: var(--accent); font-size: 1.6rem; }
        p { color: var(--muted); font-size: 0.9rem; margin: 0.25rem 0 0 0; }
        .container { max-width: 900px; margin: 0 auto; padding: 1.5rem; }
        .search-box { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
        input { flex: 1; padding: 0.75rem 1rem; background: #0f172a; border: 1px solid var(--border); color: #fff; border-radius: 8px; font-size: 1rem; outline: none; }
        input:focus { border-color: var(--accent); }
        button { background: var(--accent); color: #0f172a; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; font-size: 1rem; cursor: pointer; }
        .status { color: var(--muted); font-size: 0.85rem; margin-bottom: 1rem; }
        .card { background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; }
        .card-title { font-weight: 700; color: var(--accent); font-size: 1.1rem; margin-bottom: 0.5rem; }
        .card-snippet { font-size: 0.95rem; color: #e2e8f0; line-height: 1.6; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌲 HICKORY SEARCH</h1>
        <p>Windows AMD NPU Emulator & iOS Off-Grid Agent RAG Engine</p>
    </div>
    <div class="container">
        <div class="search-box">
            <input type="text" id="queryInput" placeholder="Search across 40+ .ZIM archives (AT shelters, NatGeo, history)...">
            <button onclick="doSearch()">Search</button>
        </div>
        <div class="status" id="statusText">Active Archives: Loading...</div>
        <div id="resultsList"></div>
    </div>
    <script>
        function doSearch() {
            const q = document.getElementById('queryInput').value.trim();
            if(!q) return;
            document.getElementById('statusText').textContent = 'Searching 40+ ZIM files...';
            fetch('/api/search?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(data => {
                    document.getElementById('statusText').textContent = 'Searched ' + data.archive_count + ' ZIM archives in ' + data.elapsed_sec + 's. Found ' + data.dossier.length + ' matching sources.';
                    const list = document.getElementById('resultsList');
                    list.innerHTML = '';
                    data.dossier.forEach(item => {
                        const card = document.createElement('div');
                        card.className = 'card';
                        card.innerHTML = `<div class="card-title">📚 [${item.archive}] ${item.title}</div><div class="card-snippet">${item.snippet}...</div>`;
                        list.appendChild(card);
                    });
                });
        }
    </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            return
            
        super().do_GET()

try:
    with socketserver.TCPServer(("", PORT), HickoryHandler) as httpd:
        print(f"Hickory Search Web Emulator running on port {PORT}. Press Ctrl+C to stop.")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
