### UninstallSHT - Script Cleanup Tool

**UninstallSHT** is a Python utility designed to help you manage and clean up unused scripts and files from specified directories. This tool automatically deletes files that haven't been accessed in a specified number of days, helping you keep your file system organized and free from clutter.

#### Features:
- **Automated Cleanup**: Scans directories and deletes files that haven't been accessed in a user-defined number of days.
- **File Type Filtering**: Specify which file types to target (e.g., `.py`, `.sh`).
- **Dry Run Mode**: Preview which files would be deleted without actually deleting them.
- **Logging**: All deletion activities are logged for your records.

#### Usage:
```bash
python uninstallsht.py --days 14 --dirs ~/projects --types .py,.sh --dry-run
```

#### Arguments:
- `--days`: Number of days to determine unused files (default: 14).
- `--dirs`: Comma-separated list of directories to clean (default: home directory).
- `--types`: Comma-separated list of file extensions to delete (default: `.py,.sh`).
- `--dry-run`: Preview files that would be deleted without actually deleting them.

This tool is ideal for developers and system administrators who want to keep their workspaces tidy by removing old and unused script files.
