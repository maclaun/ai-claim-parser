@echo off
title n8n Server
echo ===================================================
echo Starting n8n Automation Server...
echo ===================================================
echo.

:: =====================================================
:: TELEGRAM BOT CONFIGURATION
:: Replace these with your actual credentials:
set "TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN"
set "TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID"
:: =====================================================

:: Allow n8n nodes to access environment variables ($env.VAR)
set N8N_BLOCK_ENV_ACCESS_IN_NODE=false

:: Add Node.js and global npm to PATH
set "PATH=C:\Program Files\nodejs;%APPDATA%\npm;%PATH%"

:: Open browser automatically in a separate process
echo [INFO] Starting browser at http://localhost:5678...
start http://localhost:5678

:: Start n8n
echo [INFO] Running n8n...
n8n start
