# Project Notes

*   **Goal:** Create a <20GB ZIM file ecosystem and RAG engine from public domain texts, PDFs, and National Geographic magazines for off-grid use.
*   **Methodology:**
    1. Python scrapers & builders to package local assets into ZIM archives (`Appalachian_Corridor.zim`, `GSMNP_Backpacking_Field_Guide.zim`, `National_Geographic_Appalachian_Collection.zim`, `Southern_Appalachian_Regional_Master.zim`).
    2. Hickory Search RAG Engine (`hickory_cli.py` & Swift `HickoryRAGEngine.swift`) using `libzim` to search across 40+ ZIM archives on-device with zero open network ports.
    3. Optional Lemonade / LMStudio IPC integration (`http://127.0.0.1:11434/v1/chat/completions`) for offline LLM synthesis.

