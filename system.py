import os
import subprocess
from colorama import init, Fore, Style
import curses

# Initialize Colorama
init(autoreset=True)

# Configuration
BASE_DIR = '/data/data/com.termux/files/home'
LOG_FILE = '/data/data/com.termux/files/home/repos_management.log'

ASCII_ART = """
  ___         _ ___           _ _ ___ _ 
 |   \\ ___ __| / __| ___ __  / / |_  ) |
 | |) / -_) _` \\__ \\/ -_) _| | | |/ /| |
 |___/\\___\\__,_|___/\\___\\__| |_|_/___|_|
"""

# Logging setup
def setup_logging():
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"[{Fore.LIGHTCYAN_EX}INFO{Style.RESET_ALL}] Log started\n")

def log_message(message: str, level: str = 'INFO'):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"[{Fore.LIGHTCYAN_EX}{level}{Style.RESET_ALL}] {message}\n")

setup_logging()

def print_header(title: str, stdscr):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()  # Get terminal dimensions
    if len(title) > max_x:
        title = title[:max_x-1]  # Truncate title if it's too long
    stdscr.addstr(0, 0, title, curses.A_BOLD)
    stdscr.addstr(1, 0, "-" * min(len(title), max_x), curses.A_BOLD)  # Ensure the line doesn't exceed width

def list_folders(directory: str, stdscr, selected_idx, start_idx):
    print_header(f"Contents of {directory}", stdscr)
    try:
        items = os.listdir(directory)
        if not items:
            stdscr.addstr(2, 0, "No items found.", curses.color_pair(1))
            return items

        items.append("nano (Edit or Create file with nano)")
        items.append("Exit")

        max_y, max_x = stdscr.getmaxyx()
        display_height = max_y - 3  # Calculate available height for items
        visible_items = items[start_idx:start_idx + display_height]

        for idx, item in enumerate(visible_items):
            display_text = item if len(item) <= max_x else item[:max_x-1]
            if idx + start_idx == selected_idx:
                stdscr.addstr(idx + 2, 0, display_text, curses.color_pair(2) | curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, display_text)
                
        stdscr.refresh()
        return items
    except Exception as e:
        log_message(f"Error listing folders: {e}", 'ERROR')
        stdscr.addstr(2, 0, f"Error: {e}", curses.color_pair(1))
        stdscr.refresh()
        return []

def execute_program(file_path: str):
    try:
        if file_path.endswith('.py'):
            subprocess.run(['python', file_path], check=True)
        elif file_path.endswith(('.sh', '.bash')):
            subprocess.run(['bash', file_path], check=True)
        elif file_path.endswith('.pl'):
            subprocess.run(['perl', file_path], check=True)
        elif file_path.endswith('.rb'):
            subprocess.run(['ruby', file_path], check=True)
        elif file_path.endswith('.js'):
            subprocess.run(['node', file_path], check=True)
        else:
            print(Fore.RED + "Unsupported file type for execution.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error executing {file_path}: {e}", 'ERROR')
        print(Fore.RED + f"Error executing {file_path}")

def edit_file(file_path: str, stdscr):
    curses.endwin()  # End curses mode before launching nano
    try:
        subprocess.run(['nano', file_path])
    except subprocess.CalledProcessError as e:
        log_message(f"Error editing {file_path}: {e}", 'ERROR')
        print(Fore.RED + f"Error editing {file_path}")
    finally:
        stdscr.refresh()
        curses.doupdate()

def prompt_file_name(stdscr):
    curses.echo()  # Enable echoing of characters typed by the user
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the full file name to edit or create (including extension): ")
    stdscr.refresh()
    file_name = stdscr.getstr().decode("utf-8")  # Read user input and decode to string
    curses.noecho()  # Disable echoing again
    return file_name

def navigate_directory(base_dir: str, stdscr):
    current_dir = base_dir
    selected_idx = 0
    start_idx = 0  # Index to keep track of the scrolling
    while True:
        items = list_folders(current_dir, stdscr, selected_idx, start_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
            if selected_idx < start_idx:
                start_idx -= 1  # Scroll up
        elif key == curses.KEY_DOWN and selected_idx < len(items) - 1:
            selected_idx += 1
            max_y, _ = stdscr.getmaxyx()
            if selected_idx >= start_idx + (max_y - 3):  # Adjust for visible area
                start_idx += 1  # Scroll down
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_item = items[selected_idx]
            if selected_item == "Exit":
                break
            elif selected_item.startswith("nano"):
                file_name = prompt_file_name(stdscr)  # Prompt user to enter the file name
                file_path = os.path.join(current_dir, file_name)
                edit_file(file_path, stdscr)  # Edit or create the file using nano
            else:
                selected_path = os.path.join(current_dir, selected_item)
                if os.path.isdir(selected_path):
                    current_dir = selected_path
                    selected_idx = 0
                    start_idx = 0  # Reset scrolling when entering a directory
                else:
                    execute_program(selected_path)
        stdscr.refresh()

def display_menu(stdscr, selected_idx, start_idx):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()  # Get terminal dimensions
    ascii_art_lines = ASCII_ART.strip().splitlines()
    
    # Print ASCII art with boundary checks
    for i, line in enumerate(ascii_art_lines):
        if i >= max_y - 4:
            break
        if len(line) > max_x:
            line = line[:max_x-1]
        stdscr.addstr(i, 0, line)
    
    menu_start_y = len(ascii_art_lines) + 1
    menu_items = ["Navigate Folders", "Exit"]
    display_height = max_y - (menu_start_y + 1)  # Height available for menu items
    visible_items = menu_items[start_idx:start_idx + display_height]

    for i, item in enumerate(visible_items):
        display_text = item if len(item) <= max_x else item[:max_x-1]
        if i + start_idx == selected_idx:
            stdscr.addstr(menu_start_y + i, 0, display_text, curses.color_pair(2) | curses.A_REVERSE)
        else:
            stdscr.addstr(menu_start_y + i, 0, display_text)

    stdscr.refresh()

def menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    selected_idx = 0
    start_idx = 0  # Index to keep track of the scrolling
    while True:
        display_menu(stdscr, selected_idx, start_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
            if selected_idx < start_idx:
                start_idx -= 1  # Scroll up
        elif key == curses.KEY_DOWN and selected_idx < 1:
            selected_idx += 1
            max_y, _ = stdscr.getmaxyx()
            if selected_idx >= start_idx + (max_y - (len(ASCII_ART.strip().splitlines()) + 2)):  # Adjust for visible area
                start_idx += 1  # Scroll down
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_idx == 0:
                navigate_directory(BASE_DIR, stdscr)
            elif selected_idx == 1:  # Exit option selected
                break
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(menu)
  
