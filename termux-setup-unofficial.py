import requests
import os
import subprocess
import threading
import sys
from colorama import init, Fore, Style
from typing import List, Dict, Tuple

# Initialize Colorama
init(autoreset=True)

# Configuration
GITHUB_USER = 'dedsec1121fk'
BASE_URL = f'https://api.github.com/users/{GITHUB_USER}/repos'
LOCAL_DIR = '/data/data/com.termux/files/home/repos'
EXCLUDED_REPO_URL = 'https://github.com/dedsec1121fk/Downloaddsfk'
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

def get_repos() -> List[Dict]:
    print_header("Fetching Repositories")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_message(f"Error fetching repositories: {e}", 'ERROR')
        print(Fore.RED + f"Error: {e}")
        return []

def set_executable_permissions(path: str):
    try:
        subprocess.run(['chmod', '+x', path], check=True)
        print(Fore.LIGHTGREEN_EX + f"Permissions set for {path}.")
        log_message(f"Permissions set for {path}.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error setting permissions for {path}: {e}", 'ERROR')
        print(Fore.RED + f"Error: {e}")

def clone_or_pull_repo(repo_url: str, repo_name: str):
    if repo_url == EXCLUDED_REPO_URL:
        print(Fore.LIGHTYELLOW_EX + f"Skipping excluded repository: {repo_name}")
        return
    repo_path = os.path.join(LOCAL_DIR, repo_name)
    try:
        if os.path.exists(repo_path):
            print(Fore.LIGHTCYAN_EX + f'Updating {repo_name}...')
            subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
        else:
            print(Fore.LIGHTCYAN_EX + f'Cloning {repo_name}...')
            subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
        set_executable_permissions(repo_path)
    except subprocess.CalledProcessError as e:
        log_message(f"Error cloning/updating {repo_name}: {e}", 'ERROR')
        print(Fore.RED + f"Error: {e}")

def delete_repo(repo_name: str):
    repo_path = os.path.join(LOCAL_DIR, repo_name)
    try:
        if os.path.exists(repo_path):
            print(Fore.LIGHTRED_EX + f'Deleting {repo_name}...')
            subprocess.run(['rm', '-rf', repo_path], check=True)
        else:
            print(Fore.LIGHTYELLOW_EX + f'{repo_name} does not exist.')
    except subprocess.CalledProcessError as e:
        log_message(f"Error deleting {repo_name}: {e}", 'ERROR')
        print(Fore.RED + f"Error: {e}")

def list_repos(repos: List[Dict]) -> Dict[int, Tuple[str, str]]:
    print_header("Available Repositories")
    repo_dict = {}
    if not repos:
        print(Fore.RED + "No repositories.")
        return repo_dict
    for i, repo in enumerate(repos):
        repo_name, repo_url = repo['name'], repo['clone_url']
        repo_dict[i + 1] = (repo_name, repo_url)
        print(f'{Fore.LIGHTGREEN_EX}{i + 1}. {repo_name}')
    return repo_dict

def find_executable_files(program_path: str) -> List[str]:
    exec_extensions = ('.py', '.bash', '.sh', '.pl')  # Add more extensions if needed
    exec_files = [
        f for f in os.listdir(program_path)
        if os.path.isfile(os.path.join(program_path, f))
        and f.endswith(exec_extensions)
        and os.access(os.path.join(program_path, f), os.X_OK)
    ]
    return exec_files

def search_for_executable_files(base_path: str) -> List[str]:
    exec_extensions = ('.py', '.bash', '.sh', '.pl')
    exec_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(exec_extensions):
                file_path = os.path.join(root, file)
                if os.access(file_path, os.X_OK):
                    exec_files.append(file_path)
    return exec_files

def display_executable_files(exec_files: List[str]):
    """Displays a list of executable files."""
    if not exec_files:
        print(Fore.RED + "No executable files found.")
        return

    print(Fore.LIGHTGREEN_EX + "Executable files:")
    for i, exec_file in enumerate(exec_files):
        print(f"{Fore.LIGHTGREEN_EX}{i + 1}. {exec_file}")

def download_all_repos(repos: List[Dict]):
    print_header("Downloading All Repositories")
    threads = []
    for repo in repos:
        repo_name, repo_url = repo['name'], repo['clone_url']
        if repo_url != EXCLUDED_REPO_URL:
            thread = threading.Thread(target=clone_or_pull_repo, args=(repo_url, repo_name))
            thread.start()
            threads.append(thread)
    
    for thread in threads:
        thread.join()
    print(Fore.LIGHTGREEN_EX + "All repositories have been processed.")

def start_program():
    print_header("Start Program")
    
    # Display the message with the command to copy and paste
    command_message = "Copy & Paste this command to the terminal:\ncd repos then write ls"
    print(Fore.LIGHTCYAN_EX + command_message)

def delete_program():
    print_header("Delete Specific Program")
    # List all downloaded repositories
    repos = get_repos()
    repo_dict = list_repos(repos)
    
    if not repo_dict:
        print(Fore.RED + "No repositories available to delete.")
        return

    choice = input(Fore.WHITE + "Enter the number of the repository to delete or 'exit' to return: ").strip()
    if choice.lower() == 'exit':
        return

    try:
        idx = int(choice)
        if 1 <= idx <= len(repo_dict):
            repo_name = repo_dict[idx - 1][0]
            print(Fore.LIGHTYELLOW_EX + f"Deleting {repo_name}...")
            delete_repo(repo_name)
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Enter a number.")

def change_user():
    new_url = input(Fore.WHITE + "Enter new GitHub profile URL (format: https://github.com/username): ").strip()
    if new_url.startswith('https://github.com/'):
        global GITHUB_USER
        GITHUB_USER = new_url.split('/')[-1]
        global BASE_URL
        BASE_URL = f'https://api.github.com/users/{GITHUB_USER}/repos'
        print(Fore.LIGHTGREEN_EX + f"GitHub user changed to {GITHUB_USER}.")
    else:
        print(Fore.RED + "Invalid URL format.")

def display_menu():
    print(Fore.WHITE + ASCII_ART)
    print(Fore.LIGHTCYAN_EX + "Menu")
    print(Fore.LIGHTCYAN_EX + "1. Download Everything")
    print(Fore.LIGHTCYAN_EX + "2. Choose To Download")
    print(Fore.LIGHTCYAN_EX + "3. Delete All")
    print(Fore.LIGHTCYAN_EX + "4. Change GitHub User")
    print(Fore.LIGHTCYAN_EX + "5. Start Program")
    print(Fore.LIGHTCYAN_EX + "6. Delete Specific Program")
    print(Fore.LIGHTCYAN_EX + "7. Exit")

def menu():
    while True:
        display_menu()
        choice = input(Fore.WHITE + "Enter your choice: ").strip()
        if choice == '1':
            repos = get_repos()
            download_all_repos(repos)
        elif choice == '2':
            start_program()
        elif choice == '3':
            repos = get_repos()
            print(Fore.LIGHTYELLOW_EX + "Deleting all repositories.")
            for repo in repos:
                delete_repo(repo['name'])
        elif choice == '4':
            change_user()
        elif choice == '5':
            start_program()
        elif choice == '6':
            delete_program()
        elif choice == '7':
            print(Fore.LIGHTGREEN_EX + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
