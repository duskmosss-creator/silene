@echo off
title Hickory Search - Off-Grid Multi-ZIM Agent (Port 8000)
cd /d "%~dp0"
echo ===============================================================
echo  HICKORY SEARCH: OFF-GRID MULTI-ZIM AGENT (PORT 8000)
echo  100%% On-Device RAG Engine | Lemonade / LMStudio Ready
echo ===============================================================
echo.

IF EXIST "zim_downloads" (
    python hickory_search/hickory_multi_zim_agent.py zim_downloads
) ELSE (
    python hickory_search/hickory_multi_zim_agent.py
)

pause
