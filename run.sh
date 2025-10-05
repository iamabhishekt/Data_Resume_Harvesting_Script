#!/bin/bash
# Quick run script for Dice Resume Harvesting Script (macOS/Linux)

echo "========================================================================"
echo "🎯 DICE RESUME HARVESTING SCRIPT"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Create a .env file with:"
    echo "  DICE_EMAIL=your_email@example.com"
    echo "  DICE_PASSWORD=your_password"
    echo "  OPENAI_API_KEY=your_openai_api_key"
    echo ""
fi

# Run the script
echo "🚀 Starting Dice scraper..."
echo ""
python3 dice_complete.py "$@"

echo ""
echo "========================================================================"
echo "✅ DONE!"
echo "========================================================================"
