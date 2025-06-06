#!/usr/bin/env python3
"""
Apple Entertainment Offer Code Extractor with Telegram Bot Integration
Designed to work with minimal dependencies on Ubuntu
Uses private browsing with no cookies to get different keys
"""

import os
import time
import re
import argparse
import random
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Try to import telegram libraries, but don't fail if not installed
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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

# Service display names
SERVICE_NAMES = {
    "tv": "Apple TV+",
    "music": "Apple Music",
    "arcade": "Apple Arcade",
    "fitness": "Apple Fitness+",
    "news": "Apple News+"
}

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
ALLOWED_USERS = [int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id]

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
    logger.info(f"Using user agent: {user_agent}")
    
    # Other common options
    options.add_argument("--headless")
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
            logger.info(f"Using Chrome binary at: {binary}")
            options.binary_location = binary
            try:
                driver = webdriver.Chrome(options=options)
                break
            except Exception as e:
                logger.error(f"Failed to initialize WebDriver with {binary}: {e}")
    
    if driver is None:
        logger.error("Could not find a working Chrome/Chromium binary. Please install Chrome or Chromium.")
        return None
        
    return driver

def clear_cache_and_cookies(driver):
    """Clear cache and cookies between requests"""
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.delete_all_cookies()

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
        logger.info(f"Navigating to {URL}")
        driver.get(URL)
        time.sleep(5)
        
        # Click button
        logger.info(f"Clicking {service} button")
        button = driver.find_element(By.XPATH, SERVICE_BUTTONS[service])
        button.click()
        time.sleep(3)
        
        # Get URL and extract code
        url = driver.current_url
        logger.info(f"Redirected to: {url}")
        
        if "code=" in url:
            code = re.search(r'code=([A-Z0-9]+)', url).group(1)
            logger.info(f"Extracted code: {code}")
            
            # Save code to file
            os.makedirs("codes", exist_ok=True)
            output_file = os.path.join("codes", SERVICE_FILES[service])
            with open(output_file, 'a') as f:
                f.write(f"{code}\n")
            logger.info(f"Saved code to {output_file}")
            
            return code
        else:
            logger.warning("No code found in URL")
            return None
    except Exception as e:
        logger.error(f"Error getting code: {e}")
        return None
    finally:
        # Close driver
        driver.quit()

def get_multiple_codes(service, count):
    """Extract multiple codes for the specified service"""
    codes = []
    for i in range(count):
        logger.info(f"Getting code {i+1}/{count}...")
        
        code = get_code(service)
        if code:
            codes.append(code)
        
        # Wait between requests
        if i < count - 1:  # Don't wait after the last request
            wait_time = random.randint(3, 7)
            logger.info(f"Waiting {wait_time} seconds before next request...")
            time.sleep(wait_time)
    
    return codes

# Telegram Bot Functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("Apple TV+", callback_data="tv"),
            InlineKeyboardButton("Apple Music", callback_data="music"),
        ],
        [
            InlineKeyboardButton("Apple Arcade", callback_data="arcade"),
            InlineKeyboardButton("Apple Fitness+", callback_data="fitness"),
        ],
        [
            InlineKeyboardButton("Apple News+", callback_data="news"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to Apple Entertainment Code Generator Bot!\n\n"
        "Choose a service to generate a code:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await query.answer("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized button press by user {user_id}")
        return
    
    await query.answer()
    
    service = query.data
    if service in SERVICE_BUTTONS:
        await query.edit_message_text(text=f"Generating code for {SERVICE_NAMES[service]}...\nThis may take a moment.")
        
        # Run code extraction in a separate thread to avoid blocking
        code = await context.application.loop.run_in_executor(None, get_code, service)
        
        if code:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await query.edit_message_text(
                text=f"✅ *{SERVICE_NAMES[service]} Code*\n\n"
                     f"`{code}`\n\n"
                     f"Generated at: {timestamp}\n\n"
                     f"To get another code, use /start",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                text="❌ Failed to generate code. Please try again later.\n\n"
                     "To try again, use /start"
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    await update.message.reply_text(
        "This bot generates Apple Entertainment offer codes.\n\n"
        "Available commands:\n"
        "/start - Start the bot and select a service\n"
        "/help - Show this help message\n"
        "/generate [service] [count] - Generate codes (e.g., /generate tv 3)\n\n"
        "Available services: tv, music, arcade, fitness, news"
    )

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate codes based on command arguments."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    args = context.args
    
    if len(args) < 1:
        await update.message.reply_text(
            "Please specify a service and optionally a count.\n"
            "Example: /generate tv 3\n\n"
            "Available services: tv, music, arcade, fitness, news"
        )
        return
    
    service = args[0].lower()
    if service not in SERVICE_BUTTONS:
        await update.message.reply_text(
            f"Unknown service: {service}\n\n"
            "Available services: tv, music, arcade, fitness, news"
        )
        return
    
    count = 1
    if len(args) >= 2:
        try:
            count = int(args[1])
            if count < 1:
                count = 1
            elif count > 5:  # Limit to 5 codes at once
                count = 5
        except ValueError:
            pass
    
    await update.message.reply_text(f"Generating {count} code(s) for {SERVICE_NAMES[service]}...\nThis may take a moment.")
    
    # Run code extraction in a separate thread to avoid blocking
    codes = await context.application.loop.run_in_executor(None, get_multiple_codes, service, count)
    
    if codes:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"✅ *{SERVICE_NAMES[service]} Codes*\n\n"
        for i, code in enumerate(codes, 1):
            message += f"{i}. `{code}`\n"
        message += f"\nGenerated at: {timestamp}\n\nTo get more codes, use /start"
        
        await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ Failed to generate codes. Please try again later.\n\n"
            "To try again, use /start"
        )

def run_telegram_bot():
    """Run the Telegram bot."""
    if not TELEGRAM_AVAILABLE:
        logger.error("Telegram libraries not installed. Run 'pip install python-telegram-bot' to use the Telegram bot.")
        return
    
    if not TELEGRAM_TOKEN:
        logger.error("Telegram token not set. Please set the TELEGRAM_TOKEN environment variable.")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CallbackQueryHandler(button))
    
    # Start the Bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to parse arguments and run the code extraction process."""
    parser = argparse.ArgumentParser(description='Extract Apple Entertainment offer codes')
    parser.add_argument('--count', type=int, default=1, help='Number of codes to extract')
    parser.add_argument('--service', type=str, default='tv', choices=SERVICE_BUTTONS.keys(),
                        help='Service to extract codes for (tv, music, arcade, fitness, news)')
    parser.add_argument('--telegram', action='store_true', help='Run as a Telegram bot')
    args = parser.parse_args()
    
    if args.telegram:
        run_telegram_bot()
    else:
        logger.info(f"Starting extraction of {args.count} {SERVICE_NAMES[args.service]} codes")
        codes = get_multiple_codes(args.service, args.count)
        
        if codes:
            logger.info("All extracted codes:")
            for code in codes:
                print(code)
        else:
            logger.error("Failed to extract any codes.")

if __name__ == "__main__":
    main()
