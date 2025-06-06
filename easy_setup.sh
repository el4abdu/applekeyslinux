#!/bin/bash

# Easy setup script for Telegram Bot on Ubuntu
echo "Setting up environment for Apple Entertainment Telegram Bot..."

# Update package lists
sudo apt update -y

# Install Chromium and ChromeDriver
echo "Installing Chromium and ChromeDriver..."
sudo apt install -y chromium-browser chromium-chromedriver

# Install Python and pip
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip

# Install Python dependencies for Telegram bot
echo "Installing Python dependencies..."
pip3 install python-telegram-bot selenium python-dotenv

# Create directories
mkdir -p codes

# Make the run script executable
chmod +x run_telegram_bot.sh

echo "Setup complete!"
echo "To run the bot, simply execute:"
echo "./run_telegram_bot.sh" 