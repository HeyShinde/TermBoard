#  Flask

Flask's CLI leans on environment variables that are easy to forget. Baking `--app` straight into your task definitions removes that whole class of "why isn't it finding my app?" moments.

---

## `termboard.toml`

```toml
[settings]
theme = "textual-dark"

[tasks]
"Dev Server" = "flask --app app run --debug"
"Dev Server (LAN)" = "flask --app app run --debug --host 0.0.0.0 --port 5000"
"Flask Shell" = "flask --app app shell"
"Routes" = "flask --app app routes"
"Tests" = "pytest -q"
```

---

### Pointing at the right app

`--app app` means "look in `app.py`". Adjust it to match your layout:

| Your layout | Flag |
| --- | --- |
| `app.py` at the root | `--app app` |
| `wsgi.py` at the root | `--app wsgi` |
| Package with `__init__.py` | `--app myproject` |
| Application factory | `--app myproject:create_app` |

Passing `--app` explicitly means the tasks keep working even when `FLASK_APP` isn't exported and `.flaskenv` isn't picked up.

### Flask-Migrate

```toml
[tasks]
"DB Migrate" = "flask --app app db migrate"
"DB Upgrade" = "flask --app app db upgrade"
```

---

## Things worth knowing

- **`Flask Shell` needs interactive mode.** It's a REPL, so it can't work in the streamed log pane. Turn on `interactive_tasks` from the Settings tab before using it, or add `interactive_tasks = true` under `[settings]`.
- **`--debug` gives you the reloader.** Reload messages and tracebacks stream straight into the Task Runner log.
- **Repetition is fine.** Yes, `--app app` appears in every task. That's the point — each button is self-contained and doesn't depend on shell state that a teammate m
ight not have.
