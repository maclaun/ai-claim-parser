@echo off
title AI Claim Parser Setup
echo ===================================================
echo Setting up AI Claim Parser ^& Lead Automation...
echo ===================================================
echo.

:: 1. Create virtual environment
echo [1/3] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Python not found or failed to create virtual environment.
    echo Please make sure Python 3.12+ is installed and added to PATH.
    pause
    exit /b 1
)

:: 2. Install dependencies
echo [2/3] Installing Python dependencies...
venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: 3. Copy env template
echo [3/3] Creating configuration files...
if not exist ".env" (
    copy .env.example .env
    echo [SUCCESS] Created .env file from template.
    echo PLEASE EDIT .env AND ADD YOUR GROQ_API_KEY!
) else (
    echo [INFO] .env file already exists. Skipping copy.
)

echo.
echo ===================================================
echo [SUCCESS] Setup completed successfully!
echo.
echo Instructions:
echo 1. Open .env and add your GROQ_API_KEY.
echo 2. Open start-n8n.bat and add your Telegram bot credentials.
echo 3. Run start-all.bat to launch both servers.
echo ===================================================
pause
