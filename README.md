**Watch_Dogs_IRL: Terminal File Explorer & Script Executor for Termux**

**Watch_Dogs_IRL** is a Python-based file explorer and script executor built specifically for the Termux environment on Android. It provides a powerful terminal interface that lets you easily navigate directories, manage and edit files, and execute scripts directly from Termux. With built-in logging, you can effortlessly track your actions and troubleshoot any issues.

### Features:
- **Directory Navigation**: Browse and view directory contents with an intuitive, colorful interface—just by using arrow keys.
- **Script Execution**: Run scripts directly from the folder by selecting them. Supports Python, Bash, Perl, Ruby, and Node.js.
- **File Editing**: Edit files using Nano directly within the terminal by selecting the "nano" option and typing the file name within the current folder.
- **File Management**: Simplify file handling with optional Flask integration.
- **SQLite Database Integration**: Manage databases directly within Termux.
- **AES Encryption**: Secure your data with AES encryption (CBC Mode, Password-based Key Derivation).
- **Automation**: Automate tasks like dependency management and server control.
- **Games**: Run or develop terminal-based games.

### Getting Started:
To make **Watch_Dogs_IRL** start automatically whenever you open Termux:
1. Open the bash configuration file by running:
   ```bash
   nano ../usr/etc/bash.bashrc
   ```
2. Add the following lines at the end of the file:
   ```bash
   cd Watch_Dogs_IRL
   chmod +x system.py
   python system.py
   ```

### Requirements:
- **Termux** on Android
- **Python 3** installed
- `colorama` Python library

### Usage:
1. Clone this repository to your Termux environment.
2. Run the script using Python.
3. Use the interactive menu to navigate directories, execute scripts, or edit files.

**Watch_Dogs_IRL** is perfect for developers, system administrators, and power users seeking a robust file management and automation tool within Termux. Whether you need to manage files, handle databases, secure data, automate tasks, or even develop games, this tool has you covered.
