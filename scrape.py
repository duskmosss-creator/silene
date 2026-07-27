import os
import urllib.request
import json
import urllib.parse
import re

# Ensure content directories exist
os.makedirs("content/texts", exist_ok=True)
os.makedirs("content/pdfs", exist_ok=True)
os.makedirs("content/audio", exist_ok=True)

# Extended list of texts & articles
gutenberg_ids = {
    '58971': ('Great Smoky Mountains National Park', 'History'),
    '71447': ('Great Smoky Mountains National Park: Open All Year', 'History'),
    '31709': ('Our Southern Highlanders', 'Culture'),
    '50952': ('The Heart of the Alleghanies', 'Travel'),
    '48408': ('Letters from the Alleghany Mountains', 'Travel'),
    '60246': ('Gatlinburg and the Great Smokies', 'History'),
    '3126': ('On Horseback', 'Travel'),
    '59522': ('Biltmore House and Gardens', 'History'),
    '31367': ('The Training of a Forester', 'Forestry'),
    '72365': ('At Home in the Smokies', 'History'),
    '45634': ('Myths of the Cherokee', 'Cherokee'),
    '46493': ('The Cherokee Nation of Indians', 'Cherokee')
}

archive_ids = {
    'westernnorthcar00arth': ('Western North Carolina: A History (1730-1913)', 'History'),
    'cadescovelifedea0000dunn': ('Cades Cove: Life and Death of a Southern Appalachian Community', 'History'),
    'greatsmokiesfrom0000pier': ('The Great Smokies: From Natural Habitat to National Park', 'History'),
    'elkmontsunclelem0000mcma': ('Elkmont\'s Uncle Lem Ownby: Sage of the Smokies', 'Culture'),
    'checklistoffungi00pete': ('Checklist of Fungi of the Great Smoky Mountains National Park', 'Nature'),
    'floraofgreatsmok00whit': ('Flora of Great Smoky Mountains National Park', 'Nature'),
    'statushistoryofm00culb': ('Status and History of the Mountain Lion in GSMNP', 'Nature'),
    'riflemakingingre13nati': ('Rifle Making in the Great Smoky Mountains', 'Culture'),
    'whitetaileddeero00wath': ('White-Tailed Deer of Cades Cove', 'Nature'),
    'lasttraintoelkmo0000weal': ('Last Train to Elkmont', 'History'),
    'folksongsofengli00shar': ('Folk-songs of English Origin in the Appalachian Mountains', 'Culture'),
    'nurserysongsfrom00shar': ('Nursery Songs from the Appalachian Mountains', 'Culture'),
    'historyofwataug00arth': ('A History of Watauga County, North Carolina', 'History'),
    'carologueaccesst00hoff': ('Carologue: Access to North Carolina', 'History'),
    'Elkmont09-18-14': ('Elkmont Historical Audio Record', 'Audio')
}

# Supplemental National Park / Geographic Articles
nps_articles = {
    'nps-gsmnp-history': ('NPS Official Overview: Human History of the Smokies', 'History',
        "The human history of the Great Smoky Mountains National Park spans thousands of years, from prehistoric Paleo-Indians and the Cherokee (Tsalagi) nation to European settlement, logging, and environmental preservation. Key historic coves like Cades Cove and Cataloochee preserve early pioneer farms and churches."),
    'nps-gsmnp-biodiversity': ('NPS Official Guide: Biodiversity & All Taxa Inventory', 'Nature',
        "Great Smoky Mountains National Park is recognized as a International Biosphere Reserve and UNESCO World Heritage Site. With over 19,000 documented species of plants, fungi, and wildlife, it is considered the most biodiverse park in the National Park system."),
    'nps-elkmont-preservation': ('NPS Historic Resource: Elkmont Logging & Cottage District', 'History',
        "Elkmont evolved from an early 20th-century lumber town operated by the Little River Railroad & Lumber Company into an exclusive summer resort for the Appalachian Club and Wonderland Club before incorporation into the national park.")
}

downloaded_items = []

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
        print(f"Error downloading {url}: {e}")
        return False

print("Downloading Gutenberg texts...")
for gid, (title, category) in gutenberg_ids.items():
    filepath = f"content/texts/{gid}.txt"
    url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
    if download_file(url, filepath):
        # Read content snippet for full-text search index
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as tf:
                content_text = tf.read()
        except:
            content_text = ""
        
        downloaded_items.append({
            'id': f"gutenberg-{gid}",
            'title': title, 
            'category': category, 
            'path': f"texts/{gid}.txt", 
            'type': 'TEXT', 
            'local': filepath,
            'content': content_text[:15000] # Embed first 15k chars for full-text search
        })

print("Downloading Internet Archive texts/metadata...")
for aid, (title, category) in archive_ids.items():
    filepath = f"content/pdfs/{aid}.json"
    url = f"https://archive.org/metadata/{aid}"
    if download_file(url, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as jf:
                content_text = jf.read()
        except:
            content_text = ""
            
        item_type = 'AUDIO' if category == 'Audio' else 'PDF / METADATA'
        downloaded_items.append({
            'id': f"archive-{aid}",
            'title': title, 
            'category': category, 
            'path': f"pdfs/{aid}.json", 
            'type': item_type, 
            'local': filepath,
            'content': content_text[:15000]
        })

print("Adding supplemental articles...")
for art_id, (title, category, body_text) in nps_articles.items():
    filepath = f"content/texts/{art_id}.txt"
    with open(filepath, 'w', encoding='utf-8') as af:
        af.write(body_text)
        
    downloaded_items.append({
        'id': art_id,
        'title': title,
        'category': category,
        'path': f"texts/{art_id}.txt",
        'type': 'ARTICLE',
        'local': filepath,
        'content': body_text
    })

# Escape content for JSON serialization
search_data_json = json.dumps([{
    'id': item['id'],
    'title': item['title'],
    'category': item['category'],
    'path': item['path'],
    'type': item['type'],
    'content': item['content']
} for item in downloaded_items])

# Generate index.html with Full-Text Search Engine
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Appalachian Corridor Digital Archive</title>
    <style>
        :root {{
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --base-font-size: 16px;
        }}

        html {{
            font-size: var(--base-font-size);
            scroll-behavior: smooth;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.5;
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
            background-color: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        header h1 {{
            color: var(--primary-color);
            margin: 0 0 0.25rem 0;
            font-size: 1.75rem;
        }}

        header p {{
            color: var(--text-muted);
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
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
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
            min-width: 200px;
            padding: 0.6rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
        }}

        .search-bar:focus {{
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }}

        .search-mode {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .settings-bar {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-muted);
        }}

        .btn {{
            background: #f3f4f6;
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
            background: #f3f4f6;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            font-size: 0.85rem;
            cursor: pointer;
            user-select: none;
        }}

        .tab.active, .tab:hover {{
            background: var(--secondary-color);
            color: white;
            border-color: var(--secondary-color);
        }}

        /* Grid Breakpoints */
        .grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
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

        /* Clean Card UI */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}

        .card:hover {{
            border-color: var(--secondary-color);
            box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        }}

        .card-title {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}

        .snippet {{
            font-size: 0.85rem;
            color: #4b5563;
            background: #f9fafb;
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            border-left: 3px solid var(--secondary-color);
        }}

        .snippet mark {{
            background: #fef08a;
            color: #854d0e;
            padding: 0 0.15rem;
            border-radius: 2px;
        }}

        .card-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            padding-top: 0.5rem;
        }}

        .badge {{
            background: #e0e7ff;
            color: #3730a3;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
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
        <h1>Appalachian Corridor Archive</h1>
        <p>Great Smoky Mountains National Park to DuPont State Recreational Forest</p>
    </header>

    <div class="container">
        <section class="controls">
            <div class="control-row">
                <input type="text" id="searchInput" class="search-bar" placeholder="Search full text of all documents, titles, or keywords...">
                
                <div class="search-mode">
                    <input type="checkbox" id="fullTextCheck" checked>
                    <label for="fullTextCheck">Full-Text Search</label>
                </div>

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
                <div class="tab active" data-category="ALL">All</div>
                <div class="tab" data-category="History">History</div>
                <div class="tab" data-category="Cherokee">Cherokee</div>
                <div class="tab" data-category="Culture">Culture</div>
                <div class="tab" data-category="Nature">Nature</div>
                <div class="tab" data-category="Travel">Travel</div>
                <div class="tab" data-category="Audio">Audio</div>
            </div>
        </section>

        <main class="grid" id="cardGrid">
            <div class="no-results" id="noResults">No matching documents found.</div>
        </main>
    </div>

    <script>
        const searchData = {search_data_json};

        const searchInput = document.getElementById('searchInput');
        const fullTextCheck = document.getElementById('fullTextCheck');
        const tabs = document.querySelectorAll('.tab');
        const cardGrid = document.getElementById('cardGrid');
        const noResults = document.getElementById('noResults');
        const lockScrollBtn = document.getElementById('lockScrollBtn');

        let currentCategory = 'ALL';
        let searchQuery = '';
        let isScrollLocked = false;

        // Font Size Control
        function setFontSize(size) {{
            document.documentElement.style.setProperty('--base-font-size', size);
            localStorage.setItem('appalachian_font_size', size);
        }}

        const savedFontSize = localStorage.getItem('appalachian_font_size');
        if (savedFontSize) {{ setFontSize(savedFontSize); }}

        // Scroll Position Saving
        window.addEventListener('scroll', () => {{
            if (!isScrollLocked) {{
                localStorage.setItem('appalachian_index_scroll', window.scrollY);
            }}
        }});

        const savedScrollPos = localStorage.getItem('appalachian_index_scroll');
        if (savedScrollPos) {{
            window.scrollTo({{ top: parseInt(savedScrollPos), behavior: 'smooth' }});
        }}

        function toggleScrollLock() {{
            isScrollLocked = !isScrollLocked;
            document.body.classList.toggle('scroll-locked', isScrollLocked);
            lockScrollBtn.classList.toggle('active', isScrollLocked);
            lockScrollBtn.textContent = isScrollLocked ? '🔓 Scroll Unlocked' : '🔒 Scroll Lock';
        }}

        // Helper to extract a text snippet with match highlighted
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

        // Render Search Results dynamically
        function renderCards() {{
            const isFullText = fullTextCheck.checked;
            cardGrid.innerHTML = '';
            let visibleCount = 0;

            searchData.forEach(item => {{
                const matchesCategory = (currentCategory === 'ALL' || item.category === currentCategory);
                let matchesSearch = false;
                let snippetHTML = '';

                if (!searchQuery) {{
                    matchesSearch = true;
                }} else {{
                    const titleMatch = item.title.toLowerCase().includes(searchQuery);
                    let bodyMatch = false;

                    if (isFullText && item.content) {{
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
                noRes.textContent = 'No matching documents found.';
                cardGrid.appendChild(noRes);
            }}
        }}

        searchInput.addEventListener('input', (e) => {{
            searchQuery = e.target.value.toLowerCase().trim();
            renderCards();
        }});

        fullTextCheck.addEventListener('change', renderCards);

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentCategory = tab.getAttribute('data-category');
                renderCards();
            }});
        }});

        // Initial render
        renderCards();
    </script>
</body>
</html>
"""

with open("content/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Full-text search enabled scrape and index.html generation complete.")
