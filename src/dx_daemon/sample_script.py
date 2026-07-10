#!/usr/bin/env python3
"""
Module: sample_script.py
Description: A beginner-friendly script demonstrating core Python features.
Author: AI Assistant
Date: July 2026
"""

import os
from datetime import datetime


def greet_user(name: str, language: str) -> str:
    """Generates a personalized greeting based on time and language."""
    now = datetime.now()
    current_hour = now.hour
    current_date = now.strftime("%B %d, %Y")
    language = language.lower().strip()

    greeting_map = {
        "english": {
            "morning": "Good morning",
            "afternoon": "Good afternoon",
            "evening": "Good evening",
        },
        "spanish": {
            "morning": "Buenos dias",
            "afternoon": "Buenas tardes",
            "evening": "Buenas noches",
        },
        "french": {
            "morning": "Bonjour",
            "afternoon": "Bon apres-midi",
            "evening": "Bonsoir",
        },
        "hindi": {
            "morning": "Suprabhat",
            "afternoon": "Namaste",
            "evening": "Shubh sandhya",
        },
    }

    selected_language = greeting_map.get(language, greeting_map["english"])

    if current_hour < 12:
        greeting = selected_language["morning"]
    elif current_hour < 18:
        greeting = selected_language["afternoon"]
    else:
        greeting = selected_language["evening"]

    return f"{greeting}, {name}! Today's date is {current_date}."


def main():
    """The main execution thread of the script."""
    print("=== START OF PYTHON SCRIPT ===")

    # 1. User Input & Greeting
    user_name = input("Please enter your name here please: ").strip() or "Guest"
    preferred_language = (
        input("Choose a greeting language from the list of languages (English/Spanish/French/Hindi): ").strip()
        or "English"
    )
    welcome_message = greet_user(user_name, preferred_language)
    print(welcome_message)


    print("\n=== END OF PYTHON SCRIPT ===")


# Ensures the script runs only when executed directly, not when imported
if __name__ == "__main__":
    main()
