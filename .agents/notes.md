

## Key Fix (2026-07-29)
The ZIM viewer pages were using <iframe> to load PDFs, which iOS Kiwix blocks entirely. Fix: regenerate all viewer HTML to use pdf.js canvas rendering (same approach as Appalachian Corridor ZIM). No iframe, no compression needed.