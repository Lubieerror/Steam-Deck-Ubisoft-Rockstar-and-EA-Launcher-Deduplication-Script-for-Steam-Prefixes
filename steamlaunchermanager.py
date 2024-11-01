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

# Ensure the Launchers directory exists
os.makedirs(launchers_dir, exist_ok=True)

# Function to handle a single launcher folder in a prefix
def process_folder(prefix_path, relative_folder):
    original_folder = os.path.join(prefix_path, "pfx/drive_c", relative_folder)
    launcher_folder = os.path.join(launchers_dir, os.path.basename(relative_folder))

    if os.path.exists(original_folder):
        if not os.path.exists(launcher_folder):
            # First occurrence: Copy folder to Launchers and create symlink
            shutil.copytree(original_folder, launcher_folder)
            print(f"Copied {original_folder} to {launcher_folder}")
        # Remove the original and replace with symlink
        shutil.rmtree(original_folder)
        os.symlink(launcher_folder, original_folder)
        print(f"Replaced {original_folder} with symlink to {launcher_folder}")

# Traverse each prefix and process the folders
for prefix in os.listdir(prefixes_root):
    prefix_path = os.path.join(prefixes_root, prefix)
    if os.path.isdir(prefix_path):
        for folder in folders_to_find:
            process_folder(prefix_path, folder)
