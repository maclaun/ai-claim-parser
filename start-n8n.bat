@echo off
title n8n Server
echo ===================================================
echo Starting n8n Automation Server...
echo ===================================================
echo.

:: Add Node.js and global npm to PATH
set "PATH=C:\Program Files\nodejs;%APPDATA%\npm;%PATH%"

:: Open browser automatically in a separate process
echo [INFO] Starting browser at http://localhost:5678...
start http://localhost:5678

:: Start n8n
echo [INFO] Running n8n...
n8n start
