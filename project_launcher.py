#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
from pathlib import Path

# --- Configurable paths ---
PROJECTS_DIR = os.path.expanduser('~/Desktop/Personal/Projects/')
LAST_PROJECT_FILE = os.path.join(PROJECTS_DIR, 'initiatorScript/last_project.txt')

# --- Helper functions ---
def get_username():
    return os.environ.get('USER').capitalize() or os.environ.get('USERNAME').capitalize()

def get_greeting():
    now = datetime.datetime.now().hour
    if now < 12:
        return f"Good Morning, {get_username()}!"
    elif now < 18:
        return f"Good Afternoon, {get_username()}!"
    else:
        return f"Good Evening, {get_username()}!"

def list_projects():
    if not os.path.isdir(PROJECTS_DIR):
        print(f"[Error] Projects directory not found: {PROJECTS_DIR}")
        sys.exit(1)
    projects = [d for d in os.listdir(PROJECTS_DIR)
                if os.path.isdir(os.path.join(PROJECTS_DIR, d)) and not d.startswith('.')]
    projects.sort()
    return projects

def read_last_project():
    try:
        with open(LAST_PROJECT_FILE, 'r') as f:
            return f.read().strip()
    except Exception:
        return None

def write_last_project(project_name):
    try:
        with open(LAST_PROJECT_FILE, 'w') as f:
            f.write(project_name)
    except Exception as e:
        print(f"[Warning] Could not save last project: {e}")

def prompt_main(last_project):
    print("\nWould you like to open a project?\n")
    print("[1] No (quit)")
    print("[2] Yes (choose a project)")
    if last_project:
        print(f"[3] Yes (open the last project: \"{last_project}\")")
    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()
        if choice in {'1', '2', '3'}:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def prompt_project_selection(projects):
    print("\nSelect a project:")
    for idx, name in enumerate(projects, 1):
        print(f"[{idx}] {name}")
    print("[0] Cancel")
    while True:
        choice = input("Enter project number: ").strip()
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(projects):
            return projects[int(choice)-1]
        print("Invalid input. Please enter a valid number.")

def execute_project_commands(project_path):
    exec_file = os.path.join(project_path, 'execute.txt')
    if os.path.isfile(exec_file):
        print(f"\n[Info] Found 'execute.txt' in {os.path.basename(project_path)}. Executing commands...\n")
        with open(exec_file, 'r') as f:
            commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        for cmd in commands:
            print(f"$ {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, cwd=project_path, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[Error] Command failed: {cmd}\n  Exit code: {e.returncode}")
    else:
        print(f"\n[Warning] No 'execute.txt' file found in {os.path.basename(project_path)}.")
        while True:
            ans = input("Would you like to create a new execute.txt file? (y/n): ").strip().lower()
            if ans == 'n':
                print("Exiting.")
                return
            elif ans == 'y':
                open(exec_file, 'w').close()
                print(f"Created {exec_file}. Opening in VS Code...")
                subprocess.run(f"code '{exec_file}'", shell=True)
                while True:
                    scan_ans = input("Would you like to scan and execute the new execute.txt now? (y/n): ").strip().lower()
                    if scan_ans == 'y':
                        if os.path.isfile(exec_file):
                            with open(exec_file, 'r') as f:
                                commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                            if not commands:
                                print("No commands found in execute.txt. Exiting.")
                                return
                            print(f"\n[Info] Executing commands from {exec_file}...\n")
                            for cmd in commands:
                                print(f"$ {cmd}")
                                try:
                                    result = subprocess.run(cmd, shell=True, cwd=project_path, check=True)
                                except subprocess.CalledProcessError as e:
                                    print(f"[Error] Command failed: {cmd}\n  Exit code: {e.returncode}")
                        else:
                            print("execute.txt not found. Exiting.")
                        return
                    elif scan_ans == 'n':
                        print("Exiting.")
                        return
                    else:
                        print("Please enter 'y' or 'n'.")
                return
            else:
                print("Please enter 'y' or 'n'.")

def main():
    if not sys.stdin.isatty():
        # we exit with 99 because inside the .zprofile there's a fallback functions that specified to run
        # we exit the script using this specific exit code.
        sys.exit(99)
    print(get_greeting())
    projects = list_projects()
    last_project = read_last_project()
    choice = prompt_main(last_project)
    if choice == '1':
        sys.exit(99)
    elif choice == '2':
        if not projects:
            print("[Error] No projects found.")
            sys.exit(99)
        project = prompt_project_selection(projects)
        if not project:
            print("No project selected. Exiting.")
            sys.exit(99)
    elif choice == '3':
        if not last_project or last_project not in projects:
            print("[Error] No valid last project found.")
            sys.exit(99)
        project = last_project
    else:
        print("[Error] Unexpected input.")
        sys.exit(99)
    project_path = os.path.join(PROJECTS_DIR, project)
    write_last_project(project)
    execute_project_commands(project_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Interrupted] Exiting.")
        sys.exit(99) 