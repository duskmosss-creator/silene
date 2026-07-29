- [x] Fix Kiwix iOS WKWebView rejecting C/index.html and falling back to texts/194701to12.txt
- [x] Fix Kiwix iOS WKWebView failing to load text content due to CORS blocked fetch() calls
- [x] Fixed circular redirect loop bug on C/index.html in National_Geographic_Appalachian_Collection.zim

- [x] Generated unified 3.7GB National Geographic ZIM file (National_Geographic_Complete_Collection_v9.zim) with chronological sorting and title wrapping.
- [x] Generated unified 3.7GB National Geographic ZIM file (National_Geographic_Complete_Collection_v10.zim) retaining original uncompressed PDFs.
## 2026-07-29
- [x] Fixed iOS loading issue: replaced iframe PDF viewer with canvas-based pdf.js rendering for all 53 magazines
- [x] Rebuilt National_Geographic_Complete_Collection_v10.zim with all 53 original uncompressed PDFs and iOS-compatible viewer HTML
## 2026-07-29 (v13 Complete)
- [x] Built 3 clean volumes under 1.7GB limit: National_Geographic_Vol1_v13.zim, National_Geographic_Vol2_v13.zim, National_Geographic_Vol3_v13.zim
- [x] Verified zero structural corruption and passed zimcheck validation
- [x] Vol 3 contains strictly 13 Modern National Geographic issues (2009-2019)
- [x] Added iOS-compatible canvas viewer + native PDF download buttons
## 2026-07-29 (v14 UI & Scaling Fix)
- [x] Updated viewer HTML template to match Appalachian Corridor styling and scaling
- [x] Fixed top-left cropping issue by implementing responsive canvas auto-scaling
- [x] Added + and - zoom controls in header bar for manual magnification adjustment
- [x] Compiled v14 ZIM files (Vol1, Vol2, Vol3) in zim_downloads
## 2026-07-29 (v15 Seamless Vertical Scroll)
- [x] Updated viewer HTML template to render all PDF pages sequentially in a continuous vertical scroll container
- [x] Auto-centered pages and scaled them seamlessly to screen width
- [x] Built and compiled v15 ZIM files (Vol1, Vol2, Vol3) in zim_downloads
## 2026-07-29 (v16 Black Screen & Photo Fix)
- [x] Extracted missing cover image for June 2019 issue to ensure 100% of cards show cover photos
- [x] Replaced IntersectionObserver with sequential async/await PDF page rendering loop to fix black screen bug on Kiwix WebViews
- [x] Compiled v16 ZIM files (Vol1, Vol2, Vol3) in zim_downloads
## 2026-07-29 (v17 Bulletproof iOS Overhaul)
- [x] Applied 7 simultaneous iOS WKWebView compatibility fixes across all HTML viewers
- [x] Disabled WebWorker requirement to prevent security blocks on zim:// custom scheme
- [x] Clamped maximum canvas resolution to 2048px to prevent iOS Safari memory crashes
- [x] Added ES5 promise queue, native PDF embed fallback, and duplicated JS asset paths
- [x] Saved v16 untouched and compiled v17 ZIM files (Vol1, Vol2, Vol3) in zim_downloads