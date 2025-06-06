#!/bin/bash

# Script to stop the key generator service

echo "Stopping key generator service..."

# Try to kill using PID file
if [ -f generator.pid ]; then
    PID=$(cat generator.pid)
    if ps -p $PID > /dev/null; then
        echo "Killing process with PID $PID"
        kill $PID
        rm generator.pid
        echo "Service stopped."
        exit 0
    else
        echo "PID file exists but process is not running."
        rm generator.pid
    fi
fi

# Try to find and kill by process name
PID=$(pgrep -f "python3 key_generator_service.py" || pgrep -f "python key_generator_service.py")
if [ -n "$PID" ]; then
    echo "Found process with PID $PID"
    kill $PID
    echo "Service stopped."
    exit 0
fi

echo "No running key generator service found." 