@echo off
title Launch ClaimAI Suite
echo ===================================================
echo Launching ClaimAI Backend ^& n8n Automation Server...
echo ===================================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Project not set up yet. Please run setup.bat first!
    pause
    exit /b 1
)

:: Start Flask Backend in a new window
echo [INFO] Starting Flask backend (port 5000)...
start run.bat

:: Start n8n Server in a new window
echo [INFO] Starting n8n server (port 5678)...
start start-n8n.bat

echo.
echo ===================================================
echo [SUCCESS] Both servers launched in separate windows!
echo ===================================================
echo.
pause
