#!/bin/bash

# Run script for Telegram Bot
echo "Starting Apple Entertainment Telegram Bot..."

# Set the environment variables
export TELEGRAM_TOKEN="8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c"
export ALLOWED_USERS=""  # Leave empty to allow all users, or add comma-separated IDs

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot
python3 simple_app_telegram.py --telegram

# Keep the script running even if there's an error
while true; do
    echo "Bot stopped. Restarting in 10 seconds..."
    sleep 10
    python3 simple_app_telegram.py --telegram
done 