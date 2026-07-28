import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = "content"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print("==================================================================")
print(" ZIMIT HTTP SERVER & AUTOMATIC CRAWLER PIPELINE")
print("==================================================================")
print(f"Serving local offline archive directory '{DIRECTORY}' at:")
print(f" -> http://127.0.0.1:{PORT}/")
print("")
print("To generate a Zimit archive using openzim/zimit, run in another terminal:")
print(f"  zimit --url http://127.0.0.1:{PORT}/ --output zim_downloads/Appalachian_Corridor_Zimit.zim --title \"Appalachian Corridor Archive\"")
print("==================================================================")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("HTTP Server active. Press Ctrl+C to stop.")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nHTTP Server stopped.")
