# System: Terminal File Explorer & Script Executor for Termux (Includes Extra Tools and Not Only)

**System** is a Python-based, terminal-focused file explorer and script executor designed specifically for the Termux environment on Android. It allows you to navigate directories, manage and edit files, and execute various scripts directly from the terminal. With built-in logging, it helps you track your actions and troubleshoot errors effectively.

### Features:
- **Directory Navigation**: Easily browse and view the contents of directories with an intuitive, colorful interface.
- **Script Execution**: Seamlessly run scripts written in Python, Bash, Perl, Ruby, and Node.js.
- **File Editing**: Edit any file using Nano directly from the terminal interface.
- **Logging**: All actions and errors are logged into a file, simplifying error tracking and management.
- **Advanced Python Development**:
  - **File Management**: Simplify file handling with potential Flask integration.
  - **SQLite Database Integration**: Manage databases directly within Termux.
  - **AES Encryption**: Secure your data with AES encryption (CBC Mode, Password-based Key Derivation).
  - **Automation**: Automate tasks like dependency management and server control.
  - **Games**: Execute or develop terminal-based games.

### Getting Started:
To make the **System** program start automatically whenever you open Termux:
1. Open the bash configuration file by running:
   ```bash
   nano ../usr/etc/bash.bashrc
   ```
2. Add the following lines at the end of the file:
   ```bash
   cd termux-setup-unofficial
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

**System** is ideal for developers, system administrators, and power users looking for a powerful and easy-to-use file management and automation tool within Termux. It offers robust features for advanced Python development, including file management, database handling, encryption, automation, and even game development.
