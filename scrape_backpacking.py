import os
import json

backpacking_dir = "backpacking_guide"
os.makedirs(f"{backpacking_dir}/texts", exist_ok=True)
os.makedirs(f"{backpacking_dir}/pdfs", exist_ok=True)

guides = [
    {
        'id': 'shelter_directory',
        'title': 'Exhaustive GSMNP Backcountry Shelter & Campsite Directory',
        'category': 'Campsites',
        'content': """# Exhaustive GSMNP Backcountry Shelter & Campsite Directory

## 1. Appalachian Trail Backcountry Shelters (South to North)

### Fontana Hilton / Fontana Dam Shelter (Elevation: 1,720 ft)
- **AT Mile**: 165.2 (From Springer Mountain)
- **Capacity**: 24 Hikers (Multi-level wooden structure)
- **Water Source**: Solar-powered water spigot & fountain nearby.
- **Amenities**: Solar cell phone charging station, hot showers at nearby Fontana marina, privy, bear cables.
- **Notes**: Premier starting point for northbound GSMNP AT thru-hikes. Permit registration kiosk located at Fontana Dam.

### Mollies Ridge Shelter (Elevation: 4,560 ft)
- **AT Mile**: 177.3
- **Capacity**: 12 Hikers
- **Water Source**: Spring located 0.2 miles down blue-blazed side trail to the west. Moderate autumn flow.
- **Bear Cables**: Mandatory bear cable system present.
- **Notes**: High ridge position between Doe Knob and Ekaneetlee Gap.

### Russell Field Shelter (Elevation: 4,340 ft)
- **AT Mile**: 183.3
- **Capacity**: 12 Hikers
- **Water Source**: Reliable spring 150 yards down side trail.
- **Bear Cables**: Yes.
- **Notes**: Popular stopover before climbing Thunderhead Mountain. Nearby grassy field provides birdwatching opportunities.

### Spence Field Shelter (Elevation: 4,900 ft)
- **AT Mile**: 186.2
- **Capacity**: 12 Hikers
- **Water Source**: Pipe spring 0.1 miles down south side trail. High reliability year-round.
- **Bear Cables**: Yes.
- **Notes**: Located near junction with Bote Mountain Trail. High exposure to gusty winds across Spence Field bald.

### Silers Bald Shelter (Elevation: 5,420 ft)
- **AT Mile**: 199.7
- **Capacity**: 12 Hikers
- **Water Source**: Spring located 0.1 miles down steep north side trail.
- **Bear Cables**: Yes.
- **Notes**: High altitude site. Cold temperatures persist into late spring. Close to Silers Bald summit (5,607 ft).

### Mount Collins Shelter (Elevation: 5,900 ft)
- **AT Mile**: 209.4
- **Capacity**: 12 Hikers
- **Water Source**: Spring 0.2 miles down Sugarland Mountain Trail junction.
- **Bear Cables**: Yes.
- **Notes**: Dense spruce-fir forest setting. Located 4 miles east of Kuwohi / Clingmans Dome.

### Icewater Spring Shelter (Elevation: 5,920 ft)
- **AT Mile**: 216.7
- **Capacity**: 12 Hikers
- **Water Source**: Famous pipe spring flowing directly out of rock wall 100 ft south of shelter. Extremely reliable year-round.
- **Bear Cables**: Yes. Includes composting privy.
- **Notes**: Most popular shelter in the park. High-volume ridge views of the Oconaluftee valley.

### Peck Corner Shelter (Elevation: 5,300 ft)
- **AT Mile**: 227.1
- **Capacity**: 12 Hikers
- **Water Source**: Spring 0.1 miles down side trail.
- **Bear Cables**: Yes.
- **Notes**: Located 0.4 miles off the AT along Peck Corner side trail. Quieter than Icewater Spring.

### Tri-Corner Knob Shelter (Elevation: 5,940 ft)
- **AT Mile**: 232.3
- **Capacity**: 12 Hikers
- **Water Source**: Spring 75 yards in front of shelter.
- **Bear Cables**: Yes.
- **Notes**: Most remote shelter in GSMNP. Junction point of Mount Sterling Ridge and main AT crest.

### Cosby Knob Shelter (Elevation: 4,770 ft)
- **AT Mile**: 239.8
- **Capacity**: 12 Hikers
- **Water Source**: Excellent high-volume spring 50 ft from shelter entrance.
- **Bear Cables**: Yes.
- **Notes**: Located at base of Mount Cammerer spur trail.

### Davenport Gap Shelter (Elevation: 2,600 ft)
- **AT Mile**: 247.5
- **Capacity**: 12 Hikers
- **Water Source**: Stream 100 yards south.
- **Bear Cables**: Yes. Features chain-link bear fence enclosure.
- **Notes**: Final AT shelter inside GSMNP boundary before crossing Big Creek into North Carolina.

---

## 2. Key Backcountry Campsites

- **Campsite 18 (West Prong)**: 2.1 miles from Laurel Falls trailhead. Stream water from West Prong of Little River.
- **Campsite 24 (Rough Fork - Cataloochee)**: Deep hemlock grove near historic Cataloochee Valley elk habitats.
- **Campsite 30 (Three Forks - Hazel Creek)**: Remote wilderness site requiring multi-day hike or boat shuttle across Fontana Lake.
- **Campsite 37 (Big Creek)**: Located along Big Creek trail. Features massive boulders and deep swimming holes.
- **Campsite 71 (Noland Creek)**: Spacious hardwood cove site near historic Noland estate ruins.
"""
    },
    {
        'id': 'trail_profiles',
        'title': 'Comprehensive Appalachian Trail & Regional Trail Profiles',
        'category': 'Trails',
        'content': """# Comprehensive Appalachian Trail & Regional Trail Profiles

## 1. AT GSMNP Crest Traverse (71.4 Total Miles)

### Waypoint & Elevation Breakdown
| Trail Segment | Distance (mi) | Elev Gain / Loss | Key Waypoints & Features |
| :--- | :--- | :--- | :--- |
| **Fontana Dam to Mollies Ridge** | 12.1 mi | +3,400 ft / -600 ft | Shuckstack Fire Tower (4,020 ft), Ekaneetlee Gap |
| **Mollies Ridge to Spence Field** | 8.9 mi | +1,800 ft / -1,460 ft | Rocky Top (5,447 ft), Thunderhead Mountain |
| **Spence Field to Silers Bald** | 13.5 mi | +2,100 ft / -1,580 ft | Bote Mountain Junction, Derrick Knob Shelter |
| **Silers Bald to Clingmans Dome** | 4.8 mi | +1,223 ft / -180 ft | Kuwohi / Clingmans Dome Summit (6,643 ft) |
| **Clingmans Dome to Newfound Gap** | 7.9 mi | -1,600 ft / +400 ft | Mount Collins Junction, Road Prong Trailhead |
| **Newfound Gap to Icewater Spring**| 3.0 mi | +900 ft / -100 ft | Sweat Heifer Trail Junction, Boulevard Trail Head |
| **Icewater Spring to Tri-Corner** | 15.6 mi | +2,400 ft / -2,380 ft | Charlies Bunion (5,375 ft), Sawtooth Ridges |
| **Tri-Corner to Davenport Gap** | 15.2 mi | -3,400 ft / +800 ft | Mount Cammerer Spur, Big Creek Crossing |

---

## 2. Signature Day & Multi-Day Trails

### Alum Cave Trail to Mount LeConte
- **Distance**: 11.0 miles round trip (+2,760 ft elevation gain).
- **Waypoints**:
  - **Arch Rock (1.4 mi)**: Natural stone arch carved by freezing and thawing.
  - **Inspiration Point (2.0 mi)**: Panoramic vista of Duckhawk Ridge and Myrtle Point.
  - **Alum Cave Bluff (2.3 mi)**: 80-foot high concave cliff face with mineral deposits.
  - **LeConte Lodge / Cliff Tops (5.5 mi)**: Summit plateau (6,593 ft) with sunset vistas.

### Mount Cammerer Fire Tower Trail
- **Distance**: 11.1 miles round trip (+3,045 ft elevation gain).
- **Features**: Octagonal stone fire lookout tower built by the Civilian Conservation Corps (CCC) in 1937. Provides a 360-degree view of the Pigeon River Gorge and Snowbird Mountains.

### Gregory Bald Trail (Azalea Bloom Peak)
- **Distance**: 11.3 miles round trip (+3,020 ft gain).
- **Features**: Famous 10-acre high mountain bald providing world-renowned flame azalea blooms in mid-to-late June.
"""
    },
    {
        'id': 'emergency_weather',
        'title': 'High-Altitude Emergency Protocols, Radio Frequencies & Weather',
        'category': 'Safety',
        'content': """# High-Altitude Emergency Protocols, Radio Frequencies & Weather

## 1. Temperature Lapse Rates & Wind Chill Hazards
- **Environmental Lapse Rate**: Expect a temperature drop of **3.5°F to 5.5°F per 1,000 feet of elevation gain**.
- **Valley vs. Summit Examples**:
  - Gatlinburg (1,289 ft): 75°F sunny
  - Clingmans Dome / Kuwohi (6,643 ft): 48°F with gusty winds and cloud fog.
- **Wind Chill Risk**: Wind speeds exceeding 35 mph on exposed bluffs (Charlies Bunion, Rocky Top) can drop effective feel to sub-freezing even in early autumn.

---

## 2. Emergency Radio Frequencies & Communications
- **NOAA Weather Radio Frequencies (Southern Appalachians)**:
  - **162.550 MHz (WX1)**: Sevier County / East Tennessee transmitter.
  - **162.400 MHz (WX2)**: Asheville / Western North Carolina transmitter.
  - **162.475 MHz (WX3)**: Waynesville / Haywood County.
- **GSMNP Park Dispatch (Emergency Only)**: (865) 436-1294.
- **Cell Service Heatmap**: Cell signals hit reliably along open ridge gaps facing cities (Newfound Gap, Charlies Bunion, Mount Cammerer), but are completely dead in deep stream coves (Hazel Creek, Cataloochee, Greenbrier).

---

## 3. High-Altitude Lightning & Severe Weather Protocols
- **Lightning Exposure Zones**: Silers Bald, Thunderhead Mountain, Charlies Bunion, Mount Cammerer tower.
- **Protocol**: If thunder sounds, immediately descend at least 300 vertical feet off the ridge line into dense timber. Do NOT seek shelter under isolated trees or rock overhangs.
"""
    },
    {
        'id': 'bear_flora_guide',
        'title': 'Black Bear Safety, Stream Crossings & Native Flora Manual',
        'category': 'Flora/Fauna',
        'content': """# Black Bear Safety, Stream Crossings & Native Flora Manual

## 1. Black Bear Encounter & Cable Operations
- **Mandatory Food Storage**: All food, trash, lip balm, toothpaste, and scented items MUST be elevated on park bear cables.
- **Bear Cable Rigging**:
  1. Attach dry bag to carabiner on cable wire.
  2. Pull control cable to hoist bag 15+ feet off the ground.
  3. Secure control cable loop around anchor post.
- **Encounter Guidelines**:
  - Never run. Running triggers predatory chase instinct.
  - Stand tall, hold arms overhead, group together, speak firmly.
  - If a bear approaches within 50 feet, yell loudly and throw rocks.

---

## 2. Edible vs. Toxic Flora Field Manual

### Edible Plants
- **Ramps (Wild Leeks - *Allium tricoccum*)**: Broad green leaves with garlic/onion aroma found in rich hardwood coves in spring.
- **Wild Blackberries & Wineberries**: Ripe mid-summer along sunny trail gaps and former homestead clearings.
- **Wood Sorrel (*Oxalis*)**: Three heart-shaped leaflets with sour lemony flavor.

### Toxic & Dangerous Plants
- **Poison Hemlock (*Conium maculatum*)**: Smooth hollow stem with distinctive purple spots. Highly fatal if ingested.
- **Stinging Nettle (*Urtica dioica*)**: Serrated leaves covered in tiny silica stinging hairs. Causes severe burning sensation.
- **White Snakeroot (*Ageratina altissima*)**: Contains tremetol toxin. Caused historic "Milk Sickness" in pioneers.
"""
    },
    {
        'id': 'firefly_ecotourism',
        'title': 'Firefly Ecotourism Peak Windows & Wildlife Waypoints',
        'category': 'Ecotourism',
        'content': """# Firefly Ecotourism Peak Windows & Wildlife Waypoints

## 1. Synchronous Fireflies (*Photinus carolinus*) - Elkmont
- **Location**: Little River Trail & Jakes Creek Trail near Elkmont, GSMNP.
- **Peak Window**: Late May to early June (2-week annual peak).
- **Flashing Sequence**: Males emit 6-8 synchronous flashes in total unison, followed by 6-8 seconds of dark silence.
- **Viewing Rules**: Red cellophane covers over all flashlights to protect insect mating displays.

---

## 2. Blue Ghost Fireflies (*Phausis reticulata*) - DuPont & Pisgah
- **Location**: DuPont State Forest & Transylvania County hardwood coves.
- **Peak Window**: Mid-May to early June.
- **Flashing Behavior**: Emits a constant, ghostly blue-green light while hovering 1-2 feet above moist leaf litter.
"""
    }
]

downloaded_backpacking = []

print("Formatting GSMNP & DuPont Backpacking Field Manual into styled HTML article readers...")
for g in guides:
    txt_filepath = f"{backpacking_dir}/texts/{g['id']}.txt"
    html_filepath = f"{backpacking_dir}/texts/{g['id']}.html"
    
    with open(txt_filepath, 'w', encoding='utf-8') as f:
        f.write(g['content'])

    article_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{g['title']}</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --accent: #22c55e;
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
            padding: 1.25rem 1.5rem;
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
        h1 {{ font-size: 1.2rem; margin: 0; color: var(--accent); }}
        .meta {{ color: var(--text-muted); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
        .md-content {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2rem;
            font-size: 1rem;
            line-height: 1.8;
            color: #e2e8f0;
        }}
        .md-content h1 {{ color: var(--accent); font-size: 1.6rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.4rem; margin-top: 2rem; }}
        .md-content h2 {{ color: var(--accent); font-size: 1.3rem; margin-top: 1.8rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }}
        .md-content h3 {{ color: #93c5fd; font-size: 1.1rem; margin-top: 1.4rem; }}
        .md-content ul {{ padding-left: 1.5rem; margin: 0.5rem 0; }}
        .md-content li {{ margin: 0.3rem 0; }}
        .md-content strong {{ color: #f8fafc; font-weight: 700; }}
        .md-content hr {{ border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }}
        .md-content code {{ background: #0f172a; padding: 0.1rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em; }}
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
                <div class="meta">Category: {g['category']}</div>
                <h1>{g['title']}</h1>
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
        <div class="md-content" id="mdContent">Loading field manual...</div>
    </div>

    <script>
        function setFontSize(size) {{
            document.documentElement.style.setProperty('--font-size', size);
            localStorage.setItem('field_doc_font_size', size);
        }}
        const savedSize = localStorage.getItem('field_doc_font_size');
        if (savedSize) setFontSize(savedSize);

        function renderMarkdown(md) {{
            const lines = md.split('\n');
            let html = '';
            let inList = false;
            for (let i = 0; i < lines.length; i++) {{
                let line = lines[i];
                // Headings
                if (line.startsWith('### ')) {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<h3>' + esc(line.slice(4)) + '</h3>';
                }} else if (line.startsWith('## ')) {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<h2>' + esc(line.slice(3)) + '</h2>';
                }} else if (line.startsWith('# ')) {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<h1>' + esc(line.slice(2)) + '</h1>';
                // Horizontal rule
                }} else if (line.match(/^-{{3,}}$/)) {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<hr>';
                // Bullet list
                }} else if (line.startsWith('- ')) {{
                    if (!inList) {{ html += '<ul>'; inList = true; }}
                    html += '<li>' + inlineFmt(line.slice(2)) + '</li>';
                // Blank line
                }} else if (line.trim() === '') {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<br>';
                }} else {{
                    if (inList) {{ html += '</ul>'; inList = false; }}
                    html += '<p>' + inlineFmt(line) + '</p>';
                }}
            }}
            if (inList) html += '</ul>';
            return html;
        }}
        function esc(s) {{ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }}
        function inlineFmt(s) {{
            s = esc(s);
            s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
            return s;
        }}
        fetch('{g["id"]}.txt')
            .then(res => res.text())
            .then(text => {{ document.getElementById('mdContent').innerHTML = renderMarkdown(text); }})
            .catch(() => {{ document.getElementById('mdContent').textContent = "{g['title']}"; }});
    </script>
</body>
</html>
"""
    with open(html_filepath, 'w', encoding='utf-8') as hf:
        hf.write(article_html)

    downloaded_backpacking.append({
        'id': g['id'],
        'title': g['title'],
        'category': g['category'],
        'path': f"texts/{g['id']}.html",
        'type': 'Markdown',
        'local': txt_filepath,
        'content': g['content']
    })

search_json = json.dumps(downloaded_backpacking)

# Unified Dark Theme Index for Backpacking Field Guide
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>GSMNP & DuPont Backpacking Field Manual</title>
    <style>
        :root {{
            --bg: #0f172a;
            --header-bg: #1e293b;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #22c55e;
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

        header h1 {{ color: var(--accent); margin: 0 0 0.5rem 0; font-size: 1.9rem; }}
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

        .search-bar:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2); }}

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

        .card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}

        .card-title {{ font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem; }}

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

        .badge {{ background: #dcfce7; color: #15803d; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700; font-size: 0.75rem; }}
    </style>
</head>
<body>
    <header>
        <h1>GSMNP & DUPONT BACKPACKING FIELD MANUAL</h1>
        <p>Offline Shelter Database, Elevation Profiles, Weather & Field Safety</p>
    </header>

    <div class="container">
        <section class="controls">
            <div class="control-row">
                <input type="text" id="searchInput" class="search-bar" placeholder="Search shelters, trail mileages, water sources, bear safety...">
            </div>

            <div class="filter-tabs" id="filterTabs">
                <div class="tab active" data-category="ALL">All Guides</div>
                <div class="tab" data-category="Campsites">Shelters & Water</div>
                <div class="tab" data-category="Trails">Trail Profiles</div>
                <div class="tab" data-category="Safety">Weather & Emergency</div>
                <div class="tab" data-category="Flora/Fauna">Bears & Flora</div>
                <div class="tab" data-category="Ecotourism">Firefly Guides</div>
            </div>
        </section>

        <main class="grid" id="cardGrid"></main>
    </div>

    <script>
        const articles = {search_json};
        const searchInput = document.getElementById('searchInput');
        const tabs = document.querySelectorAll('.tab');
        const cardGrid = document.getElementById('cardGrid');

        let currentCategory = 'ALL';
        let searchQuery = '';

        function renderArticles() {{
            cardGrid.innerHTML = '';
            articles.forEach(item => {{
                const matchesCategory = (currentCategory === 'ALL' || item.category === currentCategory);
                let matchesSearch = !searchQuery || item.title.toLowerCase().includes(searchQuery) || (item.content && item.content.toLowerCase().includes(searchQuery));

                if (matchesSearch && matchesCategory) {{
                    const card = document.createElement('a');
                    card.className = 'card';
                    card.href = item.path;
                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            <div style="margin-top: 0.75rem; color: var(--accent); font-weight: 700; font-size: 0.9rem;">
                                📋 Read Field Manual →
                            </div>
                        </div>
                        <div class="card-meta">
                            <span>Category: ${{item.category}}</span>
                            <span class="badge">${{item.type}}</span>
                        </div>
                    `;
                    cardGrid.appendChild(card);
                }}
            }});
        }}

        searchInput.addEventListener('input', (e) => {{ searchQuery = e.target.value.toLowerCase().trim(); renderArticles(); }});
        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentCategory = tab.getAttribute('data-category');
                renderArticles();
            }});
        }});
        renderArticles();
    </script>
</body>
</html>
"""

with open(f"{backpacking_dir}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Exhaustive backpacking field manual generation complete.")
