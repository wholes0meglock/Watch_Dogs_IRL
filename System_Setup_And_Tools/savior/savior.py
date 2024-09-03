import os
import subprocess
import hashlib
import threading
import logging
import shutil
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    filename='/data/data/com.termux/files/home/savior.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add a handler to also log to STDOUT
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# Request storage permissions
def request_storage_permissions():
    os.system("termux-setup-storage")

# Calculate file checksum
def calculate_checksum(file_path, hash_func=hashlib.sha256):
    hash_obj = hash_func()
    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except IOError:
        logging.error(f"Unable to read file: {file_path}")
        return None

# Save checksums in a database (a simple file)
def save_checksum(file_path, checksum, db_path='/data/data/com.termux/files/home/savior_checksums.txt'):
    with open(db_path, 'a') as db:
        db.write(f"{file_path},{checksum}\n")

# Load checksums from the database
def load_checksums(db_path='/data/data/com.termux/files/home/savior_checksums.txt'):
    checksums = {}
    if os.path.exists(db_path):
        with open(db_path, 'r') as db:
            for line in db:
                file_path, checksum = line.strip().split(',')
                checksums[file_path] = checksum
    return checksums

# Check if a file is corrupted by comparing checksums
def is_file_corrupted(file_path, checksums):
    current_checksum = calculate_checksum(file_path)
    if current_checksum is None:
        return False
    original_checksum = checksums.get(file_path)
    return current_checksum != original_checksum

# Backup files before making changes
def backup_file(file_path, backup_dir='/data/data/com.termux/files/home/savior_backups'):
    os.makedirs(backup_dir, exist_ok=True)
    try:
        backup_path = os.path.join(backup_dir, os.path.basename(file_path))
        shutil.copy2(file_path, backup_path)
        logging.info(f"Backup created for {file_path} at {backup_path}")
    except IOError as e:
        logging.error(f"Failed to backup {file_path}: {e}")

# Manage backups: restore or delete old versions
def manage_backups(action, backup_dir='/data/data/com.termux/files/home/savior_backups'):
    backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
    
    match action:
        case 'restore':
            if not backup_files:
                logging.info("No backups available to restore.")
                return
            latest_backup = max(backup_files, key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
            original_file = os.path.join('/data/data/com.termux/files/home', os.path.basename(latest_backup))
            shutil.copy2(os.path.join(backup_dir, latest_backup), original_file)
            logging.info(f"Restored {original_file} from backup.")
        case 'delete':
            for backup_file in backup_files:
                os.remove(os.path.join(backup_dir, backup_file))
                logging.info(f"Deleted backup: {backup_file}")
        case _:
            logging.error("Invalid backup action specified.")

# Auto-download and install required tools
def setup_environment():
    essential_packages = ['git', 'python', 'curl', 'shellcheck']
    
    # Install missing apt packages
    for package in essential_packages:
        try:
            subprocess.run(['apt', 'install', '-y', package], check=True, capture_output=True, text=True)
            logging.info(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {package} via apt: {e.stderr}")

    # Ensure pip is installed and up-to-date
    try:
        subprocess.run(['apt', 'install', '-y', 'python-pip'], check=True, capture_output=True, text=True)
        logging.info("pip installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install pip via apt: {e.stderr}")

    # Pip packages to install
    pip_packages = ['autopep8', 'black', 'pyflakes']
    for package in pip_packages:
        try:
            subprocess.run(['pip', 'install', '--upgrade', package], check=True, capture_output=True, text=True)
            logging.info(f"{package} installed/updated successfully via pip.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install/update {package} via pip: {e.stderr}")

# Fix Python files with AI assistance
def fix_python_file(file_path):
    try:
        subprocess.run(['python', '-m', 'py_compile', file_path], check=True, capture_output=True, text=True)
        logging.info(f"{file_path} compiled successfully.")
    except subprocess.CalledProcessError:
        logging.warning(f"{file_path} has syntax errors! Attempting to fix...")
        subprocess.run(['autopep8', '--in-place', '--aggressive', '--aggressive', file_path], capture_output=True, text=True)
        logging.info(f"Auto-fixed Python syntax for {file_path}.")
        try:
            subprocess.run(['python', '-m', 'py_compile', file_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            logging.error(f"Could not automatically fix {file_path}. Manual intervention needed.")

# Fix Bash scripts with AI assistance
def fix_bash_file(file_path):
    try:
        subprocess.run(['bash', '-n', file_path], check=True, capture_output=True, text=True)
        logging.info(f"{file_path} passed Bash syntax check.")
    except subprocess.CalledProcessError:
        logging.warning(f"{file_path} has syntax errors! Attempting to fix...")
        subprocess.run(['shellcheck', '--shell=bash', '--format=gcc', file_path], check=True, capture_output=True, text=True)
        logging.info(f"Auto-fixed Bash syntax for {file_path}.")
        try:
            subprocess.run(['bash', '-n', file_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError:
            logging.error(f"Could not automatically fix {file_path}. Manual intervention needed.")

# Scan and fix files in a directory
def scan_and_fix_directory(directory, checksums):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_file_corrupted(file_path, checksums):
                logging.warning(f"Corrupted file found: {file_path}")
                backup_file(file_path)
            if file_name.endswith(".py"):
                fix_python_file(file_path)
            elif file_name.endswith(".sh"):
                fix_bash_file(file_path)

# Parallelize the scanning process
def parallel_scan(base_dir, checksums):
    num_threads = multiprocessing.cpu_count()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        dirs.append(base_dir)
        executor.map(lambda d: scan_and_fix_directory(d, checksums), dirs)

# Self-update functionality
def self_update():
    repo_url = "https://github.com/dedsec1121fk/Nothing"  # Replace with your actual repo URL
    result = subprocess.run(['git', 'pull', repo_url], capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("Savior updated successfully.")
    else:
        logging.error(f"Failed to update Savior: {result.stderr}")

# Main menu for user interaction
def main_menu():
    while True:
        print("\nSavior")
        print("1. Scan & Fix System")
        print("2. Backup Management")
        print("3. Update Savior")
        print("4. Exit")
        choice = input("Choose an option: ")

        match choice:
            case '1':
                logging.info("Started scanning and fixing system files.")
                checksums = load_checksums()
                parallel_scan('/data/data/com.termux/files/home', checksums)
                logging.info("Scan completed.")
            case '2':
                print("Backup Management:")
                print("1. Backup current state")
                print("2. Restore from backup")
                print("3. Delete old backups")
                backup_choice = input("Choose an option: ")

                match backup_choice:
                    case '1':
                        logging.info("Creating backup of all system files.")
                        checksums = load_checksums()
                        parallel_scan('/data/data/com.termux/files/home', checksums)
                        logging.info("Backup completed.")
                    case '2':
                        manage_backups('restore')
                    case '3':
                        manage_backups('delete')
                    case _:
                        logging.error("Invalid backup choice.")
            case '3':
                self_update()
            case '4':
                logging.info("Exiting Savior.")
                break
            case _:
                logging.error("Invalid choice. Please try again.")

# Main function to start the program
def main():
    request_storage_permissions()
    setup_environment()
    main_menu()

if __name__ == "__main__":
    main()
  
