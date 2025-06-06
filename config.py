"""
Configuration settings for the Apple Entertainment Offer Code Extractor
"""

# URLs
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

# Browser settings
BROWSER_SETTINGS = {
    "headless": True,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "window_width": 1920,
    "window_height": 1080
}

# Timeouts (in seconds)
TIMEOUTS = {
    "page_load": 30,
    "element_wait": 10,
    "between_requests": 2
}

# Output directory for saving codes
OUTPUT_DIR = "codes"

# Log file
LOG_FILE = "extraction.log" 