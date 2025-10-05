# 🎯 Dice Resume Harvesting Script

A powerful automated tool to scrape and collect candidate resumes from Dice.com with advanced features including duplicate detection, automatic query generation, and smart sorting.

## ✨ Features

- 🤖 **Automated Resume Scraping** - Uses Playwright for reliable browser automation
- 🔍 **Smart Search** - Boolean query generation using OpenAI ChatGPT API
- 🚫 **Duplicate Detection** - Automatically filters out duplicate candidates
- 📊 **Excel & CSV Export** - Multi-sheet Excel files with search parameters
- 🔄 **Auto-Regeneration** - Updates search queries when job description changes
- 📅 **Smart Sorting** - Sorts candidates by most recent update
- 🎨 **Clean Output** - Hidden profile URLs, organized data structure
- 🔒 **Secure** - Uses environment variables for credentials

## 📋 Requirements

- Python 3.8 or higher
- Dice.com account with employer access
- OpenAI API key (for automatic query generation)

## 🚀 Quick Start - ONE CLICK SETUP

### For macOS/Linux:
\`\`\`bash
chmod +x setup.sh run.sh
./setup.sh
\`\`\`

### For Windows:
\`\`\`cmd
setup.bat
\`\`\`

### Configuration

1. Copy \`.env.example\` to \`.env\`:
\`\`\`bash
cp .env.example .env
\`\`\`

2. Edit \`.env\` with your credentials:
\`\`\`env
DICE_EMAIL=your_email@example.com
DICE_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
\`\`\`

3. (Optional) Edit \`job_description.txt\` with your job requirements

### Running the Script

#### For macOS/Linux:
\`\`\`bash
./run.sh
\`\`\`

#### For Windows:
\`\`\`cmd
run.bat
\`\`\`

## 📖 Usage

### Basic Usage

Run the script and follow the prompts for location, distance, and days.

### Command Line Options

\`\`\`bash
python3 dice_complete.py --pages 5      # Scrape 5 pages
python3 dice_complete.py --debug        # Enable debug mode
\`\`\`

### Generate Boolean Query

\`\`\`bash
python3 dice_api.py
\`\`\`

## 📂 Output Files

- \`dice_candidates_YYYYMMDD_HHMMSS.xlsx\` - Excel with 2 sheets (Candidates + Search Parameters)
- \`dice_candidates_YYYYMMDD_HHMMSS.csv\` - CSV backup

## 🛠️ Troubleshooting

**Setup Issues:**
- Ensure Python 3.8+ is installed
- Run \`pip3 install -r requirements.txt\` manually if setup fails
- Run \`playwright install chromium\` to install browser

**Runtime Issues:**
- Check \`.env\` file has correct credentials
- Verify Boolean query in \`Dice_string.txt\`
- Use \`--debug\` flag to see detailed output

## 📚 Documentation

- \`MANUAL_QUERY_GUIDE.md\` - Pre-built queries for 10 common roles
- \`AUTO_REGENERATION_FEATURE.md\` - Query regeneration guide
- \`FEATURE_COMPLETE_SUMMARY.txt\` - Complete feature list

## 🔒 Security

- Never commit \`.env\` file
- Keep credentials secure
- Handle candidate data responsibly

---

**Made with ❤️ for recruiters and hiring managers**
