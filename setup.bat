@echo off
REM Setup script for Dice Resume Harvesting Script (Windows)

echo ========================================================================
echo 🚀 DICE RESUME HARVESTING SCRIPT - SETUP
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Found Python
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed!
    echo Please install pip
    pause
    exit /b 1
)

echo ✅ Found pip
echo.

REM Create virtual environment (optional but recommended)
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing Python packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo 🌐 Installing Playwright browsers...
playwright install chromium

echo.
echo ========================================================================
echo ✅ SETUP COMPLETE!
echo ========================================================================
echo.
echo 📋 Next Steps:
echo.
echo 1. Create a .env file with your credentials:
echo    DICE_EMAIL=your_email@example.com
echo    DICE_PASSWORD=your_password
echo    OPENAI_API_KEY=your_openai_api_key
echo.
echo 2. (Optional) Edit job_description.txt with your job requirements
echo.
echo 3. Run the script:
echo    venv\Scripts\activate.bat  (Activate virtual environment)
echo    python dice_complete.py
echo.
echo ========================================================================
pause
