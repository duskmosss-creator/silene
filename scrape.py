import os
import urllib.request
import json
import urllib.parse

os.makedirs("content/texts", exist_ok=True)
os.makedirs("content/pdfs", exist_ok=True)
os.makedirs("content/audio", exist_ok=True)

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
    'westernnorthcar00arth': ('Western North Carolina: A History (1730-1913)', 'History', 'PDF'),
    'cadescovelifedea0000dunn': ('Cades Cove: Life and Death of a Southern Appalachian Community', 'History', 'PDF'),
    'greatsmokiesfrom0000pier': ('The Great Smokies: From Natural Habitat to National Park', 'History', 'PDF'),
    'elkmontsunclelem0000mcma': ('Elkmont\'s Uncle Lem Ownby: Sage of the Smokies', 'Culture', 'PDF'),
    'checklistoffungi00pete': ('Checklist of Fungi of the Great Smoky Mountains National Park', 'Nature', 'PDF'),
    'floraofgreatsmok00whit': ('Flora of Great Smoky Mountains National Park', 'Nature', 'PDF'),
    'statushistoryofm00culb': ('Status and History of the Mountain Lion in GSMNP', 'Nature', 'PDF'),
    'riflemakingingre13nati': ('Rifle Making in the Great Smoky Mountains', 'Culture', 'PDF'),
    'whitetaileddeero00wath': ('White-Tailed Deer of Cades Cove', 'Nature', 'PDF'),
    'lasttraintoelkmo0000weal': ('Last Train to Elkmont', 'History', 'PDF'),
    'folksongsofengli00shar': ('Folk-songs of English Origin in the Appalachian Mountains', 'Culture', 'PDF'),
    'nurserysongsfrom00shar': ('Nursery Songs from the Appalachian Mountains', 'Culture', 'PDF'),
    'historyofwataug00arth': ('A History of Watauga County, North Carolina', 'History', 'PDF'),
    'carologueaccesst00hoff': ('Carologue: Access to North Carolina', 'History', 'PDF'),
    'Elkmont09-18-14': ('Elkmont Historical Audio Recording', 'Audio', 'AUDIO')
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
        print(f"Notice: {e}")
        return False

print("Downloading Gutenberg texts...")
for gid, (title, category) in gutenberg_ids.items():
    filepath = f"content/texts/{gid}.txt"
    url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
    if download_file(url, filepath):
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
            'content': content_text[:15000]
        })

print("Downloading Internet Archive PDF & Audio items...")
for aid, data in archive_ids.items():
    title, category, item_kind = data[0], data[1], data[2]
    
    if item_kind == 'AUDIO':
        filepath = f"content/audio/{aid}.mp3"
        url = f"https://archive.org/download/{aid}/{aid}.mp3"
        item_path = f"audio/{aid}.mp3"
        item_type = 'AUDIO'
    else:
        filepath = f"content/pdfs/{aid}.pdf"
        url = f"https://archive.org/download/{aid}/{aid}.pdf"
        item_path = f"pdfs/{aid}.pdf"
        item_type = 'PDF'
        
    download_file(url, filepath)
    
    downloaded_items.append({
        'id': f"archive-{aid}",
        'title': title, 
        'category': category, 
        'path': item_path, 
        'type': item_type, 
        'local': filepath,
        'content': f"{title} - {item_type} Resource"
    })

search_json = json.dumps(downloaded_items)

# Generate Clean UI index.html (No scroll lock, proper PDF & Audio rendering, elegant typography)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Appalachian Corridor Digital Archive</title>
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --primary-color: #1e3a8a;
            --secondary-color: #2563eb;
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
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
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
            padding: 1.75rem 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}

        header h1 {{
            color: var(--primary-color);
            margin: 0 0 0.25rem 0;
            font-size: 1.8rem;
            font-weight: 700;
        }}

        header p {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin: 0;
        }}

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
            min-width: 220px;
            padding: 0.65rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
        }}

        .search-bar:focus {{
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
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
            background: var(--secondary-color);
            color: white;
            border-color: var(--secondary-color);
        }}

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
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}

        .card:hover {{
            border-color: var(--secondary-color);
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }}

        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}

        .snippet {{
            font-size: 0.85rem;
            color: #475569;
            background: #f8fafc;
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            border-left: 3px solid var(--secondary-color);
        }}

        .snippet mark {{
            background: #fef08a;
            color: #854d0e;
        }}

        audio {{
            width: 100%;
            margin-top: 0.5rem;
            height: 36px;
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
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.75rem;
        }}

        .badge-text {{ background: #e0e7ff; color: #3730a3; }}
        .badge-pdf {{ background: #fee2e2; color: #991b1b; }}
        .badge-audio {{ background: #fef3c7; color: #92400e; }}

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
                <input type="text" id="searchInput" class="search-bar" placeholder="Search full text across all books, PDFs, and audio...">
                
                <div class="settings-bar">
                    <span>Font Size:</span>
                    <button class="btn" onclick="setFontSize('14px')">S</button>
                    <button class="btn active" id="btnMed" onclick="setFontSize('16px')">M</button>
                    <button class="btn" onclick="setFontSize('18px')">L</button>
                    <button class="btn" onclick="setFontSize('20px')">XL</button>
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
        const searchData = {search_json};

        const searchInput = document.getElementById('searchInput');
        const tabs = document.querySelectorAll('.tab');
        const cardGrid = document.getElementById('cardGrid');
        const noResults = document.getElementById('noResults');

        let currentCategory = 'ALL';
        let searchQuery = '';

        function setFontSize(size) {{
            document.documentElement.style.setProperty('--base-font-size', size);
            localStorage.setItem('appalachian_font_size', size);
        }}

        const savedFontSize = localStorage.getItem('appalachian_font_size');
        if (savedFontSize) {{ setFontSize(savedFontSize); }}

        // Scroll Position Saving
        window.addEventListener('scroll', () => {{
            localStorage.setItem('appalachian_index_scroll', window.scrollY);
        }});

        const savedScrollPos = localStorage.getItem('appalachian_index_scroll');
        if (savedScrollPos) {{
            window.scrollTo({{ top: parseInt(savedScrollPos), behavior: 'smooth' }});
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

        function renderCards() {{
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
                    const card = document.createElement('div');
                    card.className = 'card';

                    let badgeClass = 'badge-text';
                    if (item.type === 'PDF') badgeClass = 'badge-pdf';
                    if (item.type === 'AUDIO') badgeClass = 'badge-audio';

                    let mediaContent = '';
                    if (item.type === 'AUDIO') {{
                        mediaContent = `<audio controls preload="none" src="${{item.path}}"></audio>`;
                    }} else if (item.type === 'PDF') {{
                        mediaContent = `<a href="${{item.path}}" target="_blank" style="color: var(--secondary-color); font-weight: 600; font-size: 0.9rem; text-decoration: none;">📄 View PDF Document →</a>`;
                    }} else {{
                        mediaContent = `<a href="${{item.path}}" style="color: var(--primary-color); font-weight: 600; font-size: 0.9rem; text-decoration: none;">📖 Read Text Document →</a>`;
                    }}

                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            ${{snippetHTML}}
                            <div style="margin-top: 0.75rem;">${{mediaContent}}</div>
                        </div>
                        <div class="card-meta">
                            <span>Category: ${{item.category}}</span>
                            <span class="badge ${{badgeClass}}">${{item.type}}</span>
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

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentCategory = tab.getAttribute('data-category');
                renderCards();
            }});
        }});

        renderCards();
    </script>
</body>
</html>
"""

with open("content/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Scrape update complete.")
