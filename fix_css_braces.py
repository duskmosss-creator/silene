"""
Fix all unescaped single-brace CSS selectors in scrape_natgeo.py f-strings.
This version only fixes CSS selectors INSIDE f-string triple-quote blocks.
"""
import re

with open('scrape_natgeo.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We'll work on f-string blocks only. Split by f""" delimiters
# Strategy: find all f-string regions, then within those, fix CSS selector lines

# Find f-string regions: f"""..."""
# We look for the pattern: f"""....""" accounting for nested quotes
lines = content.split('\n')

# Track which lines are inside f-string blocks
in_fstring = False
fstring_lines = set()

for i, line in enumerate(lines):
    if not in_fstring:
        # Check if this line starts an f-string
        if 'f"""' in line:
            in_fstring = True
            fstring_lines.add(i)
    else:
        fstring_lines.add(i)
        if '"""' in line and not line.strip().startswith('#'):
            # End of f-string
            in_fstring = False

print(f"Found {len(fstring_lines)} lines inside f-strings")

# Now fix CSS selector lines that are inside f-strings
# Pattern: line that matches CSS selector with single { at end
# CSS selector: optional whitespace, then CSS selector chars, then space, then single {, then optional whitespace
css_selector_pattern = re.compile(
    r'^(\s+)([\w\.#,> ~\+\[:*\]\-\"\'@]+)\s*\{\s*$'
)

fixed_lines = list(lines)
changes = 0

for i, line in enumerate(lines):
    if i in fstring_lines:
        m = css_selector_pattern.match(line)
        if m:
            # Check it's not already {{ 
            if '{' in line and '{{' not in line:
                # Replace the single { with {{
                new_line = line.rstrip().rstrip('{').rstrip() + ' {'
                # Now we need to double the brace
                new_line = line.replace(' {', ' {{').replace('\t{', '\t{{')
                if new_line != line:
                    fixed_lines[i] = new_line
                    changes += 1
                    print(f"Fixed line {i+1}: {line.strip()[:60]}")

print(f"\nMade {changes} changes")

fixed = '\n'.join(fixed_lines)

# Verify syntax
try:
    compile(fixed, 'scrape_natgeo.py', 'exec')
    print("Syntax OK!")
    with open('scrape_natgeo.py', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("File written.")
except SyntaxError as e:
    print(f"Still SyntaxError at line {e.lineno}: {e.msg}")
    err_lines = fixed.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(err_lines), e.lineno + 3)
    for idx, ln in enumerate(err_lines[start:end], start + 1):
        marker = '>>>' if idx == e.lineno else '   '
        print(f"{marker} {idx}: {ln}")
