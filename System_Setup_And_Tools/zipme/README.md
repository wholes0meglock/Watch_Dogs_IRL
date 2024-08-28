# Advanced File Compression and Decompression Tool

This Python script provides an efficient way to compress and decompress files within a directory using gzip, with support for specifying custom compression levels and ignoring specific file patterns. The tool is designed for batch processing of files and integrates a progress bar for real-time feedback.

## Features

- **Compression and Decompression**: Easily switch between compressing and decompressing files with gzip.
- **Custom Compression Levels**: Choose from compression levels 1 (fastest) to 9 (most compressed).
- **Ignore Specific Files**: Specify file patterns to exclude from processing, e.g., `*.log`.
- **Batch Processing with Progress Bar**: Process all files in a directory with a clear progress indicator.
- **Automatic Package Installation**: Ensures all required Python packages are installed.

## Usage

```bash
python script_name.py <compress|decompress> <path> [--ignore "*.pattern"] [--compression-level 1-9]
```

### Examples

- Compress all files in a directory, ignoring `.log` files:
  ```bash
  python script_name.py compress /path/to/directory --ignore "*.log"
  ```

- Decompress all gzip files in a directory:
  ```bash
  python script_name.py decompress /path/to/directory
  ```

## Requirements

- Python 3.x
- Required packages are automatically installed when the script is run.

## Installation

Clone the repository and run the script:

```bash
git clone https://github.com/yourusername/repo-name.git
cd repo-name
python script_name.py ...
```
