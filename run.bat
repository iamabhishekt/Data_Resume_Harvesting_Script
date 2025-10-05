@echo off
REM Quick run script for Dice Resume Harvesting Script (Windows)

echo ========================================================================
echo 🎯 DICE RESUME HARVESTING SCRIPT
echo ========================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo Create a .env file with:
    echo   DICE_EMAIL=your_email@example.com
    echo   DICE_PASSWORD=your_password
    echo   OPENAI_API_KEY=your_openai_api_key
    echo.
)

REM Run the script
echo 🚀 Starting Dice scraper...
echo.
python dice_complete.py %*

echo.
echo ========================================================================
echo ✅ DONE!
echo ========================================================================
pause
