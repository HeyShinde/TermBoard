<div align="center">
  <img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/logo.png" alt="TermBoard Logo" width="600">
  <p><b>A beautiful, interactive terminal dashboard for Python projects, environments, and tasks.</b></p>
  <br>
  
  [![PyPI](https://img.shields.io/pypi/v/termboard.svg)](https://pypi.org/project/termboard/)
  [![Python](https://img.shields.io/pypi/pyversions/termboard.svg)](https://pypi.org/project/termboard/)
  [![License](https://img.shields.io/pypi/l/termboard.svg)](https://github.com/HeyShinde/TermBoard/blob/main/LICENSE)
</div>

---

## The Problem: "Why not just use a script?"

As developers, we often write `Makefile`s or bash scripts (like `test.sh` or `lint.sh`) to manage our project workflows. While scripts work, they have severe limitations:

1. **Context Switching:** You have to remember the exact command or script name, type it out, and watch it vomit hundreds of lines of output into your terminal, erasing your history.
2. **Environment Hell:** Did you remember to activate your virtual environment? Are you using `uv`, `poetry`, or `conda`? Running the wrong script in the wrong environment is a daily frustration.
3. **Discoverability:** New developers joining your project don't know what scripts exist or what they do.

## The Solution: TermBoard

**TermBoard** replaces your scripts with a persistent, interactive Terminal UI (TUI).

- 🧠 **Smart Environment Detection:** TermBoard automatically detects if you are using `uv`, `poetry`, `pipenv`, or a standard `.venv`, and executes your tasks in the correct environment—no manual activation required.
- ⚡ **Asynchronous Streaming:** Tasks run asynchronously in the background. Their output is streamed directly into a beautiful, scrollable Rich Log window without freezing the UI or polluting your terminal history.
- 🛠️ **Fully Customizable:** Define custom tasks in a `termboard.toml` file. Your team can clone the repo, run `termboard`, and instantly have a UI with clickable buttons for deploying, testing, and building.

---

## ✨ Features

### 📋 Project Info
Instantly see your project's version, python requirements, and virtual environment status.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-1.png" alt="Project Info" width="800">

### 📦 Visual Package Manager (PyPI)
Search PyPI for packages, read descriptions, and install directly using `uv add` natively in the terminal.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-2.png" alt="Visual Package Manager" width="800">

### 🌿 Git Integration
Shows current branch, uncommitted changes, and provides actions to stage, unstage, commit, and push.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-3.png" alt="Git Status" width="800">

### 🐳 Docker Services
View, start, stop, and delete running Docker containers without leaving the dashboard.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-4.png" alt="Docker Services" width="800">

### 🚀 Task Runner
Define and execute custom project tasks via `./termboard.toml` or `~/.termboard.toml`. Toggle interactive tasks to suspend the UI!
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-5.png" alt="Task Runner" width="800">

### 🐙 GitHub Integration
Browse active pull requests, monitor GitHub Actions workflow statuses, and track Issues natively.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-6.png" alt="GitHub Integration" width="800">

### ⚙️ In-App Settings & 📁 Global Workspaces
Override environment variables, add new custom tasks, and save configurations globally. Easily switch between your recent projects using the `Ctrl+P` Quick Switcher.
<br>
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-7.png" alt="Project Settings" width="800">
<img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-8.png" alt="Global Settings" width="800">

## Installation

TermBoard is designed to be installed globally on your machine so you can run it inside *any* Python project.

**1. Using `uv` (Recommended):**
```bash
uv tool install termboard
```

**2. Using `pipx`:**
```bash
pipx install termboard
```

**3. Using `pip`:**
```bash
pip install termboard
```

## Quick Start & Usage

Navigate to any Python project directory and use one of the following commands:

**If installed globally (via uv tool, pipx, or global pip):**
```bash
termboard
```

**If you want to run it dynamically without installing:**
```bash
uvx termboard
```

*(If you don't have any custom tasks defined, TermBoard will automatically provide defaults for testing and linting).*

## 💖 Support & Community

If you like TermBoard, please consider supporting the project!

- ⭐️ **Star on GitHub**: [HeyShinde/TermBoard](https://github.com/HeyShinde/TermBoard)
- 🐞 **Report Issues**: [GitHub Issues](https://github.com/HeyShinde/TermBoard/issues)
- 💬 **Follow / Contact**: [@heyshinde](https://github.com/HeyShinde)
- 💖 **Sponsor / Donate**: Press the `s` hotkey directly in the TUI, or visit my [GitHub Sponsors](https://github.com/sponsors/HeyShinde) or [Razorpay](https://razorpay.me/@heyshinde).
