import os
import subprocess
import sys
import time
import threading
from pathlib import Path

# Define required packages
REQUIRED_TERMUX_PACKAGES = [
    'python',
    'mpv'
]

# Check and install Termux packages
def install_termux_packages():
    for pkg in REQUIRED_TERMUX_PACKAGES:
        print(f"Checking if Termux package '{pkg}' is installed...")
        result = subprocess.run(['pkg', 'list-installed', pkg], stdout=subprocess.PIPE)
        if pkg not in result.stdout.decode():
            print(f"Installing Termux package: {pkg}")
            subprocess.run(['pkg', 'install', '-y', pkg])

# Function to list music files
def list_music_files(music_dir):
    files = []
    for root, dirs, filenames in os.walk(music_dir):
        for filename in filenames:
            if filename.lower().endswith(('.mp3', '.wav')):
                files.append(os.path.join(root, filename))
    return files

# Function to display the current song and commands
def display_status():
    if current_track:
        print(f"\nCurrently playing: {os.path.basename(current_track)}")
    print("\nCommands: p <number> - Play, n - Next, b - Previous, s - Stop, q - Quit")

# Function to play music
def play_music(file_path):
    global player_process, current_track
    # Stop any currently playing music
    if player_process:
        player_process.terminate()
        player_process.wait()  # Ensure the process has ended before starting a new one
    player_process = subprocess.Popen(['mpv', file_path])
    current_track = file_path
    display_status()

# Function to pause music
def pause_music():
    if player_process:
        subprocess.Popen(['mpv', '--pause'])

# Function to stop music
def stop_music():
    global player_process, current_track
    if player_process:
        player_process.terminate()
        player_process.wait()  # Ensure the process has ended
        print('Music stopped')
        player_process = None
        current_track = None
    display_status()

# Function to skip to the next track
def next_track(track_list):
    global track_index
    track_index = (track_index + 1) % len(track_list)
    play_music(track_list[track_index])

# Function to go to the previous track
def previous_track(track_list):
    global track_index
    track_index = (track_index - 1) % len(track_list)
    play_music(track_list[track_index])

# Function to show the menu and handle user input
def show_menu(track_list):
    global track_index
    while True:
        display_status()
        print("\nAvailable tracks:")
        for idx, file_path in enumerate(track_list):
            print(f"{idx}: {os.path.basename(file_path)}")

        command = input("Enter command: ").strip().lower()

        if command.startswith('p '):
            try:
                choice = int(command.split(' ')[1])
                if 0 <= choice < len(track_list):
                    track_index = choice
                    play_music(track_list[track_index])
                else:
                    print("Invalid choice")
            except ValueError:
                print("Invalid input")
        elif command == 'n':
            next_track(track_list)
        elif command == 'b':
            previous_track(track_list)
        elif command == 's':
            stop_music()
        elif command == 'q':
            stop_music()
            break
        else:
            print("Unknown command")

# Function to handle automatic playback of the next song
def auto_play(track_list):
    global player_process
    while True:
        if player_process and player_process.poll() is not None:  # Check if the process has ended
            next_track(track_list)
        time.sleep(1)

# Main function
def main():
    install_termux_packages()

    MUSIC_DIR = "/sdcard/Music"  # Change this to your music directory
    if not Path(MUSIC_DIR).exists():
        print(f"Music directory {MUSIC_DIR} does not exist.")
        return

    track_list = list_music_files(MUSIC_DIR)
    if not track_list:
        print("No music files found.")
        return

    # Start auto-play in a separate thread
    threading.Thread(target=auto_play, args=(track_list,), daemon=True).start()

    show_menu(track_list)

if __name__ == '__main__':
    global current_track, player_process, track_index
    current_track = None
    player_process = None
    track_index = 0
    main()
