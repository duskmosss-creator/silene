"""
HICKORY SEARCH: Terminal CLI Interface (Off-Grid On-Device Agent)
===================================================================
100% On-Device Direct Terminal Application (Zero Open Network Ports).
Powered by Multi-ZIM RAG and Lemonade/LMStudio local LLM integration.

Usage:
    python hickory_search/hickory_cli.py
    python hickory_search/hickory_cli.py --zim E:\\zim_files

Lemonade integration:
    Set LEMONADE_API_URL env var, or it defaults to port 11434 (Lemonade default).
    The web app uses port 8000 separately — no conflict.
"""

import os
import sys
import glob
import time
import re
import json
import argparse
import urllib.request
from libzim.reader import Archive

# Lemonade default port is 11434. LMStudio uses 1234. Ollama uses 11434.
# hickory_web_app.py uses 8000 for its own server — no conflict here.
LEMONADE_API_URL = os.environ.get("LEMONADE_API_URL", "http://127.0.0.1:11434/v1/chat/completions")
LEMONADE_MODEL   = os.environ.get("LEMONADE_MODEL", "lemonade")


class HickoryTerminalAgent:
    def __init__(self, zim_dir="zim_downloads"):
        self.zim_dir = zim_dir
        self.archives = {}
        self.load_archives()

    def load_archives(self):
        """Discovers and opens all .zim files in the given directory."""
        zim_files = glob.glob(os.path.join(self.zim_dir, "*.zim"))

        if not zim_files:
            print(f"\n[HickoryCLI] WARNING: No .zim files found in '{self.zim_dir}'")
            print(f"  Run with --zim <path> to point at your SD card folder.")
        else:
            print(f"\n[HickoryCLI] Discovered {len(zim_files)} .zim archives in '{self.zim_dir}'")

        for zfile in zim_files:
            try:
                name = os.path.basename(zfile)
                self.archives[name] = Archive(zfile)
                print(f"  [OK] {name}")
            except Exception as e:
                print(f"  [ERR] {os.path.basename(zfile)}: {e}")

        print("-" * 65)

    def call_lemonade(self, prompt):
        """
        Sends the research dossier to a locally running Lemonade / LMStudio
        / Ollama model. Returns None silently if the model server is offline.
        """
        payload = {
            "model": LEMONADE_MODEL,
            "messages": [
                {"role": "system", "content": "You are Hickory Search, an off-grid research assistant. Answer ONLY from the provided research dossier. Cite your sources."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1000,
            "stream": False
        }

        try:
            req = urllib.request.Request(
                LEMONADE_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data['choices'][0]['message']['content'].strip()
        except Exception:
            return None  # Lemonade offline — fallback to direct output

    def search_zim_archives(self, keyword):
        """Scans all loaded ZIM files for content matching the keyword."""
        results = []
        clean_kw = keyword.lower().strip()

        for name, archive in self.archives.items():
            try:
                # Prefer index.html — it has clean readable content.
                # mainPage redirects to index.html but has CSS dumped first.
                entry = None
                for candidate in ['index.html', 'mainPage']:
                    if archive.has_entry_by_path(candidate):
                        entry = archive.get_entry_by_path(candidate)
                        break
                if entry is None:
                    entry = archive.main_entry

                item = entry.get_item()
                raw = bytes(item.content).decode('utf-8', errors='ignore')

                # Strip <style> and <script> blocks so CSS doesn't pollute snippets
                raw = re.sub(r'<style[^>]*>.*?</style>', ' ', raw, flags=re.DOTALL)
                raw = re.sub(r'<script[^>]*>.*?</script>', ' ', raw, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', raw)
                text = re.sub(r'\s+', ' ', text).strip()

                if clean_kw in text.lower():
                    results.append({
                        'archive': name,
                        'title': entry.title if entry.title else entry.path,
                        'snippet': text[:1200]
                    })
            except Exception:
                pass

        return results

    def run_nested_loop_research(self, user_query):
        """
        Nested Loop Execution:
        1. Planner: Extract keywords from question
        2. Research Loop: Search all ZIM files per keyword, deduplicate
        3. Early stopping at 8+ verified sources
        4. Synthesis: Pass dossier to Lemonade or print directly
        """
        start_time = time.time()
        print(f"\n[HickoryCLI] Query: '{user_query}'")

        # Phase 1: Keyword planning
        stopwords = {'tell', 'about', 'what', 'where', 'when', 'who', 'how',
                     'list', 'all', 'the', 'and', 'in', 'to', 'around', 'find', 'give', 'show'}
        words = [w for w in re.findall(r'\w+', user_query)
                 if len(w) > 2 and w.lower() not in stopwords]
        keywords = words[:5] if words else ["Appalachian", "history"]
        print(f"  -> [Phase 1] Keywords: {keywords}")

        dossier = []
        seen_archives = set()   # Dedup: one result per archive per query
        searched_terms = set()

        # Phase 2: Research loop
        for term in keywords:
            if term.lower() in searched_terms:
                continue
            searched_terms.add(term.lower())

            print(f"  -> [Phase 2] Searching '{term}' across {len(self.archives)} archives...")
            hits = self.search_zim_archives(term)

            for hit in hits:
                if hit['archive'] not in seen_archives:
                    dossier.append(hit)
                    seen_archives.add(hit['archive'])
                    print(f"      [+] [{hit['archive']}] {hit['title']}")

            if len(dossier) >= 8:
                print("  -> [Phase 2] Early stop: 8+ verified sources gathered.")
                break

        # Phase 3: Synthesis
        print(f"  -> [Phase 3] Synthesizing from {len(dossier)} sources...")
        context_str = "\n\n".join(
            [f"=== SOURCE [{d['archive']}]: {d['title']} ===\n{d['snippet']}" for d in dossier]
        )
        prompt = (
            f"User Question: {user_query}\n\n"
            f"RESEARCH DOSSIER:\n{context_str}\n\n"
            f"Synthesize a concise, cited response based ONLY on the dossier above."
        )

        llm_response = self.call_lemonade(prompt)
        elapsed = time.time() - start_time

        print("\n" + "=" * 65)
        print(" HICKORY SEARCH ANSWER")
        print("=" * 65)

        if llm_response:
            print(f"[Lemonade Model: {LEMONADE_MODEL}]\n\n{llm_response}")
        else:
            if dossier:
                print(f"[Direct Output — Lemonade offline | {len(self.archives)} ZIM files in {elapsed:.2f}s]\n")
                for idx, item in enumerate(dossier[:4], 1):
                    print(f"{idx}. [{item['archive']}] {item['title']}")
                    print(f"   {item['snippet'][:300].strip()}...\n")
            else:
                print(f"[No results found across {len(self.archives)} archives in {elapsed:.2f}s]")
                print("  Try broadening your search terms, or check that your --zim path is correct.")

        print("=" * 65)
        print(f"[Done] {elapsed:.2f}s")


def main():
    parser = argparse.ArgumentParser(description="Hickory Search: Off-Grid Terminal RAG Agent")
    parser.add_argument(
        "--zim",
        default="zim_downloads",
        help="Path to folder containing your .zim files (default: zim_downloads)"
    )
    args = parser.parse_args()

    print("""
  =================================================================
   HICKORY SEARCH: OFF-GRID TERMINAL AGENT
   100% On-Device | Zero Open Ports | AMD NPU + Lemonade Ready
  =================================================================
    """)

    if not os.path.isdir(args.zim):
        print(f"[ERROR] ZIM directory not found: '{args.zim}'")
        print("  Usage: python hickory_search/hickory_cli.py --zim E:\\zim_files")
        sys.exit(1)

    agent = HickoryTerminalAgent(args.zim)

    while True:
        try:
            user_input = input("\nHickorySearch> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'q', ':q']:
                print("Goodbye.")
                break
            agent.run_nested_loop_research(user_input)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
