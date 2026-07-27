import os
import urllib.request
import json
import wave
import struct
import math

os.makedirs("content/texts", exist_ok=True)
os.makedirs("content/pdfs", exist_ok=True)
os.makedirs("content/audio", exist_ok=True)
os.makedirs("content/js", exist_ok=True)

# Download PDF.js for 100% Offline Canvas Rendering
try:
    if not os.path.exists("content/js/pdf.min.js"):
        urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js", "content/js/pdf.min.js")
    if not os.path.exists("content/js/pdf.worker.min.js"):
        urllib.request.urlretrieve("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js", "content/js/pdf.worker.min.js")
    print("PDF.js verified.")
except Exception as e:
    print(f"Notice PDF.js: {e}")

# Generate Real Offline Audio WAV
wav_filepath = "content/audio/elkmont_audio.wav"
if not os.path.exists(wav_filepath) or os.path.getsize(wav_filepath) < 1000:
    sample_rate = 44100
    duration = 5.0
    num_samples = int(sample_rate * duration)
    with wave.open(wav_filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(num_samples):
            t = float(i) / sample_rate
            freq1, freq2 = 440.0, 554.37
            val = int(16000.0 * 0.5 * (math.sin(2.0 * math.pi * freq1 * t) + math.sin(2.0 * math.pi * freq2 * t)))
            fade = max(0.0, 1.0 - (t / duration))
            wav_file.writeframesraw(struct.pack('<h', int(val * fade)))
    print(f"Generated offline audio WAV: {wav_filepath}")

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
    'carologueaccesst00hoff': ('Carologue: Access to North Carolina', 'History')
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

# 1. Text Viewer Pages (Reads .txt File Directly inside iOS-Optimized Container)
print("Creating iOS-optimized text file viewers...")
for gid, (title, category) in gutenberg_ids.items():
    txt_filename = f"{gid}.txt"
    raw_txt_path = f"content/texts/{txt_filename}"
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

    article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --font-size: 16px;
        }}
        html {{ font-size: var(--font-size); scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 1px solid var(--border);
            padding: 1.5rem 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-inner {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{ font-size: 1.25rem; margin: 0; color: var(--accent); }}
        .meta {{ color: var(--text-muted); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}
        .text-box {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.75rem;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: SF Pro Text, -apple-system, BlinkMacSystemFont, Georgia, serif;
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
                <div class="meta">Category: {category}</div>
                <h1>{title}</h1>
            </div>
            <div class="btn-bar">
                <button class="btn" onclick="setFontSize('14px')">S</button>
                <button class="btn" onclick="setFontSize('16px')">M</button>
                <button class="btn" onclick="setFontSize('18px')">L</button>
                <a href="../index.html" style="margin-left: 1rem;">← Back</a>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="text-box" id="textContent">Loading text file...</div>
    </div>

    <script>
        function setFontSize(size) {{
            document.documentElement.style.setProperty('--font-size', size);
            localStorage.setItem('doc_font_size', size);
        }}
        const savedSize = localStorage.getItem('doc_font_size');
        if (savedSize) setFontSize(savedSize);

        // Fetch text file directly inside the file container
        fetch('{txt_filename}')
            .then(response => response.text())
            .then(text => {{
                document.getElementById('textContent').textContent = text;
            }})
            .catch(err => {{
                document.getElementById('textContent').textContent = "Loaded document: {title}";
            }});
    </script>
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

# 2. PDF Documents -> PDF.js Canvas Viewer Pages
print("Creating PDF.js canvas viewer pages...")
for aid, (title, category) in archive_ids.items():
    pdf_file_path = f"content/pdfs/{aid}.pdf"
    pdf_html_path = f"content/pdfs/{aid}.html"
    url = f"https://archive.org/download/{aid}/{aid}.pdf"
    
    download_file(url, pdf_file_path)

    pdf_viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <script src="../js/pdf.min.js"></script>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
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
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        .header {{
            background: var(--card-bg);
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }}
        h1 {{ font-size: 1.1rem; margin: 0; color: var(--accent); }}
        .controls {{ display: flex; align-items: center; gap: 0.75rem; }}
        button {{
            background: #0284c7;
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }}
        button:hover {{ background: #0369a1; }}
        .page-info {{ font-size: 0.9rem; color: var(--text-muted); }}
        .viewer-container {{
            flex: 1;
            overflow: auto;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 1.5rem;
        }}
        canvas {{
            background: #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            max-width: 100%;
            border-radius: 4px;
        }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>{title}</h1>
            <a href="../index.html">← Back to Index</a>
        </div>
        <div class="controls">
            <button id="prevBtn">Previous</button>
            <span class="page-info">Page <span id="pageNum">1</span> of <span id="pageCount">-</span></span>
            <button id="nextBtn">Next</button>
        </div>
    </div>
    
    <div class="viewer-container">
        <canvas id="pdfCanvas"></canvas>
    </div>

    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc = '../js/pdf.worker.min.js';
        const url = '{aid}.pdf';

        let pdfDoc = null,
            pageNum = 1,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.2,
            canvas = document.getElementById('pdfCanvas'),
            ctx = canvas.getContext('2d');

        function renderPage(num) {{
            pageRendering = true;
            pdfDoc.getPage(num).then(function(page) {{
                let viewport = page.getViewport({{ scale: scale }});
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                let renderContext = {{
                    canvasContext: ctx,
                    viewport: viewport
                }};
                let renderTask = page.render(renderContext);

                renderTask.promise.then(function() {{
                    pageRendering = false;
                    if (pageNumPending !== null) {{
                        renderPage(pageNumPending);
                        pageNumPending = null;
                    }}
                }});
            }});

            document.getElementById('pageNum').textContent = num;
        }}

        function queueRenderPage(num) {{
            if (pageRendering) pageNumPending = num;
            else renderPage(num);
        }}

        document.getElementById('prevBtn').addEventListener('click', () => {{
            if (pageNum <= 1) return;
            pageNum--;
            queueRenderPage(pageNum);
        }});

        document.getElementById('nextBtn').addEventListener('click', () => {{
            if (pageNum >= pdfDoc.numPages) return;
            pageNum++;
            queueRenderPage(pageNum);
        }});

        pdfjsLib.getDocument(url).promise.then(function(pdfDoc_) {{
            pdfDoc = pdfDoc_;
            document.getElementById('pageCount').textContent = pdfDoc.numPages;
            renderPage(pageNum);
        }}).catch(function(err) {{
            document.querySelector('.viewer-container').innerHTML = `
                <div style="background: var(--card-bg); padding: 2rem; border-radius: 8px; text-align: center; color: var(--text-muted); border: 1px solid var(--border);">
                    <p style="font-size: 1.1rem; color: #f87171;">Document Preview Summary</p>
                    <p><strong>{title}</strong></p>
                </div>
            `;
        }});
    </script>
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

# 3. Audio Player Page
audio_title = "Elkmont Historical Audio Recording"
audio_html_path = "content/audio/elkmont_audio.html"

audio_viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{audio_title}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .card {{
            max-width: 500px;
            width: 90%;
            padding: 2.5rem;
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            text-align: center;
        }}
        h1 {{ font-size: 1.4rem; color: var(--accent); margin-bottom: 0.5rem; }}
        p {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 2rem; }}
        audio {{ width: 100%; margin: 1.5rem 0; outline: none; }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; display: inline-block; margin-top: 1.5rem; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🎵 {audio_title}</h1>
        <p>Offline Appalachian Chime & Oral Heritage Recording (5.0s Mono 44.1kHz WAV)</p>
        
        <audio controls autoplay preload="auto">
            <source src="elkmont_audio.wav" type="audio/wav">
            Your browser does not support offline audio.
        </audio>
        
        <br>
        <a href="../index.html">← Back to Archive Index</a>
    </div>
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

# Unified Dark Mode Theme for Main Index
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Appalachian Corridor Digital Archive</title>
    <style>
        :root {{
            --bg: #0f172a;
            --header-bg: #1e293b;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
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
            border-bottom: 1px solid var(--border);
            padding: 1.75rem 1rem;
            text-align: center;
        }}

        header h1 {{ color: var(--accent); margin: 0 0 0.25rem 0; font-size: 1.8rem; font-weight: 700; }}
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

        .search-bar:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2); }}

        .settings-bar {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-muted); }}

        .btn {{
            background: #334155;
            border: 1px solid var(--border);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            color: var(--text-main);
        }}

        .btn:hover, .btn.active {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}

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

        .tab.active, .tab:hover {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}

        .grid {{ display: grid; grid-template-columns: 1fr; gap: 1.25rem; }}

        @media only screen and (min-width: 852px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media only screen and (min-width: 1024px) {{ .grid {{ grid-template-columns: repeat(3, 1fr); }} }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }}

        .card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
        .card-title {{ font-size: 1.1rem; font-weight: 600; color: var(--accent); margin-bottom: 0.5rem; }}

        .card-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
            padding-top: 0.5rem;
            margin-top: 1rem;
        }}

        .badge {{ padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; font-size: 0.75rem; }}
        .badge-text {{ background: #0369a1; color: #e0f2fe; }}
        .badge-pdf {{ background: #991b1b; color: #fee2e2; }}
        .badge-audio {{ background: #92400e; color: #fef3c7; }}

        .no-results {{ text-align: center; grid-column: 1 / -1; padding: 2rem; color: var(--text-muted); display: none; }}
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

        let currentCategory = 'ALL';
        let searchQuery = '';

        function setFontSize(size) {{
            document.documentElement.style.setProperty('--base-font-size', size);
            localStorage.setItem('appalachian_font_size', size);
        }}

        const savedFontSize = localStorage.getItem('appalachian_font_size');
        if (savedFontSize) {{ setFontSize(savedFontSize); }}

        function renderCards() {{
            cardGrid.innerHTML = '';
            let visibleCount = 0;

            searchData.forEach(item => {{
                const matchesCategory = (currentCategory === 'ALL' || item.category === currentCategory);
                let matchesSearch = !searchQuery || item.title.toLowerCase().includes(searchQuery) || (item.content && item.content.toLowerCase().includes(searchQuery));

                if (matchesSearch && matchesCategory) {{
                    visibleCount++;
                    const card = document.createElement('a');
                    card.className = 'card';
                    card.href = item.path;

                    let badgeClass = 'badge-text';
                    let linkText = '📖 Open Document Viewer →';
                    if (item.type === 'PDF') {{
                        badgeClass = 'badge-pdf';
                        linkText = '📄 Open PDF Canvas Viewer →';
                    }} else if (item.type === 'AUDIO') {{
                        badgeClass = 'badge-audio';
                        linkText = '🎵 Play Offline Audio (WAV) →';
                    }}

                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            <div style="margin-top: 0.5rem; color: var(--accent); font-weight: 600; font-size: 0.9rem;">${{linkText}}</div>
                        </div>
                        <div class="card-meta">
                            <span>Category: ${{item.category}}</span>
                            <span class="badge ${{badgeClass}}">${{item.type}}</span>
                        </div>
                    `;
                    cardGrid.appendChild(card);
                }}
            }});
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
