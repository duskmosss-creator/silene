import os
import glob
import re

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def parse_date(filename):
    fn = os.path.basename(filename)
    if fn == '194701to12.pdf': return (1947, 1)
    if fn == '194905.pdf': return (1949, 5)
    if fn == '195011.pdf': return (1950, 11)
    if fn == '195105.pdf': return (1951, 5)
    if fn == '195204.pdf': return (1952, 4)
    if fn == '195304.pdf': return (1953, 4)
    if fn.startswith('20'):
        m = re.search(r'^(20\d\d)(\d\d)', fn)
        if m:
            month = int(m.group(2))
            if month > 12: month = 1
            return (int(m.group(1)), month)
    m = re.search(r'NG(20\d\d)(\d\d)', fn)
    if m: return (int(m.group(1)), int(m.group(2)))
    m = re.search(r'(20\d\d)', fn)
    if m:
        year = int(m.group(1))
        month = 1
        name = fn.lower()
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        for i, mo in enumerate(months):
            if mo in name or mo[:3] in name:
                month = i + 1
                break
        return (year, month)
    m = re.search(r'1888_1_1', fn)
    if m: return (1888, 1)
    m = re.search(r'(18\d\d|19\d\d)', fn)
    if m: return (int(m.group(1)), 1)
    return (9999, 1)

def make_title(aid):
    y, m = parse_date(aid + '.pdf')
    if y == 9999:
        return f'National Geographic (Archival)'
    return f'National Geographic - {MONTHS[m]} {y}'

def generate_viewer_html(aid):
    title = make_title(aid)
    pdf_file = f"{aid}.pdf"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <script src="../js/pdf.min.js"></script>
    <script src="js/pdf.min.js"></script>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #fbbf24;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0; padding: 0;
            background-color: var(--bg);
            color: var(--text-main);
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 0.6rem 1rem;
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}
        h1 {{
            font-size: 1rem;
            margin: 0;
            color: var(--accent);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 50vw;
        }}
        .controls {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}
        button, a.btn-link {{
            background: #0284c7;
            color: white;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            text-decoration: none;
            display: inline-block;
        }}
        button:hover, a.btn-link:hover {{ background: #0369a1; }}
        .page-info {{ font-size: 0.85rem; color: var(--text-muted); white-space: nowrap; }}
        a.back-link {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.85rem; white-space: nowrap; }}
        
        .scroll-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1.5rem;
            padding-top: 75px;
            padding-bottom: 3rem;
            max-width: 950px;
            margin: 0 auto;
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
            background: #ffffff;
        }}
        #loading {{
            padding: 3rem;
            color: var(--text-muted);
            font-size: 1.1rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>{title}</h1>
            <a class="back-link" href="../index.html">&#8592; Back to Library</a>
        </div>
        <div class="controls">
            <span class="page-info"><span id="pageCount">-</span> Pages</span>
            <a class="btn-link" href="{pdf_file}" data-href="{pdf_file}" target="_blank">&#128196; Raw PDF</a>
        </div>
    </div>
    
    <div class="scroll-container" id="pdfScrollContainer">
        <div id="loading">
            <p>Loading {title}...</p>
            <p style="margin-top: 1rem;"><a href="{pdf_file}" class="btn-link" style="padding: 0.6rem 1.2rem;">&#128196; Open PDF Directly</a></p>
        </div>
    </div>

    <script>
        // Force fake worker to avoid iOS WKWebView worker security errors
        if (window.pdfjsLib) {{
            try {{
                pdfjsLib.GlobalWorkerOptions.workerSrc = '';
            }} catch(e) {{}}
        }}

        const url = '{pdf_file}';
        const container = document.getElementById('pdfScrollContainer');

        if (window.pdfjsLib) {{
            pdfjsLib.getDocument(url).promise.then(function(pdfDoc) {{
                document.getElementById('pageCount').textContent = pdfDoc.numPages;
                container.innerHTML = '';

                function renderSequentially(pageNum) {{
                    if (pageNum > pdfDoc.numPages) return;

                    const wrap = document.createElement('div');
                    wrap.className = 'pdf-page-wrap';
                    
                    const canvas = document.createElement('canvas');
                    wrap.appendChild(canvas);
                    container.appendChild(wrap);

                    pdfDoc.getPage(pageNum).then(function(page) {{
                        // Calculate viewport with iOS canvas size protection (max 2048px)
                        const scale = 1.3;
                        let viewport = page.getViewport({{ scale: scale }});
                        
                        if (viewport.width > 2048) {{
                            const maxScale = 2048 / page.getViewport({{ scale: 1 }}).width;
                            viewport = page.getViewport({{ scale: maxScale }});
                        }}

                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        const renderTask = page.render({{
                            canvasContext: canvas.getContext('2d'),
                            viewport: viewport
                        }});

                        renderTask.promise.then(function() {{
                            renderSequentially(pageNum + 1);
                        }}).catch(function() {{
                            renderSequentially(pageNum + 1);
                        }});
                    }}).catch(function() {{
                        renderSequentially(pageNum + 1);
                    }});
                }}

                renderSequentially(1);

            }}).catch(function(err) {{
                showFallback();
            }});
        }} else {{
            showFallback();
        }}

        function showFallback() {{
            container.innerHTML = `
                <div style="background: var(--card-bg); padding: 2rem; border-radius: 8px; text-align: center; color: var(--text-muted); border: 1px solid var(--border); margin-top: 2rem; width: 100%;">
                    <p style="font-size: 1.2rem; color: var(--accent); font-weight: 700;">{title}</p>
                    <p>Tap below to view full original magazine:</p>
                    <a href="{pdf_file}" data-href="{pdf_file}" class="btn-link" style="padding: 0.8rem 1.6rem; font-size: 1.1rem; margin-top: 1rem;">&#128196; Open {title} PDF</a>
                    <div style="margin-top: 1.5rem;">
                        <object data="{pdf_file}" data-pdf-src="{pdf_file}" type="application/pdf" width="100%" height="600px">
                            <embed src="{pdf_file}" data-pdf-src="{pdf_file}" type="application/pdf" width="100%" height="600px" />
                        </object>
                    </div>
                </div>
            `;
        }}
    </script>
</body>
</html>'''

pdfs = glob.glob('natgeo_collection/pdfs/*.pdf')
print(f'Generating v17 bulletproof iOS viewer HTML for {len(pdfs)} PDFs...')
for p in pdfs:
    aid = os.path.splitext(os.path.basename(p))[0]
    out = f'natgeo_collection/pdfs/{aid}.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(generate_viewer_html(aid))

print('Done generating v17 viewer HTML!')
