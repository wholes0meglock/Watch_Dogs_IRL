# Music Player for Termux

`musicpl.py` is a simple music player script designed for Termux that allows you to play, pause, skip, and go back through songs stored on your device. The player supports MP3 and WAV formats and provides command-line controls through the terminal.

## Features

- **Play music files**: Supports MP3 and WAV formats.
- **Navigate through songs**: Play, pause, skip to the next song, and go back to the previous song.
- **Auto-play next song**: Automatically plays the next song in the list when the current song ends.
- **Command-line controls**: Simple commands to control playback.

## Installation

1. **Ensure Termux is Installed**: You need Termux installed on your Android device. You can get it from the [Google Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/packages/com.termux/).

2. **Install Required Packages**: Open Termux and install the required packages by running the following commands:
    ```bash
    pkg update
    pkg install python mpv
    ```

3. **Download the Script**: Save the `musicpl.py` script to your Termux home directory or any directory of your choice.

4. **Make the Script Executable**:
    ```bash
    chmod +x musicpl.py
    ```

## Usage

1. **Run the Script**: Execute the script by running:
    ```bash
    python musicpl.py
    ```

2. **Commands**:
    - `p <number>`: Play the song with the given number from the list.
    - `n`: Skip to the next song.
    - `b`: Go back to the previous song.
    - `s`: Stop the currently playing song.
    - `q`: Quit the music player.

3. **Directory**: By default, the script looks for music files in `/sdcard/Music`. Change the `MUSIC_DIR` variable in the script if your music is stored in a different location.

## Example

```bash
$ python musicpl.py
```

Upon running, the script will display a list of available tracks and prompt you to enter a command.

## Troubleshooting

- **No Music Files Found**: Make sure your music files are in the specified directory and the directory path is correct.
- **Permission Issues**: Ensure Termux has the necessary permissions to access your storage. You might need to run:
    ```bash
    termux-setup-storage
    ```