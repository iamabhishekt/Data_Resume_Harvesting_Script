# 🎲 Complete Dice Talent Search & Scraper

## 📋 Overview

**`dice_complete.py`** is a single, all-in-one script that handles the entire Dice talent search and data extraction process from start to finish.

## 🚀 Features

- ✅ **Single Script** - No multiple files to manage
- 🔐 **Auto-Login** - Uses saved cookies for authentication
- 🎯 **Smart Filtering** - Applies comprehensive search filters automatically
- 📊 **Data Extraction** - Extracts 13+ data fields per candidate
- 📄 **Multi-Page Support** - Scrape up to 10 pages automatically
- 💾 **Professional Export** - Excel files with timestamps
- 🔍 **Debug Mode** - Visual debugging with screenshots
- 🛡️ **Anti-Detection** - Built-in browser automation protection

## 🔍 Search Configuration

The script is pre-configured to search for:
- **Keywords**: Appian OR "Appian Developer" OR "Appian Engineer" (with SAIL, BPM, Java, etc.)
- **Location**: McLean, VA, USA
- **Distance**: 50 miles
- **Last Active**: 20 days

## 📊 Data Fields Extracted

1. **Name** - Candidate's full name
2. **Title** - Current or desired position
3. **Location** - Geographic location
4. **Experience** - Years of work experience
5. **Work Permit** - Work authorization status
6. **Relocate** - Willingness to relocate
7. **Compensation** - Salary expectations
8. **Remote** - Remote/hybrid work preference
9. **Updated** - Profile last updated date
10. **Last Active** - Last activity on Dice
11. **Likely Switch** - Job switch likelihood
12. **Profile URL** - Direct link to Dice profile
13. **Scraped Date** - When data was extracted
14. **Page Number** - Source page number

## 🚀 Quick Start

### Basic Usage (Default Settings)
```bash
python dice_complete.py
```
- Headless mode (no browser window)
- Scrapes 1 page
- Saves to Excel with timestamp

### Debug Mode (Visible Browser)
```bash
python dice_complete.py --debug
```
- Browser window visible
- Screenshots at each step
- Real-time console logging
- Great for first-time use

### Multiple Pages
```bash
python dice_complete.py --pages 5
```
- Scrapes up to 5 pages
- Automatic pagination
- All data in single Excel file

### Full Debug Mode
```bash
python dice_complete.py --debug --pages 3
```
- Visible browser with screenshots
- Scrapes 3 pages
- Maximum debugging information

## 📈 Expected Output

```
[12:30:45] INFO: 🎲 === Complete Dice Scraper Process ===
[12:30:45] INFO: 🔍 Debug Mode: ON
[12:30:45] INFO: 📄 Pages to scrape: 3
[12:30:45] INFO: ⏰ Start time: 2025-10-04 12:30:45
==================================================
[12:30:46] INFO: 🚀 Setting up browser...
[12:30:47] INFO: ✅ Browser setup complete
[12:30:47] INFO: 📸 Screenshot saved: dice_browser_setup_20251004_123047.png
[12:30:48] INFO: 🌐 Navigating to Dice talent search...
[12:30:50] INFO: 📍 URL: https://www.dice.com/employer/talent/search/
[12:30:50] INFO: 📄 Title: Dice Talent Search
[12:30:50] INFO: ✅ Successfully navigated to search page
[12:30:50] INFO: 📸 Screenshot saved: dice_search_page_loaded_20251004_123050.png

🎯 Step 1: Applying search filters...
[12:30:51] INFO: 🎯 Applying search filters...
[12:30:52] INFO: ✅ Boolean search applied
[12:30:53] INFO: ✅ Location set
[12:30:53] INFO: ✅ Location selected from autocomplete
[12:30:54] INFO: ✅ Distance set
[12:30:54] INFO: ✅ Last active days set
[12:30:55] INFO: ✅ Willing to relocate checked
[12:30:56] INFO: ✅ Search executed

⏳ Waiting for search results...
[12:31:01] INFO: 📸 Screenshot saved: dice_filters_applied_20251004_123101.png

📊 Step 2: Extracting candidate data...
[12:31:01] INFO: 📄 Starting to scrape 3 pages...

📄 Processing page 1/3
[12:31:04] INFO: ✅ Extracted 25 candidates from current page
[12:31:04] INFO: ✅ Found 25 candidates on page 1
[12:31:04] INFO:    1. John Smith - McLean, VA - Appian Developer
[12:31:04] INFO:    2. Jane Doe - Arlington, VA - Appian Architect
[12:31:04] INFO:    3. Bob Johnson - Washington, DC - Appian Engineer
[12:31:05] INFO: 📸 Screenshot saved: dice_page_1_results_20251004_123105.png

📄 Processing page 2/3
[12:31:08] INFO: ✅ Extracted 23 candidates from current page
[12:31:08] INFO: ✅ Found 23 candidates on page 2
[12:31:09] INFO: 📸 Screenshot saved: dice_page_2_results_20251004_123109.png

📄 Processing page 3/3
[12:31:12] INFO: ✅ Extracted 27 candidates from current page
[12:31:12] INFO: ✅ Found 27 candidates on page 3
[12:31:13] INFO: 📸 Screenshot saved: dice_page_3_results_20251004_123113.png

💾 Step 3: Saving results...
[12:31:15] INFO: ✅ Data saved to dice_candidates_20251004_123115.xlsx
[12:31:15] INFO: 📊 Total records: 75

📋 Sample data:
[12:31:15] INFO:    1. John Smith - McLean, VA - Appian Developer
[12:31:15] INFO:    2. Jane Doe - Arlington, VA - Appian Architect
[12:31:15] INFO:    3. Bob Johnson - Washington, DC - Appian Engineer

🎉 === PROCESS COMPLETED SUCCESSFULLY ===
[12:31:15] INFO: ⏱️ Total duration: 90.23 seconds
[12:31:15] INFO: 👥 Total candidates extracted: 75
[12:31:15] INFO: 📄 Pages processed: 3

📋 Console Messages Summary:
[12:31:15] INFO:    Errors: 0, Warnings: 2
[12:31:15] INFO:    📸 Screenshots saved in current directory
[12:31:15] INFO: 🧹 Browser cleanup complete

🎉 Success! Check the Excel files for candidate data.
```

## 📁 Generated Files

### Main Output
- **`dice_candidates_YYYYMMDD_HHMMSS.xlsx`** - Primary data file with all candidates

### Debug Screenshots (if --debug enabled)
- `dice_browser_setup_*.png` - Browser initialization
- `dice_search_page_loaded_*.png` - Search page loaded
- `dice_filters_applied_*.png` - After filters applied
- `dice_page_N_results_*.png` - Results from each page
- `dice_error_screenshot_*.png` - If any errors occur

## ⚙️ Configuration

To modify the search criteria, edit the variables at the top of the script:

```python
# ===== Configuration =====
BOOLEAN = '(Appian OR "Appian Developer" OR "Appian Engineer" ...)'
LOCATION = 'McLean, VA, USA'
DISTANCE_MILES = 50
LAST_ACTIVE_DAYS = 20
```

## 🔧 Troubleshooting

### No Candidates Found
1. Check if cookies are still valid (cookies expire over time)
2. Try running with `--debug` flag to see what's happening
3. Verify search criteria aren't too restrictive

### Login Issues
- Re-run the login process to refresh cookies
- Check if you're still logged into Dice.com in a browser

### Navigation Errors
- Use `--debug` mode to see the page loading
- Check internet connection
- Try running with different user agent

### Large Scale Scraping
- Limit to 10 pages maximum (500+ candidates)
- Use headless mode for faster execution
- Add delays between page requests if needed

## 🛡️ Anti-Detection Features

- Random user agents
- Realistic browser settings
- Natural delays between actions
- Proper session management
- Error handling and retry logic

## 📋 Requirements

- Python 3.7+
- pandas (`pip install pandas`)
- playwright (`pip install playwright && playwright install`)
- Valid Dice.com login cookies (embedded in script)

## 🎯 Perfect For

- **Recruiters** - Building candidate databases
- **Hiring Managers** - Finding qualified talent
- **Market Research** - Analyzing candidate pools
- **Competitive Intelligence** - Understanding skill availability

## 📞 Support

The script includes comprehensive logging and debugging features. If you encounter issues:

1. Run with `--debug` flag for detailed output
2. Check generated screenshots for visual debugging
3. Review console messages for error details
4. Adjust search criteria if results are too narrow

---

**🎉 Ready to start scraping Dice for Appian talent!**