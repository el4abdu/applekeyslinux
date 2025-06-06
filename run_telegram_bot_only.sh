#!/bin/bash

# Script to run the Telegram bot only (assumes key generator service is already running)

# Make sure the script is executable
chmod +x "$0"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Install required packages if not already installed
echo "Installing required packages..."
pip3 install python-telegram-bot==20.7 --upgrade

# Set Telegram token from environment variable or use default
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c}"
export TELEGRAM_TOKEN

# Check if the key generator service is running
if ! pgrep -f "python3 key_generator_service.py" > /dev/null; then
    echo "Warning: Key generator service does not appear to be running."
    echo "You should start it first with ./run_generator_background.sh"
    
    # Ask if the user wants to continue
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Starting Telegram bot..."
python3 telegram_bot_with_generator.py 