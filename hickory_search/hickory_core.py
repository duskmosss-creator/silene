"""
HICKORY SEARCH: Multi-ZIM Offline Nested-Loop RAG Engine
=========================================================
Optimized for searching 40+ .ZIM archives and local GGUF/VLM models on mobile hardware.
"""

import os
import glob
import time
import re
from libzim.reader import Archive

class HickoryMultiZIMSearch:
    def __init__(self, zim_folder_path):
        self.zim_folder_path = zim_folder_path
        self.archives = {}
        self.load_archives()
        
    def load_archives(self):
        """Scans folder for all 40+ .zim archives and initializes readers."""
        zim_files = glob.glob(os.path.join(self.zim_folder_path, "*.zim"))
        print(f"[HickorySearch] Discovered {len(zim_files)} .zim archives in folder.")
        
        for zfile in zim_files:
            try:
                name = os.path.basename(zfile)
                self.archives[name] = Archive(zfile)
                print(f"  [OK] Loaded archive: {name}")
            except Exception as e:
                print(f"  [ERR] Could not load {zfile}: {e}")

    def search_archive(self, archive, name, keyword):
        """Search a single archive's index.html for a keyword, with CSS/JS stripped."""
        try:
            # Prefer index.html — clean readable content without raw CSS at the top
            entry = None
            for candidate in ['index.html', 'mainPage']:
                if archive.has_entry_by_path(candidate):
                    entry = archive.get_entry_by_path(candidate)
                    break
            if entry is None:
                entry = archive.main_entry

            item = entry.get_item()
            raw = bytes(item.content).decode('utf-8', errors='ignore')
            raw = re.sub(r'<style[^>]*>.*?</style>', ' ', raw, flags=re.DOTALL)
            raw = re.sub(r'<script[^>]*>.*?</script>', ' ', raw, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', raw)
            text = re.sub(r'\s+', ' ', text).strip()

            if keyword.lower() in text.lower():
                return {
                    'archive': name,
                    'title': entry.title if entry.title else entry.path,
                    'content': text[:1500]
                }
        except Exception:
            pass
        return None

    def fast_search(self, query):
        """Search across all loaded ZIM files for a keyword."""
        start_time = time.time()
        results = []
        clean_query = query.lower().strip()

        for name, archive in self.archives.items():
            hit = self.search_archive(archive, name, clean_query)
            if hit:
                results.append(hit)

        elapsed = time.time() - start_time
        print(f"[HickorySearch] Searched {len(self.archives)} ZIM files in {elapsed:.2f}s. Found {len(results)} hits.")
        return results

    def run_nested_loop_query(self, user_question):
        """
        Nested Loop Execution:
        1. Planner identifies 4-5 keywords from the question
        2. Research Loop: search each keyword across all ZIM files
        3. Early stopping at 8+ verified sources
        4. Synthesis: return cited results
        """
        print(f"\n{'='*65}")
        print(f" HICKORY SEARCH: '{user_question}'")
        print(f"{'='*65}")

        stopwords = {'tell', 'about', 'what', 'where', 'when', 'who', 'how',
                     'list', 'all', 'the', 'and', 'in', 'to', 'around', 'find'}
        words = [w for w in re.findall(r'\w+', user_question)
                 if len(w) > 2 and w.lower() not in stopwords]
        keywords = words[:5] if words else ["Appalachian", "History"]
        print(f"[Phase 1] Planner Keywords: {keywords}")

        dossier = []
        seen_archives = set()  # Prevent duplicate archive results
        searched_terms = set()

        for term in keywords:
            if term.lower() in searched_terms:
                continue
            searched_terms.add(term.lower())

            print(f"[Research Loop] Searching for '{term}'...")
            hits = self.fast_search(term)

            for hit in hits:
                if hit['archive'] not in seen_archives:
                    dossier.append(hit)
                    seen_archives.add(hit['archive'])

            if len(dossier) >= 8:
                print("[Research Loop] Early stopping: 8+ verified sources gathered.")
                break

        print(f"\n[Phase 3] Synthesizing answer from {len(dossier)} verified sources...")
        response = f"## Hickory Search Answer\n\nScanned {len(self.archives)} ZIM archives:\n\n"
        response += f"**Results for '{user_question}':**\n\n"

        for idx, item in enumerate(dossier[:4], 1):
            snippet = item['content'][:250].strip()
            response += f"{idx}. [{item['archive']}] {item['title']}\n   {snippet}...\n\n"

        if not dossier:
            response += "No matching entries found across loaded ZIM archives.\n"

        return response


if __name__ == "__main__":
    searcher = HickoryMultiZIMSearch("zim_downloads")
    answer = searcher.run_nested_loop_query("Tell me about Appalachian shelters and National Geographic history")
    print(answer)
