#!/bin/bash

# Default values
COUNT=1
SERVICE="tv"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --count)
      COUNT="$2"
      shift 2
      ;;
    --service)
      SERVICE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Setting up..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements are installed
if ! pip freeze | grep -q selenium; then
  echo "Installing requirements..."
  pip install -r requirements.txt
fi

# Run the application
echo "Running Apple Entertainment Offer Code Extractor..."
echo "Extracting $COUNT codes for $SERVICE"
python app.py --count "$COUNT" --service "$SERVICE" 