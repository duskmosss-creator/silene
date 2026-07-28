@echo off
title Hickory Multi-ZIM Wiki Agent
cd /d "%~dp0\.."
echo ===============================================================
echo  HICKORY MULTI-ZIM WIKI AGENT
echo  Full System Logging ^| Multi-ZIM Search ^| Lemonade / LMStudio
echo ===============================================================
echo.
echo Starting Multi-ZIM Wiki Agent...
echo (Press Ctrl+C at any time to quit)
echo.

python hickory_search/hickory_multi_zim_agent.py zim_downloads

pause
