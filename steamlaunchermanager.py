#!/usr/bin/env python3

import os
import shutil

# Define paths and folders
launchers_dir = "/home/deck/.local/share/Steam/steamapps/compatdata/Launchers"
prefixes_root = "/home/deck/.local/share/Steam/steamapps/compatdata"
folders_to_find = [
    "Program Files (x86)/Ubisoft",
    "Program Files/Rockstar Games",
    "Program Files/Electronic Arts"
]
savegames_relative_path = "Program Files (x86)/Ubisoft/Ubisoft Game Launcher/savegames"

# Ensure the Launchers directory exists
os.makedirs(launchers_dir, exist_ok=True)

# Counter for processed folders
processed_count = 0

# Helper function for printing in bold green
def print_bold_green(text):
    print(f"\033[1m\033[92m{text}\033[0m")

# Function to handle savegames with conflict check
def copy_savegames_with_conflict_check(src, dest):
    # Prevent copying if the source is within the Launchers folder
    if src.startswith(launchers_dir):
        print_bold_green(f"Skipping savegames copy from {src} (Launchers folder is not a source).")
        return
    
    for root, _, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src)
            dest_file = os.path.join(dest, rel_path)

            # Ensure source and destination are not the same file
            if os.path.abspath(src_file) == os.path.abspath(dest_file):
                print_bold_green(f"Skipping copy for {src_file} as source and destination are the same.")
                continue

            if os.path.exists(dest_file):
                # Check for conflict by comparing file sizes
                if os.path.getsize(src_file) != os.path.getsize(dest_file):
                    print_bold_green(f"Conflict detected for savegame file: {src_file}")
                    print_bold_green(f"Existing file: {dest_file}")
                    print_bold_green("Files have different sizes. Please back up and press Enter to continue...")
                    input()  # Wait for user to press Enter after backup
                    continue  # Skip conflicting file after warning

            # Copy file if no conflict or conflict resolved
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            print_bold_green(f"Copied savegame file {src_file} to {dest_file}")

# Function to handle a single launcher folder in a prefix
def process_folder(prefix_path, relative_folder):
    global processed_count
    original_folder = os.path.join(prefix_path, "pfx/drive_c", relative_folder)
    launcher_folder = os.path.join(launchers_dir, os.path.basename(relative_folder))
    
    # Check if original_folder is a symlink already pointing to the launcher_folder
    if os.path.islink(original_folder) and os.readlink(original_folder) == launcher_folder:
        print(f"Symlink already exists for {original_folder}, skipping.")
        return

    if os.path.exists(original_folder):
        if not os.path.exists(launcher_folder):
            # First occurrence: Copy folder to Launchers and create symlink
            shutil.copytree(original_folder, launcher_folder)
            print(f"Copied {original_folder} to {launcher_folder}")
        # Remove the original and replace with symlink
        shutil.rmtree(original_folder)
        os.symlink(launcher_folder, original_folder)
        print(f"Replaced {original_folder} with symlink to {launcher_folder}")
        processed_count += 1  # Increment counter

# Traverse each prefix and process the folders
for prefix in os.listdir(prefixes_root):
    prefix_path = os.path.join(prefixes_root, prefix)
    if os.path.isdir(prefix_path):
        # Skip processing if the prefix path is the Launchers folder
        if prefix_path == launchers_dir:
            print_bold_green(f"Skipping processing of the Launchers folder: {launchers_dir}")
            continue

        # Check if Ubisoft is a symlink and skip savegames processing if true
        ubisoft_path = os.path.join(prefix_path, "pfx/drive_c", "Program Files (x86)/Ubisoft")
        if os.path.islink(ubisoft_path):
            print_bold_green(f"Skipping savegames processing for symlinked Ubisoft folder: {ubisoft_path}")
            continue

        # Check and handle savegames folder separately for Ubisoft
        savegames_folder = os.path.join(prefix_path, "pfx/drive_c", savegames_relative_path)
        target_savegames_folder = os.path.join(launchers_dir, "Ubisoft/Ubisoft Game Launcher/savegames")
        
        if os.path.exists(savegames_folder):
            print_bold_green(f"Processing savegames from {savegames_folder}")
            copy_savegames_with_conflict_check(savegames_folder, target_savegames_folder)

        # Process main folders (Ubisoft, Rockstar, EA)
        for folder in folders_to_find:
            process_folder(prefix_path, folder)

# Display success message with GitHub link
print_bold_green(f"Processing complete. Total folders processed: {processed_count}")
print_bold_green("Follow for new updates of this script: https://github.com/F3edo/Steam-Deck-Ubisoft-Rockstar-and-EA-Launcher-Deduplication-Script-for-Steam-Prefixes")
