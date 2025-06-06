@echo off
REM Windows batch file to run the key generator service and Telegram bot

echo Creating codes directory...
if not exist codes mkdir codes

echo Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install selenium python-telegram-bot==20.7 webdriver-manager requests --upgrade

echo Setting Telegram token...
set TELEGRAM_TOKEN=8176235314:AAGjCqOKEeLYeveUt6rEv2_bNxrXC-iEm6c

echo Starting key generator service in the background...
start /b python key_generator_service.py > generator.log 2>&1

echo Waiting for generator service to initialize...
timeout /t 5 /nobreak > nul

echo Starting Telegram bot...
python telegram_bot_with_generator.py

echo Done.
pause 