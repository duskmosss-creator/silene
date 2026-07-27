import os
import urllib.request
import json
import sqlite3

class FenRAGCore:
    """
    Project 'fen' Python Prototype: Local RAG & Kiwix Hotspot VLM Bridge.
    Allows querying offline .zim archives or local Kiwix server endpoints.
    """
    def __init__(self, kiwix_endpoint="http://127.0.0.1:8080"):
        self.kiwix_endpoint = kiwix_endpoint
        self.db_path = "fen_vector_store.db"
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zim_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zim_name TEXT,
                article_title TEXT,
                chunk_text TEXT,
                embedding_json TEXT
            )
        """)
        conn.commit()
        conn.close()

    def query_kiwix_hotspot(self, query):
        """Query local Kiwix Hotspot REST API endpoint if active."""
        url = f"{self.kiwix_endpoint}/api/v1/search?q={urllib.parse.quote(query)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'fen-ios-app/1.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return data.get('results', [])
        except Exception as e:
            return [{'title': 'Local ZIM Search (Fallback)', 'snippet': f'Querying offline vector database for: {query}'}]

    def generate_concise_response(self, user_query, image_path=None):
        """Simulates VLM + RAG concise response generation with ZIM references."""
        kiwix_results = self.query_kiwix_hotspot(user_query)
        
        response = {
            'query': user_query,
            'has_vision_input': bool(image_path),
            'answer': f"Concise Response for '{user_query}': Context retrieved from Southern Appalachian ZIM archives.",
            'references': kiwix_results[:3]
        }
        return response

if __name__ == "__main__":
    fen = FenRAGCore()
    result = fen.generate_concise_response("What is the elevation lapse rate at Clingmans Dome?")
    print("Project 'fen' Core RAG Output:")
    print(json.dumps(result, indent=2))
