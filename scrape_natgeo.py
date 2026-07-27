import os
import urllib.request
import json
import urllib.parse

natgeo_dir = "natgeo_collection"
os.makedirs(f"{natgeo_dir}/texts", exist_ok=True)
os.makedirs(f"{natgeo_dir}/pdfs", exist_ok=True)

# Real National Geographic Magazine Identifiers on Internet Archive
real_natgeo_volumes = [
    {
        'id': 'nationalgeograph11889nati',
        'title': 'The National Geographic Magazine (Volume I - 1889 Archive)',
        'category': 'Historical',
        'ia_id': 'nationalgeograph11889nati'
    },
    {
        'id': 'nationalgeograph37natiuoft',
        'title': 'National Geographic Magazine (Volume 37 - 1920 Expedition & Parks Archive)',
        'category': 'Smokies',
        'ia_id': 'nationalgeograph37natiuoft'
    },
    {
        'id': '194701to12',
        'title': 'National Geographic Magazine (1947 Full Year Collection)',
        'category': 'Appalachia',
        'ia_id': '194701to12'
    },
    {
        'id': '194905',
        'title': 'National Geographic Magazine (1949 Full Year Collection)',
        'category': 'Nature',
        'ia_id': '194905'
    },
    {
        'id': '195011',
        'title': 'National Geographic Magazine (1950 Full Year Collection)',
        'category': 'Appalachia',
        'ia_id': '195011'
    },
    {
        'id': '195105',
        'title': 'National Geographic Magazine (1951 Full Year Collection)',
        'category': 'Historical',
        'ia_id': '195105'
    },
    {
        'id': '195204',
        'title': 'National Geographic Magazine (1952 Full Year Collection)',
        'category': 'Nature',
        'ia_id': '195204'
    },
    {
        'id': '195304',
        'title': 'National Geographic Magazine (1953 Full Year Collection)',
        'category': 'Historical',
        'ia_id': '195304'
    },
    {
        'id': 'jishankhan_hotmail_1954',
        'title': 'National Geographic Magazine (1954 Full Year Collection)',
        'category': 'Historical',
        'ia_id': 'jishankhan_hotmail_1954'
    }
]

downloaded_natgeo = []

def download_file(url, filepath):
    if os.path.exists(filepath):
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Notice: {e}")
        return False

print("Fetching real National Geographic magazine metadata & djvu texts from Internet Archive...")

for item in real_natgeo_volumes:
    filepath = f"{natgeo_dir}/pdfs/{item['id']}.json"
    metadata_url = f"https://archive.org/metadata/{item['ia_id']}"
    
    print(f"Downloading IA metadata for {item['title']}...")
    download_file(metadata_url, filepath)
    
    # Try fetching djvu text summary if available
    txt_filepath = f"{natgeo_dir}/texts/{item['id']}.txt"
    djvu_url = f"https://archive.org/stream/{item['ia_id']}/{item['ia_id']}_djvu.txt"
    
    if not os.path.exists(txt_filepath):
        print(f"Fetching DJVU full text for {item['id']}...")
        if not download_file(djvu_url, txt_filepath):
            # Fallback text if djvu endpoint differs
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {item['title']}\nInternet Archive ID: {item['ia_id']}\n\nArchival National Geographic Volume metadata and text index.")

    # Read snippet for index
    content_snippet = ""
    try:
        with open(txt_filepath, 'r', encoding='utf-8', errors='ignore') as tf:
            content_snippet = tf.read()[:15000]
    except:
        content_snippet = f"Archival text for {item['title']}"

    downloaded_natgeo.append({
        'id': item['id'],
        'title': item['title'],
        'category': item['category'],
        'path': f"texts/{item['id']}.txt",
        'type': 'NATGEO ARCHIVE',
        'local': txt_filepath,
        'content': content_snippet
    })

# JSON serialization for client-side search
search_json = json.dumps(downloaded_natgeo)

# Generate clean, responsive, non-glass index.html
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>National Geographic Archived Magazines Collection</title>
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --primary-color: #b45309;
            --header-bg: #0f172a;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border-color: #cbd5e1;
            --base-font-size: 16px;
        }}

        html {{
            font-size: var(--base-font-size);
            scroll-behavior: smooth;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        body.scroll-locked {{
            overflow: hidden;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding-top: max(1rem, env(safe-area-inset-top));
            padding-right: max(1rem, env(safe-area-inset-right));
            padding-bottom: max(1rem, env(safe-area-inset-bottom));
            padding-left: max(1rem, env(safe-area-inset-left));
        }}

        header {{
            background-color: var(--header-bg);
            color: #ffffff;
            border-bottom: 4px solid var(--primary-color);
            padding: 2rem 1rem;
            text-align: center;
        }}

        header h1 {{
            color: #fbbf24;
            margin: 0 0 0.5rem 0;
            font-size: 1.9rem;
            letter-spacing: 0.03em;
        }}

        header p {{
            color: #94a3b8;
            font-size: 0.95rem;
            margin: 0;
        }}

        /* Controls Section */
        .controls {{
            background: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 1.5rem 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}

        .control-row {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
        }}

        .search-bar {{
            flex: 1;
            min-width: 220px;
            padding: 0.65rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
        }}

        .search-bar:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(180, 83, 9, 0.2);
        }}

        .settings-bar {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}

        .btn {{
            background: #f1f5f9;
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            color: var(--text-main);
            user-select: none;
        }}

        .btn:hover, .btn.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}

        .filter-tabs {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }}

        .tab {{
            padding: 0.4rem 0.85rem;
            border-radius: 6px;
            background: #f1f5f9;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            font-size: 0.85rem;
            cursor: pointer;
            user-select: none;
        }}

        .tab.active, .tab:hover {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}

        /* Grid Layout for iPhone 15 Pro, Pro Max, iPad Mini 6 */
        .grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }}

        @media only screen and (min-width: 852px) and (orientation: landscape) {{
            .grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        @media only screen and (min-width: 744px) and (orientation: portrait) {{
            .grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        @media only screen and (min-width: 1024px) {{
            .grid {{ grid-template-columns: repeat(3, 1fr); }}
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-color);
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }}

        .card-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--header-bg);
            margin-bottom: 0.5rem;
        }}

        .snippet {{
            font-size: 0.85rem;
            color: #475569;
            background: #f8fafc;
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            border-left: 3px solid var(--primary-color);
        }}

        .snippet mark {{
            background: #fef08a;
            color: #854d0e;
        }}

        .card-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            padding-top: 0.5rem;
            margin-top: 1rem;
        }}

        .badge {{
            background: #fef3c7;
            color: #92400e;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.75rem;
        }}

        .no-results {{
            text-align: center;
            grid-column: 1 / -1;
            padding: 2rem;
            color: var(--text-muted);
            display: none;
        }}
    </style>
</head>
<body>
    <header>
        <h1>NATIONAL GEOGRAPHIC ARCHIVED MAGAZINES</h1>
        <p>Full-Text Searched Collection of Historical Internet Archive Volumes</p>
    </header>

    <div class="container">
        <section class="controls">
            <div class="control-row">
                <input type="text" id="searchInput" class="search-bar" placeholder="Search full text across all National Geographic volumes...">
                
                <div class="settings-bar">
                    <span>Font Size:</span>
                    <button class="btn" onclick="setFontSize('14px')">S</button>
                    <button class="btn active" id="btnMed" onclick="setFontSize('16px')">M</button>
                    <button class="btn" onclick="setFontSize('18px')">L</button>
                    <button class="btn" onclick="setFontSize('20px')">XL</button>
                    <button class="btn" id="lockScrollBtn" onclick="toggleScrollLock()">🔒 Scroll Lock</button>
                </div>
            </div>

            <div class="filter-tabs" id="filterTabs">
                <div class="tab active" data-category="ALL">All Volumes</div>
                <div class="tab" data-category="Historical">Historical (1888-1900)</div>
                <div class="tab" data-category="Smokies">Smokies & Parks</div>
                <div class="tab" data-category="Appalachia">Appalachia</div>
                <div class="tab" data-category="Nature">Nature & Wildlife</div>
            </div>
        </section>

        <main class="grid" id="cardGrid">
            <div class="no-results" id="noResults">No matching volumes found.</div>
        </main>
    </div>

    <script>
        const articles = {search_json};

        const searchInput = document.getElementById('searchInput');
        const tabs = document.querySelectorAll('.tab');
        const cardGrid = document.getElementById('cardGrid');
        const noResults = document.getElementById('noResults');
        const lockScrollBtn = document.getElementById('lockScrollBtn');

        let currentCategory = 'ALL';
        let searchQuery = '';
        let isScrollLocked = false;

        function setFontSize(size) {{
            document.documentElement.style.setProperty('--base-font-size', size);
            localStorage.setItem('natgeo_font_size', size);
        }}

        const savedFontSize = localStorage.getItem('natgeo_font_size');
        if (savedFontSize) {{ setFontSize(savedFontSize); }}

        window.addEventListener('scroll', () => {{
            if (!isScrollLocked) {{
                localStorage.setItem('natgeo_scroll_pos', window.scrollY);
            }}
        }});

        const savedScrollPos = localStorage.getItem('natgeo_scroll_pos');
        if (savedScrollPos) {{
            window.scrollTo({{ top: parseInt(savedScrollPos), behavior: 'smooth' }});
        }}

        function toggleScrollLock() {{
            isScrollLocked = !isScrollLocked;
            document.body.classList.toggle('scroll-locked', isScrollLocked);
            lockScrollBtn.classList.toggle('active', isScrollLocked);
            lockScrollBtn.textContent = isScrollLocked ? '🔓 Scroll Unlocked' : '🔒 Scroll Lock';
        }}

        function getSnippet(content, query) {{
            if (!query || !content) return '';
            const idx = content.toLowerCase().indexOf(query.toLowerCase());
            if (idx === -1) return '';

            const start = Math.max(0, idx - 40);
            const end = Math.min(content.length, idx + query.length + 60);
            let snippet = content.substring(start, end);

            const regex = new RegExp(`(${{query}})`, 'gi');
            snippet = snippet.replace(regex, '<mark>$1</mark>');

            return (start > 0 ? '...' : '') + snippet + (end < content.length ? '...' : '');
        }}

        function renderArticles() {{
            cardGrid.innerHTML = '';
            let visibleCount = 0;

            articles.forEach(item => {{
                const matchesCategory = (currentCategory === 'ALL' || item.category === currentCategory);
                let matchesSearch = false;
                let snippetHTML = '';

                if (!searchQuery) {{
                    matchesSearch = true;
                }} else {{
                    const titleMatch = item.title.toLowerCase().includes(searchQuery);
                    let bodyMatch = false;

                    if (item.content) {{
                        const snippetText = getSnippet(item.content, searchQuery);
                        if (snippetText) {{
                            bodyMatch = true;
                            snippetHTML = `<div class="snippet">${{snippetText}}</div>`;
                        }}
                    }}

                    matchesSearch = titleMatch || bodyMatch;
                }}

                if (matchesSearch && matchesCategory) {{
                    visibleCount++;
                    const card = document.createElement('a');
                    card.className = 'card';
                    card.href = item.path;
                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            ${{snippetHTML}}
                        </div>
                        <div class="card-meta">
                            <span>Category: ${{item.category}}</span>
                            <span class="badge">${{item.type}}</span>
                        </div>
                    `;
                    cardGrid.appendChild(card);
                }}
            }});

            if (visibleCount === 0) {{
                const noRes = document.createElement('div');
                noRes.className = 'no-results';
                noRes.style.display = 'block';
                noRes.textContent = 'No matching volumes found.';
                cardGrid.appendChild(noRes);
            }}
        }}

        searchInput.addEventListener('input', (e) => {{
            searchQuery = e.target.value.toLowerCase().trim();
            renderArticles();
        }});

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentCategory = tab.getAttribute('data-category');
                renderArticles();
            }});
        }});

        renderArticles();
    </script>
</body>
</html>
"""

with open(f"{natgeo_dir}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("NatGeo Internet Archive scraping and indexing complete.")
