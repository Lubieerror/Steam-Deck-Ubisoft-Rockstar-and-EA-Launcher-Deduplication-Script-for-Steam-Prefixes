Steam Deck Ubisoft Rockstar and EA Launcher Deduplication Script for Steam Prefixes

This script searches through game prefix folders on the Steam Deck to identify installed launchers from Ubisoft, Rockstar, and EA. It consolidates these launchers into a shared folder, removes duplicate copies within each prefix, and creates a shortcut to the shared folder in each prefix.

Benefits:

Increased Disk Space: By consolidating multiple launcher copies into one, you save valuable storage space.

Unified Updates: Launchers are updated only once, allowing multiple games from the same publisher to use the same, up-to-date version.

Centralized Settings Management: Configure launcher settings in one location rather than multiple instances across prefixes.

Automatic Login Functionality: Seamlessly log into all games using the shared launcher.

Changelog for v1.1

1. Multi-use Capability

The script now supports multiple uses by skipping launcher folders that already have symlinks in place. This prevents redundant operations and speeds up processing. Please be advised, version 1.0 is one use only.

2. Automatic Copying and Merging of Save Games

Automatically copies and merges save games from different prefixes for the Ubisoft launcher. All saves are consolidated into a single shared folder for easy access.

3. Save Game Size Check

The script checks the size of Ubisoft launcher save games before copying to avoid accidentally overwriting different versions in the shared folder, ensuring data preservation and integrity.

---

Instructions:

1. Go to the Steam Deck desktop.

2. Download the file and save it in /home/deck/Downloads (default path).

3. Open the terminal and enter the following commands:

cd /home/deck/Downloads

chmod +x steamlaunchermanager.py

python3 steamlaunchermanager.py

4. After running the script, you can find the shared launchers in compatdata/Launchers.



