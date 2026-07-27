# Southern Appalachian Offline ZIM Suite

An offline digital archive and backpacking field manual for the Great Smoky Mountains National Park (GSMNP), DuPont State Recreational Forest, and the Southern Appalachian corridor.

Designed for seamless offline use in mobile ZIM readers (such as [Kiwix](https://www.kiwix.org/)) with custom reader controls and viewport optimizations for mobile and tablet devices.

---

## 📦 Downloadable ZIM Archives

All compiled `.zim` files are located in the [`zim_downloads/`](./zim_downloads/) directory:

| Archive File | Description | Size | Key Topics |
| :--- | :--- | :--- | :--- |
| **`Appalachian_Corridor.zim`** | **Main History & Literature Collection** | 1.67 MB | GSMNP Creation, Elkmont & Cades Cove History, Cherokee Nation Treaties & Mythology, Biltmore Scientific Forestry, Horace Kephart's *Our Southern Highlanders*. |
| **`National_Geographic_Appalachian_Collection.zim`** | **National Geographic Magazine Collection** | 840 KB | Real archived volumes & full DJVU texts from Internet Archive (1889-1954) covering Appalachian expeditions, park establishment, and natural history. |
| **`GSMNP_Backpacking_Field_Guide.zim`** | **Wilderness Backpacking Field Guide** | 41.6 KB | AT Shelters & Backcountry Campsites, Spring Reliability Notes, Elevation Profiles, Weather Lapse Rates, Emergency Radio Frequencies, Bear Cables, Edible/Toxic Flora, Firefly Ecotourism (*Photinus carolinus* & *Phausis reticulata*). |

---

## ✨ Features & Capabilities

### 🔍 Full-Text Search Engine
* Every document's full body text is indexed.
* Real-time search matching with dynamic `<mark>` highlighted text snippets.
* Includes a toggle (`[x] Full-Text Search`) to switch between title matching and full-body content search.

### 📱 Responsive Device Viewports
Explicitly formatted for iOS and mobile/tablet devices in both Portrait and Landscape orientations:
* **iPhone 15 Pro** (393px × 852px)
* **iPhone 15 Pro Max** (430px × 932px)
* **iPad Mini (6th Gen)** (744px × 1133px)
* Includes native iOS safe-area handling (`env(safe-area-inset-*)`).

### 🛠️ Reader Controls & Accessibility
* **Font Size Choice**: Select between **S** (14px), **M** (16px), **L** (18px), and **XL** (20px) font sizes. Choices persist across sessions via `localStorage`.
* **Fluid Scroll & Location Saving**: Smooth fluid scrolling (`scroll-behavior: smooth`) with automatic scroll position saving in `localStorage`. Automatically restores your reading position upon returning to a page.
* **Scroll Lock**: Dedicated toggle button (`🔒 Scroll Lock`) to lock or unlock scrolling as needed.
* **Clean UI**: High-contrast, clean UI design built for maximum legibility in low-light wilderness conditions.

---

## 🏗️ Architecture & 2-Step Build Pipeline

Each collection uses a distinct two-step pipeline separating data extraction from ZIM packaging:

```
[ Step 1: Extractor Script ]  ---> Downloads text/metadata & builds index.html
[ Step 2: Builder Script   ]  ---> Uses libzim Python API to package into .zim file
```

### 1. Main Appalachian Corridor Archive
```bash
python scrape.py         # Step 1: Downloads Gutenberg/IA texts & builds index.html
python build_zim.py      # Step 2: Packages content/ into Appalachian_Corridor.zim
```

### 2. National Geographic Magazine Collection
```bash
python scrape_natgeo.py       # Step 1: Fetches IA DJVU texts & metadata
python build_natgeo_zim.py    # Step 2: Packages natgeo_collection/ into ZIM
```

### 3. GSMNP Backpacking Field Guide
```bash
python scrape_backpacking.py       # Step 1: Builds shelter & elevation guides
python build_backpacking_zim.py    # Step 2: Packages backpacking_guide/ into ZIM
```

---

## 💻 Requirements & Dependencies

- **Python 3.8+**
- **`libzim`** (`pip install libzim`)

---

## 📖 How to Use on Mobile / Offline Readers

1. Download any `.zim` file from the `zim_downloads/` folder to your device.
2. Open the file using **Kiwix** (available on iOS App Store, Google Play, macOS, and Windows).
3. Browse, search, filter, and read all Appalachian history, National Geographic volumes, and backpacking manuals offline without internet or cell reception!
