#!/usr/bin/env python3
"""
Super simple version of Apple Entertainment Offer Code Extractor
Designed to work with minimal dependencies on Ubuntu
"""

import os
import time
import re
import argparse
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

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Extract Apple Entertainment offer codes')
    parser.add_argument('--count', type=int, default=1, help='Number of codes to extract')
    parser.add_argument('--service', type=str, default='tv', choices=SERVICE_BUTTONS.keys(),
                        help='Service to extract codes for (tv, music, arcade, fitness, news)')
    args = parser.parse_args()
    
    print(f"Starting extraction of {args.count} {args.service} codes")
    
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
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
        return
    
    # Create output directory
    os.makedirs("codes", exist_ok=True)
    output_file = os.path.join("codes", SERVICE_FILES[args.service])
    
    # Get codes
    codes = []
    for i in range(args.count):
        print(f"Getting code {i+1}/{args.count}...")
        
        try:
            # Navigate to page
            driver.get(URL)
            time.sleep(5)
            
            # Click button
            button = driver.find_element(By.XPATH, SERVICE_BUTTONS[args.service])
            button.click()
            time.sleep(3)
            
            # Get URL and extract code
            url = driver.current_url
            print(f"URL: {url}")
            
            if "code=" in url:
                code = re.search(r'code=([A-Z0-9]+)', url).group(1)
                codes.append(code)
                print(f"Code: {code}")
                
                # Save code to file
                with open(output_file, 'a') as f:
                    f.write(f"{code}\n")
                print(f"Saved code to {output_file}")
            else:
                print("No code found in URL")
        except Exception as e:
            print(f"Error getting code: {e}")
        
        time.sleep(2)
    
    # Print all codes
    print("\nAll extracted codes:")
    for code in codes:
        print(code)
    
    # Close driver
    driver.quit()

if __name__ == "__main__":
    main() 