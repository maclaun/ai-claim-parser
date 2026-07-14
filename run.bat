@echo off
title AI Claim Parser Server
echo ===================================================
echo Starting AI Claim Parser ^& Lead Automation Dashboard
echo ===================================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup first or create venv manually.
    pause
    exit /b 1
)

:: Open browser automatically in a separate process
echo [INFO] Starting browser at http://localhost:5000...
start http://localhost:5000

:: Run the Flask server
echo [INFO] Starting Flask server...
venv\Scripts\python.exe app.py

pause
