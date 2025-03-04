# yazi-rmpc-opener

This script adds the ability to use `rmpc` (a client for controlling the MPD music player) in the `yazi` file manager. With it, you can open and play music files directly from `yazi`, adding them to the MPD playlist.

**Key Features:**
- Opening and playing music files via `rmpc`.
- Adding selected tracks to the MPD playlist.

**How to Use:**
1. Make the Script Executable
   ```sh
   chmod +x qute-rofi-translate.py
   ```
2. Ensure that `yazi`, `rmpc`, and `mpd` are installed on your system.
3. Add the script to the `yazi.toml` configuration file in the `[opener]` section, as shown below. You can specify your own path and script name:
   ```toml
   [opener]
   audio = [
       { run = '~/path/to/run_for_yazi.py "$@"', block = true, for = "unix" }
   ]
   ```
4. Add a rule for opening audio files in the `[open]` section:
   ```toml
   [open]
   prepend_rules = [
       { mime = "audio/*", use = "audio" },
   ]
   ```
5. Save the changes and restart `yazi`.
6. Now, when you select a music file in `yazi`, it will automatically open and play via `rmpc`.

**Dependencies:**
- `yazi` (file manager)
- `rmpc` (MPD control client)
- `mpd` (music server)

**Example Workflow:**
1. Open `yazi` and navigate to a folder containing music.
2. Select a music file.
3. The file will automatically be added to the MPD playlist and start playing.
