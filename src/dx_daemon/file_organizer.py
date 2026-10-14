#!/usr/bin/env python3
"""
Module: file_organizer.py
Description: Automates local file management by sorting files into subfolders.
Author: AI Assistant
Date: July 2026
"""

import os
import shutil


def organize_folder(target_directory: str):
    """Scans a directory and organizes files by category mapping."""
    # Define file extension categories
    extension_map = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    }

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        print(f"Error: The directory '{target_directory}' does not exist.")
        return

    print(f"=== Scanning: {target_directory} ===\n")
    moved_count = 0

    # Iterate through all items in the folder
    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)

        # Skip folders, only process files
        if os.path.isdir(file_path):
            continue

        # Get file extension in lowercase
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()

        # Find the correct category folder
        destination_folder = "Others"
        for category, extensions in extension_map.items():
            if file_extension in extensions:
                destination_folder = category
                break

        # Create destination folder path
        category_dir = os.path.join(target_directory, destination_folder)

        # Create the subfolder if it does not exist yet
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            print(f"Created category folder: {destination_folder}")

        # Move the file
        destination_path = os.path.join(category_dir, filename)
        shutil.move(file_path, destination_path)
        print(f"Moved: '{filename}' -> {destination_folder}/")
        moved_count += 1

    print(f"\n=== Cleanup Complete! Sorted {moved_count} files. ===")


def main():
    """Main execution point."""
    # Create a dummy sandbox folder in the current directory for testing
    test_folder = os.path.join(os.getcwd(), "test_sandbox")

    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
        # Create a few empty dummy files for demonstration
        open(os.path.join(test_folder, "invoice.pdf"), "w").close()
        open(os.path.join(test_folder, "vacation.jpg"), "w").close()
        open(os.path.join(test_folder, "song.mp3"), "w").close()
        open(os.path.join(test_folder, "notes.txt"), "w").close()
        print(f"Created temporary sandbox folder with mock files at:\n{test_folder}\n")

    # Run the organizer on the test folder
    organize_folder(test_folder)


if __name__ == "__main__":
    main()
