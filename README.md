# Southern Appalachian Offline ZIM Suite & Project `fen`

An offline digital archive, regional master collection, and mobile AI RAG system for the Great Smoky Mountains National Park (GSMNP), Pisgah, Nantahala, Shenandoah National Park, Blue Ridge Parkway, and DuPont State Recreational Forest.

---

## 📦 Downloadable ZIM Archives

All compiled `.zim` files are located in the [`zim_downloads/`](./zim_downloads/) directory:

| Archive File | Description | Size | Key Topics |
| :--- | :--- | :--- | :--- |
| **`Southern_Appalachian_Regional_Master.zim`** | **Expanded Regional Master** | 41.8 KB | Pisgah National Forest (Linville Gorge, Looking Glass Rock), Nantahala (Nantahala Gorge, Joyce Kilmer Old Growth), Shenandoah (Skyline Drive, Old Rag), Blue Ridge Parkway (Mt. Mitchell, Grandfather Mountain). |
| **`Appalachian_Corridor.zim`** | **Main History & Literature** | 1.67 MB | GSMNP Creation, Elkmont & Cades Cove History, Cherokee Nation Treaties & Mythology, Biltmore Scientific Forestry, Horace Kephart's *Our Southern Highlanders*. |
| **`National_Geographic_Appalachian_Collection.zim`** | **NatGeo Magazine Collection** | 840 KB | Real archived volumes & full DJVU texts from Internet Archive (1889-1954) covering Appalachian expeditions, park establishment, and natural history. |
| **`GSMNP_Backpacking_Field_Guide.zim`** | **Backpacking Field Manual** | 41.6 KB | AT Shelters & Backcountry Campsites, Spring Reliability Notes, Elevation Profiles, Weather Lapse Rates, Emergency Radio Frequencies, Bear Cables, Edible/Toxic Flora, Firefly Ecotourism. |

---

## 📱 Project `fen` (iOS LM Studio-Style Local VLM & ZIM RAG App)

Located in [`fen_app/`](./fen_app/):

### Core Architecture
* **On-Device Multimodal Inference**: Powered by `llama.cpp` + Metal GPU acceleration for GGUF VLM models (e.g. Qwen2.5-VL / MiniCPM-V).
* **Local Vector RAG Engine**: Indexes ZIM files via `sqlite-vec` / `ObjectBox` vector embeddings for offline semantically-ranked context retrieval.
* **Kiwix Hotspot Bridge**: Connects over local Wi-Fi to active Kiwix Hotspot REST endpoints (`http://kiwix.local:8080/api/v1/search`) or reads `.zim` files directly from iOS Files / SD card adapters.
* **SwiftUI Reader UI**: Clean, high-contrast, non-glass layout featuring font-size selection (**S**, **M**, **L**, **XL**), fluid scroll position saving (`localStorage`), and scroll locking.

### Quick Start (Python Prototype)
```bash
python fen_core.py
```

---

## 🏗️ 2-Step Scraping & ZIM Build Pipeline

### 1. Expanded Regional Master
```bash
python scrape_appalachia_regional.py
python build_appalachia_regional_zim.py
```

### 2. Main Appalachian Corridor Archive
```bash
python scrape.py
python build_zim.py
```

### 3. National Geographic Magazine Collection
```bash
python scrape_natgeo.py
python build_natgeo_zim.py
```

### 4. GSMNP Backpacking Field Guide
```bash
python scrape_backpacking.py
python build_backpacking_zim.py
```

---

## 💻 Requirements

- **Python 3.8+**
- **`libzim`** (`pip install libzim`)
- **iOS 16.0+ / Xcode 15+** (for building `fen_app/`)
