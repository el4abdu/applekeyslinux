#!/bin/bash

# Setup script for Telegram Bot on Ubuntu
echo "Setting up environment for Apple Entertainment Telegram Bot..."

# Update package lists
sudo apt update -y

# Install Chromium and ChromeDriver
echo "Installing Chromium and ChromeDriver..."
sudo apt install -y chromium-browser chromium-chromedriver

# Verify installation
echo "Chromium version:"
chromium-browser --version

echo "ChromeDriver version:"
chromedriver --version

# Install Python and pip
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies for Telegram bot
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r telegram_requirements.txt

# Create directories
mkdir -p codes

# Copy .env.example to .env
cp env.example .env

echo "Setup complete!"
echo "Now, you need to edit the .env file with your Telegram token and allowed user IDs:"
echo "nano .env"
echo ""
echo "After setting up the .env file, you can run the bot with:"
echo "python3 simple_app_telegram.py --telegram" 