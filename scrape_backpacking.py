import os
import json

backpacking_dir = "backpacking_guide"
os.makedirs(f"{backpacking_dir}/texts", exist_ok=True)
os.makedirs(f"{backpacking_dir}/pdfs", exist_ok=True)

guides = [
    {
        'id': 'shelter_directory',
        'title': 'GSMNP Backcountry Shelter & Campsite Directory',
        'category': 'Campsites',
        'content': """# GSMNP Backcountry Shelter & Campsite Directory

## Key AT Shelters & Water Source Reliability
1. **Icewater Spring Shelter** (Elevation: 5,920 ft)
   - Capacity: 12 hikers.
   - Bear Cables: Yes (Mandatory food hanging).
   - Water Source: Pipe spring 100 ft south of shelter. Extremely reliable year-round.
2. **Mount LeConte Shelter** (Elevation: 6,400 ft)
   - Capacity: 12 hikers (Permit required).
   - Bear Cables: Yes.
   - Water Source: Spring near lodge trail junction. Can slow to a drip in late October.
3. **Spence Field Shelter** (Elevation: 4,900 ft)
   - Capacity: 12 hikers.
   - Bear Cables: Yes.
   - Water Source: Spring down trail 0.1 miles. Reliable spring and summer; moderate autumn flow.
4. **Mollies Ridge Shelter** (Elevation: 4,560 ft)
   - Capacity: 12 hikers.
   - Bear Cables: Yes.
   - Water Source: Spring 0.2 miles down blue-blazed side trail.

## Backcountry Campsites (Cades Cove & Little River Region)
- **Campsite 18 (West Prong)**: Easy 2.1 mile hike in. Good water source from Little River.
- **Campsite 24 (Rough Fork)**: Deep forest site along Cataloochee area.
- **Campsite 30 (Three Forks)**: High elevation stream access near Hazel Creek.
"""
    },
    {
        'id': 'trail_profiles',
        'title': 'Appalachian Trail & Segment Elevation Profiles',
        'category': 'Trails',
        'content': """# Appalachian Trail & Regional Segment Elevation Profiles

## 1. Appalachian Trail (GSMNP Section: 71 Miles)
- **Fontana Dam to Davenport Gap**
- Total Elevation Gain: ~18,000 ft ascent / ~17,000 ft descent.
- Highest Point: Kuwohi / Clingmans Dome (6,643 ft).
- Key Segment Distances:
  - Fontana Dam to Spence Field Shelter: 16.4 miles (+4,100 ft)
  - Spence Field to Silers Bald Shelter: 14.1 miles
  - Silers Bald to Clingmans Dome: 4.8 miles (+1,700 ft)
  - Clingmans Dome to Newfound Gap: 7.9 miles (-1,600 ft)
  - Newfound Gap to Icewater Spring: 3.0 miles (+900 ft)
  - Icewater Spring to Tri-Corner Knob: 12.7 miles
  - Tri-Corner Knob to Davenport Gap: 12.1 miles (-3,900 ft)

## 2. Alum Cave & Boulevard Trails to Mt. LeConte
- **Alum Cave Trail**: 5.5 miles one way (+2,760 ft gain). Features Arch Rock, Inspiration Point, Alum Cave Bluff.
- **The Boulevard Trail**: 5.4 miles one way from AT junction (+1,500 ft aggregate gain along crest).

## 3. DuPont State Forest Trail Network
- **Triple Falls to High Falls Loop**: 2.2 miles, gentle 350 ft elevation gain.
- **Bridal Veil Falls Trail**: 4.4 miles round trip, 400 ft gain.
"""
    },
    {
        'id': 'emergency_weather',
        'title': 'High-Altitude Emergency & Weather Protocols',
        'category': 'Safety',
        'content': """# High-Altitude Emergency & Weather Protocols

## Temperature & Altitude Calculations
- **Lapse Rate**: Expect a **3.5°F to 5.5°F drop in temperature per 1,000 feet of elevation gain**.
- **Clingmans Dome vs. Gatlinburg**: Clingmans Dome (6,643 ft) is routinely 15°F to 22°F colder than Gatlinburg (1,289 ft). High winds on ridges produce severe wind chill.
- **Hypothermia Warning**: Wet clothing combined with 45°F temperatures and wind is the #1 cause of backcountry hypothermia in spring and fall.

## Emergency Contacts & Offline Radio Frequencies
- **GSMNP Emergency Dispatch**: (865) 436-1294 (Cell service unreliable on trails; SMS sometimes transmits on ridges).
- **NOAA Weather Radio Frequencies (Southern Appalachians)**:
  - 162.550 MHz (WX1 - Knoxville/Sevier County)
  - 162.400 MHz (WX2 - Asheville/WNC)
- **Ranger Stations**:
  - Sugarlands Visitor Center / Backcountry Office: (865) 436-1297
  - Oconaluftee Visitor Center: (828) 497-1904
"""
    },
    {
        'id': 'bear_flora_guide',
        'title': 'Black Bear Safety & Native Flora Field Manual',
        'category': 'Flora/Fauna',
        'content': """# Black Bear Safety & Native Flora Field Manual

## Black Bear Encounter & Cable Protocols
- **Food Storage**: All food, trash, toothpaste, and scented items MUST be hung on park-provided bear cable systems at every backcountry campsite and shelter.
- **Cable Operation**: Clip dry bag to carabiner -> Hoist cable to top pulley -> Secure loop on anchor post.
- **Encounter Guidelines**:
  - Do NOT run.
  - Stand tall, raise arms, speak in a loud, firm voice.
  - Back away slowly.
  - If a bear approaches aggressively, make loud noises and throw objects.

## Native Flora: Edible vs Toxic Species
- **Edible**:
  - **Ramps (Wild Leeks)**: Broad green leaves with onion/garlic aroma in rich hardwood coves.
  - **Blackberries & Wineberries**: Ripe in mid-to-late summer along sunny trail gaps.
- **Toxic / Dangerous**:
  - **Poison Hemlock**: Smooth green stem with purple spots. Extremely toxic.
  - **Stinging Nettle**: Serrated leaves with fine stinging hairs along lower moist trails.
  - **Poison Ivy**: "Leaves of three, let it be." Abundant in lower elevation river coves.
"""
    },
    {
        'id': 'firefly_ecotourism',
        'title': 'Firefly Ecotourism Peak Windows & Trail Waypoints',
        'category': 'Ecotourism',
        'content': """# Firefly Ecotourism Peak Windows & Trail Waypoints

## 1. Synchronous Fireflies (*Photinus carolinus*) - Elkmont
- **Location**: Little River & Jakes Creek Trailheads near Elkmont, GSMNP.
- **Peak Window**: Late May to early June (approx. 2-week window).
- **Behavior**: Thousands of male fireflies flash in near-perfect unison (6-8 flashes followed by 6-8 seconds of total darkness).
- **Best Viewing Time**: 9:30 PM to 11:00 PM.
- **Rules**: Red cellophane filters over all flashlights to protect insect mating cycles.

## 2. Blue Ghost Fireflies (*Phausis reticulata*) - DuPont Forest & Pisgah
- **Location**: DuPont State Recreational Forest & surrounding Transylvania/Henderson County woods.
- **Peak Window**: Mid-May to early June.
- **Behavior**: Emits a continuous, ghostly blue-green glow while hovering 1-2 feet above the moist forest floor.
- **Best Viewing Time**: 9:00 PM to 10:30 PM in dense, undisturbed leaf litter.
"""
    }
]

downloaded_backpacking = []

for g in guides:
    filepath = f"{backpacking_dir}/texts/{g['id']}.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(g['content'])
        
    downloaded_backpacking.append({
        'id': g['id'],
        'title': g['title'],
        'category': g['category'],
        'path': f"texts/{g['id']}.txt",
        'type': 'GUIDE',
        'local': filepath,
        'content': g['content']
    })

search_json = json.dumps(downloaded_backpacking)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>GSMNP & DuPont Backpacking Field Manual</title>
    <style>
        :root {{
            --bg-color: #f4f6f8;
            --card-bg: #ffffff;
            --primary-color: #15803d;
            --header-bg: #064e3b;
            --text-main: #0f172a;
            --text-muted: #475569;
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
            background-color: var(--header-bg);
            color: #ffffff;
            border-bottom: 4px solid var(--primary-color);
            padding: 2rem 1rem;
            text-align: center;
        }}

        header h1 {{
            color: #86efac;
            margin: 0 0 0.5rem 0;
            font-size: 1.9rem;
        }}

        header p {{
            color: #a7f3d0;
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
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
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
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(21, 128, 61, 0.2);
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
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
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
            border-left: 4px solid var(--primary-color);
            border-radius: 8px;
            padding: 1.25rem;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        }}

        .card-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--header-bg);
            margin-bottom: 0.5rem;
        }}

        .snippet {{
            font-size: 0.85rem;
            color: #475569;
            background: #f8fafc;
            padding: 0.5rem;
            border-radius: 4px;
            margin-top: 0.5rem;
            border-left: 3px solid var(--primary-color);
        }}

        .snippet mark {{
            background: #fef08a;
            color: #854d0e;
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
            background: #dcfce7;
            color: #15803d;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 700;
            font-size: 0.75rem;
        }}

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
        <h1>GSMNP & DUPONT BACKPACKING FIELD MANUAL</h1>
        <p>Offline Shelter Database, Elevation Profiles, Weather & Field Safety</p>
    </header>

    <div class="container">
        <section class="controls">
            <div class="control-row">
                <input type="text" id="searchInput" class="search-bar" placeholder="Search shelters, trail mileages, water sources, bear safety...">
                
                <div class="settings-bar">
                    <span>Font Size:</span>
                    <button class="btn" onclick="setFontSize('14px')">S</button>
                    <button class="btn active" id="btnMed" onclick="setFontSize('16px')">M</button>
                    <button class="btn" onclick="setFontSize('18px')">L</button>
                    <button class="btn" onclick="setFontSize('20px')">XL</button>
                </div>
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

        <main class="grid" id="cardGrid">
            <div class="no-results" id="noResults">No matching guides found.</div>
        </main>
    </div>

    <script>
        const articles = {search_json};

        const searchInput = document.getElementById('searchInput');
        const tabs = document.querySelectorAll('.tab');
        const cardGrid = document.getElementById('cardGrid');
        const noResults = document.getElementById('noResults');

        let currentCategory = 'ALL';
        let searchQuery = '';

        function setFontSize(size) {{
            document.documentElement.style.setProperty('--base-font-size', size);
            localStorage.setItem('backpack_font_size', size);
        }}

        const savedFontSize = localStorage.getItem('backpack_font_size');
        if (savedFontSize) {{ setFontSize(savedFontSize); }}

        window.addEventListener('scroll', () => {{
            localStorage.setItem('backpack_scroll_pos', window.scrollY);
        }});

        const savedScrollPos = localStorage.getItem('backpack_scroll_pos');
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

        function renderArticles() {{
            cardGrid.innerHTML = '';
            let visibleCount = 0;

            articles.forEach(item => {{
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
                    card.innerHTML = `
                        <div>
                            <div class="card-title">${{item.title}}</div>
                            ${{snippetHTML}}
                            <div style="margin-top: 0.75rem;">
                                <a href="${{item.path}}" style="color: var(--primary-color); font-weight: 700; font-size: 0.9rem; text-decoration: none;">📋 Read Field Guide →</a>
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

            if (visibleCount === 0) {{
                const noRes = document.createElement('div');
                noRes.className = 'no-results';
                noRes.style.display = 'block';
                noRes.textContent = 'No matching guides found.';
                cardGrid.appendChild(noRes);
            }}
        }}

        searchInput.addEventListener('input', (e) => {{
            searchQuery = e.target.value.toLowerCase().trim();
            renderArticles();
        }});

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

print("Backpacking scrape update complete.")
