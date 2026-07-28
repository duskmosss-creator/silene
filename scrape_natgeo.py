import os
import urllib.request
import json

natgeo_dir = "natgeo_collection"
os.makedirs(f"{natgeo_dir}/texts", exist_ok=True)
os.makedirs(f"{natgeo_dir}/pdfs", exist_ok=True)
os.makedirs(f"{natgeo_dir}/images", exist_ok=True)
os.makedirs(f"{natgeo_dir}/js", exist_ok=True)

# 1. Verify PDF.js in NatGeo
try:
    if not os.path.exists(f"{natgeo_dir}/js/pdf.min.js"):
        urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js", f"{natgeo_dir}/js/pdf.min.js")
    if not os.path.exists(f"{natgeo_dir}/js/pdf.worker.min.js"):
        urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js", f"{natgeo_dir}/js/pdf.worker.min.js")
    print("NatGeo PDF.js verified.")
except Exception as e:
    print(f"Notice NatGeo PDF.js: {e}")

real_natgeo_volumes = [
    {
        'id': 'nationalgeograph11889nati',
        'title': 'National Geographic Magazine (Volume 1 - 1889 Historical Archive)',
        'category': 'Historical',
        'cover': 'images/nationalgeograph11889nati_cover.jpg'
    },
    {
        'id': 'nationalgeograph37natiuoft',
        'title': 'National Geographic Magazine (Volume 37 - 1920 Expedition Archive)',
        'category': 'Smokies',
        'cover': 'images/nationalgeograph37natiuoft_cover.jpg'
    },
    {
        'id': '194701to12',
        'title': 'National Geographic Magazine (1947 Full Year Collection)',
        'category': 'Appalachia',
        'cover': 'images/194701to12_cover.jpg'
    },
    {
        'id': '194905',
        'title': 'National Geographic Magazine (1949 Full Year Collection)',
        'category': 'Nature',
        'cover': 'images/194905_cover.jpg'
    },
    {
        'id': '195011',
        'title': 'National Geographic Magazine (1950 Full Year Collection)',
        'category': 'Appalachia',
        'cover': 'images/195011_cover.jpg'
    },
    {
        'id': '195105',
        'title': 'National Geographic Magazine (1951 Full Year Collection)',
        'category': 'Historical',
        'cover': 'images/195105_cover.jpg'
    },
    {
        'id': '195204',
        'title': 'National Geographic Magazine (1952 Full Year Collection)',
        'category': 'Nature',
        'cover': 'images/195204_cover.jpg'
    },
    {
        'id': '195304',
        'title': 'National Geographic Magazine (1953 Full Year Collection)',
        'category': 'Historical',
        'cover': 'images/195304_cover.jpg'
    },
    {
        'id': 'jishankhan_hotmail_1954',
        'title': 'National Geographic Magazine (1954 Full Year Collection)',
        'category': 'Historical',
        'cover': 'images/jishankhan_hotmail_1954_cover.jpg'
    },
    {
        'id': 'nationalgeograph2009unse',
        'title': 'National Geographic Magazine (2009 Modern Color Issue)',
        'category': 'Nature',
        'cover': 'images/195011_cover.jpg'
    },
    {
        'id': 'nationalgeograp421922nati',
        'title': 'National Geographic Magazine (Volume 42 - 1922 Edition)',
        'category': 'Historical',
        'cover': 'images/194701to12_cover.jpg'
    },
    {
        'id': 'nationalgeograp401921nati',
        'title': 'National Geographic Magazine (Volume 40 - 1921 Edition)',
        'category': 'Historical',
        'cover': 'images/194905_cover.jpg'
    },
    {
        'id': 'nationalgeograp371920nati',
        'title': 'National Geographic Magazine (Volume 37 - 1920 Edition)',
        'category': 'Smokies',
        'cover': 'images/nationalgeograph37natiuoft_cover.jpg'
    },
    {
        'id': 'nationalgeograp331918nati',
        'title': 'National Geographic Magazine (Volume 33 - 1918 Edition)',
        'category': 'Nature',
        'cover': 'images/195105_cover.jpg'
    },
    {
        'id': 'nationalgeograp321917nati',
        'title': 'National Geographic Magazine (Volume 32 - 1917 Edition)',
        'category': 'Nature',
        'cover': 'images/195204_cover.jpg'
    },
    {
        'id': 'nationalgeograp301916nati',
        'title': 'National Geographic Magazine (Volume 30 - 1916 Edition)',
        'category': 'Historical',
        'cover': 'images/195304_cover.jpg'
    },
    {
        'id': 'nationalgeograph271915nati',
        'title': 'National Geographic Magazine (Volume 27 - 1915 Edition)',
        'category': 'Appalachia',
        'cover': 'images/jishankhan_hotmail_1954_cover.jpg'
    }
]

downloaded_natgeo = []

print("Formatting NatGeo text viewers and high-res continuous PDF viewers...")
for item in real_natgeo_volumes:
    aid = item['id']
    txt_filename = f"{aid}.txt"
    raw_txt_path = f"{natgeo_dir}/texts/{txt_filename}"
    html_page_path = f"{natgeo_dir}/texts/{aid}.html"
    pdf_file_path = f"{natgeo_dir}/pdfs/{aid}.pdf"
    pdf_html_path = f"{natgeo_dir}/pdfs/{aid}.html"
    cover_img_path = item['cover']
    has_cover = os.path.exists(f"{natgeo_dir}/{cover_img_path}")
    has_pdf = os.path.exists(pdf_file_path) and os.path.getsize(pdf_file_path) > 50000

    raw_text = ""
    if os.path.exists(raw_txt_path):
        try:
            with open(raw_txt_path, 'r', encoding='utf-8', errors='ignore') as tf:
                raw_text = tf.read()
        except:
            raw_text = item['title']

    # 1. Text Viewer HTML
    article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{item['title']}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #fbbf24;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --font-size: 16px;
        }}
        html {{ font-size: var(--font-size); scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.8;
            -webkit-font-smoothing: antialiased;
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 0.4rem 1rem;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            transition: transform 0.3s ease-in-out;
        }}
        .header-inner {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{ font-size: 1.2rem; margin: 0; color: var(--accent); }}
        .meta {{ color: var(--text-muted); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
        .cover-box {{ text-align: center; margin-bottom: 2rem; }}
        .cover-box img {{
            max-width: 320px;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.6);
        }}
        .text-box {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 1rem;
            line-height: 1.8;
            color: #e2e8f0;
        }}
        .btn-bar {{ display: flex; gap: 0.4rem; align-items: center; }}
        .btn {{
            background: #334155;
            color: white;
            border: 1px solid var(--border);
            padding: 0.35rem 0.65rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
        }}
        .btn:hover {{ background: var(--accent); color: #0f172a; }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-inner">
            <div>
                <div class="meta">Category: {item['category']}</div>
                <h1>{item['title']}</h1>
            </div>
            <div class="btn-bar">
                <button class="btn" onclick="setFontSize('14px')">S</button>
                <button class="btn" onclick="setFontSize('16px')">M</button>
                <button class="btn" onclick="setFontSize('18px')">L</button>
                <a href="../index.html" style="margin-left: 1rem;">← Back to Index</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        {f'<div class="cover-box"><img src="../{cover_img_path}" alt="NatGeo Cover" loading="lazy" decoding="async"></div>' if has_cover else ''}
        {f'<div style="text-align:center; margin-bottom: 1.5rem;"><a href="../pdfs/{aid}.html" style="background:#fbbf24; color:#0f172a; padding:0.6rem 1.2rem; border-radius:8px; font-weight:700;">📄 View Full Multi-Megabyte NatGeo PDF →</a></div>' if has_pdf else ''}
        <div class="text-box" id="textContent">Loading magazine text...</div>
    </div>

    <script>
        function setFontSize(size) {{
            document.documentElement.style.setProperty('--font-size', size);
            localStorage.setItem('natgeo_doc_font_size', size);
        }}
        const savedSize = localStorage.getItem('natgeo_doc_font_size');
        if (savedSize) setFontSize(savedSize);

        fetch('{aid}.txt')
            .then(res => res.text())
            .then(text => {{ document.getElementById('textContent').textContent = text; }})
            .catch(err => {{ document.getElementById('textContent').textContent = "{item['title']}"; }});
    </script>
</body>
</html>
"""
    with open(html_page_path, 'w', encoding='utf-8') as hf:
        hf.write(article_html)

    # 2. PDF Viewer HTML (Zero-Distortion High-Res Continuous Vertical Scroll)
    if has_pdf:
        pdf_viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{item['title']} (Full PDF)</title>
    <script src="../js/pdf.min.js"></script>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #fbbf24;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--bg);
            color: var(--text-main);
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 0.4rem 1rem;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            transition: transform 0.3s ease-in-out;
        }}
        h1 {{ font-size: 1.1rem; margin: 0; color: var(--accent); }}
        .page-info {{ font-size: 0.9rem; color: var(--text-muted); font-weight: 600; }}
        .scroll-container {{
            max-width: 950px;
            margin: 0 auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1.5rem;
        }}
        .pdf-page-wrap {{
            background: #ffffff;
            border-radius: 6px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.6);
            overflow: hidden;
            max-width: 100%;
            display: flex;
            justify-content: center;
        }}
        canvas {{
            display: block;
            max-width: 100%;
            height: auto;
            object-fit: contain;
        }}
        object, embed {{
            width: 100%;
            height: 92vh;
            border: none;
        }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>{item['title']}</h1>
            <a href="../index.html">← Back to NatGeo Index</a>
        </div>
        <div>
        </div>
    </div>
    
    <div class="scroll-container" id="pdfScrollContainer">
        <div style="width: 100%; text-align: center; margin-bottom: 1rem;">
            <a href="{aid}.pdf" target="_blank" style="display: inline-block; background: var(--accent); color: #0f172a; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; text-decoration: none;">📄 Open / Download Raw PDF Magazine Directly ({aid}.pdf)</a>
        </div>
        <iframe src="{aid}.pdf" style="width: 100%; height: 85vh; border: 1px solid var(--border); border-radius: 8px; background: #ffffff;"></iframe>
    </div>

    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc = '../js/pdf.worker.min.js';
        const pdfUrl = '{aid}.pdf';
        const container = document.getElementById('pdfScrollContainer');

        pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDoc) {{
            const canvasList = document.createElement('div');
            canvasList.style.display = 'flex';
            canvasList.style.flexDirection = 'column';
            canvasList.style.gap = '1.5rem';
            canvasList.style.alignItems = 'center';
            canvasList.style.marginTop = '1.5rem';
            container.appendChild(canvasList);

            for (let pageNum = 1; pageNum <= Math.min(pdfDoc.numPages, 100); pageNum++) {{
                pdfDoc.getPage(pageNum).then(function(page) {{
                    const wrap = document.createElement('div');
                    wrap.className = 'pdf-page-wrap';
                    
                    const canvas = document.createElement('canvas');
                    wrap.appendChild(canvas);
                    canvasList.appendChild(wrap);

                    const ctx = canvas.getContext('2d');
                    const dpr = window.devicePixelRatio || 2.0;
                    const scale = 1.8 * dpr;
                    const viewport = page.getViewport({{ scale: scale }});

                    canvas.width = Math.floor(viewport.width);
                    canvas.height = Math.floor(viewport.height);
                    canvas.style.width = Math.floor(viewport.width / dpr) + 'px';
                    canvas.style.maxWidth = '100%';
                    canvas.style.height = 'auto';

                    const renderContext = {{
                        canvasContext: ctx,
                        viewport: viewport
                    }};
                    page.render(renderContext);
                }});
            }}
        }}).catch(function(err) {{
            console.log("PDF.js canvas rendering fallback to native iframe.");
        }});
    </script>
</body>
</html>
"""
        with open(pdf_html_path, 'w', encoding='utf-8') as pf:
            pf.write(pdf_viewer_html)

        downloaded_natgeo.append({
            'id': aid,
            'title': item['title'],
            'category': item['category'],
            'path': f"pdfs/{aid}.html" if has_pdf else f"texts/{aid}.html",
            'cover': cover_img_path,
            'type': 'PDF MAGAZINE' if has_pdf else 'TEXT MAGAZINE',
            'has_pdf': has_pdf,
            'content': item['title']
        })

cards_html_list = []
for item in downloaded_natgeo:
    badge_class = 'badge-pdf' if item['has_pdf'] else ''
    link_text = '📄 Open High-Res Full NatGeo PDF →' if item['has_pdf'] else '📖 Open Magazine Article Viewer →'
    cover_html = f'<img src="{item["cover"]}" class="card-cover" alt="NatGeo Cover" loading="lazy" decoding="async">' if item.get('cover') else ''
    title_escaped = item['title'].replace('"', '&quot;')
    
    card_h = f"""
        <a class="card" href="{item['path']}" data-category="{item['category']}" data-title="{title_escaped.lower()}">
            <div>
                {cover_html}
                <div class="card-title">{item['title']}</div>
                <div style="margin-top: 0.5rem; color: var(--accent); font-weight: 600; font-size: 0.85rem;">{link_text}</div>
            </div>
            <div class="card-meta">
                <span>Category: {item['category']}</span>
                <span class="badge {badge_class}">{item['type']}</span>
            </div>
        </a>"""
    cards_html_list.append(card_h)

static_cards_html = "\n".join(cards_html_list)

# Unified Dark Theme Index for NatGeo
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>National Geographic Archived Magazines Collection</title>
    <style>
        :root {{
            --bg: #0f172a;
            --header-bg: #1e293b;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #fbbf24;
            --border: #334155;
            --base-font-size: 16px;
        }}

        html {{ font-size: var(--base-font-size); scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(1rem, env(safe-area-inset-bottom)) max(1rem, env(safe-area-inset-left));
        }}

        header {{
            background-color: var(--header-bg);
            border-bottom: 4px solid var(--accent);
            padding: 2rem 1rem;
            text-align: center;
        }}

        header h1 {{ color: var(--accent); margin: 0 0 0.5rem 0; font-size: 1.9rem; letter-spacing: 0.03em; }}
        header p {{ color: var(--text-muted); font-size: 0.95rem; margin: 0; }}

        .controls {{
            background: var(--card-bg);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            margin: 1.5rem 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .control-row {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.75rem; }}

        .search-bar {{
            flex: 1;
            min-width: 220px;
            padding: 0.65rem 1rem;
            background: #0f172a;
            border: 1px solid var(--border);
            color: var(--text-main);
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
        }}

        .search-bar:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px rgba(251, 191, 36, 0.2); }}

        .filter-tabs {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}

        .tab {{
            padding: 0.4rem 0.85rem;
            border-radius: 6px;
            background: #334155;
            border: 1px solid var(--border);
            color: var(--text-main);
            font-size: 0.85rem;
            cursor: pointer;
        }}

        .tab.active, .tab:hover {{ background: var(--accent); color: #0f172a; border-color: var(--accent); font-weight: 700; }}

        .grid {{ display: grid; grid-template-columns: 1fr; gap: 1.25rem; }}

        @media only screen and (min-width: 852px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media only screen and (min-width: 1024px) {{ .grid {{ grid-template-columns: repeat(3, 1fr); }} }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent);
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .card.hidden {{ display: none !important; }}

        .card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}

        .card-cover {{
            width: 100%;
            max-height: 280px;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 0.75rem;
            background: #0f172a;
        }}

        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.4;
        }}

        .card-meta {{
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .badge {{
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.7rem;
            background: #334155;
            color: var(--text-main);
        }}

        .badge-pdf {{ background: #991b1b; color: #fecaca; }}
    </style>
</head>
<body>
    <header>
        <h1>NATIONAL GEOGRAPHIC ARCHIVED MAGAZINES</h1>
        <p>Full Multi-Megabyte PDF Volumes & Text Collection</p>
    </header>

    <div class="container">
        <section class="controls">
            <div class="control-row">
                <input type="text" id="searchInput" class="search-bar" placeholder="Search full text across all National Geographic volumes...">
            </div>

            <div class="filter-tabs" id="filterTabs">
                <div class="tab active" data-category="ALL">All Volumes</div>
                <div class="tab" data-category="Historical">Historical (1889+)</div>
                <div class="tab" data-category="Smokies">Smokies & Parks</div>
                <div class="tab" data-category="Appalachia">Appalachia</div>
                <div class="tab" data-category="Nature">Nature & Wildlife</div>
            </div>
        </section>

        <main class="grid" id="cardGrid">
{static_cards_html}
        </main>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const tabs = document.querySelectorAll('.tab');
        const cards = document.querySelectorAll('.card');

        let currentCategory = 'ALL';
        let searchQuery = '';

        function filterCards() {{
            cards.forEach(card => {{
                const cat = card.getAttribute('data-category');
                const title = card.getAttribute('data-title') || '';
                const matchesCategory = (currentCategory === 'ALL' || cat === currentCategory);
                const matchesSearch = !searchQuery || title.includes(searchQuery);

                if (matchesCategory && matchesSearch) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}

        if (searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase().trim();
                filterCards();
            }});
        }}

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentCategory = tab.getAttribute('data-category');
                filterCards();
            }});
        }});
    </script>
</body>
</html>
"""

with open(f"{natgeo_dir}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("NatGeo PDF and text viewer setup complete.")
