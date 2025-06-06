#!/bin/bash

# Script to run the key generator service and Telegram bot together

# Make sure the script is executable
chmod +x "$0"

# Create codes directory if it doesn't exist
mkdir -p codes

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
pip3 install selenium python-telegram-bot==20.7 --upgrade

# Check if Chrome/Chromium is installed
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null; then
    echo "Chrome or Chromium is not installed. Installing Chromium..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y chromium-browser
    elif command -v yum &> /dev/null; then
        sudo yum install -y chromium
    else
        echo "Could not install Chromium. Please install Chrome or Chromium manually."
        exit 1
    fi
fi

# Check if ChromeDriver is installed
if ! command -v chromedriver &> /dev/null; then
    echo "ChromeDriver is not installed. Installing ChromeDriver..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y chromium-chromedriver
    else
        echo "Could not install ChromeDriver. Please install ChromeDriver manually."
        exit 1
    fi
fi

# Set Telegram token from environment variable or use default
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c}"
export TELEGRAM_TOKEN

echo "Starting key generator service in the background..."
python3 key_generator_service.py > generator.log 2>&1 &
GENERATOR_PID=$!

# Wait for the generator to initialize
sleep 5

echo "Starting Telegram bot..."
python3 telegram_bot_with_generator.py

# If the bot exits, also kill the generator service
kill $GENERATOR_PID 