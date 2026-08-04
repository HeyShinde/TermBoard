#  Framework Integrations

TermBoard is framework-agnostic — anything you can type into a shell can become a button. These pages give you copy-pasteable `termboard.toml` snippets for the most common Python web frameworks.

Drop one into a `termboard.toml` at your project root, run `termboard`, and your dev server is one click away.

---

## How these examples work

Every example follows the same shape:

```toml
[settings]
# optional settings

[tasks]
"Button Label" = "shell command"
```

- The **key** is the text that appears on the button in the Task Runner.
- The **value** is the raw shell command.
- TermBoard auto-detects `uv`, `poetry`, `pipenv`, or a plain `.venv` and prefixes your command for you. That's why the examples say `uvicorn main:app --reload` and not `uv run uvicorn main:app --reload`. To override the detection, see [Configuration](../configuration.md).

---

## Two ways to run a dev server

A dev server is long-running, which makes it different from a one-shot `pytest`. TermBoard gives you two modes.

### Streamed (default)

Output is piped into the Task Runner's log pane. Good for watching reload messages and tracebacks while you keep poking around the Git and Docker tabs.

Tasks run on a single exclusive worker, so **launching another task cancels the one currently streaming**. Think of the log pane as "one server at a time".

### Interactive

```toml
[settings]
interactive_tasks = true
```

This suspends the TUI and drops you into the raw terminal, so `Ctrl+C` reaches the server directly and coloured output survives untouched. It's the right mode for anything that expects real keyboard input — `manage.py shell`, `createsuperuser`, `flask shell`, or a `breakpoint()`.

Note that this is a global switch, not a per-task one. You can flip it any time from the **Settings** tab.

---

## Pick your framework

- [FastAPI](fastapi.md)
- [Django](django.md)
- [Flask](flask.md)
- [Stre
- amlit](streamlit.md)
