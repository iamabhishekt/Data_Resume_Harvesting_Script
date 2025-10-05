#!/bin/bash
# Setup script for Dice Resume Harvesting Script (macOS/Linux)

echo "========================================================================"
echo "🚀 DICE RESUME HARVESTING SCRIPT - SETUP"
echo "========================================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip3 is not installed!"
    echo "Please install pip3"
    exit 1
fi

echo "✅ Found pip3"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing Python packages..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo ""
echo "========================================================================"
echo "✅ SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create a .env file with your credentials:"
echo "   DICE_EMAIL=your_email@example.com"
echo "   DICE_PASSWORD=your_password"
echo "   OPENAI_API_KEY=your_openai_api_key"
echo ""
echo "2. (Optional) Edit job_description.txt with your job requirements"
echo ""
echo "3. Run the script:"
echo "   source venv/bin/activate  # Activate virtual environment"
echo "   python3 dice_complete.py"
echo ""
echo "========================================================================"
