import os
import gzip
import zlib
import argparse
import subprocess
import sys
import logging
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import tqdm

# Configure logging to print to STDOUT
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# Ensure required packages are installed
def install_packages():
    required_packages = ['tqdm']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            logging.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def compress_file(file_path, compression_level=9):
    """Compress a single file using gzip with a specified compression level."""
    compressed_path = file_path + '.gz'
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb', compresslevel=compression_level) as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"Compressed {file_path} to {compressed_path}")
    except Exception as e:
        logging.error(f"Error compressing {file_path}: {e}")

def decompress_file(file_path):
    """Decompress a single file using gzip."""
    if not file_path.endswith('.gz'):
        logging.warning(f"Skipping {file_path}: Not a gzip file.")
        return
    
    decompressed_path = file_path[:-3]
    try:
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logging.info(f"Decompressed {file_path} to {decompressed_path}")
    except Exception as e:
        logging.error(f"Error decompressing {file_path}: {e}")

def process_file(file_path, action, compression_level):
    match action:
        case 'compress':
            compress_file(file_path, compression_level)
        case 'decompress':
            decompress_file(file_path)
        case _:
            logging.error("Unsupported action. Please use 'compress' or 'decompress'.")

def process_directory(base_path, action, ignore_patterns, compression_level):
    if not os.path.isdir(base_path):
        logging.error(f"Error: {base_path} is not a valid directory.")
        return

    ignore_patterns = [Path(p) for p in ignore_patterns]
    
    # Use dynamic thread count based on system capabilities
    max_workers = os.cpu_count() or 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, _, files in os.walk(base_path):
            for file in files:
                file_path = os.path.join(root, file)
                if any(Path(file).match(p) for p in ignore_patterns):
                    continue
                futures.append(executor.submit(process_file, file_path, action, compression_level))
        
        for future in tqdm.tqdm(futures, desc=f"{action.capitalize()}ing", unit="file"):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing file: {e}")
    
    logging.info(f'{action.capitalize()}ion completed for directory: {base_path}')

def main():
    install_packages()
    
    parser = argparse.ArgumentParser(description='Advanced file compression and decompression tool.')
    parser.add_argument('action', choices=['compress', 'decompress'], help='Action to perform: compress or decompress')
    parser.add_argument('path', help='Path to the directory to process')
    parser.add_argument('--ignore', nargs='*', default=[], help='Patterns of files to ignore (e.g., "*.log")')
    parser.add_argument('--compression-level', type=int, default=9, choices=range(1, 10),
                        help='Compression level for gzip (1-9, default is 9)')
    args = parser.parse_args()

    process_directory(args.path, args.action, args.ignore, args.compression_level)

if __name__ == '__main__':
    main()
        
