#!/usr/bin/env python3
"""
Example script demonstrating how to use the extracted Apple Entertainment offer codes.
This script reads the codes from the output files and prints them in a formatted way.
"""

import os
import sys
from pathlib import Path

def read_codes(service_name):
    """
    Read codes from the specified service's output file
    
    Args:
        service_name (str): Name of the service (tv, music, arcade, fitness, news)
        
    Returns:
        list: List of extracted codes
    """
    # Map service names to file names
    file_mapping = {
        'tv': 'tv_plus_codes.txt',
        'music': 'music_codes.txt',
        'arcade': 'arcade_codes.txt',
        'fitness': 'fitness_codes.txt',
        'news': 'news_codes.txt'
    }
    
    # Map service names to display names
    service_display_names = {
        'tv': 'Apple TV+',
        'music': 'Apple Music',
        'arcade': 'Apple Arcade',
        'fitness': 'Apple Fitness+',
        'news': 'Apple News+'
    }
    
    if service_name not in file_mapping:
        print(f"Error: Unknown service '{service_name}'")
        print(f"Available services: {', '.join(file_mapping.keys())}")
        return []
    
    file_path = os.path.join('codes', file_mapping[service_name])
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r') as f:
            codes = [line.strip() for line in f if line.strip()]
        return codes
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def display_codes(service_name, codes):
    """
    Display the codes in a formatted way
    
    Args:
        service_name (str): Name of the service
        codes (list): List of codes to display
    """
    service_display_names = {
        'tv': 'Apple TV+',
        'music': 'Apple Music',
        'arcade': 'Apple Arcade',
        'fitness': 'Apple Fitness+',
        'news': 'Apple News+'
    }
    
    display_name = service_display_names.get(service_name, service_name)
    
    print(f"\n{'-' * 50}")
    print(f"{display_name} Redemption Codes")
    print(f"{'-' * 50}")
    
    if not codes:
        print("No codes found.")
        return
    
    for i, code in enumerate(codes, 1):
        print(f"{i}. {code}")
    
    print(f"\nTotal codes: {len(codes)}")
    print(f"{'-' * 50}")
    
    # Print redemption instructions
    print(f"\nRedemption Instructions for {display_name}:")
    print("1. Open the App Store on your iOS device")
    print("2. Tap on your profile picture")
    print("3. Tap 'Redeem Gift Card or Code'")
    print("4. Enter the code or use the camera to scan it")
    print("5. Follow the on-screen instructions to complete redemption")
    print(f"{'-' * 50}\n")

def main():
    """
    Main function to parse arguments and display codes
    """
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <service_name>")
        print("Available services: tv, music, arcade, fitness, news")
        return
    
    service_name = sys.argv[1].lower()
    codes = read_codes(service_name)
    display_codes(service_name, codes)

if __name__ == "__main__":
    main() 