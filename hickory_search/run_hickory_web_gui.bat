@echo off
title Hickory Search - Web Interface
cd /d "%~dp0"
echo ===============================================================
echo  HICKORY SEARCH: WEB INTERFACE
echo  Opening browser at http://localhost:8000
echo ===============================================================
echo.

start http://localhost:8000
python hickory_search/hickory_web_app.py

pause
