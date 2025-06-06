#!/bin/bash

# Simple setup script for Ubuntu environment
echo "Setting up minimal environment for Apple Entertainment Offer Code Extractor..."

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
sudo apt install -y python3 python3-pip

# Install Selenium
echo "Installing Selenium..."
pip3 install selenium

# Create directories
mkdir -p codes

echo "Setup complete!"
echo "To run the application:"
echo "python3 simple_app.py --count <number_of_codes> --service <service_name>"
echo ""
echo "Available services: tv, music, arcade, fitness, news" 