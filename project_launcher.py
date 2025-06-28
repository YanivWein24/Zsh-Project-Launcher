import os
import sys
import subprocess
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.table import Table
    from rich.text import Text
    from rich import box
except ImportError:
    print("[!] The 'rich' library is required. Please install it using: pip install rich")
    sys.exit(1)

console = Console()

# --- Configurable paths ---
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.abspath(os.path.join(REPO_ROOT, '..'))
LAST_PROJECT_FILE = os.path.join(REPO_ROOT, 'last_project.txt')

# --- Helper functions ---
def get_username() -> str:
    return os.environ.get('USER').capitalize() or os.environ.get('USERNAME').capitalize()

def get_greeting() -> str:
    now = datetime.datetime.now().hour
    if now < 12:
        return f"Good Morning, {get_username()}!"
    elif now < 18:
        return f"Good Afternoon, {get_username()}!"
    else:
        return f"Good Evening, {get_username()}!"

def print_exit_message() -> None:
    return console.print(Panel.fit("Keep On Coding! 👨🏻‍💻", style="bold blue"))

def list_projects() -> list[str]:
    if not os.path.isdir(PROJECTS_DIR):
        console.print(f"[bold red][Error][/bold red] Main Projects directory not found: {PROJECTS_DIR}")
        sys.exit(99)
    projects: list[str] = [d for d in os.listdir(PROJECTS_DIR)
                if os.path.isdir(os.path.join(PROJECTS_DIR, d)) and not d.startswith('.')]
    projects.sort()
    return projects

def read_last_project() -> str:
    last_project_dir = os.path.dirname(LAST_PROJECT_FILE)
    os.makedirs(last_project_dir, exist_ok=True)
    if not os.path.isfile(LAST_PROJECT_FILE):
        with open(LAST_PROJECT_FILE, 'w') as f:
            f.write("")
        return ""
    try:
        with open(LAST_PROJECT_FILE, 'r') as f:
            return f.read().strip()
    except Exception:
        return ""

def write_last_project(project_name: str) -> None:
    last_project_dir = os.path.dirname(LAST_PROJECT_FILE)
    os.makedirs(last_project_dir, exist_ok=True)
    try:
        with open(LAST_PROJECT_FILE, 'w') as f:
            f.write(project_name)
    except Exception as e:
        console.print(f"[bold yellow][Warning][/bold yellow] Could not save last project: {e}")

def prompt_main(last_project: str) -> str:
    console.print(Panel.fit("Would you like to open a project?", style="bold cyan"))
    options = [
        "[1] No (quit)",
        "[2] Yes (choose a project)",
    ]
    valid_choices = ["1", "2"]
    # Only show the last project option if it is not None and not empty
    if last_project and last_project.strip():
        options.append(f"[3] Yes (open the last project: [bold green]\"{last_project}\"[/bold green])")
        valid_choices.append("3")
    for opt in options:
        console.print(opt)
    while True:
        choice = Prompt.ask("[bold yellow]\nEnter your choice ({})[/bold yellow]".format("/".join(valid_choices)), choices=valid_choices, default="2")
        return choice

def prompt_project_selection(projects: list[str]) -> str:
    # Returns the selected project name, or an empty string if cancelled
    table = Table(title="Select a project", box=box.ROUNDED, show_lines=True, style="cyan")
    table.add_column("#", style="bold yellow", justify="right")
    table.add_column("Project Name", style="bold white")
    for idx, name in enumerate(projects, 1):
        table.add_row(str(idx), name)
    table.add_row("0", "[red]Cancel[/red]")
    console.print(table)
    while True:
        choice = IntPrompt.ask("[bold yellow]Enter project number[/bold yellow]", default=0)
        if choice == 0:
            return ""
        if 1 <= choice <= len(projects):
            return projects[choice-1]
        console.print("[red]Invalid input. Please enter a valid number.[/red]")

def execute_project_commands(project_path: str) -> None:
    exec_file = os.path.join(project_path, 'execute.txt')
    if os.path.isfile(exec_file):
        console.print(Panel.fit(f"Found 'execute.txt' in [bold green]{os.path.basename(project_path)}[/bold green]. Executing commands...", style="bold magenta"))
        with open(exec_file, 'r') as f:
            commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        for cmd in commands:
            console.print(f"[bold blue]$ {cmd}[/bold blue]")
            try:
                result = subprocess.run(cmd, shell=True, cwd=project_path, check=True)
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red][Error][/bold red] Command failed: {cmd}\n  Exit code: {e.returncode}")
    else:
        console.print(Panel.fit(f"No 'execute.txt' file found in [bold yellow]{os.path.basename(project_path)}[/bold yellow].", style="bold red"))
        while True:
            ans = Confirm.ask("Would you like to create a new execute.txt file?", default=False)
            if not ans:
                console.print("[bold cyan]Exiting.[/bold cyan]")
                return
            else:
                open(exec_file, 'w').close()
                console.print(f"Created [bold green]{exec_file}[/bold green]. Opening in VS Code...")
                subprocess.run(f"code '{exec_file}'", shell=True)
                while True:
                    scan_ans = Confirm.ask("Would you like to scan and execute the new execute.txt now?", default=True)
                    if not scan_ans:
                        console.print("[bold cyan]Exiting.[/bold cyan]")
                        return

                    if not os.path.isfile(exec_file):
                        console.print("[bold red]execute.txt not found. Exiting.[/bold red]")
                        return

                    with open(exec_file, 'r') as f:
                        commands = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
                    if not commands:
                        console.print("[bold yellow]No commands found in execute.txt. Exiting.[/bold yellow]")
                        return

                    console.print(Panel.fit(f"Executing commands from [bold green]{exec_file}[/bold green]...", style="bold magenta"))
                    for cmd in commands:
                        console.print(f"[bold blue]$ {cmd}[/bold blue]")
                        try:
                            result = subprocess.run(cmd, shell=True, cwd=project_path, check=True)
                        except subprocess.CalledProcessError as e:
                            console.print(f"[bold red][Error][/bold red] Command failed: {cmd}\n  Exit code: {e.returncode}")
                    return

def main() -> None:
    if not sys.stdin.isatty():
        sys.exit(99)
    console.print(Panel.fit(get_greeting(), style="bold green"))
    projects = list_projects()
    last_project = read_last_project()
    choice = prompt_main(last_project)
    if choice == '1':
        print_exit_message()
        sys.exit(99)
    elif choice == '2':
        if not projects:
            console.print("[bold red][Error][/bold red] No projects found - Exiting")
            print_exit_message()
            sys.exit(99)
        project = prompt_project_selection(projects)
        if not project:
            console.print("[bold yellow]No project selected - Exiting.[/bold yellow]")
            print_exit_message()
            sys.exit(99)
    elif choice == '3':
        if not last_project or last_project not in projects:
            console.print("[bold red][Error][/bold red] No valid last project found.")
            print_exit_message()
            sys.exit(99)
        project = last_project
    else:
        console.print("[bold red][Error][/bold red] Unexpected input.")
        sys.exit(99)
    project_path = os.path.join(PROJECTS_DIR, project)
    write_last_project(project)
    execute_project_commands(project_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][Interrupted] Exiting.[/bold yellow]")
        sys.exit(99) 