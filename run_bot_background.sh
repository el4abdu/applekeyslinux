#!/bin/bash

# Run the Telegram bot in the background
echo "Starting Apple Entertainment Telegram Bot in background..."

# Set the environment variables
export TELEGRAM_TOKEN="8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c"
export ALLOWED_USERS=""  # Leave empty to allow all users, or add comma-separated IDs

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot in the background
nohup python3 simple_app_telegram.py --telegram > bot.log 2>&1 &

# Save the process ID
echo $! > bot.pid

echo "Bot is running in background with PID $(cat bot.pid)"
echo "To view logs, use: tail -f bot.log"
echo "To stop the bot, use: kill $(cat bot.pid)" 