"""
HICKORY SEARCH: Multi-ZIM Autonomous Wiki Agent
===================================================================
100% On-Device Off-Grid Research Agent powered by Multi-ZIM search
and local LLM inference (Lemonade, LM Studio, Ollama).

Features:
- Multi-ZIM support: Scans and queries 40+ .zim archives simultaneously.
- Autonomous Tool Calling: Model uses `SEARCH: [term]` and `CONTINUE`.
- Backend Probing: Auto-detects Lemonade (11434/8000), LM Studio (1234), Ollama (11434).
- Full Research Logging: Detailed phase logging, thought streams, and source attribution.
"""

import sys
import os
import glob
import time
import re
import json
import urllib.request
import urllib.parse
import concurrent.futures
from bs4 import BeautifulSoup
from libzim.reader import Archive

# ================= CONFIGURATION =================
ZIM_DIR = os.environ.get("ZIM_DIR", "zim_downloads")
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "lemonade-local")
MAX_SEARCH_STEPS = 10
CHUNK_SIZE = 1200

CURRENT_ARTICLE_CACHE = {}
ZIM_ARCHIVES = {}

def _load_single_zim(zfile):
    try:
        name = os.path.basename(zfile)
        archive = Archive(zfile)
        print(f"     [OK] Loaded archive: {name}")
        return name, archive
    except Exception as e:
        print(f"     [ERR] Could not load {os.path.basename(zfile)}: {e}")
        return None, None

def load_all_zim_archives(zim_dir=ZIM_DIR):
    """Discovers and opens all .zim files in the specified directory using multi-threading."""
    global ZIM_ARCHIVES
    ZIM_ARCHIVES.clear()
    
    zim_files = glob.glob(os.path.join(zim_dir, "*.zim"))
    print(f"\n   [MultiZIM] Discovered {len(zim_files)} .zim archives in '{zim_dir}'")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, len(zim_files) or 1)) as executor:
        results = executor.map(_load_single_zim, zim_files)
        for name, archive in results:
            if name and archive:
                ZIM_ARCHIVES[name] = archive
            
    print("   " + "-" * 60)
    return ZIM_ARCHIVES

def smart_http_get(url, timeout=3):
    """Probes an HTTP endpoint cleanly without crashing."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HickoryWikiAgent/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode('utf-8'))
    except Exception:
        pass
    return None

def smart_http_post(url, json_data, timeout=120):
    """Executes a JSON POST request with timeout and error handling."""
    data_bytes = json.dumps(json_data).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def detect_and_configure_backend():
    """Probes local AI backends prioritizing Lemonade on port 8000."""
    global API_BASE, MODEL_NAME
    
    print("\n   [WikiAgent] Probing for local AI backends (Port 8000)...")
    
    backends = [
        ("Lemonade (Port 8000)", "http://127.0.0.1:8000/v1", "lemonade-local"),
        ("Lemonade IPv6 (Port 8000)", "http://[::1]:8000/v1", "lemonade-local"),
        ("Lemonade Localhost (Port 8000)", "http://localhost:8000/v1", "lemonade-local"),
        ("Lemonade / Ollama (Port 11434)", "http://127.0.0.1:11434/v1", "lemonade"),
        ("LM Studio (Port 1234)", "http://127.0.0.1:1234/v1", "local-model")
    ]
    
    for name, base_url, default_model in backends:
        res = smart_http_get(f"{base_url}/models")
        if res:
            API_BASE = base_url
            if isinstance(res, dict) and 'data' in res and len(res['data']) > 0:
                MODEL_NAME = res['data'][0].get('id', default_model)
            else:
                MODEL_NAME = default_model
            print(f"   [WikiAgent] [OK] Connected to {name}")
            print(f"   [WikiAgent] Endpoint: {API_BASE} | Model: {MODEL_NAME}")
            return True
            
    print("   [WikiAgent] [!] No active local LLM backend detected (Lemonade/LMStudio/Ollama offline).")
    print(f"   [WikiAgent] Defaulting to endpoint: {API_BASE} ({MODEL_NAME})")
    return False

def search_multi_zim_tool(query):
    """
    SEARCH TOOL: Searches across ALL loaded ZIM archives for matching articles.
    Strips HTML and returns structured text + source archive attribution.
    """
    clean_query = query.strip().strip("'\"").lower()
    print(f"   [TOOL] Searching ALL {len(ZIM_ARCHIVES)} ZIM archives for: '{query}'...")
    
    if not ZIM_ARCHIVES:
        return "SYSTEM ERROR: No ZIM archives loaded. Verify ZIM_DIR configuration."

    hits = []
    
    def _search_single_archive(zim_item):
        zim_name, archive = zim_item
        try:
            entry = None
            for candidate in ['index.html', 'mainPage', clean_query, f"A/{clean_query}"]:
                if archive.has_entry_by_path(candidate):
                    entry = archive.get_entry_by_path(candidate)
                    break
            
            if entry is None:
                entry = archive.main_entry

            item = entry.get_item()
            raw_bytes = bytes(item.content)
            
            soup = BeautifulSoup(raw_bytes, "html.parser")
            for tag in soup(["script", "style", "table", "footer", "nav", "div.references"]):
                tag.decompose()
            text = soup.get_text(separator=' ', strip=True)
            text = re.sub(r'\s+', ' ', text).strip()
            
            title = entry.title if entry.title else entry.path
            if clean_query in text.lower() or clean_query in title.lower():
                return {'zim': zim_name, 'title': title, 'text': text}
        except Exception:
            pass
        return None

    # Search across all loaded ZIM archives in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, len(ZIM_ARCHIVES) or 1)) as executor:
        results = executor.map(_search_single_archive, ZIM_ARCHIVES.items())
        for res in results:
            if res:
                hits.append(res)

    if not hits:
        return f"SYSTEM NOTICE: No entries found matching '{query}' across {len(ZIM_ARCHIVES)} ZIM archives. Try broader keywords."

    combined_text = ""
    for hit in hits:
        combined_text += f"SOURCE ARCHIVE: [{hit['zim']}] | TITLE: {hit['title']}\n{hit['text']}\n\n"
    
    print(f"   [V] Verified Match ({len(hits)} total hits across archives)")
    
    # Pagination
    global CURRENT_ARTICLE_CACHE
    if len(combined_text) > CHUNK_SIZE:
        CURRENT_ARTICLE_CACHE = {
            'full_text': combined_text,
            'current_index': CHUNK_SIZE,
            'title': "Multiple Sources",
            'zim': "Multiple Archives"
        }
        return (
            f"CONTENT:\n{combined_text[:CHUNK_SIZE]}\n\n"
            f"[SYSTEM NOTICE: Content is long ({len(combined_text)} chars). Output truncated. "
            f"To read the next section, issue tool command: CONTINUE]"
        )
    else:
        CURRENT_ARTICLE_CACHE = {}
        return (
            f"CONTENT:\n{combined_text}"
        )

def continue_reading_tool():
    """Returns the next chunk of the currently cached article."""
    global CURRENT_ARTICLE_CACHE
    if not CURRENT_ARTICLE_CACHE:
        return "SYSTEM NOTICE: No active article to continue. Use SEARCH first."
        
    full_text = CURRENT_ARTICLE_CACHE['full_text']
    idx = CURRENT_ARTICLE_CACHE['current_index']
    title = CURRENT_ARTICLE_CACHE['title']
    zim_name = CURRENT_ARTICLE_CACHE['zim']
    
    if idx >= len(full_text):
        return "SYSTEM NOTICE: End of article reached."
        
    next_idx = idx + CHUNK_SIZE
    chunk = full_text[idx:next_idx]
    CURRENT_ARTICLE_CACHE['current_index'] = next_idx
    
    remaining = len(full_text) - next_idx
    notice = "[SYSTEM NOTICE: Still more text remaining. Use CONTINUE for next part.]" if remaining > 0 else "[SYSTEM NOTICE: End of article.]"
    
    return (
        f"SOURCE ARCHIVE: [{zim_name}]\n"
        f"ARTICLE TITLE: {title} (Continuation)\n\n"
        f"CONTENT:\n{chunk}\n\n{notice}"
    )

def get_agent_response(user_question, include_thoughts=True):
    """
    Main Autonomous Agent Loop:
    Translates user query -> AI thought -> TOOL call -> ZIM observation -> Final Answer.
    """
    system_prompt = (
        "You are Hickory Wiki Agent, an off-grid research assistant with access to 40+ offline ZIM archives.\n"
        "Your goal is to answer the user's question accurately using facts from the ZIM archives.\n\n"
        "TOOLS AVAILABLE:\n"
        "- SEARCH: [term]\n"
        "- CONTINUE\n"
        "  (Use CONTINUE to read the next part of a long article if truncated.)\n\n"
        "PROTOCOL:\n"
        "1. Start by calling SEARCH: [keyword] to find relevant articles.\n"
        "2. Analyze the observations returned from the archives.\n"
        "3. If an article is truncated and you need more details, issue CONTINUE.\n"
        "4. Synthesize a concise, cited final answer referencing the source archives.\n"
        "5. DO NOT hallucinate facts not present in the dossier.\n"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
    
    step = 0
    start_time = time.time()
    
    while step < MAX_SEARCH_STEPS:
        print(f"   ...Thinking (Step {step+1}/{MAX_SEARCH_STEPS})...")
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1500,
            "stop": ["Observation:"]
        }
        
        try:
            res = smart_http_post(f"{API_BASE}/chat/completions", payload, timeout=120)
            if 'choices' not in res or not res['choices']:
                break
                
            response_text = res['choices'][0]['message']['content'].strip()
            
            # Check for TOOL call
            match_search = re.search(r"^\s*SEARCH:\s*\[?([^\]\n]+)\]?", response_text, re.IGNORECASE | re.MULTILINE)
            match_continue = re.search(r"^\s*CONTINUE\s*$", response_text, re.IGNORECASE | re.MULTILINE)
            
            if match_search:
                search_term = match_search.group(1).strip()
                print(f"   [WikiAgent] ACTION: SEARCH '{search_term}'")
                observation = search_multi_zim_tool(search_term)
                
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content": f"Observation:\n{observation}"})
                step += 1
                
            elif match_continue:
                print(f"   [WikiAgent] ACTION: CONTINUE READING...")
                observation = continue_reading_tool()
                
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content": f"Observation:\n{observation}"})
                step += 1
                
            else:
                # Final Answer reached
                elapsed = time.time() - start_time
                print(f"\n   [WikiAgent] Research completed in {elapsed:.2f} seconds ({step} search steps).")
                
                if not include_thoughts:
                    clean_resp = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL).strip()
                    return clean_resp if clean_resp else response_text
                return response_text
                
        except Exception as e:
            # Direct ZIM research fallback if local LLM server is offline
            print(f"   [WikiAgent Notice] Local LLM server offline ({e}). Executing direct multi-ZIM research...")
            stopwords = {'tell', 'about', 'what', 'where', 'when', 'who', 'how', 'list', 'all', 'the', 'and', 'in', 'to'}
            words = [w for w in re.findall(r'\w+', user_question) if len(w) > 2 and w.lower() not in stopwords]
            keywords = words[:4] if words else ["Appalachian"]
            
            dossier = []
            for kw in keywords:
                obs = search_multi_zim_tool(kw)
                if "ARTICLE TITLE" in obs:
                    dossier.append(obs)
                if len(dossier) >= 3:
                    break
                    
            elapsed = time.time() - start_time
            answer = f"## Hickory Multi-ZIM Research Answer\n\nDirect ZIM search across {len(ZIM_ARCHIVES)} archives ({elapsed:.2f}s):\n\n"
            for idx, item in enumerate(dossier, 1):
                lines = item.split('\n')
                src = lines[0] if lines else ""
                title = lines[1] if len(lines) > 1 else ""
                answer += f"{idx}. **{src}** — {title}\n"
            return answer

    return "Wiki Agent reached maximum search steps without a final answer."

def run_agent_loop(query):
    """Executes single query with logging."""
    print(f"\n[AGENT] Question: \"{query}\"")
    answer = get_agent_response(query, include_thoughts=True)
    print("\n" + "=" * 65)
    print(" HICKORY MULTI-ZIM WIKI AGENT ANSWER")
    print("=" * 65)
    print(answer)
    print("=" * 65)

def main():
    print("""===============================================================
 HICKORY MULTI-ZIM WIKI AGENT
 Full System Logging | Multi-ZIM Search | Lemonade / LMStudio
===============================================================

Starting Multi-ZIM Wiki Agent...
(Press Ctrl+C at any time to quit)""")
    
    target_dir = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ZIM_DIR
    load_all_zim_archives(target_dir)
    detect_and_configure_backend()
    
    print("\n  Type your question below (Type 'exit' or 'quit' to stop).")
    
    while True:
        try:
            q = input("\nRequest> ").strip()
            if not q:
                continue
            if q.lower() in ('exit', 'quit', 'q', ':q'):
                print("Exiting Hickory Wiki Agent. Goodbye!")
                break
            run_agent_loop(q)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Hickory Wiki Agent. Goodbye!")
            break

if __name__ == "__main__":
    main()
