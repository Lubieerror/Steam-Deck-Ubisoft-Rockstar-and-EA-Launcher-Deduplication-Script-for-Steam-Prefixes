script that searches through game prefix folders to identify installed launchers from Ubisoft, Rockstar, and EA. It creates a shared folder with a single copy of each launcher, removes duplicate copies within each prefix, and adds a shortcut to the shared folder in each prefix.

Pros:

Increased disk space: By consolidating multiple launcher copies into one, you save storage space.

Unified updates: Launchers are updated only once, allowing multiple games from the same publisher to use the same, up-to-date version.

Centralized settings management: Configure launcher settings in one location instead of multiple instances across prefixes.

Automatic login functionality: Enjoy seamless automatic login across all games using the shared launcher.

Instructions:

Go to the Steam Deck desktop.

Download the file and save it in /home/deck/Downloads (default path).

Open the terminal.

In the terminal, type:

cd /home/deck/Downloads

5. Grant executable permissions to the file by typing:

chmod +x steamlaunchermanager.py

6. Run the script:

python3 steamlaunchermanager.py

7. Launcher folders are located in compatdata/Launchers.
