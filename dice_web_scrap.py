import pandas as pd
import time
import json
import random
from urllib.parse import urljoin
import re
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

# Import cookies and user agents from dice-filters.py for consistency
try:
    with open('/Users/abhishek/Data_Resume_Harvesting_Script/dice-filters.py', 'r') as f:
        content = f.read()
        # Extract cookies array
        start = content.find('cookies_json = [')
        end = content.find(']', start) + 1
        exec(content[start:end])
        # Extract USER_AGENTS array
        start = content.find('USER_AGENTS = [')
        end = content.find(']', start) + 1
        exec(content[start:end])
except Exception as e:
    print(f"Warning: Could not import from dice-filters.py: {e}")
    # Fallback minimal cookies
    cookies_json = [
        {"domain": "www.dice.com", "hostOnly": True, "httpOnly": False, "name": "cms-gtm-randomNumSample", "path": "/", "sameSite": None, "secure": False, "session": True, "storeId": None, "value": "4"}
    ]
    USER_AGENTS = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36']

def verify_page_and_take_screenshot(page, step_name):
    """Verify page is loaded correctly and take screenshot for debugging"""
    try:
        current_url = page.url
        print(f"📸 Step: {step_name}")
        print(f"   Current URL: {current_url}")

        # Take screenshot
        screenshot_path = f"/Users/abhishek/Data_Resume_Harvesting_Script/debug_{step_name.replace(' ', '_').lower()}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"   Screenshot saved: {screenshot_path}")

        # Check if we're on the right page
        if "jobs" in current_url.lower() or "search" in current_url.lower() or "talent" in current_url.lower():
            print(f"   ✅ Page verification passed")
            return True
        else:
            print(f"   ❌ Page verification failed - not on search page")
            return False

    except Exception as e:
        print(f"   ❌ Error during verification: {e}")
        return False

def extract_candidate_data(page):
    """Extract candidate data from the current page with extensive debugging"""

    print("🔍 Extracting candidate data from page...")

    # JavaScript to extract all candidate information with debugging
    js_code = r"""
    () => {
        console.log('🎲 === Dice Scraper Debug Script ===');
        console.log('🌐 Current URL:', window.location.href);
        console.log('📄 Page Title:', document.title);

        const candidates = [];

        // Debug function to analyze page structure
        const debugPageStructure = () => {
            console.log('🔍 === Page Structure Debug ===');

            // Check for various candidate card selectors
            const selectors = [
                '[data-cy="profile-name-text"]',
                '.profile-name-text',
                '[class*="profile"]',
                '[class*="candidate"]',
                '[class*="result"]',
                'card',
                '[data-cy*="profile"]',
                '[data-cy*="candidate"]'
            ];

            selectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                if (elements.length > 0) {
                    console.log(`✅ Found ${elements.length} elements with selector: ${selector}`);
                    // Show first element details
                    const first = elements[0];
                    console.log(`   First element classes: ${first.className}`);
                    console.log(`   First element tag: ${first.tagName}`);
                    console.log(`   First element id: ${first.id}`);
                } else {
                    console.log(`❌ No elements found with selector: ${selector}`);
                }
            });

            // Check for data attributes
            const dataCyElements = document.querySelectorAll('[data-cy]');
            console.log(`📊 Found ${dataCyElements.length} elements with data-cy attributes`);

            // Show unique data-cy values
            const dataCyValues = new Set();
            dataCyElements.forEach(el => {
                dataCyValues.add(el.getAttribute('data-cy'));
            });
            console.log('📊 Unique data-cy values:', Array.from(dataCyValues));

            // Look for any links to profiles
            const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
            console.log(`🔗 Found ${profileLinks.length} profile links`);

            // Look for any names or candidate info
            const nameElements = document.querySelectorAll('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]');
            console.log(`👤 Found ${nameElements.length} potential name elements`);

            return {
                profileLinks: profileLinks.length,
                nameElements: nameElements.length,
                dataCyElements: dataCyElements.length
            };
        };

        // Debug page structure first
        const pageDebug = debugPageStructure();

        // Find all candidate cards/profiles with multiple selector strategies
        let candidateCards = [];

        // Strategy 1: Original selector
        candidateCards = Array.from(document.querySelectorAll('[data-cy="profile-name-text"], .profile-name-text'));
        console.log(`🎯 Strategy 1 - Found ${candidateCards.length} candidate name elements (original selector)`);

        // Strategy 2: Find cards containing profile links
        if (candidateCards.length === 0) {
            const profileLinks = document.querySelectorAll('a[href*="/employer/talent/profile/"]');
            candidateCards = profileLinks.map(link => {
                const card = link.closest('div, card, article, section');
                return card ? card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]') : link;
            }).filter(el => el);
            console.log(`🎯 Strategy 2 - Found ${candidateCards.length} candidate elements via profile links`);
        }

        // Strategy 3: Find any elements with profile-related classes
        if (candidateCards.length === 0) {
            candidateCards = Array.from(document.querySelectorAll('[class*="profile"], [class*="candidate"], [class*="result"]'))
                .map(card => card.querySelector('h1, h2, h3, h4, [class*="name"], [data-cy*="name"]'))
                .filter(el => el);
            console.log(`🎯 Strategy 3 - Found ${candidateCards.length} candidate elements via profile classes`);
        }

        // Strategy 4: Look for any name-like elements
        if (candidateCards.length === 0) {
            const allNames = document.querySelectorAll('h1, h2, h3, h4');
            candidateCards = Array.from(allNames).filter(name => {
                const text = name.textContent.trim();
                return text.length > 2 && text.length < 50 && /^[A-Za-z\s\-']+$/.test(text);
            });
            console.log(`🎯 Strategy 4 - Found ${candidateCards.length} potential name elements`);
        }

        console.log(`🎯 Final candidate elements found: ${candidateCards.length}`);

        candidateCards.forEach((nameElement, index) => {
            try {
                console.log(`👤 Processing candidate ${index + 1}...`);

                // Get the candidate card container
                let card = nameElement.closest('card, [class*="card"], [class*="profile"], [class*="result"], div');

                if (!card) {
                    console.log(`⚠️ Could not find card container for candidate ${index + 1}, using parent`);
                    card = nameElement.parentElement;
                }

                const candidate = {};
                let foundAnyData = false;

                // 0. Profile Name
                const nameElement_final = card.querySelector('[data-cy="profile-name-text"], .profile-name-text, h1, h2, h3, h4, [class*="name"], [data-cy*="name"]');
                candidate['profile-name-text'] = nameElement_final ? nameElement_final.textContent.trim() : '';

                if (candidate['profile-name-text']) {
                    console.log(`✅ Candidate ${index + 1} name: ${candidate['profile-name-text']}`);
                    foundAnyData = true;
                } else {
                    console.log(`⚠️ Candidate ${index + 1}: No name found`);
                    return; // Skip if no name found
                }

                // 0.1. Profile URL
                const linkElement = card.querySelector('a[href*="/employer/talent/profile/"]');
                if (linkElement) {
                    const href = linkElement.getAttribute('href');
                    candidate['profile-url'] = href.startsWith('http') ? href : `https://www.dice.com${href}`;
                    console.log(`🔗 Profile URL: ${candidate['profile-url']}`);
                } else {
                    candidate['profile-url'] = '';
                }

                // Helper function to find element with multiple selectors
                const findElement = (selectors) => {
                    for (const selector of selectors) {
                        const element = card.querySelector(selector);
                        if (element && element.textContent.trim()) {
                            return element;
                        }
                    }
                    return null;
                };

                // 1. Preferred Job Title
                const jobTitleElement = findElement([
                    '[data-cy="pref-prev-job-title"]',
                    '[class*="preferred"]',
                    '[class*="position"]',
                    '[class*="title"]'
                ]);
                candidate['pref-prev-job-title'] = jobTitleElement ? jobTitleElement.textContent.trim() : '';

                // 2. Location
                const locationElement = findElement([
                    '[data-cy="location"]',
                    '.location-name',
                    '[class*="location"]',
                    '[data-cy*="location"]'
                ]);
                candidate['location'] = locationElement ? locationElement.textContent.trim() : '';

                // 3. Work Experience
                const workExpElement = findElement([
                    '[data-cy="work-exp"]',
                    '.total-work-exp',
                    '[class*="experience"]',
                    '[class*="work"]'
                ]);
                candidate['work-exp'] = workExpElement ? workExpElement.textContent.trim() : '';

                // 4. Work Permit
                const workPermitElement = findElement([
                    '[data-cy="work-permit"]',
                    '.work-permits',
                    '[class*="permit"]',
                    '[class*="auth"]'
                ]);
                candidate['work-permit'] = workPermitElement ? workPermitElement.textContent.trim() : '';

                // 5. Willing to Relocate
                const relocateElement = findElement([
                    '[data-cy="willing-to-relocate"]',
                    '.willing-to-relocate',
                    '[class*="relocate"]'
                ]);
                candidate['willing-to-relocate'] = relocateElement ? relocateElement.textContent.trim() : '';

                // 6. Compensation
                const compensationElement = findElement([
                    '[data-cy="compensation"]',
                    '.salary-info',
                    '[class*="salary"]',
                    '[class*="comp"]'
                ]);
                candidate['compensation'] = compensationElement ? compensationElement.textContent.trim() : '';

                // 7. Desired Work Setting
                const workSettingElement = findElement([
                    '[data-cy="desired-work-setting"]',
                    '[class*="remote"]',
                    '[class*="hybrid"]'
                ]);
                candidate['desired-work-setting'] = workSettingElement ? workSettingElement.textContent.trim() : '';

                // 8. Date Updated
                const dateUpdatedElement = findElement([
                    '[data-cy="date-updated"]',
                    '.last-updated',
                    '[class*="updated"]'
                ]);
                candidate['date-updated'] = dateUpdatedElement ? dateUpdatedElement.textContent.trim() : '';

                // 9. Date Last Active
                const dateLastActiveElement = findElement([
                    '[data-cy="date-last-active"]',
                    '.last-active-on-brand',
                    '[class*="active"]'
                ]);
                candidate['date-last-active'] = dateLastActiveElement ? dateLastActiveElement.textContent.trim() : '';

                // 10. Likely to Switch
                const likelyToSwitchElement = findElement([
                    '[data-cy="likely-to-switch-text"]',
                    '[class*="switch"]',
                    '[class*="likely"]'
                ]);
                candidate['likely-to-switch'] = likelyToSwitchElement ? likelyToSwitchElement.textContent.trim() : '';

                // Log what we found for this candidate
                const filledFields = Object.entries(candidate).filter(([key, value]) => value && value.trim()).length;
                console.log(`📊 Candidate ${index + 1}: ${filledFields}/11 fields filled`);

                if (filledFields > 1) { // At least name + one other field
                    candidates.push(candidate);
                } else {
                    console.log(`⚠️ Candidate ${index + 1} skipped: insufficient data`);
                }

            } catch (error) {
                console.error(`❌ Error processing candidate ${index + 1}:`, error);
            }
        });

        console.log(`✅ Successfully extracted ${candidates.length} candidates with complete data`);

        // Log summary of found data
        if (candidates.length > 0) {
            console.log('📋 === Extraction Summary ===');
            candidates.forEach((candidate, i) => {
                console.log(`Candidate ${i+1}: ${candidate['profile-name-text']} | ${candidate['location']} | ${candidate['pref-prev-job-title']}`);
            });
        }

        // Return debug info along with candidates
        return {
            candidates: candidates,
            debug: {
                url: window.location.href,
                title: document.title,
                pageStructure: pageDebug,
                totalCandidates: candidates.length
            }
        };
    }
    """

    try:
        result = page.evaluate(js_code)

        # Handle the new data structure
        if isinstance(result, dict) and 'candidates' in result:
            candidates = result['candidates']
            debug_info = result['debug']

            print(f"✅ Extracted {len(candidates)} candidates from page")
            print(f"🔍 Debug info:")
            print(f"   URL: {debug_info.get('url', 'N/A')}")
            print(f"   Title: {debug_info.get('title', 'N/A')}")
            print(f"   Profile links found: {debug_info.get('pageStructure', {}).get('profileLinks', 0)}")
            print(f"   Name elements found: {debug_info.get('pageStructure', {}).get('nameElements', 0)}")
            print(f"   Data-cy elements found: {debug_info.get('pageStructure', {}).get('dataCyElements', 0)}")
        else:
            # Handle old format (just candidates array)
            candidates = result
            print(f"✅ Extracted {len(candidates)} candidates from page (legacy format)")

        return candidates
    except Exception as e:
        print(f"❌ Error extracting candidate data: {e}")
        return []

def scrape_current_page_results(page, debug_mode=False):
    """Scrape candidate data from the current page (assumes filters already applied)"""

    print("🎲 === Dice Web Scraper - Post Filter Data Extraction ===")
    print("📄 Extracting candidate data from current page")
    print("🔐 Using saved login cookies")
    if debug_mode:
        print("🔍 Debug mode enabled - browser will be visible")
    print()

    all_candidates = []

    try:
        # Console log capture for debugging
        console_messages = []
        def handle_console(msg):
            console_messages.append(f"[{msg.type}] {msg.text}")
            if debug_mode or 'error' in msg.type.lower():
                print(f"🌐 Browser Console: [{msg.type}] {msg.text}")

        page.on("console", handle_console)

        # Take initial screenshot to verify we're on the right page
        if debug_mode:
            verify_page_and_take_screenshot(page, "Before Data Extraction")

        # Check if we're on a search results page
        current_url = page.url
        page_title = page.title()

        print(f"📍 Current page: {current_url}")
        print(f"📄 Page title: {page_title}")

        if not any(indicator in current_url.lower() for indicator in ['talent/search', 'search', 'candidates']):
            print("⚠️ Warning: May not be on a search results page")
            print("🔍 This script should be run after dice-filters.py has applied filters")
        else:
            print("✅ Appears to be on a search results page")

        # Wait for results to be fully loaded
        print("⏳ Waiting for page to fully load...")
        page.wait_for_load_state('networkidle', timeout=10000)
        time.sleep(2)

        # Check if there are any results on the page
        print("🔍 Checking for search results...")
        result_elements = page.query_selector_all('[data-cy="profile-name-text"], .profile-name-text, [class*="profile"], [class*="candidate"], [class*="result"]')
        print(f"📊 Found {len(result_elements)} potential result elements")

        if len(result_elements) == 0:
            print("❌ No search results found on this page")
            print("💡 Make sure you have:")
            print("   1. Applied search filters using dice-filters.py")
            print("   2. Let the search results load completely")
            print("   3. Are on a page with actual search results")
            return []

        # Extract candidate data from current page
        print("🔍 Extracting candidate data...")
        candidates = extract_candidate_data(page)
        all_candidates.extend(candidates)

        print(f"✅ Found {len(candidates)} candidates on this page")

        # Take screenshot after data extraction
        if debug_mode:
            verify_page_and_take_screenshot(page, "After Data Extraction")

        # Show sample of extracted data
        if candidates:
            print(f"\n📋 Sample of extracted candidates:")
            for i, candidate in enumerate(candidates[:3], 1):
                print(f"   {i}. {candidate.get('profile-name-text', 'N/A')} - {candidate.get('location', 'N/A')} - {candidate.get('pref-prev-job-title', 'N/A')}")

        # Print console logs if debug mode
        if debug_mode and console_messages:
            print(f"\n📋 Browser Console Logs (last 10 messages):")
            for msg in console_messages[-10:]:
                print(f"   {msg}")

        return all_candidates

    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        if debug_mode:
            verify_page_and_take_screenshot(page, "Scraping Error")
        return []

def scrape_dice_results(max_pages=1, headless=True, debug_mode=False):
    """Main function to scrape Dice search results from existing browser session"""

    print("🎲 === Dice Web Scraper - Enhanced Version ===")
    print("📄 This script should be run AFTER dice-filters.py has applied filters")
    print(f"📄 Scraping up to {max_pages} pages")
    print("🔐 Using saved login cookies")
    if debug_mode:
        print("🔍 Debug mode enabled - browser will be visible")
    print()

    all_candidates = []

    try:
        with sync_playwright() as p:
            # Launch browser with anti-detection settings
            browser = p.chromium.launch(
                headless=not debug_mode,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )

            # Create context with random user agent
            context = browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={'width': 1920, 'height': 1080},
                ignore_https_errors=True
            )

            page = context.new_page()

            # Console log capture for debugging
            console_messages = []
            def handle_console(msg):
                console_messages.append(f"[{msg.type}] {msg.text}")
                if debug_mode or 'error' in msg.type.lower():
                    print(f"🌐 Browser Console: [{msg.type}] {msg.text}")

            page.on("console", handle_console)

            print("🔐 Setting up login cookies...")

            # Set cookies for login
            for cookie in cookies_json:
                try:
                    playwright_cookie = {
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie['domain'],
                        'path': cookie['path'],
                        'httpOnly': cookie.get('httpOnly', False),
                        'secure': cookie.get('secure', False),
                        'sameSite': 'None' if cookie.get('sameSite') is None else cookie.get('sameSite')
                    }

                    if 'expirationDate' in cookie:
                        playwright_cookie['expires'] = cookie['expirationDate']

                    context.add_cookies([playwright_cookie])
                except Exception as e:
                    print(f"Warning: Could not set cookie {cookie['name']}: {e}")

            print("✅ Cookies set successfully")

            # Navigate to talent search page (same URL that dice-filters.py uses)
            search_url = 'https://www.dice.com/employer/talent/search/'
            print("🌐 Navigating to Dice talent search page...")

            page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_load_state('networkidle', timeout=10000)
            time.sleep(3)

            # Verify we're on the correct page
            current_url = page.url
            page_title = page.title()
            print(f"📍 After navigation - URL: {current_url}")
            print(f"📄 After navigation - Title: {page_title}")

            if 'talent/search' not in current_url.lower():
                print("❌ ERROR: Not on the search page!")
                print("🔍 This indicates a redirect or navigation issue")
                page.screenshot(path='dice_scraper_navigation_error.png', full_page=True)
                return []

            print("✅ Successfully on the search page")

            # Take screenshot of initial state
            if debug_mode:
                verify_page_and_take_screenshot(page, "Initial Page Load")

            # Scrape multiple pages
            for page_num in range(1, max_pages + 1):
                print(f"\n📄 Scraping page {page_num}...")

                # Scrape current page
                candidates = scrape_current_page_results(page, debug_mode)
                all_candidates.extend(candidates)

                # Go to next page if not the last page
                if page_num < max_pages:
                    try:
                        # Look for next page button
                        next_button = page.query_selector('button[aria-label*="next"], a[aria-label*="next"], .pagination-next, [data-cy="next-page"]')
                        if next_button:
                            next_button.click()
                            page.wait_for_load_state('domcontentloaded', timeout=15000)
                            time.sleep(2)
                            print("➡️ Navigated to next page")
                        else:
                            print("ℹ️ No next page button found, ending scraping")
                            break
                    except Exception as e:
                        print(f"⚠️ Error navigating to next page: {e}")
                        break

            browser.close()

    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return []

    print(f"\n✅ Scraping completed! Total candidates found: {len(all_candidates)}")
    return all_candidates

def save_to_excel(candidates, filename="dice_candidates.xlsx"):
    """Save candidate data to Excel file"""

    if not candidates:
        print("❌ No candidates to save")
        return

    # Define column order
    columns = [
        'profile-name-text',
        'profile-url',
        'pref-prev-job-title',
        'location',
        'work-exp',
        'work-permit',
        'willing-to-relocate',
        'compensation',
        'desired-work-setting',
        'date-updated',
        'date-last-active',
        'likely-to-switch'
    ]

    # Create DataFrame
    df = pd.DataFrame(candidates)

    # Reorder columns according to our defined order
    df = df.reindex(columns=columns, fill_value='')

    # Save to Excel
    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Data saved to {filename}")
        print(f"📊 Total records: {len(df)}")
        print(f"📝 Columns: {', '.join(df.columns)}")

        # Show sample data
        print("\n📋 Sample data:")
        print(df.head(3).to_string(index=False))

    except Exception as e:
        print(f"❌ Error saving to Excel: {e}")
        # Fallback to CSV
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"✅ Data saved to CSV instead: {csv_filename}")

def main():
    """Main function with enhanced command line options"""
    import sys

    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        print("🎲 Dice Web Scraper - Post Filter Data Extraction")
        print("\nUsage:")
        print("  python dice_web_scrap.py [options]")
        print("\nImportant:")
        print("  ⚠️  Run this script AFTER dice-filters.py has applied search filters!")
        print("\nOptions:")
        print("  --debug, --visible     Run in visible browser mode for debugging")
        print("  --pages N             Number of pages to scrape (default: 1, max: 10)")
        print("  --help, -h            Show this help message")
        print("\nDebug Features:")
        print("  • Comprehensive console logging")
        print("  • Step-by-step navigation verification")
        print("  • Screenshots at each major step")
        print("  • Real-time browser console output")
        print("  • Candidate data extraction debugging")
        print("\nWorkflow:")
        print("  1. First run: python dice-filters.py --visible")
        print("  2. Let filters apply and search complete")
        print("  3. Then run: python dice_web_scrap.py --debug --pages 3")
        print("\nExamples:")
        print("  python dice_web_scrap.py                    # Run in headless mode, 1 page")
        print("  python dice_web_scrap.py --debug               # Run in visible mode for debugging")
        print("  python dice_web_scrap.py --pages 3            # Scrape 3 pages")
        print("  python dice_web_scrap.py --debug --pages 5     # Debug mode, 5 pages")
        return

    print("🎲 === Dice Web Scraper - Post Filter Data Extraction ===")
    print("📋 This script will:")
    print("   1. Login using saved cookies")
    print("   2. Navigate to talent search page")
    print("   3. Extract candidate data from existing search results")
    print("   4. Save to Excel file with timestamp")
    print("\n💡 Make sure you have already run dice-filters.py to apply search filters!")

    # Parse command line arguments
    debug_mode = '--debug' in sys.argv or '--visible' in sys.argv

    # Get number of pages from command line or user input
    max_pages = 1
    for i, arg in enumerate(sys.argv):
        if arg == '--pages' and i + 1 < len(sys.argv):
            try:
                max_pages = int(sys.argv[i + 1])
                max_pages = max(1, min(max_pages, 10))  # Limit to 10 pages
            except:
                max_pages = 1
                print("⚠️ Invalid page number, using default: 1")

    print(f"📄 Scraping up to {max_pages} pages")
    print(f"🔐 Using saved login cookies")
    if debug_mode:
        print("🔍 Debug mode enabled - browser will be visible")
    print()

    # Scrape results
    candidates = scrape_dice_results(max_pages=max_pages, headless=not debug_mode, debug_mode=debug_mode)

    if candidates:
        # Save to Excel with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"dice_candidates_{timestamp}.xlsx"
        save_to_excel(candidates, filename)

        print(f"\n🎉 Scraping completed successfully!")
        print(f"📁 File saved: {filename}")
        print(f"👥 Total candidates: {len(candidates)}")

        if debug_mode:
            print("\n🐛 Debug browser window will remain open for inspection")
            print("📸 Screenshots saved in current directory")
    else:
        print("\n❌ No candidates found. Please check:")
        print("   • Are you logged in correctly? (Check cookies)")
        print("   • Did you run dice-filters.py first to apply search filters?")
        print("   • Are there search results on the page?")
        print("   • Try running with --debug flag to see what's happening")

if __name__ == "__main__":
    main()