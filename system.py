import os
import subprocess
from colorama import init, Fore, Style

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

def print_header(title: str):
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + title)
    print(Fore.LIGHTWHITE_EX + "-" * len(title))

def list_folders(directory: str):
    print_header(f"Contents of {directory}")
    try:
        items = os.listdir(directory)
        if not items:
            print(Fore.RED + "No items found.")
            return
        for idx, item in enumerate(items, 1):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                print(f"{Fore.LIGHTGREEN_EX}{idx}. {item}/")
            else:
                print(f"{Fore.LIGHTCYAN_EX}{idx}. {item}")
        print(f"{Fore.LIGHTCYAN_EX}{len(items) + 1}. nano (Edit file with nano)")
        print(f"{Fore.LIGHTCYAN_EX}{len(items) + 2}. Exit")
    except Exception as e:
        log_message(f"Error listing folders: {e}", 'ERROR')
        print(Fore.RED + f"Error: {e}")

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

def navigate_directory(base_dir: str):
    current_dir = base_dir
    while True:
        list_folders(current_dir)
        choice = input(Fore.WHITE + "Enter the number of the folder to navigate: ").strip()
        try:
            items = os.listdir(current_dir)
            nano_option = len(items) + 1
            exit_option = len(items) + 2
            
            if choice.lower() == 'nano' or int(choice) == nano_option:
                file_name = input(Fore.WHITE + "Enter the filename to edit: ").strip()
                file_path = os.path.join(current_dir, file_name)
                if os.path.isfile(file_path):
                    edit_file(file_path)
                else:
                    print(Fore.RED + "File does not exist.")
            elif int(choice) == exit_option:
                print(Fore.LIGHTGREEN_EX + "Exiting...")
                break
            else:
                idx = int(choice)
                if 1 <= idx <= len(items):
                    selected_item = items[idx - 1]
                    selected_path = os.path.join(current_dir, selected_item)
                    if os.path.isdir(selected_path):
                        current_dir = selected_path
                    else:
                        execute_program(selected_path)
                else:
                    print(Fore.RED + "Invalid choice.")
        except ValueError:
            print(Fore.RED + "Invalid input. Enter a number or 'nano'.")

def display_menu():
    print(Fore.WHITE + ASCII_ART)
    print(Fore.LIGHTCYAN_EX + "Menu")
    print(Fore.LIGHTCYAN_EX + "1. Navigate Folders")
    print(Fore.LIGHTCYAN_EX + "2. Exit")

def menu():
    while True:
        display_menu()
        choice = input(Fore.WHITE + "Enter your choice: ").strip()
        if choice == '1':
            navigate_directory(BASE_DIR)
        elif choice == '2':
            print(Fore.LIGHTGREEN_EX + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
