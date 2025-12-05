import os
import subprocess
import sys
import json
import tkinter as tk
from tkinter import filedialog

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("==================================================")
    print("       Flask Testing")
    print("==================================================")

def run_command(command, env=None):
    try:
        subprocess.run(command, check=True, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def get_docker_image_tag(tar_path):
    """Extracts the first repo tag from a docker save tarball"""
    try:
        print(f"Loading image from {tar_path}...")
        result = subprocess.run(f"sudo docker load -i '{tar_path}'", shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error loading image: {result.stderr}")
            return None
            
        print(result.stdout)
        
        for line in result.stdout.splitlines():
            if "Loaded image:" in line:
                return line.split("Loaded image:")[1].strip()
        
        print("Could not auto-detect image tag from output.")
        return input("Please enter the image tag (e.g., webapp:latest): ").strip()
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def select_folder():
    """Opens a dialog to select a folder"""
    root = tk.Tk()
    root.withdraw() # Hide main window
    folder_path = filedialog.askdirectory(title="Select App Folder")
    root.destroy()
    return folder_path

def select_file():
    """Opens a dialog to select a .tar file"""
    root = tk.Tk()
    root.withdraw() # Hide main window
    file_path = filedialog.askopenfilename(
        title="Select Docker Image",
        filetypes=[("Docker Image", "*.tar"), ("All Files", "*.*")]
    )
    root.destroy()
    return file_path

def main():
    clear_screen()
    print_header()
    print("Select the application source to test:")
    print("1. Default App (Flask-Testing/app)")
    print("2. Custom App Folder (Select path)")
    print("3. Docker Image (Select .tar file)")
    print("0. Exit")
    
    choice = input("\nEnter option (0-3): ").strip()
    
    env = os.environ.copy()
    
    if choice == '1':
        print("\nUsing default app in ./app")
        env['APP_CONTEXT'] = './app'
        env['APP_IMAGE'] = 'webapp:latest' 
        
        print("Starting tests...")
        run_command("sudo -E docker compose up --build test-runner", env=env)
        
    elif choice == '2':
        print("\nOpening file dialog...")
        path = select_folder()
        
        if not path:
            print("No folder selected. Exiting.")
            sys.exit(1)
            
        print(f"Selected path: {path}")
        
        if not os.path.exists(path):
            print("Error: Path does not exist.")
            sys.exit(1)
            
        print(f"\nUsing custom app in {path}")
        env['APP_CONTEXT'] = path
        env['APP_IMAGE'] = 'webapp:custom'
        
        print("Starting tests...")
        run_command("sudo -E docker compose up --build test-runner", env=env)
        
    elif choice == '3':
        print("\nOpening file dialog...")
        tar_path = select_file()
        
        if not tar_path:
            print("No file selected. Exiting.")
            sys.exit(1)
            
        print(f"Selected file: {tar_path}")
        
        if not os.path.exists(tar_path):
            print("Error: File does not exist.")
            sys.exit(1)
            
        tag = get_docker_image_tag(tar_path)
        if not tag:
            print("Error: Could not determine image tag.")
            sys.exit(1)
            
        print(f"\nUsing Docker image: {tag}")
        
        env['APP_CONTEXT'] = './app' # Dummy context
        env['APP_IMAGE'] = tag
        
        print("Starting tests (Integration only)...")
        run_command("sudo -E docker compose up test-runner", env=env)
        
    elif choice == '0':
        sys.exit(0)
    else:
        print("Invalid option.")
        sys.exit(1)

if __name__ == "__main__":
    main()
