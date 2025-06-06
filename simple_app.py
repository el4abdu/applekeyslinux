#!/usr/bin/env python3
"""
Super simple version of Apple Entertainment Offer Code Extractor
Designed to work with minimal dependencies on Ubuntu
Uses private browsing with no cookies to get different keys
"""

import os
import time
import re
import argparse
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Main URL
URL = "https://redeem.services.apple/card-apple-entertainment-offer-1-2025"

# Service button XPaths
SERVICE_BUTTONS = {
    "tv": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/button",
    "music": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]/button",
    "arcade": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[3]/div/div[2]/button",
    "fitness": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[4]/div/div[2]/button",
    "news": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[5]/div/div[2]/button"
}

# Service output files
SERVICE_FILES = {
    "tv": "tv_plus_codes.txt",
    "music": "music_codes.txt",
    "arcade": "arcade_codes.txt",
    "fitness": "fitness_codes.txt",
    "news": "news_codes.txt"
}

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

def setup_driver():
    """Set up Chrome WebDriver with private browsing and no cookies"""
    options = Options()
    
    # Use incognito mode for private browsing
    options.add_argument("--incognito")
    
    # Disable cookies
    options.add_argument("--disable-cookie-encryption")
    options.add_argument("--disable-cookie-storage")
    options.add_argument("--block-new-web-content")
    
    # Use a random user agent
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")
    print(f"Using user agent: {user_agent}")
    
    # Other common options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Try different Chrome/Chromium binaries
    chrome_binaries = [
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/snap/bin/chromium"
    ]
    
    driver = None
    for binary in chrome_binaries:
        if os.path.exists(binary):
            print(f"Using Chrome binary at: {binary}")
            options.binary_location = binary
            try:
                driver = webdriver.Chrome(options=options)
                break
            except Exception as e:
                print(f"Failed to initialize WebDriver with {binary}: {e}")
    
    if driver is None:
        print("Could not find a working Chrome/Chromium binary. Please install Chrome or Chromium.")
        return None
        
    return driver

def clear_cache_and_cookies(driver):
    """Clear cache and cookies between requests"""
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.delete_all_cookies()

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Extract Apple Entertainment offer codes')
    parser.add_argument('--count', type=int, default=1, help='Number of codes to extract')
    parser.add_argument('--service', type=str, default='tv', choices=SERVICE_BUTTONS.keys(),
                        help='Service to extract codes for (tv, music, arcade, fitness, news)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    args = parser.parse_args()
    
    print(f"Starting extraction of {args.count} {args.service} codes")
    
    # Create output directory
    os.makedirs("codes", exist_ok=True)
    output_file = os.path.join("codes", SERVICE_FILES[args.service])
    
    # Get codes
    codes = []
    for i in range(args.count):
        print(f"\nGetting code {i+1}/{args.count}...")
        
        # Create a new browser instance for each code
        driver = setup_driver()
        if driver is None:
            print("Failed to create WebDriver. Exiting.")
            return
            
        # Add headless mode if requested (after driver is initialized)
        if args.headless:
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
        
        try:
            # Navigate to page
            print(f"Navigating to {URL}")
            driver.get(URL)
            time.sleep(5)
            
            # Click button
            print(f"Clicking {args.service} button")
            button = driver.find_element(By.XPATH, SERVICE_BUTTONS[args.service])
            button.click()
            time.sleep(3)
            
            # Get URL and extract code
            url = driver.current_url
            print(f"Redirected to: {url}")
            
            if "code=" in url:
                code = re.search(r'code=([A-Z0-9]+)', url).group(1)
                codes.append(code)
                print(f"Extracted code: {code}")
                
                # Save code to file
                with open(output_file, 'a') as f:
                    f.write(f"{code}\n")
                print(f"Saved code to {output_file}")
            else:
                print("No code found in URL")
        except Exception as e:
            print(f"Error getting code: {e}")
        
        # Close driver
        driver.quit()
        
        # Wait between requests
        wait_time = random.randint(3, 7)
        print(f"Waiting {wait_time} seconds before next request...")
        time.sleep(wait_time)
    
    # Print all codes
    print("\nAll extracted codes:")
    for code in codes:
        print(code)

if __name__ == "__main__":
    main() 