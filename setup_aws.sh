#!/bin/bash

# Setup script for AWS Linux environment
# This script installs Chrome, ChromeDriver, and required dependencies

echo "Setting up environment for Apple Entertainment Offer Code Extractor..."

# Update package lists
sudo yum update -y

# Install required dependencies
sudo yum install -y wget unzip libX11 libXcomposite libXcursor libXdamage \
    libXext libXi libXtst cups-libs libXScrnSaver libXrandr alsa-lib pango \
    atk at-spi2-atk gtk3 python3 python3-pip

# Install Chrome
echo "Installing Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
rm google-chrome-stable_current_x86_64.rpm

# Verify Chrome installation
echo "Chrome version:"
google-chrome --version

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
echo "To run the application, activate the virtual environment and run app.py:"
echo "source venv/bin/activate"
echo "python app.py --count <number_of_codes> --service <service_name>" 