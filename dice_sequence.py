#!/usr/bin/env python3
"""
Dice Sequence Script - Runs dice-filters.py and dice_web_scrap.py sequentially
Simple sequential execution without complex UI
"""

import subprocess
import sys
import time
from datetime import datetime
import os

def run_script(script_name, description):
    """Run a Python script and display output"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"📂 Running: {script_name}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # Run the script
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Print output in real-time
        print("📝 Output:")
        print("-" * 40)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   {output.strip()}")

        # Get the return code
        return_code = process.poll()
        end_time = time.time()
        duration = end_time - start_time

        print("-" * 40)
        if return_code == 0:
            print(f"✅ {script_name} completed successfully")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            return True
        else:
            print(f"❌ {script_name} failed with return code {return_code}")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            return False

    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def run_script_with_args(cmd, description):
    """Run a Python script with arguments and display output"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"📂 Running: {' '.join(cmd)}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        # Run the script with arguments
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Print output in real-time
        print("📝 Output:")
        print("-" * 40)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   {output.strip()}")

        # Get the return code
        return_code = process.poll()
        end_time = time.time()
        duration = end_time - start_time

        print("-" * 40)
        if return_code == 0:
            print(f"✅ {' '.join(cmd)} completed successfully")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            return True
        else:
            print(f"❌ {' '.join(cmd)} failed with return code {return_code}")
            print(f"⏱️  Duration: {duration:.2f} seconds")
            return False

    except Exception as e:
        print(f"❌ Error running {' '.join(cmd)}: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = ["dice-filters.py", "dice_web_scrap.py"]
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure both dice-filters.py and dice_web_scrap.py are in the current directory.")
        return False

    return True

def check_generated_files():
    """Check for generated output files"""
    print(f"\n{'='*60}")
    print("📋 Checking for generated files...")
    print(f"{'='*60}")

    excel_files = []
    screenshot_files = []
    log_files = []

    # Look for various output files
    for file in os.listdir('.'):
        if file.startswith('dice_'):
            if file.endswith('.xlsx'):
                excel_files.append(file)
            elif file.endswith('.png'):
                screenshot_files.append(file)
            elif file.endswith('.json'):
                log_files.append(file)

    print(f"📊 Excel files found: {len(excel_files)}")
    for file in excel_files:
        print(f"   📄 {file}")

    print(f"📸 Screenshot files found: {len(screenshot_files)}")
    for file in screenshot_files:
        print(f"   📷 {file}")

    print(f"📝 Log files found: {len(log_files)}")
    for file in log_files:
        print(f"   📄 {file}")

    if not excel_files and not screenshot_files:
        print("⚠️  No output files found")

    return len(excel_files) > 0

def main():
    """Main sequence execution"""
    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        print("🎲 Dice Sequence Script - Automated Execution")
        print("\nThis script runs the complete Dice talent search and scraping sequence:")
        print("  1. 🎯 Apply search filters using dice-filters.py")
        print("  2. 📊 Scrape candidate data using dice_web_scrap.py")
        print("  3. 💾 Save results to Excel files")
        print("\nUsage:")
        print("  python dice_sequence.py")
        print("\nFeatures:")
        print("  • Interactive configuration")
        print("  • Real-time output display")
        print("  • File generation tracking")
        print("  • Error handling and reporting")
        print("\nRequirements:")
        print("  • dice-filters.py (search filter application)")
        print("  • dice_web_scrap.py (candidate data extraction)")
        print("  • Valid Dice.com login cookies")
        print("\nExample:")
        print("  python dice_sequence.py")
        return

    print("🎲 === DICE SEQUENCE EXECUTION ===")
    print("Sequential execution: dice-filters.py → dice_web_scrap.py")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check if required files exist
    if not check_files():
        return

    # Get user preferences
    print(f"\n{'='*60}")
    print("⚙️  Configuration")
    print(f"{'='*60}")

    # Ask about scraping pages
    try:
        pages_input = input("📄 How many pages to scrape? (default: 1): ").strip() or "1"
        max_pages = int(pages_input)
        max_pages = max(1, min(max_pages, 10))
    except (ValueError, KeyboardInterrupt):
        max_pages = 1

    print(f"📊 Will scrape up to {max_pages} page(s)")

    # Ask for confirmation
    print(f"\n{'='*60}")
    print("🎯 Ready to start sequence execution")
    print("1. 🎯 Apply search filters using dice-filters.py")
    print("2. 📊 Scrape candidate data using dice_web_scrap.py")
    print("3. 💾 Save results to Excel files")
    print(f"4. 📄 Scrape {max_pages} page(s)")
    print(f"{'='*60}")

    confirm = input("🚀 Start execution? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("⏹️  Execution cancelled by user.")
        return

    # Start timing
    total_start_time = time.time()

    # Step 1: Run dice-filters.py
    filter_cmd = [sys.executable, "dice-filters.py"]

    # Ask if user wants debug mode for filters
    debug_filters = input("🔍 Run filter application in debug mode? (y/N): ").strip().lower()
    if debug_filters in ['y', 'yes']:
        filter_cmd.append("--visible")
        print("🐛 Filter debug mode enabled - browser will be visible")
    else:
        print("🚀 Running filters in headless mode")

    filter_success = run_script_with_args(
        filter_cmd,
        "Step 1: Apply Search Filters"
    )

    if filter_success:
        print("✅ Filters applied successfully!")
    else:
        print("⚠️  Filter application may have failed, continuing with scraping...")

    # Wait between steps
    print(f"\n⏳ Waiting 5 seconds before starting scraper...")
    time.sleep(5)

    # Step 2: Run dice_web_scrap.py with command line arguments
    print(f"\n{'='*60}")
    print("📊 Starting scraper with command line arguments...")
    print(f"{'='*60}")

    try:
        # Build command with arguments
        cmd = [sys.executable, "dice_web_scrap.py", "--pages", str(max_pages)]

        # Add debug flag if user wants
        debug_choice = input("🔍 Run scraper in debug mode? (y/N): ").strip().lower()
        if debug_choice in ['y', 'yes']:
            cmd.append("--debug")
            print("🐛 Debug mode enabled - browser will be visible")
        else:
            print("🚀 Running in headless mode")

        print(f"📝 Command: {' '.join(cmd)}")

        # Run the scraper with command line arguments
        scrape_success = run_script_with_args(
            cmd,
            "Step 2: Scrape Candidate Data"
        )

        if scrape_success:
            print("✅ Scraping completed successfully!")
        else:
            print("⚠️  Scraping may have failed")

    except Exception as e:
        print(f"❌ Error running scraper: {e}")
        scrape_success = False

    # Calculate total time
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time

    # Final summary
    print(f"\n{'='*60}")
    print("🎉 SEQUENCE EXECUTION COMPLETE")
    print(f"{'='*60}")
    print(f"⏱️  Total duration: {total_duration:.2f} seconds")
    print(f"🎯 Filters applied: {'✅' if filter_success else '❌'}")
    print(f"📊 Data scraped: {'✅' if scrape_success else '❌'}")

    # Check for generated files
    has_excel_files = check_generated_files()

    # Final summary
    print(f"\n📋 SUMMARY:")
    print(f"🎯 Search filters: {'Applied' if filter_success else 'Failed'}")
    print(f"📊 Data scraping: {'Success' if scrape_success else 'Failed'}")
    print(f"📄 Excel files: {'Created' if has_excel_files else 'None'}")

    if has_excel_files:
        print(f"\n🎉 Success! Check the Excel files for candidate data.")
    else:
        print(f"\n⚠️  No Excel files created. Check the output above for issues.")

    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⏹️  Execution interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")