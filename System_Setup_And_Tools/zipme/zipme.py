import os
import gzip
import zlib
import argparse
import subprocess
import sys
import tqdm
from pathlib import Path

# Ensure required packages are installed
def install_packages():
    required_packages = ['tqdm']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def compress_file(file_path, compression_level=9):
    """Compress a single file using gzip with a specified compression level."""
    compressed_path = file_path + '.gz'
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb', compresslevel=compression_level) as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Compressed {file_path} to {compressed_path}")
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

def decompress_file(file_path):
    """Decompress a single file using gzip."""
    if not file_path.endswith('.gz'):
        print(f"Skipping {file_path}: Not a gzip file.")
        return
    
    decompressed_path = file_path[:-3]
    try:
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Decompressed {file_path} to {decompressed_path}")
    except Exception as e:
        print(f"Error decompressing {file_path}: {e}")

def process_directory(base_path, action, ignore_patterns, compression_level):
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a valid directory.")
        return

    ignore_patterns = [Path(p) for p in ignore_patterns]

    for root, _, files in os.walk(base_path):
        for file in tqdm.tqdm(files, desc=f"{action.capitalize()}ing", unit="file"):
            file_path = os.path.join(root, file)
            if any(Path(file).match(p) for p in ignore_patterns):
                continue
            
            if action == 'compress':
                compress_file(file_path, compression_level)
            elif action == 'decompress':
                decompress_file(file_path)
            else:
                print("Unsupported action. Please use 'compress' or 'decompress'.")
                return

    print(f'{action.capitalize()}ion completed for directory: {base_path}')

def main():
    install_packages()
    
    parser = argparse.ArgumentParser(description='Advanced file compression and decompression tool.')
    parser.add_argument('action', choices=['compress', 'decompress'], help='Action to perform: compress or decompress')
    parser.add_argument('path', help='Path to the directory to process')
    parser.add_argument('--ignore', nargs='*', default=[], help='Patterns of files to ignore (e.g., "*.log")')
    parser.add_argument('--compression-level', type=int, default=9, choices=range(1, 10),
                        help='Compression level for gzip (1-9, default is 9)')
    args = parser.parse_args()

    if args.action == 'compress' and args.compression_level not in range(1, 10):
        print("Error: Compression level must be between 1 and 9.")
        return

    process_directory(args.path, args.action, args.ignore, args.compression_level)

if __name__ == '__main__':
    main()