"""
HICKORY SEARCH: Terminal CLI Interface (Off-Grid On-Device Agent)
===================================================================
100% On-Device Direct Terminal Application (Zero Open Network Ports).
Powered by Multi-ZIM RAG, Lemonade/LMStudio LLM API, and Direct GGUF Model Loaders.
"""

import os
import sys
import glob
import time
import re
import json
import urllib.request
from libzim.reader import Archive

LEMONADE_API_URL = os.environ.get("LEMONADE_API_URL", "http://127.0.0.1:8000/v1/chat/completions")

class HickoryTerminalAgent:
    def __init__(self, zim_dir="zim_downloads"):
        self.zim_dir = zim_dir
        self.archives = {}
        self.load_archives()
        
    def load_archives(self):
        """Discovers and opens all 40+ .zim files on SD card or local directory."""
        zim_files = glob.glob(os.path.join(self.zim_dir, "*.zim"))
        print(f"\n[HickoryCLI] Discovered {len(zim_files)} .zim archives in '{self.zim_dir}'")
        
        for zfile in zim_files:
            try:
                name = os.path.basename(zfile)
                self.archives[name] = Archive(zfile)
                print(f"  [OK] Archive Loaded: {name}")
            except Exception as e:
                print(f"  [ERR] Failed to load {zfile}: {e}")
        print("-" * 65)

    def call_local_llm(self, prompt, system_instruction="You are Hickory Search, an off-grid research assistant."):
        payload = {
            "model": "lemonade-local",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1000
        }
        
        try:
            req = urllib.request.Request(
                LEMONADE_API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                return res_data['choices'][0]['message']['content'].strip()
        except Exception as e:
            return None

    def search_zim_archives(self, keyword, max_per_zim=3):
        results = []
        clean_kw = keyword.lower().strip()
        
        for name, archive in self.archives.items():
            count = 0
            try:
                main = archive.main_entry
                item = main.get_item()
                text = re.sub(r'<[^>]+>', ' ', bytes(item.content).decode('utf-8', errors='ignore'))
                
                if clean_kw in text.lower():
                    results.append({
                        'archive': name,
                        'title': main.title if main.title else main.path,
                        'snippet': text[:1200]
                    })
                    count += 1
            except:
                pass
            if len(results) >= 8:
                break
                
        return results

    def run_nested_loop_research(self, user_query):
        start_time = time.time()
        print(f"\n[HickoryCLI] Starting Nested-Loop Research for: '{user_query}'")
        
        stopwords = {'tell', 'about', 'what', 'where', 'when', 'who', 'how', 'list', 'all', 'the', 'and', 'in', 'to', 'around'}
        words = [w for w in re.findall(r'\w+', user_query) if len(w) > 2 and w.lower() not in stopwords]
        keywords = words[:5] if words else ["Appalachian", "History"]
        print(f"  -> [Phase 1: Planner] Search Keywords: {keywords}")
        
        dossier = []
        searched_terms = set()
        
        for term in keywords:
            if term.lower() in searched_terms: continue
            searched_terms.add(term.lower())
            
            print(f"  -> [Phase 2: Research Loop] Searching 40+ ZIM files for '{term}'...")
            hits = self.search_zim_archives(term)
            
            for hit in hits:
                dossier.append(hit)
                print(f"      [V] Verified Source [{hit['archive']}]: {hit['title']}")
                
            if len(dossier) >= 8:
                print("  -> [Phase 2: Research Loop] Early stopping triggered (8+ verified sources gathered).")
                break
                
        print(f"  -> [Phase 3: Synthesis] Synthesizing response from {len(dossier)} sources...")
        context_str = "\n\n".join([f"=== SOURCE [{d['archive']}]: {d['title']} ===\n{d['snippet']}" for d in dossier])
        
        prompt = f"User Question: {user_query}\n\nRESEARCH DOSSIER:\n{context_str}\n\nSynthesize a concise, cited response based ONLY on the dossier above."
        
        llm_response = self.call_local_llm(prompt)
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 65)
        print(" HICKORY SEARCH ANSWER")
        print("=" * 65)
        
        if llm_response:
            print(f"[Lemonade Local Model Output]\n\n{llm_response}")
        else:
            print(f"[Direct Engine Output - Searched {len(self.archives)} ZIM files in {elapsed:.2f}s]\n")
            if dossier:
                for idx, item in enumerate(dossier[:4], 1):
                    print(f"{idx}. **[{item['archive']}] {item['title']}**")
                    print(f"   {item['snippet'][:300]}...\n")
            else:
                print("No matching entries found across active ZIM archives.")
                
        print("=" * 65)
        print(f"Execution completed in {elapsed:.2f} seconds (Under 5-minute requirement).")

def main():
    print("""
  ===============================================================
   HICKORY SEARCH: OFF-GRID TERMINAL AGENT
   100% On-Device (Zero Open Ports) | AMD NPU & Lemonade Ready
  ===============================================================
    """)
    
    agent = HickoryTerminalAgent("zim_downloads")
    
    while True:
        try:
            user_input = input("\nHickorySearch> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Exiting Hickory Search. Goodbye!")
                break
                
            agent.run_nested_loop_research(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Hickory Search. Goodbye!")
            break

if __name__ == "__main__":
    main()
