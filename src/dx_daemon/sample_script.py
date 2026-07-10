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
    """Generates a personalized greeting based on the current time."""
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return f"{greeting}, {name}!"


def process_numbers(limit: int):
    """Loops through numbers, classifying them as even or odd."""
    print(f"\n--- Classifying numbers from 1 to {limit} ---")
    for num in range(1, limit + 1):
        status = "even" if num % 2 == 0 else "odd"
        print(f"Number {num} is {status}.")


def safe_divide(a: float, b: float):
    """Demonstrates error handling during division."""
    print(f"\n--- Attempting Division: {a} / {b} ---")
    try:
        result = a / b
        print(f"Success! Result: {result}")
    except ZeroDivisionError:
        print("Error: You cannot divide a number by zero.")


def check_system_directory():
    """Checks the existence of the current working directory."""
    print("\n--- System Check ---")
    current_dir = os.getcwd()
    print(f"Current Working Directory: {current_dir}")
    if os.path.exists(current_dir):
        print("Status: Directory verified and accessible.")


def main():
    """The main execution thread of the script."""
    print("=== START OF PYTHON SCRIPT ===")

    # 1. User Input & Greeting
    user_name = input("Please enter your name: ").strip() or "Guest"
    welcome_message = greet_user(user_name)
    print(welcome_message)

    # 2. Control Flow & Loops
    process_numbers(limit=5)

    # 3. Error Handling (Try/Except)
    safe_divide(10, 2)
    safe_divide(10, 0)

    # 4. OS Interaction
    check_system_directory()

    print("\n=== END OF PYTHON SCRIPT ===")


# Ensures the script runs only when executed directly, not when imported
if __name__ == "__main__":
    main()
