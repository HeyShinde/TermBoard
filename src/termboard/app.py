from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from termboard.ui.dashboard import Dashboard
from termboard.core.config import load_config, update_global_theme


class TermBoardApp(App):
    """A Textual app to manage Python projects."""

    CSS_PATH = "app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]
    TITLE = "TermBoard"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield Dashboard()
        yield Footer()

    def on_mount(self) -> None:
        config = load_config()
        self.theme = config.theme

    def watch_theme(self, old_theme: str | None, new_theme: str) -> None:
        if old_theme is not None:
            update_global_theme(new_theme)
