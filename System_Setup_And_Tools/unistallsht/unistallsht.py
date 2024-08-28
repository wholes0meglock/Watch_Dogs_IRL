#!/usr/bin/env python3

import os
import time
import argparse
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(filename='unistallsht.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def install_required_packages():
    """Install required packages if not already installed."""
    packages = ['requests']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"{package} installed successfully.")

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
                            print(f"Would delete {file_path}")
                        else:
                            os.remove(file_path)
                            logging.info(f"Deleted {file_path}")
                            print(f"Deleted {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting {file_path}: {e}")
                    print(f"Error deleting {file_path}: {e}")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Delete unused scripts and files.")
    parser.add_argument('--days', type=int, default=14, help='Number of days to determine unused files (default: 14)')
    parser.add_argument('--dirs', type=str, default=None, help='Comma-separated list of directories to clean (default: home directory)')
    parser.add_argument('--types', type=str, default='.py,.sh', help='Comma-separated list of file extensions to delete (default: .py,.sh)')
    parser.add_argument('--dry-run', action='store_true', help='Preview files that would be deleted without actually deleting them')
    return parser.parse_args()

def main():
    install_required_packages()

    args = parse_args()
    if args.days <= 0:
        print("Error: Number of days must be a positive integer.")
        return

    file_types = args.types.split(',')
    directories = [args.dirs] if args.dirs else [os.path.expanduser("~")]
    if not isinstance(directories, list):
        directories = directories.split(',')

    print(f"Starting cleanup for files not accessed in the last {args.days} days...")
    
    for directory in directories:
        directory = directory.strip()
        if not os.path.isdir(directory):
            print(f"Warning: Directory {directory} does not exist and will be skipped.")
            continue

        # Confirm directory to clean
        if not args.dry_run:
            confirm = input(f"Are you sure you want to clean the directory {directory}? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print(f"Skipping directory {directory}.")
                continue

        delete_old_files(directory, args.days, file_types, args.dry_run)
    
    print("Cleanup completed.")
    logging.info("Cleanup completed.")

if __name__ == "__main__":
    main()