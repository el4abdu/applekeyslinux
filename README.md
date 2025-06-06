# Apple Entertainment Offer Code Extractor

This Python application automates the process of extracting Apple Entertainment offer codes from the Apple Card promotion page.

## Features

- Navigates to the Apple Entertainment offer page
- Clicks on redemption buttons
- Extracts and saves redemption codes
- Supports headless operation on Linux/AWS
- Docker support for easy deployment

## Requirements

- Python 3.8+
- Selenium WebDriver
- Chrome/Chromium browser
- Chrome WebDriver

## Installation

### Method 1: Direct Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Chrome/Chromium and appropriate WebDriver

### Method 2: Using the Setup Script (AWS Linux)

1. Make the setup script executable:
   ```
   chmod +x setup_aws.sh
   ```
2. Run the setup script:
   ```
   ./setup_aws.sh
   ```

### Method 3: Using Docker

1. Build and run using Docker Compose:
   ```
   docker-compose up --build
   ```

## Usage

### Method 1: Using Python Directly

```bash
python app.py --count <number_of_codes> --service <service_name>
```

Where:
- `<number_of_codes>` is the number of redemption codes you want to extract
- `<service_name>` is one of: tv, music, arcade, fitness, news

### Method 2: Using the Run Script

```bash
chmod +x run.sh
./run.sh --count <number_of_codes> --service <service_name>
```

### Method 3: Using Docker

Edit the `docker-compose.yml` file to set the desired count and service, then run:

```bash
docker-compose up
```

## Available Services

- `tv` - Apple TV+
- `music` - Apple Music
- `arcade` - Apple Arcade
- `fitness` - Apple Fitness+
- `news` - Apple News+

## Output

Extracted codes are saved to the `codes/` directory in separate files for each service:

- `tv_plus_codes.txt`
- `music_codes.txt`
- `arcade_codes.txt`
- `fitness_codes.txt`
- `news_codes.txt`

## Configuration

Edit the `config.py` file to customize:
- Target URLs
- XPath selectors
- Browser settings
- Timeouts
- Output file locations 