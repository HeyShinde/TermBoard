# Configuration

TermBoard uses TOML configuration files. It supports both **Global** configurations (stored in your home directory) and **Project-specific** configurations (stored in your project root). 

Project-specific tasks take precedence over global ones.

## The Settings UI

The easiest way to configure TermBoard is to run it and press the `Settings` tab. You can add tasks, specify environment commands, and toggle options directly through the UI. When you press "Save", it will automatically write to the correct file.

## Manual Configuration

If you prefer to edit files manually, you can create a `termboard.toml` in your project root.

### `termboard.toml`

```toml
[settings]
env_command = "uv run"
theme = "textual-dark"
ignore_global_tasks = true

[tasks]
"Test (pytest)" = "pytest"
"Lint (ruff)" = "ruff check"
"Format (ruff)" = "ruff format"
"Build docs" = "mkdocs build"
```

### Options Explained

- **`env_command`**: The prefix command used to run tasks in the virtual environment. Defaults to empty, but usually `uv run`, `poetry run`, or `pipenv run`. TermBoard tries to auto-detect this, but you can explicitly override it here.
- **`theme`**: The Textual UI theme to use.
- **`ignore_global_tasks`**: A boolean that, when true, will ignore any tasks defined in your global `~/.termboard.toml` and only display the project-specific tasks.
- **`tasks`**: A dictionary where the key is the label that will appear on the button, and the value is the terminal command to execute.
