# Zsh Project Launcher

## Overview

**Zsh Project Launcher** is a productivity tool designed for developers who frequently switch between multiple projects and want to automate the setup of their development environments. It streamlines the process of launching all necessary services, tools, and commands for any project, right from your terminal startup—while still allowing you to opt out or select a different project as needed.

## Problem Statement

Manually setting up your development environment for each project can be repetitive and error-prone. You may need to:

- Start servers, databases, or background services
- Open editors or terminals in specific directories
- Run project-specific scripts

This tool eliminates the friction by letting you define per-project startup commands and automatically launching them when you open your terminal, while still giving you the flexibility to skip or choose a different project.

## Features

- **Automatic Project Detection:** Scans your `PROJECTS_DIR` for available projects.
- **Per-Project Setup:** Each project can have an `execute.txt` file listing the commands to run for setup.
- **Dynamic Command Execution:** If `execute.txt` is missing, you can create and edit it on the fly.
- **Recent Project Recall:** Automatically offers to launch the last opened project, or lets you pick another.
- **Fallback Behavior:** Optionally run fallback commands or simply open a shell if you choose not to launch a project.
- **Customizable:** Easily edit the projects directory and fallback logic in the script.
- **Seamless Integration:** Designed to run automatically on terminal startup via `.zshrc` or `.zprofile`.
- **Rich Terminal UI:** Uses the `rich` Python library for a pleasant CLI experience.

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/YanivWein24/Zsh-Project-Launcher.git
cd Zsh_Project_Launcher
```

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure Your Projects Directory

Edit the `PROJECTS_DIR` variable in `project_launcher.py` to point to your projects folder:

```python
PROJECTS_DIR = os.path.expanduser('~/Desktop/Personal/Projects/')
```

By default, `PROJECTS_DIR` is set to the parent folder of this repository. This means the launcher will look for your projects in the same directory that contains the `Zsh_Project_Launcher` folder.

### 4. Integrate with Zsh

Add the following to your `~/.zshrc` or `~/.zprofile` (see `.zshrc.txt` and `.zprofile.txt` in this repo for examples):

**For `~/.zshrc`:**

```sh
if [[ $- == *i* ]]; then
  python3 ~/path/to/Zsh_Project_Launcher/project_launcher.py
fi
```

**For `~/.zprofile`:**

```sh
if [[ $- == *i* ]]; then
  project_launcher
fi
```

> **Note:** The `.zprofile` example assumes you have defined a `project_launcher` function as shown in `.zprofile.txt` in this repo. This allows for more advanced fallback logic and custom behavior on exit.

For advanced fallback logic, see the `.zprofile.txt` example.

## Usage

- On opening a new terminal, the launcher will prompt you to:
  - Open the last used project
  - Select a different project from your projects directory
  - Skip project setup and run fallback commands (if configured)
- For each project, ensure there is an `execute.txt` file with the commands to run. If missing, the launcher will help you create one.

## Example `execute.txt`

```
source venv/bin/activate
npm run dev
open http://localhost:3000
```

## Requirements

- Python 3.x
- Zsh (for automatic launching on terminal startup)
- [rich](https://github.com/Textualize/rich) Python library (see `requirements.txt`)

## Security

- All commands are run locally under your user account. No authentication or external integrations are required.
- **Caution:** Only include trusted commands in your `execute.txt` files.

## Roadmap

- ~~Interactive & multi-color UI~~
- ~~Enhanced error handling and logging~~
- Conversational setup for `PROJECTS_DIR` and `LAST_PROJECT_FILE` on first run
- Cross-shell support (e.g., Bash)
- More customization options (e.g., per-project environment variables)

## License

MIT License

---

_Contributions and suggestions are welcome!_
