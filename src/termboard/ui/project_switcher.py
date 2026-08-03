import os
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, ListView, ListItem

from termboard.core.config import load_global_config


class ProjectSwitcherScreen(ModalScreen[str]):
    """Screen to select a recent project."""

    def compose(self) -> ComposeResult:
        with Vertical(id="project_switcher_dialog", classes="modal-dialog"):
            yield Label("Select a Recent Project", classes="modal-title")

            config = load_global_config()
            list_view = ListView(id="project-list")
            for project in config.recent_projects:
                name = os.path.basename(project)
                list_view.append(
                    ListItem(
                        Label(f"📁 {name}\n   [dim]{project}[/dim]"),
                        id=f"proj_{project}",
                    )
                )

            yield list_view

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id and event.item.id.startswith("proj_"):
            project_path = event.item.id.replace("proj_", "", 1)
            self.dismiss(project_path)
