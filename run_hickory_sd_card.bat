@echo off
title Hickory Search - SD Card / Custom Directory Launcher
cd /d "%~dp0"
echo ===============================================================
echo  HICKORY SEARCH: SD CARD ZIM LAUNCHER
echo ===============================================================
echo.

set /p ZIM_PATH="Enter the full path to your SD card ZIM folder (e.g. E:\zim_files): "

if "%ZIM_PATH%"=="" (
    echo No path entered. Defaulting to 'zim_downloads'.
    set ZIM_PATH=zim_downloads
)

python hickory_search/hickory_cli.py --zim "%ZIM_PATH%"

pause
