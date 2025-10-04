# Dice Resume Harvesting Script

Complete solution for scraping candidate data from Dice.com talent search with filter application and Excel export.

## Features

✅ **Comprehensive Filtering** - Applies 9 different search filters
✅ **Data Extraction** - Extracts 15 fields per candidate
✅ **Profile Tracking** - Detects if profiles have been viewed
✅ **Excel Export** - Clean, organized output with timestamps
✅ **Debug Mode** - Screenshots and HTML saved in organized folders
✅ **Multi-page Support** - Scrape up to 10 pages

## Quick Start

```bash
# Basic usage - Headless mode, 1 page
python dice_complete.py

# Debug mode - See browser, save screenshots
python dice_complete.py --debug

# Multiple pages
python dice_complete.py --pages 5

# Debug + multiple pages
python dice_complete.py --debug --pages 3
```

## Files Generated

### Excel Output
- **Format**: `dice_candidates_YYYYMMDD_HHMMSS.xlsx`
- **Location**: Current directory
- **Contains**: All candidate data with 14 fields

### Debug Files (Debug Mode Only)
- **Folder**: `debug_YYYYMMDD_HHMMSS/`
- **Contains**:
  - Screenshots (PNG files) at each step
  - HTML files for manual inspection
  - Same timestamp as Excel file

## Extracted Data Fields

| Field | Description |
|-------|-------------|
| profile-name-text | Candidate's full name |
| profile-url | Link to candidate profile |
| **profile-viewed** | **Whether profile has been viewed (Yes/No)** |
| pref-prev-job-title | Preferred/Previous job title |
| location | Candidate location |
| work-exp | Work experience |
| work-permit | Work authorization status |
| willing-to-relocate | Relocation preference |
| compensation | Desired salary |
| desired-work-setting | Remote/Hybrid/Onsite |
| date-updated | Profile last updated |
| date-last-active | Last active on platform |
| likely-to-switch | Likelihood to switch jobs |
| scraped-date | When data was scraped |
| page-number | Which page found on |

## Applied Filters

The script automatically applies these filters:
1. ✅ Boolean/Keyword search (Appian Developer + skills)
2. ✅ Location (McLean, VA, USA)
3. ✅ Distance (50 miles)
4. ✅ Willing to relocate
5. ✅ Last active (20 days)
6. ✅ Profile source (Any)
7. ✅ Contact methods (unchecked)
8. ✅ Additional filters (unchecked)
9. ✅ Search execution

## Cleanup Debug Files

### Manual Cleanup
```bash
# Delete specific debug folder
rm -rf debug_20251004_144149

# Delete all debug folders
rm -rf debug_*
```

### Automated Cleanup
```bash
# Use the cleanup script
./cleanup_debug.sh
```

The cleanup script will:
- Show all debug folders
- Display total size
- Ask for confirmation before deleting

## Configuration

### Boolean Query (Search Keywords)

**NEW**: The Boolean query is now loaded from `Dice_string.txt` instead of hardcoded!

**Option 1: Auto-generate with ChatGPT** (Recommended)
```bash
# 1. Edit job_description.txt with your job requirements
# 2. Set up .env with OPENAI_API_KEY=sk-your-key
# 3. Generate query
python dice_api.py

# The query is saved to Dice_string.txt and automatically used
```

**Option 2: Manual editing**
```bash
# Edit the query directly
nano Dice_string.txt
```

**Option 3: Use default** (Appian Developer)
```bash
# If Dice_string.txt doesn't exist, default query is used
```

📖 See [QUERY_GENERATION_GUIDE.md](QUERY_GENERATION_GUIDE.md) for detailed instructions.

### Other Settings

Edit in `dice_complete.py`:
```python
LOCATION = 'McLean, VA, USA'
DISTANCE_MILES = 50
LAST_ACTIVE_DAYS = 30
```

## Requirements

```bash
pip install playwright pandas openpyxl
playwright install chromium
```

## Command Line Options

```bash
python dice_complete.py --help

options:
  -h, --help     show this help message and exit
  --debug        Run in visible browser mode for debugging
  --pages PAGES  Number of pages to scrape (default: 1, max: 10)
```

## Example Output

```
🎲 === Complete Dice Scraper ===
🔍 Debug Mode: ON
📄 Pages to scrape: 2
⏰ Start time: 2025-10-04 14:42:10
==================================================

[14:42:15] INFO: ✅ Successfully navigated to search page
[14:42:18] INFO: ✅ Filters applied successfully
[14:42:20] INFO: ✅ Extracted 2 candidates from current page
[14:42:20] INFO: ✅ Data saved to dice_candidates_20251004_144149.xlsx

🎉 === PROCESS COMPLETED SUCCESSFULLY ===
⏱️ Total duration: 30.65 seconds
👥 Total candidates extracted: 2
📄 Pages processed: 1
📁 Debug files saved in: debug_20251004_144149/
💡 You can delete this folder later: rm -rf debug_20251004_144149
```

## Troubleshooting

### No candidates extracted
- Check if you're logged in (cookies may be expired)
- Try running with `--debug` to see what's happening
- Verify search filters are appropriate

### Browser not launching
```bash
playwright install chromium
```

### Excel not saving
```bash
pip install openpyxl pandas
```

### Permission errors on cleanup
```bash
chmod +x cleanup_debug.sh
```

## File Structure

```
Data_Resume_Harvesting_Script/
├── dice_complete.py          # Main script
├── dice-filters.py            # Filter reference
├── dice_web_scrap.py          # Extraction reference
├── cleanup_debug.sh           # Debug cleanup script
├── README.md                  # This file
├── dice_candidates_*.xlsx     # Output files
└── debug_*/                   # Debug folders (optional)
    ├── browser_setup.png
    ├── browser_setup.html
    ├── search_page_loaded.png
    ├── search_page_loaded.html
    ├── filters_applied.png
    ├── filters_applied.html
    ├── page_1_results.png
    └── page_1_results.html
```

## Notes

- Debug files can be large (2-5 MB per run)
- Regular cleanup recommended to save disk space
- Excel files are compact (~5-10 KB per run)
- Timestamps ensure no file overwrites

## License

For internal use only.
