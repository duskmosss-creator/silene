import re

with open('scrape_natgeo.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Try to compile the file and get the real error
try:
    compile(content, 'scrape_natgeo.py', 'exec')
    print("No syntax errors found")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    # Print context around the error
    lines = content.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 3)
    for i, line in enumerate(lines[start:end], start + 1):
        marker = '>>>' if i == e.lineno else '   '
        print(f"{marker} {i}: {line}")
