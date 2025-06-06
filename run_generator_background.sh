#!/bin/bash

# Script to run the key generator service in the background

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
pip3 install selenium --upgrade

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

# Kill any existing generator processes
pkill -f "python3 key_generator_service.py" || true

# Start the key generator service in the background
echo "Starting key generator service in the background..."
nohup python3 key_generator_service.py > generator.log 2>&1 &

# Save the PID to a file
echo $! > generator.pid

echo "Key generator service started with PID $(cat generator.pid)"
echo "You can check the logs in generator.log"
echo "To stop the service, run: kill $(cat generator.pid)" 