#!/bin/bash
# Generate Dice Boolean query from job description

echo "🔍 Dice Boolean Query Generator"
echo "================================"
echo ""

# Check if job_description.txt exists
if [ ! -f "job_description.txt" ]; then
    echo "❌ Error: job_description.txt not found!"
    echo "💡 Create a job_description.txt file with the job requirements"
    exit 1
fi

echo "📄 Found job_description.txt"
echo ""

# Check if .env file exists and has API key
if [ -f ".env" ]; then
    if grep -q "OPENAI_API_KEY" .env; then
        echo "✅ Found .env with API key"
        echo "🤖 Generating Boolean query using ChatGPT..."
        echo ""
        python dice_api.py

        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Query generated successfully!"
            echo "📁 Output: Dice_string.txt"
            echo ""
            echo "📋 Generated Query:"
            echo "─────────────────────────────────────────────────────────"
            cat Dice_string.txt
            echo ""
            echo "─────────────────────────────────────────────────────────"
        else
            echo ""
            echo "❌ Failed to generate query using ChatGPT"
            echo "💡 Check your API key in .env file"
        fi
    else
        echo "⚠️  .env exists but no OPENAI_API_KEY found"
        echo "💡 Add your OpenAI API key to .env:"
        echo "   OPENAI_API_KEY=sk-your-api-key-here"
    fi
else
    echo "⚠️  No .env file found"
    echo "💡 To use ChatGPT for query generation:"
    echo "   1. Create a .env file"
    echo "   2. Add: OPENAI_API_KEY=sk-your-api-key-here"
    echo "   3. Run this script again"
    echo ""
    echo "📋 For now, using the existing Dice_string.txt or default query"
fi

echo ""
echo "💡 You can manually edit Dice_string.txt to customize the query"
echo "💡 Then run: python dice_complete.py --debug --pages 1"
