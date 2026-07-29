import os, glob

natgeo_dir = 'natgeo_collection'
pdfs = glob.glob(f'{natgeo_dir}/pdfs/*.pdf')
print(f'Found {len(pdfs)} PDFs in {natgeo_dir}/pdfs')

pdf_viewer_template = """<!DOCTYPE html>
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
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>{title}</h1>
            <a href="../index.html">← Back to National Geographic Archive</a>
        </div>
    </div>
    
    <div class="scroll-container" id="pdfScrollContainer" style="padding-top: 80px;">
        <div style="width: 100%; text-align: center; margin-bottom: 1rem;">
            <a href="{pdf_filename}" target="_blank" style="display: inline-block; background: var(--accent); color: #0f172a; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 700; text-decoration: none;">📄 Open / Download Raw PDF Magazine Directly ({pdf_filename})</a>
        </div>
        <iframe src="{pdf_filename}" style="width: 100%; height: 85vh; border: 1px solid var(--border); border-radius: 8px; background: #ffffff;"></iframe>
    </div>

    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc = '../js/pdf.worker.min.js';
        const pdfUrl = '{pdf_filename}';
        const container = document.getElementById('pdfScrollContainer');

        pdfjsLib.getDocument(pdfUrl).promise.then(function(pdfDoc) {{
            const canvasList = document.createElement('div');
            canvasList.style.display = 'flex';
            canvasList.style.flexDirection = 'column';
            canvasList.style.gap = '1.5rem';
            canvasList.style.alignItems = 'center';
            canvasList.style.marginTop = '1.5rem';
            container.appendChild(canvasList);

            for (let pageNum = 1; pageNum <= Math.min(pdfDoc.numPages, 150); pageNum++) {{
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

cards_html = ''
for p in sorted(pdfs):
    basename = os.path.basename(p)
    aid = os.path.splitext(basename)[0]
    title = f'National Geographic ({aid})'
    
    # Check for cover img
    cover_path = f'../images/{aid}_cover.jpg'
    local_cover = f'natgeo_collection/images/{aid}_cover.jpg'
    if not os.path.exists(local_cover):
        cover_path = '../images/nationalgeograph11889nati_cover.jpg'
        
    # Write wrapper HTML
    html_content = pdf_viewer_template.format(title=title, pdf_filename=basename)
    with open(f'{natgeo_dir}/pdfs/{aid}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Create card for index
    cards_html += f'''
        <a class="card" href="pdfs/{aid}.html">
            <div>
                <img src="{cover_path.replace('../', '')}" class="card-cover" alt="Cover" loading="lazy">
                <div class="card-title">{title}</div>
                <div style="margin-top: 0.5rem; color: var(--accent); font-weight: 600; font-size: 0.85rem;">📄 Open PDF Magazine →</div>
            </div>
        </a>
'''

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>National Geographic Archive</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #fbbf24;
            --text-main: #f8fafc;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 0;
        }}
        .header {{
            background: var(--card-bg);
            border-bottom: 2px solid var(--accent);
            padding: 1.5rem 1rem;
            text-align: center;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            border: 1px solid #334155;
        }}
        .card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
        }}
        .card-cover {{
            width: 100%;
            height: 320px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 1rem;
            background: #000;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.3;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color: var(--accent); margin:0;">National Geographic Magazine Archive</h1>
        <p style="color: #94a3b8; margin-top:0.5rem;">Exclusive Appalachian Collection & Full Photo Issues</p>
    </div>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>"""

with open(f'{natgeo_dir}/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print('Successfully generated NatGeo PDF wrappers and index.html!')
