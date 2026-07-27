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
    'carologueaccesst00hoff': ('Carologue: Access to North Carolina', 'History', 'PDF')
}

downloaded_items = []

def download_file(url, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            if len(data) > 0:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return True
    except Exception as e:
        print(f"Notice: {e}")
    return False

# 1. Download & Wrap Gutenberg Texts into Styled HTML Articles
print("Processing Gutenberg texts into styled HTML articles...")
for gid, (title, category) in gutenberg_ids.items():
    raw_txt_path = f"content/texts/{gid}_raw.txt"
    html_page_path = f"content/texts/{gid}.html"
    url = f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt"
    
    download_file(url, raw_txt_path)
    
    raw_text = ""
    if os.path.exists(raw_txt_path):
        try:
            with open(raw_txt_path, 'r', encoding='utf-8', errors='ignore') as tf:
                raw_text = tf.read()
        except:
            raw_text = title

    # Format text into clean paragraphs
    paragraphs = raw_text.split('\n\n')
    formatted_p_html = "".join([f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()])

    article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
            line-height: 1.8;
            color: #1e293b;
            background-color: #ffffff;
            max-width: 850px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}
        header {{
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}
        h1 {{ color: #0f172a; font-size: 1.8rem; margin: 0 0 0.5rem 0; }}
        .meta {{ color: #64748b; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; }}
        p {{ margin-bottom: 1.25rem; word-wrap: break-word; white-space: pre-wrap; }}
        a {{ color: #2563eb; text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <div class="meta">Category: {category}</div>
        <h1>{title}</h1>
        <a href="../index.html">← Back to Archive Index</a>
    </header>
    <main>
        {formatted_p_html}
    </main>
</body>
</html>
"""
    with open(html_page_path, 'w', encoding='utf-8') as hf:
        hf.write(article_html)

    downloaded_items.append({
        'id': f"gutenberg-{gid}",
        'title': title, 
        'category': category, 
        'path': f"texts/{gid}.html", 
        'type': 'TEXT', 
        'content': raw_text[:10000]
    })

# 2. Process PDFs with Low-Resource Web Viewer Wrapper
print("Processing PDF documents into low-resource web viewers...")
for aid, data in archive_ids.items():
    title, category = data[0], data[1]
    
    pdf_file_path = f"content/pdfs/{aid}.pdf"
    pdf_html_path = f"content/pdfs/{aid}.html"
    url = f"https://archive.org/download/{aid}/{aid}.pdf"
    
    has_pdf = download_file(url, pdf_file_path)

    # Build low-resource PDF viewer page
    if has_pdf:
        viewer_content = f"""<iframe src="{aid}.pdf" style="width: 100%; height: 82vh; border: 1px solid #cbd5e1; border-radius: 8px;"></iframe>"""
    else:
        viewer_content = f"""<div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 2rem; border-radius: 8px; text-align: center;">
            <p>PDF Document Metadata & Text Summary for <strong>{title}</strong></p>
            <p><a href="https://archive.org/details/{aid}" target="_blank" style="color: #2563eb;">View Original Document on Internet Archive ↗</a></p>
        </div>"""

    pdf_viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 1rem;
            background-color: #f8fafc;
            color: #0f172a;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e2e8f0;
        }}
        h1 {{ font-size: 1.25rem; margin: 0; color: #1e3a8a; }}
        a {{ color: #2563eb; text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <a href="../index.html">← Back to Archive Index</a>
    </div>
    {viewer_content}
</body>
</html>
"""
    with open(pdf_html_path, 'w', encoding='utf-8') as pf:
        pf.write(pdf_viewer_html)

    downloaded_items.append({
        'id': f"archive-{aid}",
        'title': title, 
        'category': category, 
        'path': f"pdfs/{aid}.html", 
        'type': 'PDF', 
        'content': f"{title} PDF Document"
    })

# 3. Add Working Audio Recording with Embedded Player Page
audio_title = "Elkmont Historical Audio Recording"
audio_html_path = "content/audio/elkmont_audio.html"

audio_viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{audio_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 600px;
            margin: 3rem auto;
            padding: 2rem;
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }}
        h1 {{ font-size: 1.4rem; color: #0f172a; margin-bottom: 1.5rem; }}
        audio {{ width: 100%; margin: 1.5rem 0; }}
        a {{ color: #2563eb; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
    <h1>🎵 {audio_title}</h1>
    <p>Historical oral record of Elkmont community & Appalachian heritage.</p>
    <audio controls>
        <source src="https://archive.org/download/Elkmont09-18-14/Elkmont09-18-14.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    <br><br>
    <a href="../index.html">← Back to Archive Index</a>
</body>
</html>
"""
with open(audio_html_path, 'w', encoding='utf-8') as af:
    af.write(audio_viewer_html)

downloaded_items.append({
    'id': 'elkmont-audio',
    'title': audio_title,
    'category': 'Audio',
    'path': 'audio/elkmont_audio.html',
    'type': 'AUDIO',
    'content': 'Elkmont Historical Audio Recording Oral History'
})

search_json = json.dumps(downloaded_items)

# Generate Main Index HTML
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
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

        window.addEventListener('scroll', () => {{
            localStorage.setItem('appalachian_index_scroll', window.scrollY);
        }});

        const savedScrollPos = localStorage.getItem('appalachian_index_scroll');
        if (savedScrollPos) {{
            window.scrollTo({{ top: parseInt(savedScrollPos), behavior: 'smooth' }});
        }}

        function renderCards() {{
            cardGrid.innerHTML = '';
            let visibleCount = 0;

            searchData.forEach(item => {{
                const matchesCategory = (currentCategory === 'ALL' || item.category === currentCategory);
                let matchesSearch = false;

                if (!searchQuery) {{
                    matchesSearch = true;
                }} else {{
                    const titleMatch = item.title.toLowerCase().includes(searchQuery);
                    const bodyMatch = item.content && item.content.toLowerCase().includes(searchQuery);
                    matchesSearch = titleMatch || bodyMatch;
                }}

                if (matchesSearch && matchesCategory) {{
                    visibleCount++;
                    const card = document.createElement('a');
                    card.className = 'card';
                    card.href = item.path;

                    let badgeClass = 'badge-text';
                    let linkText = '📖 Read Formatted Article →';
                    if (item.type === 'PDF') {{
                        badgeClass = 'badge-pdf';
                        linkText = '📄 View PDF Document →';
                    }} else if (item.type === 'AUDIO') {{
                        badgeClass = 'badge-audio';
                        linkText = '🎵 Play Audio Recording →';
                    }}

                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            <div style="margin-top: 0.5rem; color: var(--secondary-color); font-weight: 600; font-size: 0.9rem;">${{linkText}}</div>
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
