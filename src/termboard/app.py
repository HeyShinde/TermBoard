from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from termboard.core.config import load_config, update_global_theme, add_recent_project
from termboard.ui.dashboard import Dashboard
from termboard.ui.project_switcher import ProjectSwitcherScreen


class TermBoardApp(App):
    """A Textual app to manage Python projects."""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("ctrl+p", "switch_project", "Switch Project"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("s", "sponsor", "Sponsor / Donate"),
        ("q", "quit", "Quit"),
    ]
    TITLE = "TermBoard"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield Dashboard()
        yield Footer()

    def on_mount(self) -> None:
        import os

        config = load_config()
        self.theme = config.theme
        add_recent_project(os.getcwd())

    def watch_theme(self, old_theme: str | None, new_theme: str) -> None:
        if old_theme is not None:
            update_global_theme(new_theme)

    def action_switch_project(self) -> None:
        self.push_screen(ProjectSwitcherScreen(), self.on_project_selected)

    async def on_project_selected(self, project_path: str | None) -> None:
        if project_path:
            import os

            os.chdir(project_path)
            add_recent_project(os.getcwd())

            # Remove old dashboard and add new one
            old_dashboard = self.query_one(Dashboard)
            await old_dashboard.remove()
            await self.mount(Dashboard())
            self.notify(
                f"Switched to {os.path.basename(project_path)}", severity="information"
            )

    def action_sponsor(self) -> None:
        import webbrowser

        webbrowser.open("https://github.com/sponsors/HeyShinde")
        self.notify("Thank you for your support!", severity="information")
