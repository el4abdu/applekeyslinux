#!/usr/bin/env python3
"""
Ubuntu-compatible version of Apple Entertainment Offer Code Extractor
"""

import os
import re
import time
import logging
import argparse
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Main URL
MAIN_URL = "https://redeem.services.apple/card-apple-entertainment-offer-1-2025"

# Service specific settings
SERVICES = {
    "tv": {
        "name": "Apple TV+",
        "button_xpath": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/button",
        "output_file": "tv_plus_codes.txt"
    },
    "music": {
        "name": "Apple Music",
        "button_xpath": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]/button",
        "output_file": "music_codes.txt"
    },
    "arcade": {
        "name": "Apple Arcade",
        "button_xpath": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[3]/div/div[2]/button",
        "output_file": "arcade_codes.txt"
    },
    "fitness": {
        "name": "Apple Fitness+",
        "button_xpath": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[4]/div/div[2]/button",
        "output_file": "fitness_codes.txt"
    },
    "news": {
        "name": "Apple News+",
        "button_xpath": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[5]/div/div[2]/button",
        "output_file": "news_codes.txt"
    }
}

def setup_driver():
    """
    Set up Chrome WebDriver using system Chrome
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Use system Chrome and ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise

def extract_code_from_url(url):
    """
    Extract the redemption code from the authentication URL
    """
    try:
        if "code=" in url:
            code_match = re.search(r'code=([A-Z0-9]+)', url)
            if code_match:
                return code_match.group(1)
        
        logger.warning(f"Could not extract code from URL: {url}")
        return None
    except Exception as e:
        logger.error(f"Error extracting code from URL: {e}")
        return None

def get_redemption_code(driver, service_key):
    """
    Navigate to the offer page and extract a redemption code for the specified service
    """
    service_info = SERVICES[service_key]
    button_xpath = service_info["button_xpath"]
    service_name = service_info["name"]
    
    try:
        # Navigate to the main page
        logger.info(f"Navigating to {MAIN_URL}")
        driver.get(MAIN_URL)
        
        # Wait for page to load
        time.sleep(5)
        
        # Wait for the button to be clickable
        logger.info(f"Waiting for {service_name} redemption button")
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        
        # Click the button
        logger.info(f"Clicking {service_name} redemption button")
        button.click()
        
        # Wait for redirect and get the URL
        time.sleep(3)
        current_url = driver.current_url
        logger.info(f"Redirected to: {current_url}")
        
        # Extract the code from the URL
        code = extract_code_from_url(current_url)
        if code:
            logger.info(f"Successfully extracted code for {service_name}: {code}")
            return code
        else:
            logger.warning(f"Failed to extract code for {service_name}")
            return None
            
    except Exception as e:
        logger.error(f"Error getting redemption code for {service_name}: {e}")
        return None

def save_code(code, service_key):
    """
    Save the extracted code to the appropriate output file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("codes", exist_ok=True)
        
        output_file = os.path.join("codes", SERVICES[service_key]["output_file"])
        
        with open(output_file, 'a') as f:
            f.write(f"{code}\n")
            
        logger.info(f"Saved code {code} to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving code: {e}")
        return False

def ensure_chrome_installed():
    """
    Ensure Chrome is installed on the system
    """
    try:
        subprocess.run(["google-chrome", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Chrome is installed")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("Chrome not found, attempting to install...")
        try:
            # Install Chrome
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "wget"], check=True)
            subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"], check=True)
            subprocess.run(["rm", "google-chrome-stable_current_amd64.deb"], check=True)
            
            # Verify installation
            subprocess.run(["google-chrome", "--version"], check=True, stdout=subprocess.PIPE)
            logger.info("Chrome installed successfully")
            return True
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to install Chrome: {e}")
            return False

def ensure_chromedriver_installed():
    """
    Ensure ChromeDriver is installed on the system
    """
    try:
        subprocess.run(["chromedriver", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("ChromeDriver is installed")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("ChromeDriver not found, attempting to install...")
        try:
            # Install ChromeDriver
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "chromium-chromedriver"], check=True)
            
            # Create symlink
            subprocess.run(["sudo", "ln", "-sf", "/usr/lib/chromium-browser/chromedriver", "/usr/bin/chromedriver"], check=True)
            
            # Verify installation
            subprocess.run(["chromedriver", "--version"], check=True, stdout=subprocess.PIPE)
            logger.info("ChromeDriver installed successfully")
            return True
        except subprocess.SubprocessError as e:
            logger.error(f"Failed to install ChromeDriver: {e}")
            return False

def main():
    """
    Main function to parse arguments and run the code extraction process
    """
    parser = argparse.ArgumentParser(description='Extract Apple Entertainment offer codes')
    parser.add_argument('--count', type=int, default=1, help='Number of codes to extract')
    parser.add_argument('--service', type=str, default='tv', choices=SERVICES.keys(),
                        help='Service to extract codes for (tv, music, arcade, fitness, news)')
    args = parser.parse_args()
    
    logger.info(f"Starting extraction of {args.count} {SERVICES[args.service]['name']} codes")
    
    # Ensure Chrome and ChromeDriver are installed
    if not ensure_chrome_installed() or not ensure_chromedriver_installed():
        logger.error("Failed to set up Chrome environment. Exiting.")
        return
    
    try:
        driver = setup_driver()
        
        codes = []
        for i in range(args.count):
            logger.info(f"Extracting code {i+1}/{args.count}")
            code = get_redemption_code(driver, args.service)
            if code:
                codes.append(code)
                save_code(code, args.service)
            
            # Add a delay between requests to avoid being detected as a bot
            time.sleep(2)
            
        driver.quit()
        
        logger.info(f"Extraction complete. {len(codes)} codes extracted.")
        print(f"\nExtracted codes:")
        for code in codes:
            print(code)
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        
    logger.info("Script execution completed")

if __name__ == "__main__":
    main()
