#  Streamlit

Streamlit is built to be launched, watched, and killed repeatedly — which makes it a natural fit for a dashboard button.

---

## `termboard.toml`

```toml
[settings]
theme = "textual-dark"

[tasks]
"Run App" = "streamlit run app.py --server.headless true"
"Run App (LAN)" = "streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501"
"Clear Cache" = "streamlit cache clear"
"Version Check" = "streamlit --version"
"Tests" = "pytest -q"
```

---

## Why `--server.headless true`

This flag matters more than it looks:

- It stops Streamlit from trying to auto-open a browser tab, which it can't do sensibly from inside a TUI.
- It skips the first-run email prompt, which would otherwise hang forever waiting for input that the streamed log pane can't deliver.

Leave it in unless you have a reason not to.

## Finding the URL

Streamlit prints its local and network URLs on startup, and they land in the Task Runner log pane. Copy the one you need from there.

If you'd rather pin it, set the port explicitly:

```toml
[tasks]
"Run App" = "streamlit run app.py --server.headless true --server.port 8501"
```

## Multi-page apps

For a multi-page app you still point at the entrypoint, not the `pages/` directory:

```toml
[tasks]
"Run App" = "streamlit run Home.py --server.headless true"
```

---

## Things worth knowing

- **Restarting is a re-click.** Streamlit reloads on file save, but if you need a full restart, launch another task and then click **Run App** again.
- **Interactive mode for a clean shutdown.** If you want `Ctrl+C` to reach the server directly, enable `interactive_tasks` fro
m the Settings tab.
