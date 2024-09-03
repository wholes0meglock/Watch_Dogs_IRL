#!/usr/bin/env python3

import os
import time
import argparse
import logging
import subprocess
import sys

# Configure logging to print to STDOUT as well
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler('unistallsht.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def install_required_packages():
    """Install required packages if not already installed."""
    packages = ['requests']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            logger.info(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                logger.info(f"{package} installed successfully.")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install {package}: {e}")

def run_command(command):
    """Run a command using subprocess and handle errors."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Command '{' '.join(command)}' ran successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(command)}' failed: {e.stderr}")
        return None

def get_file_modification_time(file_path):
    """Get the last modification time of a file."""
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return 0

def delete_old_files(directory, threshold_days, file_types, dry_run):
    """Delete files in the directory that haven't been accessed in threshold_days."""
    threshold_seconds = threshold_days * 86400  # Convert days to seconds
    now = time.time()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path == os.path.abspath(__file__):
                continue  # Skip this script file

            if any(file_path.endswith(ft) for ft in file_types):
                try:
                    last_access_time = get_file_modification_time(file_path)
                    if now - last_access_time > threshold_seconds:
                        if dry_run:
                            logger.info(f"Would delete {file_path}")
                        else:
                            os.remove(file_path)
                            logger.info(f"Deleted {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting {file_path}: {e}")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Delete unused scripts and files.")
    parser.add_argument('--days', type=int, default=14, help='Number of days to determine unused files (default: 14)')
    parser.add_argument('--dirs', type=str, default=None, help='Comma-separated list of directories to clean (default: home directory)')
    parser.add_argument('--types', type=str, default='.py,.sh', help='Comma-separated list of file extensions to delete (default: .py,.sh)')
    parser.add_argument('--dry-run', action='store_true', help='Preview files that would be deleted without actually deleting them')
    return parser.parse_args()

def clean_directory(directory, file_types, threshold_days, dry_run):
    """Clean a specific directory after user confirmation."""
    directory = directory.strip()
    if not os.path.isdir(directory):
        logger.warning(f"Directory {directory} does not exist and will be skipped.")
        return

    # Confirm directory to clean
    if not dry_run:
        confirm = input(f"Are you sure you want to clean the directory {directory}? (yes/no): ").strip().lower()
        if confirm != 'yes':
            logger.info(f"Skipping directory {directory}.")
            return

    delete_old_files(directory, threshold_days, file_types, dry_run)

def main():
    install_required_packages()

    args = parse_args()
    if args.days <= 0:
        logger.error("Error: Number of days must be a positive integer.")
        return

    file_types = args.types.split(',')
    directories = [args.dirs] if args.dirs else [os.path.expanduser("~")]
    if not isinstance(directories, list):
        directories = directories.split(',')

    logger.info(f"Starting cleanup for files not accessed in the last {args.days} days...")
    
    for directory in directories:
        clean_directory(directory, file_types, args.days, args.dry_run)
    
    logger.info("Cleanup completed.")

if __name__ == "__main__":
    main()
    
