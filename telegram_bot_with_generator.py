#!/usr/bin/env python3
"""
Telegram Bot for Apple Entertainment Codes
Uses pre-generated codes from the key generator service
"""

import os
import logging
import asyncio
from datetime import datetime
import key_generator_service as generator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Configure logging
logging.basicConfig(
    filename='telegram_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Telegram token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c")

# Allowed users (empty list means all users are allowed)
ALLOWED_USERS = [int(user_id) for user_id in os.getenv("ALLOWED_USERS", "").split(",") if user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("Apple TV+", callback_data="tv"),
            InlineKeyboardButton("Apple Music", callback_data="music"),
        ],
        [
            InlineKeyboardButton("Apple Arcade", callback_data="arcade"),
            InlineKeyboardButton("Apple Fitness+", callback_data="fitness"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to Apple Entertainment Code Generator Bot!\n\n"
        "Choose a service to get a code:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await query.answer("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized button press by user {user_id}")
        return
    
    await query.answer()
    
    service = query.data
    if service in generator.SERVICE_BUTTONS:
        await query.edit_message_text(text=f"Getting {generator.SERVICE_NAMES[service]} code from storage...")
        
        # Check if we have a stored code
        code = generator.get_stored_code(service)
        
        if code:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await query.edit_message_text(
                text=f"✅ *{generator.SERVICE_NAMES[service]} Code*\n\n"
                     f"`{code}`\n\n"
                     f"Generated at: {timestamp}\n\n"
                     f"To get another code, use /start",
                parse_mode="Markdown"
            )
        else:
            # If no stored code, generate one on the fly
            await query.edit_message_text(text=f"No stored codes available. Generating a new {generator.SERVICE_NAMES[service]} code...\nThis may take a moment.")
            
            # Run code extraction in a separate thread to avoid blocking
            code = await context.application.loop.run_in_executor(None, generator.get_code, service)
            
            if code:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await query.edit_message_text(
                    text=f"✅ *{generator.SERVICE_NAMES[service]} Code*\n\n"
                         f"`{code}`\n\n"
                         f"Generated at: {timestamp}\n\n"
                         f"To get another code, use /start",
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text(
                    text="❌ Failed to generate code. Please try again later.\n\n"
                         "To try again, use /start"
                )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    # Get current code counts
    counts = {service: generator.count_codes(service) for service in generator.SERVICE_BUTTONS}
    
    status_text = "Current available codes:\n"
    for service, count in counts.items():
        status_text += f"• {generator.SERVICE_NAMES[service]}: {count} codes\n"
    
    await update.message.reply_text(
        "This bot provides Apple Entertainment offer codes.\n\n"
        "Available commands:\n"
        "/start - Start the bot and select a service\n"
        "/help - Show this help message\n"
        "/status - Show current code counts\n"
        "/generate [service] [count] - Generate codes (e.g., /generate tv 3)\n\n"
        "Available services: tv, music, arcade, fitness\n\n"
        f"{status_text}"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current status of code storage."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    # Get current code counts
    counts = {service: generator.count_codes(service) for service in generator.SERVICE_BUTTONS}
    
    status_text = "Current available codes:\n"
    for service, count in counts.items():
        status_text += f"• {generator.SERVICE_NAMES[service]}: {count} codes\n"
    
    await update.message.reply_text(status_text)

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate codes based on command arguments."""
    user_id = update.effective_user.id
    
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return
    
    args = context.args
    
    if len(args) < 1:
        await update.message.reply_text(
            "Please specify a service and optionally a count.\n"
            "Example: /generate tv 3\n\n"
            "Available services: tv, music, arcade, fitness"
        )
        return
    
    service = args[0].lower()
    if service not in generator.SERVICE_BUTTONS:
        await update.message.reply_text(
            f"Unknown service: {service}\n\n"
            "Available services: tv, music, arcade, fitness"
        )
        return
    
    count = 1
    if len(args) >= 2:
        try:
            count = int(args[1])
            if count < 1:
                count = 1
            elif count > 5:  # Limit to 5 codes at once
                count = 5
        except ValueError:
            pass
    
    await update.message.reply_text(f"Getting {count} {generator.SERVICE_NAMES[service]} code(s) from storage...")
    
    codes = []
    # Try to get codes from storage first
    for _ in range(count):
        code = generator.get_stored_code(service)
        if code:
            codes.append(code)
    
    # If we don't have enough codes, generate some on the fly
    if len(codes) < count:
        await update.message.reply_text(f"Only {len(codes)} codes available in storage. Generating {count - len(codes)} more...")
        
        # Generate remaining codes
        for _ in range(count - len(codes)):
            # Run code extraction in a separate thread to avoid blocking
            code = await context.application.loop.run_in_executor(None, generator.get_code, service)
            if code:
                codes.append(code)
    
    if codes:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"✅ *{generator.SERVICE_NAMES[service]} Codes*\n\n"
        for i, code in enumerate(codes, 1):
            message += f"{i}. `{code}`\n"
        message += f"\nGenerated at: {timestamp}\n\nTo get more codes, use /start"
        
        await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ Failed to generate codes. Please try again later.\n\n"
            "To try again, use /start"
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CallbackQueryHandler(button))
    
    # Start the Bot
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
