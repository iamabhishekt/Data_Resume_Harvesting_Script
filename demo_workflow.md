# Dice Scraper Workflow Demonstration

## 🎯 Complete Workflow

The sequence script runs the entire process end-to-end:

### Step 1: Configuration
```bash
python dice_sequence.py
```

### Step 2: Interactive Setup
- Number of pages to scrape: (1-10)
- Debug mode for filters: (y/N)
- Debug mode for scraper: (y/N)

### Step 3: Automatic Execution
1. **Apply Search Filters** (`dice-filters.py`)
   - Login with saved cookies
   - Apply Appian + SAIL boolean search
   - Set location to McLean, VA
   - Configure distance (50 miles)
   - Set last active (20 days)
   - Execute search

2. **Wait Period** (5 seconds)
   - Allows search results to fully load

3. **Extract Candidate Data** (`dice_web_scrap.py`)
   - Navigate to search results
   - Extract candidate profiles
   - Collect 11 data fields per candidate
   - Navigate through multiple pages
   - Save to Excel with timestamp

### Step 4: Output Files Generated
- `dice_candidates_YYYYMMDD_HHMMSS.xlsx` - Main data file
- `dice_before_filters.png` - Screenshot before filters
- `dice_search_results.png` - Screenshot after search
- `debug_*.png` - Debug screenshots (if debug mode enabled)

## 📊 Data Fields Extracted

1. **Profile Name** - Candidate's full name
2. **Profile URL** - Direct link to Dice profile
3. **Preferred Job Title** - Current or desired position
4. **Location** - Candidate's location
5. **Work Experience** - Years of experience
6. **Work Permit** - Work authorization status
7. **Willing to Relocate** - Relocation preference
8. **Compensation** - Salary expectations
9. **Desired Work Setting** - Remote/hybrid/office preference
10. **Date Updated** - Profile last updated
11. **Date Last Active** - Last activity on Dice
12. **Likely to Switch** - Job switch likelihood

## 🚀 Running the Sequence

### Quick Start (Default Settings)
```bash
# Interactive mode with prompts
python dice_sequence.py

# Follow the prompts:
# - Pages: 1 (default)
# - Debug filters: n (headless)
# - Debug scraper: n (headless)
```

### Debug Mode (Visible Browser)
```bash
python dice_sequence.py
# Pages: 3
# Debug filters: y (visible browser)
# Debug scraper: y (visible browser)
```

### Large Scale Scraping
```bash
python dice_sequence.py
# Pages: 5
# Debug filters: n (headless for speed)
# Debug scraper: n (headless for speed)
```

## 🔍 Debug Mode Benefits

When debug mode is enabled:
- **Visible Browser**: See what the script is doing in real-time
- **Screenshots**: Automatic screenshots at each step
- **Console Logs**: Browser console output displayed
- **Error Diagnosis**: Visual debugging of issues

## 📋 Expected Output

```
🎲 === DICE SEQUENCE EXECUTION ===
Sequential execution: dice-filters.py → dice_web_scrap.py
⏰ Started at: 2025-10-04 12:30:45

============================================================
⚙️  Configuration
============================================================
📄 How many pages to scrape? (default: 1): 3
📊 Will scrape up to 3 page(s)

============================================================
🎯 Ready to start sequence execution
1. 🎯 Apply search filters using dice-filters.py
2. 📊 Scrape candidate data using dice_web_scrap.py
3. 💾 Save results to Excel files
4. 📄 Scrape 3 page(s)
============================================================
🚀 Start execution? (y/N): y

============================================================
🚀 Step 1: Apply Search Filters
📂 Running: python dice-filters.py --visible
============================================================
📝 Output:
   🎲 === Dice Talent Search Automation with Enhanced Debug ===
   🔍 Boolean Search: (Appian OR "Appian Developer"...
   📍 Location: McLean, VA, USA
   ...
   ✅ Filters applied successfully
   ⏱️ Duration: 45.23 seconds

✅ Filters applied successfully!

⏳ Waiting 5 seconds before starting scraper...

============================================================
🚀 Step 2: Scrape Candidate Data
📂 Running: python dice_web_scrap.py --debug --pages 3
============================================================
📝 Output:
   🎲 === Dice Web Scraper - Post Filter Data Extraction ===
   📄 Scraping up to 3 pages
   ...
   ✅ Found 25 candidates on page 1
   ✅ Found 23 candidates on page 2
   ✅ Found 27 candidates on page 3
   ✅ Data exported to dice_candidates_20251004_123456.xlsx
   ⏱️ Duration: 67.89 seconds

✅ Scraping completed successfully!

============================================================
🎉 SEQUENCE EXECUTION COMPLETE
============================================================
⏱️ Total duration: 118.45 seconds
🎯 Filters applied: ✅
📊 Data scraped: ✅

============================================================
📋 Checking for generated files...
============================================================
📊 Excel files found: 1
   📄 dice_candidates_20251004_123456.xlsx
📸 Screenshot files found: 3
   📷 dice_before_filters.png
   📷 dice_search_results.png
   📷 debug_initial_page_load.png

📋 SUMMARY:
🎯 Search filters: Applied
📊 Data scraping: Success
📄 Excel files: Created

🎉 Success! Check the Excel files for candidate data.
⏰ Completed at: 2025-10-04 12:32:43
```

## ⚠️ Important Notes

1. **Run `dice-filters.py` first** if you want to test individual components
2. **Valid login cookies** must be available in `dice-filters.py`
3. **Dice.com may block** excessive scraping - use reasonable page limits
4. **Headless mode** is faster for large scale operations
5. **Debug mode** is recommended for first-time use

## 🔧 Troubleshooting

- **No candidates found**: Check if search filters applied correctly
- **Login issues**: Re-run `dice_login.py` to refresh cookies
- **Navigation errors**: Use debug mode to see what's happening
- **Empty Excel file**: Check if search returned any results

The sequence script handles all errors gracefully and provides detailed feedback for troubleshooting.