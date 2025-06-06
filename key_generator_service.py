#!/usr/bin/env python3
"""
Background Key Generator Service for Apple Entertainment Codes
Continuously generates keys for different services and stores them in files
"""

import os
import time
import re
import random
import logging
import threading
import queue
import signal
import sys
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configure logging
logging.basicConfig(
    filename='generator.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Main URL
URL = "https://redeem.services.apple/card-apple-entertainment-offer-1-2025"

# Service button XPaths
SERVICE_BUTTONS = {
    "tv": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/button",
    "music": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[2]/div/div[2]/button",
    "arcade": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[3]/div/div[2]/button",
    "fitness": "/html/body/div[1]/main/div/div[1]/div/div/div/div[1]/div[4]/div/div[2]/button",
}

# Service output files
SERVICE_FILES = {
    "tv": "codes/tv_plus_codes.txt",
    "music": "codes/music_codes.txt",
    "arcade": "codes/arcade_codes.txt",
    "fitness": "codes/fitness_codes.txt",
}

# Service display names
SERVICE_NAMES = {
    "tv": "Apple TV+",
    "music": "Apple Music",
    "arcade": "Apple Arcade",
    "fitness": "Apple Fitness+",
}

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Minimum number of codes to keep in storage for each service
MIN_CODES = 5

# Maximum number of codes to store for each service
MAX_CODES = 20

# Flag to control service shutdown
running = True

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
    
    # Other common options
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Try to use WebDriver Manager first
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("Successfully initialized WebDriver using WebDriver Manager")
        return driver
    except Exception as e:
        logger.warning(f"Failed to initialize WebDriver using WebDriver Manager: {e}")
        logger.info("Trying alternative methods...")
    
    # Try different Chrome/Chromium binaries based on OS
    if platform.system() == "Windows":
        chrome_binaries = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Chromium\Application\chrome.exe",
            r"C:\Program Files (x86)\Chromium\Application\chrome.exe"
        ]
    else:  # Linux/Mac
        chrome_binaries = [
            "/usr/bin/chromium-browser",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium",
            "/snap/bin/chromium"
        ]
    
    driver = None
    for binary in chrome_binaries:
        if os.path.exists(binary):
            options.binary_location = binary
            try:
                driver = webdriver.Chrome(options=options)
                logger.info(f"Successfully initialized WebDriver with {binary}")
                break
            except Exception as e:
                logger.error(f"Failed to initialize WebDriver with {binary}: {e}")
    
    if driver is None:
        logger.error("Could not find a working Chrome/Chromium binary. Please install Chrome or Chromium.")
        return None
        
    return driver

def get_code(service):
    """Extract a code for the specified service"""
    logger.info(f"Getting code for {SERVICE_NAMES[service]}")
    
    # Create a new browser instance
    driver = setup_driver()
    if driver is None:
        logger.error("Failed to create WebDriver.")
        return None
    
    try:
        # Navigate to page
        driver.get(URL)
        time.sleep(5)
        
        # Click button
        button = driver.find_element(By.XPATH, SERVICE_BUTTONS[service])
        button.click()
        time.sleep(3)
        
        # Get URL and extract code
        url = driver.current_url
        
        if "code=" in url:
            code = re.search(r'code=([A-Z0-9]+)', url).group(1)
            logger.info(f"Extracted {SERVICE_NAMES[service]} code: {code}")
            return code
        else:
            logger.warning(f"No code found in URL for {SERVICE_NAMES[service]}")
            return None
    except Exception as e:
        logger.error(f"Error getting {SERVICE_NAMES[service]} code: {e}")
        return None
    finally:
        # Close driver
        driver.quit()

def save_code(service, code):
    """Save code to the appropriate file"""
    os.makedirs("codes", exist_ok=True)
    
    with open(SERVICE_FILES[service], 'a') as f:
        f.write(f"{code}\n")
    
    logger.info(f"Saved {SERVICE_NAMES[service]} code to {SERVICE_FILES[service]}")

def count_codes(service):
    """Count how many codes are stored for a service"""
    if not os.path.exists(SERVICE_FILES[service]):
        return 0
    
    with open(SERVICE_FILES[service], 'r') as f:
        return len(f.readlines())

def get_stored_code(service):
    """Get a stored code for the specified service and remove it from storage"""
    if not os.path.exists(SERVICE_FILES[service]):
        return None
    
    try:
        with open(SERVICE_FILES[service], 'r') as f:
            codes = f.readlines()
        
        if not codes:
            return None
        
        # Get the first code
        code = codes[0].strip()
        
        # Write back the remaining codes
        with open(SERVICE_FILES[service], 'w') as f:
            f.writelines(codes[1:])
        
        logger.info(f"Retrieved stored {SERVICE_NAMES[service]} code: {code}")
        return code
    except Exception as e:
        logger.error(f"Error retrieving stored {SERVICE_NAMES[service]} code: {e}")
        return None

def service_worker(service, status_queue):
    """Worker thread for a specific service"""
    logger.info(f"Starting {SERVICE_NAMES[service]} worker thread")
    
    while running:
        try:
            # Check how many codes we have stored
            code_count = count_codes(service)
            status_queue.put((service, code_count))
            
            # If we have enough codes, sleep for a while
            if code_count >= MAX_CODES:
                time.sleep(60)  # Sleep for 1 minute
                continue
            
            # Generate a new code
            code = get_code(service)
            if code:
                save_code(service, code)
            
            # Random delay between requests
            delay = random.randint(5, 15)
            time.sleep(delay)
            
        except Exception as e:
            logger.error(f"Error in {SERVICE_NAMES[service]} worker: {e}")
            time.sleep(30)  # Sleep longer if there's an error

def status_monitor(status_queue):
    """Monitor thread to display status of code generation"""
    status = {service: 0 for service in SERVICE_BUTTONS}
    
    while running:
        try:
            # Update status with any new information from the queue
            while not status_queue.empty():
                service, count = status_queue.get(block=False)
                status[service] = count
            
            # Display status
            logger.info("Current code counts:")
            for service in SERVICE_BUTTONS:
                logger.info(f"  {SERVICE_NAMES[service]}: {status[service]} codes")
            
            time.sleep(60)  # Update status every minute
            
        except Exception as e:
            logger.error(f"Error in status monitor: {e}")
            time.sleep(30)

def signal_handler(sig, frame):
    """Handle Ctrl+C and other termination signals"""
    global running
    logger.info("Shutting down key generator service...")
    running = False
    sys.exit(0)

def main():
    """Main function to start the key generator service"""
    logger.info("Starting Apple Entertainment Code Generator Service")
    
    # Create codes directory
    os.makedirs("codes", exist_ok=True)
    
    # Register signal handler for Unix systems
    if platform.system() != "Windows":
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    # Create status queue
    status_queue = queue.Queue()
    
    # Start worker threads
    threads = []
    for service in SERVICE_BUTTONS:
        thread = threading.Thread(target=service_worker, args=(service, status_queue))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(2)  # Stagger thread starts
    
    # Start status monitor
    monitor_thread = threading.Thread(target=status_monitor, args=(status_queue,))
    monitor_thread.daemon = True
    monitor_thread.start()
    
    logger.info("All worker threads started. Press Ctrl+C to stop.")
    
    try:
        # Keep the main thread alive
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")
        running = False

if __name__ == "__main__":
    main()
