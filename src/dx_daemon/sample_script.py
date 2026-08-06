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


def get_todo_suggestions() -> list[str]:
    """Returns a sample list of things to do based on the current time of day."""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return [
            "Review your calendar and prioritize today's tasks",
            "Drink a glass of water and stretch for a few minutes",
            "Tackle your most important deep-work task first",
            "Send any overnight follow-ups while your inbox is quiet",
        ]
    elif current_hour < 18:
        return [
            "Check progress on morning goals and adjust as needed",
            "Take a short walk or stretch break to reset focus",
            "Block time for afternoon deep work or meetings",
            "Clear quick emails and messages before the day winds down",
        ]
    else:
        return [
            "Wrap up remaining work and note tomorrow's top priorities",
            "Tidy your workspace so tomorrow starts clean",
            "Spend some time on a personal hobby or reading",
            "Wind down with a short walk or stretch before bed",
        ]


def main():
    """The main execution thread of the script."""
    print("=== START OF PYTHON SCRIPT ===")

    # 1. User Input & Greeting
    user_name = input("Please enter your name here please: ").strip() or "Guest"
    welcome_message = greet_user(user_name)
    print(welcome_message)

    # 2. Time-based todo suggestions
    print("\nHere's a sample list of things to do right now:")
    for index, item in enumerate(get_todo_suggestions(), start=1):
        print(f"  {index}. {item}")

    print("\n=== END OF PYTHON SCRIPT ===")


# Ensures the script runs only when executed directly, not when imported
if __name__ == "__main__":
    main()
