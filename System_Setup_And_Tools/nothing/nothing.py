#!/data/data/com.termux/files/usr/bin/python

import os
import subprocess
import sqlite3
import random
import string
import base64
import ssl
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import sys
import urllib.request

# Constants
DATABASE_FILE = 'app_data.db'
UPLOAD_FOLDER = "/storage/emulated/0/Cloud"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
REPO_URL = "https://github.com/dedsec1121fk/Nothing"
RAW_URL = "https://raw.githubusercontent.com/dedsec1121fk/Nothing/main/"

# ASCII Art
def display_ascii_art():
    print("""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@#**+::....:......=%@@@@@@@@@@@@
@@@@@@@@@@+**+@@@%+*#=..:=++--*@@@@@@@@@@@@
@@@@@@@@%.:-#@@@@@@%+...+..:+#@@@@@@@@@@@@@
@@@@@@@%+@@*:+#@@@@@@#-.....-@@%@@@@@@@@@@@
@@@@@@@%#--.+*#%@@@@#@@+:...:+%+-@@@@@@@@@@
@@@@@@@+*@@@##*%@@%**=++@*...-=%**@@@@@@@@@
@@@@@@%*@:..-%@@*==*+--+-*##%*:-%#@@@@@@@@@
@@@@@@%#@=+=+:.:%@@*+#%%%#%@@%#*:-@@@@@@@@@
@@@@@@@%@@%@@@%=:.=@@@@@@@@@@@@=.=@@@@@@@@@
@@@@@@@%@@@@%%@@@#=::+*%%%#*+++:=@@@@@@@@@@
@@@@@@@%@@@@@@@@@@@@%#++*#%%%%%%@@@@@@@@@@@
@@@@@@@@#@@@@@@@@@@@@@@@@@@@@@@+%@@@@@@@@@@
@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@#-%@@@@@@@@@
@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@%+*#@@@@@@@@
@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@*@:+*@@@@@@
@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@#@*#*==@@@@
@@@@@@@@*=@@@@@@@@@@@@@@@@@@@@@@@%*@@*..=@@
@@@@@@-:+##@@@@@@@@@@@@@@@@@@@@@@%%@@@+.*#%
@@@@+=*@@%*@@@@@@@@@@@@@@@@@@@@@@@@@@@+.-@*
@@@-##@@@%+@@@@@@@@@@@@@@@@@@@@@@@@@@@=:%@+
@*:=@@@@@%+@@@@@@@@@@@@@@@@@@@@@@@@@@%-+@%:
""")

# Psila,psila,ta maura ta mpere,den ta,den ta,den ta nikoun pote!
# 2023 E' ESSO

# Function to generate a random password
def generate_password():
    """Generate a random password of 16 characters."""
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16))

# Secure encryption/decryption functions
def derive_key(password: str, salt: bytes):
    """Derive a key from a password and salt using PBKDF2HMAC."""
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    ).derive(password.encode())

def encrypt_text(text: str, password: str):
    """Encrypt text using AES CBC mode."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(128).padder()
    ciphertext = cipher.encryptor().update(padder.update(text.encode()) + padder.finalize()) + cipher.encryptor().finalize()
    return base64.b64encode(salt + iv + ciphertext).decode()

def decrypt_text(encrypted_text: str, password: str):
    """Decrypt text encrypted with AES CBC mode."""
    data = base64.b64decode(encrypted_text)
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(128).unpadder()
    decrypted_data = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
    return padder.update(decrypted_data) + padder.finalize()

# Database operations with SQLite
def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_data():
    """Add new data to the database."""
    data = input("Enter data to add: ")
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("INSERT INTO data (content) VALUES (?)", (data,))
    conn.commit()
    conn.close()
    print("Data added successfully.")

def edit_data():
    """Edit existing data in the database."""
    search_term = input("Enter search term to edit: ")
    conn = sqlite3.connect(DATABASE_FILE)
    results = conn.execute("SELECT id, content FROM data WHERE content LIKE ?", ('%' + search_term + '%',)).fetchall()

    if not results:
        print("No matching data found.")
        return
    
    for row in results:
        print(f"{row[0]}: {row[1]}")
    
    data_id = input("Enter the ID of the record to edit: ")
    new_content = input("Enter new content: ")
    conn.execute("UPDATE data SET content = ? WHERE id = ?", (new_content, data_id))
    conn.commit()
    conn.close()
    print("Data edited successfully.")

def search_data():
    """Search for data in the database."""
    search_term = input("Enter search term: ")
    conn = sqlite3.connect(DATABASE_FILE)
    results = conn.execute("SELECT content FROM data WHERE content LIKE ?", ('%' + search_term + '%',)).fetchall()
    conn.close()

    if not results:
        print("No matching data found.")
    else:
        print("Matching data:")
        for row in results:
            print(row[0])

def see_database():
    """Display all data in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    data = conn.execute("SELECT content FROM data").fetchall()
    conn.close()

    if not data:
        print("The database is empty.")
    else:
        for row in data:
            print(row[0])

def database_menu():
    """Display the database menu and handle user input."""
    while True:
        display_ascii_art()
        print("\n1) Add Data")
        print("2) Edit Data")
        print("3) Search Data")
        print("4) See Database")
        print("5) Return to Main Menu\n")
        
        print("Psila,psila,ta maura ta mpere,den ta,den ta,den ta nikoun pote!\n2023 E' ESSO\n")

        option = input("Choose an option: ")

        if option == '1':
            add_data()
        elif option == '2':
            edit_data()
        elif option == '3':
            search_data()
        elif option == '4':
            see_database()
        elif option == '5':
            break
        else:
            print("Invalid option. Please try again.")

# Automate package installation and setup
def install_packages():
    """Install required Python packages."""
    try:
        subprocess.run(["pip", "install", "--upgrade", "Flask", "bcrypt", "cryptography"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}. Please install them manually.")
        sys.exit(1)

try:
    install_packages()
except ImportError:
    raise ImportError("Please install required packages using 'pip install Flask bcrypt cryptography'.")

app = Flask(__name__)
bcrypt = Bcrypt(app)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page, listing files by extension."""
    files_by_extension = get_files_by_extension()
    return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DedSec1121 Local Cloud Storage</title>
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                h1, h2 {
                    color: white;
                }
                a {
                    color: white;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <h1>DedSec1121 Local Cloud Storage</h1>
            <h2>Upload New File</h2>
            <form method=post enctype=multipart/form-data action="/upload">
                <input type=file name=file>
                <input type=submit value=Upload>
            </form>
            <h2>Files</h2>
            <ul>
                {% for extension, files in files_by_extension.items()|sort %}
                    <li>
                        <strong>{{ extension }}</strong>
                        <ul>
                            {% for file in files|sort %}
                                <li>
                                    <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a>
                                    <a href="{{ url_for('delete_file', filename=file) }}">(Delete)</a>
                                </li>
                            {% endfor %}
                        </ul>
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
    """, files_by_extension=files_by_extension)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and save the file to the upload folder."""
    if 'file' not in request.files or not request.files['file'].filename:
        return redirect(url_for('index'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    """Serve a file for download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete_file(filename):
    """Delete a file from the upload folder."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

def get_files_by_extension():
    """Get a dictionary of files categorized by their extensions."""
    files_by_extension = {}
    # Check if the upload folder exists, create if not
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # List files and categorize by extension
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        extension = os.path.splitext(filename)[1].lower()
        if extension not in files_by_extension:
            files_by_extension[extension] = []
        files_by_extension[extension].append(filename)
    return files_by_extension

def stop_flask_server(force=False):
    """Stops the Flask server. Forcefully if 'force' is True."""
    try:
        # Find the PID of the Flask server process
        pgrep_command = "pgrep -f 'python.*f.py'"
        pids = subprocess.check_output(pgrep_command, shell=True).decode().strip().split()

        if not pids:
            print("No Flask server is currently running.")
            return

        for pid in pids:
            if force:
                print(f"Forcefully stopping Flask server with PID: {pid}")
                subprocess.run(f"kill -9 {pid}", shell=True, check=True)
            else:
                print(f"Stopping Flask server with PID: {pid}")
                subprocess.run(f"kill {pid}", shell=True, check=True)

        print("Flask server(s) stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Flask server: {e}")

# Main Menu
def main_menu():
    """Display the main menu and handle user input."""
    init_db()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    while True:
        display_ascii_art()
        print("\n1) Database Operations")
        print("2) Run Local Server")
        print("3) Generate Password")
        print("4) Encrypt Text")
        print("5) Decrypt Text")
        print("6) Quit\n")
        
        print("Psila,psila,ta maura ta mpere,den ta,den ta,den ta nikoun pote!\n2023 E' ESSO\n")

        option = input("Choose an option: ")

        if option == '1':
            database_menu()
        elif option == '2':
            local_server_menu()
        elif option == '3':
            print("Generated password:", generate_password())
        elif option == '4':
            text = input("Enter text to encrypt: ")
            password = input("Enter password: ")
            print("Encrypted text:", encrypt_text(text, password))
        elif option == '5':
            encrypted_text = input("Enter text to decrypt: ")
            password = input("Enter password: ")
            try:
                print("Decrypted text:", decrypt_text(encrypted_text, password))
            except Exception as e:
                print("Decryption failed:", e)
        elif option == '6':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

def local_server_menu():
    """Display the local server menu and handle user input."""
    while True:
        display_ascii_art()
        print("\n1) Start Local Server")
        print("2) Stop Local Server Gracefully")
        print("3) Force Stop Local Server")
        print("4) Return to Main Menu\n")

        option = input("Choose an option: ")

        if option == '1':
            print("Starting Flask server...")
            app.run(host='0.0.0.0', port=5000)
        elif option == '2':
            print("Stopping Flask server gracefully...")
            stop_flask_server(force=False)
        elif option == '3':
            print("Force stopping Flask server...")
            stop_flask_server(force=True)
        elif option == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()

