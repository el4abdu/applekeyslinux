# Apple Entertainment Codes Generator

This application automatically generates and manages Apple Entertainment offer codes from the Apple Card promotion page. It includes a background key generator service and a Telegram bot interface.

## Features

- **Background Key Generation**: Continuously generates codes for multiple services (Apple TV+, Music, Arcade, Fitness+) and stores them for later use
- **Telegram Bot Interface**: Request codes via Telegram with simple commands
- **Multi-Service Support**: Generate codes for different Apple services
- **Code Storage**: Maintains a pool of pre-generated codes for quick access
- **Anti-Detection Measures**: Uses rotating user agents and private browsing

## Setup

### Requirements

- Python 3.7+
- Chrome or Chromium browser
- Linux/Ubuntu environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/el4abdu/applekeyslinux.git
   cd applekeyslinux
   ```

2. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

3. Make the scripts executable:
   ```
   chmod +x *.sh
   ```

## Usage

### Option 1: Run Both Services Together

To run both the key generator service and Telegram bot together:

```
./run_bot_with_generator.sh
```

### Option 2: Run Services Separately

1. Start the key generator service in the background:
   ```
   ./run_generator_background.sh
   ```

2. Start the Telegram bot in a separate terminal:
   ```
   ./run_telegram_bot_only.sh
   ```

### Telegram Bot Commands

Once the bot is running, you can use these commands in Telegram:

- `/start` - Start the bot and select a service
- `/help` - Show help message and current code counts
- `/status` - Show current code counts for all services
- `/generate [service] [count]` - Generate specific number of codes for a service
  - Example: `/generate tv 3` to generate 3 Apple TV+ codes

### Available Services

- `tv` - Apple TV+
- `music` - Apple Music
- `arcade` - Apple Arcade
- `fitness` - Apple Fitness+

## Configuration

### Telegram Bot Token

The default Telegram bot token is included in the scripts. To use your own token:

```
export TELEGRAM_TOKEN="your_token_here"
./run_telegram_bot_only.sh
```

### User Restrictions

To restrict the bot to specific Telegram user IDs:

```
export ALLOWED_USERS="user_id_1,user_id_2"
./run_telegram_bot_only.sh
```

## Monitoring

- Check `generator.log` for key generator service logs
- Check `telegram_bot.log` for Telegram bot logs

## Stopping the Services

- To stop the key generator service: `kill $(cat generator.pid)`
- To stop the Telegram bot: Press Ctrl+C in its terminal

## Troubleshooting

If you encounter issues:

1. Check that Chrome/Chromium is installed
2. Verify that the correct ChromeDriver is installed
3. Check the log files for specific error messages
4. Ensure you have a stable internet connection

## License

This project is for educational purposes only. 