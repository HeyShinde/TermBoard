<div align="center">
  <h1>🎯 TermBoard</h1>
  <p><b>A beautiful, interactive terminal dashboard for Python projects, environments, and tasks.</b></p>
  <br>
  <img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-3.png" alt="TermBoard Tasks UI" width="600">
  <br>
  <img src="https://raw.githubusercontent.com/HeyShinde/TermBoard/refs/heads/main/assets/screenshot-4.png" alt="TermBoard Settings UI" width="600">
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

## Features

- **Project Info:** Instantly see your project's version, python requirements, and virtual environment status.
- **Dependency Viewer:** A clean data table of all your project's dependencies parsed directly from `pyproject.toml`.
- **Dynamic Tasks Engine:** Clickable buttons for your workflows (e.g., `pytest`, `ruff`) that execute asynchronously.
- **In-App Settings:** Override environment variables, add new custom tasks, and save configurations globally without leaving the terminal.

## Installation

TermBoard is designed to be installed globally on your machine so you can run it inside *any* Python project.

**Using `uv` (Recommended):**

```bash
uv tool install termboard
```

**Using `pipx`:**

```bash
pipx install termboard
```

## Quick Start

Navigate to any Python project directory and simply type:

```bash
termboard
```

*(If you don't have any custom tasks defined, TermBoard will automatically provide defaults for testing and linting).*
