# Project `fen` — Windows-to-iOS Guide (No Mac Required)

Since you are working from a **Windows PC** with an **iPhone** and **iPad Mini (6th Gen)**, you do **NOT** need a Mac or Xcode to use project `fen`!

Here are the 2 easiest, most secure methods to run `fen` on your iOS devices from Windows:

---

## 🌟 Method 1: Offline Progressive Web App (PWA) (Recommended & Easiest!)

You can run `fen` directly on your iPhone & iPad Mini via Safari as an installed Home Screen Web App:

1. **Run `fen_core.py` on your Windows PC**:
   On your Windows laptop, start the local RAG & Kiwix server:
   ```cmd
   python fen_core.py
   ```
   This hosts the local VLM & ZIM RAG server on your local Wi-Fi network.

2. **Open on iPhone / iPad Mini**:
   - Connect your iPhone/iPad to the same Wi-Fi network as your Windows PC.
   - Open **Safari** on your iPhone/iPad and navigate to your Windows PC's local IP address (e.g. `http://192.168.1.50:8080`).

3. **Install to Home Screen**:
   - In Safari, tap the **Share button** (square with up arrow).
   - Scroll down and tap **Add to Home Screen**.
   - `fen` will now launch as a fullscreen, native-feeling, secure app on your iPhone and iPad Mini!

---

## 🛠️ Method 2: Sideload Native App via Sideloadly / AltStore (Windows Native)

If you want a standalone native iOS app installed via `.ipa` without needing Xcode:

1. **Install Sideloadly on Windows**:
   Download [Sideloadly for Windows](https://sideloadly.io/) (Free).
2. **Connect iPhone / iPad to Windows PC via USB**:
   Plug your iPhone or iPad Mini into your Windows laptop.
3. **Sideload `.ipa`**:
   - Select your pre-built `fen.ipa` package in Sideloadly.
   - Enter your Apple ID (used locally by Sideloadly to sign the app).
   - Click **Start**.
4. **Trust & Open on iOS**:
   - On your iPhone/iPad, go to **Settings -> General -> VPN & Device Management**.
   - Tap your Apple ID and select **Trust**.
   - Open `fen` natively on your device!

---

## 🔒 Security & Privacy Features

* **Zero Cloud Data Egress**: All data processing is strictly local between your Windows PC and iPhone/iPad over local Wi-Fi.
* **No Telemetry**: No third-party analytics or external network calls.
* **Offline Kiwix Hotspot Compatible**: Works out-of-the-box when connected to a local Kiwix Wi-Fi Hotspot on trails or in the field.
