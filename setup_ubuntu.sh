#!/bin/bash

# Setup script for Ubuntu environment
# This script installs Chrome, ChromeDriver, and required dependencies

echo "Setting up environment for Apple Entertainment Offer Code Extractor on Ubuntu..."

# Update package lists
sudo apt update -y

# Install required dependencies
sudo apt install -y wget unzip python3-pip python3-venv xvfb \
    libxi6 libgconf-2-4 libnss3 libglib2.0-0 libfontconfig1 libx11-6 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 \
    libxi6 libxrandr2 libxrender1 libxss1 libxtst6 fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libnspr4 libnss3

# Install Chrome
echo "Installing Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Verify Chrome installation
echo "Chrome version:"
google-chrome --version

# Install ChromeDriver
echo "Installing ChromeDriver..."
sudo apt install -y chromium-chromedriver
sudo ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

# Verify ChromeDriver installation
echo "ChromeDriver version:"
chromedriver --version

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p codes

echo "Setup complete!"
echo "To run the application, activate the virtual environment and run ubuntu_app.py:"
echo "source venv/bin/activate"
echo "python ubuntu_app.py --count <number_of_codes> --service <service_name>" 