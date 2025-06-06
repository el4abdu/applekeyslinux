#!/usr/bin/env python3
"""
Apple Entertainment Offer Code Extractor

This script automates the process of extracting Apple Entertainment offer codes
from the Apple Card promotion page.
"""

import os
import re
import time
import logging
import argparse
from urllib.parse import urlparse, parse_qs
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Import configuration
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_driver():
    """
    Set up and configure the Chrome WebDriver
    
    Returns:
        webdriver: Configured Chrome WebDriver instance
    """
    chrome_options = Options()
    
    if config.BROWSER_SETTINGS["headless"]:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument(f"--window-size={config.BROWSER_SETTINGS['window_width']},{config.BROWSER_SETTINGS['window_height']}")
    chrome_options.add_argument(f"user-agent={config.BROWSER_SETTINGS['user_agent']}")
    
    # Additional options for AWS Linux environment
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(config.TIMEOUTS["page_load"])
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise


def extract_code_from_url(url):
    """
    Extract the redemption code from the authentication URL
    
    Args:
        url (str): The authentication URL containing the code
        
    Returns:
        str: The extracted redemption code or None if not found
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        if 'returnPath' in query_params:
            return_path = query_params['returnPath'][0]
            if 'code=' in return_path:
                code_match = re.search(r'code=([A-Z0-9]+)', return_path)
                if code_match:
                    return code_match.group(1)
        
        # Alternative method if the above doesn't work
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
    
    Args:
        driver (webdriver): Chrome WebDriver instance
        service_key (str): Key of the service to get code for (e.g., 'tv', 'music')
        
    Returns:
        str: The extracted redemption code or None if failed
    """
    service_info = config.SERVICES[service_key]
    button_xpath = service_info["button_xpath"]
    service_name = service_info["name"]
    
    try:
        # Navigate to the main page
        logger.info(f"Navigating to {config.MAIN_URL}")
        driver.get(config.MAIN_URL)
        
        # Wait for the button to be clickable
        logger.info(f"Waiting for {service_name} redemption button")
        button = WebDriverWait(driver, config.TIMEOUTS["element_wait"]).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        
        # Click the button
        logger.info(f"Clicking {service_name} redemption button")
        button.click()
        
        # Wait for redirect and get the URL
        time.sleep(config.TIMEOUTS["between_requests"])
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
            
    except TimeoutException:
        logger.error(f"Timeout waiting for {service_name} button")
        return None
    except NoSuchElementException:
        logger.error(f"Could not find {service_name} button using XPath: {button_xpath}")
        return None
    except Exception as e:
        logger.error(f"Error getting redemption code for {service_name}: {e}")
        return None


def save_code(code, service_key):
    """
    Save the extracted code to the appropriate output file
    
    Args:
        code (str): The redemption code to save
        service_key (str): Key of the service the code is for
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        output_file = os.path.join(config.OUTPUT_DIR, config.SERVICES[service_key]["output_file"])
        
        with open(output_file, 'a') as f:
            f.write(f"{code}\n")
            
        logger.info(f"Saved code {code} to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving code: {e}")
        return False


def main():
    """
    Main function to parse arguments and run the code extraction process
    """
    parser = argparse.ArgumentParser(description='Extract Apple Entertainment offer codes')
    parser.add_argument('--count', type=int, default=1, help='Number of codes to extract')
    parser.add_argument('--service', type=str, default='tv', choices=config.SERVICES.keys(),
                        help='Service to extract codes for (tv, music, arcade, fitness, news)')
    args = parser.parse_args()
    
    logger.info(f"Starting extraction of {args.count} {config.SERVICES[args.service]['name']} codes")
    
    try:
        driver = setup_driver()
        
        codes = []
        for i in tqdm(range(args.count), desc=f"Extracting {args.service} codes"):
            code = get_redemption_code(driver, args.service)
            if code:
                codes.append(code)
                save_code(code, args.service)
            
            # Add a delay between requests to avoid being detected as a bot
            time.sleep(config.TIMEOUTS["between_requests"])
            
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