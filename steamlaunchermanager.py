#!/usr/bin/env python3

import os
import shutil

# Define paths and folders
launchers_dir = "/home/deck/.local/share/Steam/steamapps/compatdata/Launchers"
prefixes_root = "/home/deck/.local/share/Steam/steamapps/compatdata"
folders_to_find = {
    "Ubisoft": "Program Files (x86)/Ubisoft/Ubisoft Game Launcher",
    "Rockstar": "Program Files/Rockstar Games",
    "EA": "Program Files/Electronic Arts"
}

# Ensure the Launchers directory exists
os.makedirs(launchers_dir, exist_ok=True)

# Function to handle copying savegames without overwriting existing files
def copy_savegames(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for root, _, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src)
            dest_file = os.path.join(dest, rel_path)
            if not os.path.exists(dest_file):
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
                print(f"Copied savegame file {src_file} to {dest_file}")

# Function to handle a single launcher folder in a prefix
def process_folder(prefix_path, launcher_name, relative_folder):
    original_folder = os.path.join(prefix_path, "pfx/drive_c", relative_folder)
    launcher_folder = os.path.join(launchers_dir, os.path.basename(relative_folder))

    if os.path.exists(original_folder):
        if launcher_name == "Ubisoft":
            # Handle Ubisoft case: only move contents except for "savegames" folder
            savegames_folder = os.path.join(original_folder, "savegames")
            if os.path.exists(savegames_folder):
                # Copy savegames without overwriting
                copy_savegames(savegames_folder, os.path.join(launcher_folder, "savegames"))
            # Move rest of the Ubisoft folder and create symlink
            for item in os.listdir(original_folder):
                item_path = os.path.join(original_folder, item)
                if item != "savegames":
                    if not os.path.exists(launcher_folder):
                        shutil.copytree(item_path, os.path.join(launcher_folder, item))
                    shutil.rmtree(item_path)
            os.symlink(launcher_folder, original_folder)
            print(f"Processed Ubisoft launcher, kept savegames and created symlink at {original_folder}")
        else:
            # Handle other folders (Rockstar, EA) as before
            if not os.path.exists(launcher_folder):
                shutil.copytree(original_folder, launcher_folder)
                print(f"Copied {original_folder} to {launcher_folder}")
            shutil.rmtree(original_folder)
            os.symlink(launcher_folder, original_folder)
            print(f"Replaced {original_folder} with symlink to {launcher_folder}")

# Traverse each prefix and process the folders
for prefix in os.listdir(prefixes_root):
    prefix_path = os.path.join(prefixes_root, prefix)
    if os.path.isdir(prefix_path):
        for launcher_name, folder in folders_to_find.items():
            process_folder(prefix_path, launcher_name, folder)
