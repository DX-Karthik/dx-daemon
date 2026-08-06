#!/usr/bin/env python3
"""
Module: sample_script.py
Description: A beginner-friendly script demonstrating core Python features.
Author: AI Assistant
Date: July 2026
"""

import os
from datetime import datetime


def greet_user(name: str) -> str:
    """Generates a personalized greeting based on time."""
    now = datetime.now()
    current_hour = now.hour
    current_date = now.strftime("%B %d, %Y")
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return f"{greeting}, {name}! Today's date is {current_date}."


def main():
    """The main execution thread of the script."""
    print("=== START OF PYTHON SCRIPT ===")

    # 1. User Input & Greeting
    user_name = input("Please enter your name here please: ").strip() or "Guest"
    welcome_message = greet_user(user_name)
    print(welcome_message)


    print("\n=== END OF PYTHON SCRIPT ===")


# Ensures the script runs only when executed directly, not when imported
if __name__ == "__main__":
    main()
