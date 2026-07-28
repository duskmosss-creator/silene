import os
import re
import html

def md_to_html(md_text):
    lines = md_text.split('\n')
    out = []
    in_list = False
    
    def esc(s):
        return html.escape(s)
        
    def inline_fmt(s):
        s = esc(s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        return s

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### '):
            if in_list: out.append('</ul>'); in_list = False
            out.append(f'<h3>{esc(line[4:])}</h3>')
        elif stripped.startswith('## '):
            if in_list: out.append('</ul>'); in_list = False
            out.append(f'<h2>{esc(line[3:])}</h2>')
        elif stripped.startswith('# '):
            if in_list: out.append('</ul>'); in_list = False
            out.append(f'<h1>{esc(line[2:])}</h1>')
        elif re.match(r'^-{3,}$', stripped):
            if in_list: out.append('</ul>'); in_list = False
            out.append('<hr>')
        elif stripped.startswith('- '):
            if not in_list: out.append('<ul>'); in_list = True
            out.append(f'<li>{inline_fmt(line[2:])}</li>')
        elif stripped == '':
            if in_list: out.append('</ul>'); in_list = False
            out.append('<br>')
        else:
            if in_list: out.append('</ul>'); in_list = False
            out.append(f'<p>{inline_fmt(line)}</p>')
            
    if in_list:
        out.append('</ul>')
        
    return '\n'.join(out)


def create_html_wrapper(title, body_html, accent_color="#22c55e"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{html.escape(title)}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: {accent_color};
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding-top: 70px;
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
        .container {{ max-width: 900px; margin: 0 auto; padding: 1rem 0.5rem; overflow-x: hidden; }}
        .md-content {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.25rem;
            font-size: 0.95rem;
            overflow-wrap: break-word;
            word-break: break-word;
            line-height: 1.8;
            color: #e2e8f0;
        }}
        .md-content h1 {{ color: var(--accent); font-size: 1.6rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.4rem; margin-top: 1.5rem; }}
        .md-content h2 {{ color: var(--accent); font-size: 1.3rem; margin-top: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }}
        .md-content h3 {{ color: #93c5fd; font-size: 1.1rem; margin-top: 1.2rem; }}
        .md-content ul {{ padding-left: 1.5rem; margin: 0.5rem 0; }}
        .md-content li {{ margin: 0.3rem 0; }}
        .md-content strong {{ color: #f8fafc; font-weight: 700; }}
        .md-content hr {{ border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }}
        .md-content code {{ background: #0f172a; padding: 0.1rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <div style="max-width: 950px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <h1 style="font-size: 0.95rem; margin: 0; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 75%; color: var(--accent);">{html.escape(title)}</h1>
            <a href="../index.html" onclick="if(window.history.length>1){{window.history.back();return false;}}else{{location.href='../index.html';return false;}}" style="font-size: 0.85rem; white-space: nowrap; color: var(--accent); text-decoration: none; font-weight: 600;">← Back</a>
        </div>
    </div>
    
    <div class="container">
        <div class="md-content">
            {body_html}
        </div>
    </div>

    <script>
        (function() {{
            let lastScrollTop = 0;
            window.addEventListener("scroll", function() {{
                let st = window.pageYOffset || document.documentElement.scrollTop;
                let header = document.querySelector(".header");
                if (header) {{
                    if (st > lastScrollTop && st > 60) {{
                        header.style.transform = "translateY(-100%)";
                    }} else {{
                        header.style.transform = "translateY(0)";
                    }}
                }}
                lastScrollTop = st <= 0 ? 0 : st;
            }});
        }})();
    </script>
</body>
</html>
"""

directories = [
    ('content', '#38bdf8'),
    ('backpacking_guide', '#22c55e'),
    ('natgeo_collection', '#f59e0b'),
    ('regional_collection', '#0369a1')
]

for d, accent in directories:
    texts_dir = os.path.join(d, 'texts')
    if not os.path.exists(texts_dir):
        continue
        
    for file in os.listdir(texts_dir):
        if file.endswith('.txt') and not file.endswith('_raw.txt'):
            txt_path = os.path.join(texts_dir, file)
            base_name = os.path.splitext(file)[0]
            html_path = os.path.join(texts_dir, f"{base_name}.html")
            
            with open(txt_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                
            # Determine title from first line or filename
            first_line = raw_text.strip().split('\n')[0]
            if first_line.startswith('# '):
                doc_title = first_line[2:].strip()
            else:
                doc_title = base_name.replace('_', ' ').replace('-', ' ').title()
                
            body_html = md_to_html(raw_text)
            full_html = create_html_wrapper(doc_title, body_html, accent)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
                
            print(f"Generated static HTML for {html_path}")

# Now update all index.html files so links point to .html instead of .txt!
for d, _ in directories:
    index_path = os.path.join(d, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace links from .txt to .html
        new_content = re.sub(r'texts/([^"\']+\.txt)', r'texts/\1.html', content)
        new_content = new_content.replace('.txt.html', '.html')
        
        if new_content != content:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated index links in {index_path}")

print("Static HTML generation complete for all text files.")
