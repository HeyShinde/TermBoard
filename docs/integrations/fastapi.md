# FastAPI

FastAPI projects usually revolve around one long-running Uvicorn process plus a handful of short tasks. That maps cleanly onto TermBoard's Task Runner.

---

## `termboard.toml`

```toml
[settings]
theme = "textual-dark"

[tasks]
"Dev Server" = "uvicorn main:app --reload"
"Dev Server (LAN)" = "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
"Tests" = "pytest -q"
"Lint" = "ruff check ."
"Format" = "ruff format ."
```

---

### Pointing at the right app

`main:app` is `module:variable`. If your `FastAPI()` instance lives in `app/main.py` and is called `api`, the target becomes `app.main:api`:

```toml
[tasks]
"Dev Server" = "uvicorn app.main:api --reload"
```

### Using the FastAPI CLI

Recent versions of FastAPI ship their own CLI, which finds the app object for you:

```toml
[tasks]
"Dev Server" = "fastapi dev main.py"
"Prod Server" = "fastapi run main.py"
```

### Database migrations

If you're using Alembic, one-shot migration commands work well as buttons:

```toml
[tasks]
"DB Upgrade" = "alembic upgrade head"
"DB Downgrade" = "alembic downgrade -1"
```

---

## Things worth knowing

- **`--reload` prints to the log pane.** Every restart shows up in the Task Runner log, so you get a live feed of your reloads without leaving the dashboard.
- **Stopping the server.** In the default streamed mode, clicking any other task cancels the stream. If you want to stop the server with a real `Ctrl+C`, turn on `interactive_tasks` from the Settings tab.
- **The docs URL.** Uvicorn prints the bind address on startup; your interactive API docs are at that addr
- ess plus `/docs`.
