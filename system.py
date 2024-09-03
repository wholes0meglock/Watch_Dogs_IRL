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
    stdscr.addstr(0, 0, title, curses.A_BOLD)
    stdscr.addstr(1, 0, "-" * len(title), curses.A_BOLD)

def list_folders(directory: str, stdscr, selected_idx):
    print_header(f"Contents of {directory}", stdscr)
    try:
        items = os.listdir(directory)
        if not items:
            stdscr.addstr(2, 0, "No items found.", curses.color_pair(1))
            return items

        items.append("nano (Edit file with nano)")
        items.append("Exit")
        
        for idx, item in enumerate(items):
            if idx == selected_idx:
                stdscr.addstr(idx + 2, 0, item, curses.color_pair(2) | curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 2, 0, item)
                
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

def edit_file(file_path: str):
    try:
        subprocess.run(['nano', file_path])
    except subprocess.CalledProcessError as e:
        log_message(f"Error editing {file_path}: {e}", 'ERROR')
        print(Fore.RED + f"Error editing {file_path}")

def navigate_directory(base_dir: str, stdscr):
    current_dir = base_dir
    selected_idx = 0
    while True:
        items = list_folders(current_dir, stdscr, selected_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(items) - 1:
            selected_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_item = items[selected_idx]
            if selected_item == "Exit":
                break
            elif selected_item.startswith("nano"):
                file_name = selected_item.split()[0]
                file_path = os.path.join(current_dir, file_name)
                if os.path.isfile(file_path):
                    edit_file(file_path)
                else:
                    max_y, max_x = stdscr.getmaxyx()
                    # Ensure the message is within the screen dimensions
                    if len(items) + 3 < max_y:
                        stdscr.addstr(len(items) + 3, 0, "File does not exist.", curses.color_pair(1))
                    else:
                        stdscr.addstr(max_y - 1, 0, "File does not exist.", curses.color_pair(1))
            else:
                selected_path = os.path.join(current_dir, selected_item)
                if os.path.isdir(selected_path):
                    current_dir = selected_path
                    selected_idx = 0
                else:
                    execute_program(selected_path)
        stdscr.refresh()

def display_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, ASCII_ART)
    stdscr.addstr(7, 0, "Menu", curses.A_BOLD)
    stdscr.addstr(8, 0, "Navigate Folders", curses.color_pair(2) | curses.A_REVERSE)
    stdscr.addstr(9, 0, "Exit")
    stdscr.refresh()

def menu(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    selected_idx = 0
    while True:
        display_menu(stdscr)
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < 1:
            selected_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_idx == 0:
                navigate_directory(BASE_DIR, stdscr)
            elif selected_idx == 1:
                break
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(menu)
  
