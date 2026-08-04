#  Django

Django's workflow is a long list of `manage.py` subcommands that everyone half-remembers. Turning them into labelled buttons is exactly the discoverability problem TermBoard exists to solve.

---

## `termboard.toml`

```toml
[settings]
theme = "textual-dark"
interactive_tasks = true

[tasks]
"Dev Server" = "python manage.py runserver"
"Dev Server (LAN)" = "python manage.py runserver 0.0.0.0:8000"
"Make Migrations" = "python manage.py makemigrations"
"Migrate" = "python manage.py migrate"
"Create Superuser" = "python manage.py createsuperuser"
"Django Shell" = "python manage.py shell"
"Tests" = "python manage.py test"
"Collect Static" = "python manage.py collectstatic --noinput"
```

---

## Why `interactive_tasks = true` here

Django is the one framework where interactive mode is the sensible default. Several of its most-used commands need real keyboard input:

- `createsuperuser` prompts for a username, email, and password.
- `shell` is a REPL.
- `runserver` wants a genuine `Ctrl+C` to shut down cleanly.

With `interactive_tasks` on, TermBoard suspends the UI and hands those commands the actual terminal. Without it, `createsuperuser` will sit there waiting for input that can never arrive.

The trade-off: the setting is global, so *every* task suspends the UI — including `migrate`, which you might rather watch stream in the log pane. If that bothers you, leave it out of `termboard.toml` and toggle it from the **Settings** tab when you need it.

---

## Multiple settings modules

If you split settings per environment, pass the module explicitly rather than relying on an exported variable:

```toml
[tasks]
"Dev Server" = "python manage.py runserver --settings=config.settings.local"
"Migrate (staging)" = "python manage.py migrate --settings=config.settings.staging"
```

## Non-standard project layout

If `manage.py` isn't at your project root, `cd` first — tasks run through a shell, so chaining works:

```toml
[tasks]
"Dev Server" = "cd backend && python manage.
py runserver"
```
