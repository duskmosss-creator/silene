@echo off
title Hickory Search - Off-Grid Terminal Agent
cd /d "%~dp0"
echo ===============================================================
echo  HICKORY SEARCH: OFF-GRID TERMINAL AGENT
echo  100%% On-Device RAG Engine (Zero Open Network Ports)
echo ===============================================================
echo.

IF EXIST "zim_downloads" (
    python hickory_search/hickory_cli.py --zim zim_downloads
) ELSE (
    python hickory_search/hickory_cli.py
)

pause
