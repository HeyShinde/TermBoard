# Installation

TermBoard is designed to be installed globally on your machine so you can run it inside *any* Python project.

## 1. Using uv (Recommended)
```bash
uv tool install termboard
```

## 2. Using pipx (Alternative)
```bash
pipx install termboard
```

## 3. Using pip (Global or Virtual Environment)
```bash
pip install termboard
```

## Usage & Execution

Navigate to any Python project directory and use one of the following commands depending on how you installed it:

**If installed globally (via uv tool, pipx, or global pip):**
```bash
termboard
```

**If you want to run it dynamically without installing:**
```bash
uvx termboard
```

**If installed locally inside your project's virtual environment:**
```bash
uv run termboard
# or
poetry run termboard
```

*(If you don't have any custom tasks defined, TermBoard will automatically provide defaults for testing and linting).*
