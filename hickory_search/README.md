# HICKORY SEARCH: Off-Grid Multi-ZIM RAG Engine for iOS

**Hickory Search** is a high-performance native iOS application and Python engine designed for **iPhone 15 Pro** and iPad Mini. It allows you to select any folder in your iOS **Files App** (or SD card / Kiwix hotspot) containing **40+ `.zim` archives** and custom `.gguf` AI models, executing complex nested-loop research queries in **under 5 minutes**.

---

## 🌟 Key Features

1. **Multi-ZIM Parallel Retrieval**:
   - Automatically scans and indexes **40+ `.zim` archives** simultaneously.
   - Multithreaded search returns verified results in seconds.

2. **iOS Files App Security-Scoped Folder Selector**:
   - Uses native `UIDocumentPickerViewController` with security-scoped URL bookmarks.
   - Remembers folder location across app restarts without re-asking permission.

3. **Custom Local AI Model Loader**:
   - Supports loading custom `.gguf`, `.bin`, or Metal models (Llama-3-8B, Qwen2.5-7B, Phi-3, Mistral) directly from your SD card or iOS Files folder.
   - Leverages iPhone 15 Pro A17 Pro Metal Performance Shaders for fast on-device inference.

4. **Off-Grid Agent Nested-Loop Architecture**:
   - **Phase 1**: Planner breaks user query into 4-6 search terms.
   - **Phase 2**: Autonomous research loop across all 40+ ZIM files with early stopping when 8+ verified sources are gathered.
   - **Phase 3**: On-device AI synthesis returning cited responses under 5 minutes.

---

## 🚀 How to Run on iPhone 15 Pro (No Mac Required)

### Option A: Safari PWA / Local Web Server
1. Run `python build_zimit_ready_site.py` on your Windows PC.
2. Connect your iPhone to the same Wi-Fi / hotspot.
3. Open Safari, navigate to `http://<PC_IP>:8000/`.
4. Tap **Share** → **Add to Home Screen**.

### Option B: Sideloading via Sideloadly (Windows)
1. Open the [`hickory_search/HickorySearchApp/`](file:///c:/wikipedia/custom%20zim/hickory_search/HickorySearchApp/) folder.
2. Plug your iPhone 15 Pro into your Windows PC.
3. Drag the app build into **Sideloadly** or **AltStore**.
4. Trust your developer profile under **Settings → General → VPN & Device Management** on your iPhone.
