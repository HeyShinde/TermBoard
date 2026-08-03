from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Input, Label
from textual import work

from ..core.git import (
    GitError,
    commit,
    get_status,
    stage_all,
    stage_file,
    unstage_all,
    unstage_file,
)


class GitTab(Container):
    """The Git integration tab."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="git-header", classes="header-bar"):
            yield Label("🌳 Git Status", classes="title")
            yield Button("Refresh", id="refresh-git", variant="primary")

        with Horizontal(id="git-tables"):
            with Vertical(classes="git-column"):
                with Horizontal(classes="git-column-header"):
                    yield Label("Unstaged Changes", classes="section-label")
                    yield Button("Stage All", id="stage-all", variant="success")
                yield DataTable(id="unstaged-table", cursor_type="row")

            with Vertical(classes="git-column"):
                with Horizontal(classes="git-column-header"):
                    yield Label("Staged Changes", classes="section-label")
                    yield Button("Unstage All", id="unstage-all", variant="error")
                yield DataTable(id="staged-table", cursor_type="row")

        with Horizontal(id="commit-bar"):
            yield Input(placeholder="Commit message...", id="commit-message")
            yield Button("Commit", id="commit-btn", variant="primary")

    def on_mount(self) -> None:
        unstaged = self.query_one("#unstaged-table", DataTable)
        unstaged.add_columns("File (Click to Stage)")

        staged = self.query_one("#staged-table", DataTable)
        staged.add_columns("File (Click to Unstage)")

        self.load_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh-git":
            self.load_data()
        elif event.button.id == "stage-all":
            self.action_stage_all()
        elif event.button.id == "unstage-all":
            self.action_unstage_all()
        elif event.button.id == "commit-btn":
            msg = self.query_one("#commit-message", Input).value
            self.action_commit(msg)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        file_path = event.data_table.get_row_at(event.cursor_row)[0]
        if "No files" in file_path:
            return

        if event.data_table.id == "unstaged-table":
            self.action_stage_file(file_path)
        elif event.data_table.id == "staged-table":
            self.action_unstage_file(file_path)

    @work(exclusive=True, thread=False)
    async def load_data(self) -> None:
        unstaged_table = self.query_one("#unstaged-table", DataTable)
        staged_table = self.query_one("#staged-table", DataTable)

        unstaged_table.clear()
        staged_table.clear()

        staged, unstaged = await get_status()

        for file in unstaged:
            unstaged_table.add_row(file)
        if not unstaged:
            unstaged_table.add_row("No unstaged files.")

        for file in staged:
            staged_table.add_row(file)
        if not staged:
            staged_table.add_row("No staged files.")

    @work(exclusive=True, thread=False)
    async def action_stage_all(self) -> None:
        await stage_all()
        self.load_data()

    @work(exclusive=True, thread=False)
    async def action_unstage_all(self) -> None:
        await unstage_all()
        self.load_data()

    @work(exclusive=True, thread=False)
    async def action_stage_file(self, filepath: str) -> None:
        await stage_file(filepath)
        self.load_data()

    @work(exclusive=True, thread=False)
    async def action_unstage_file(self, filepath: str) -> None:
        await unstage_file(filepath)
        self.load_data()

    @work(exclusive=True, thread=False)
    async def action_commit(self, message: str) -> None:
        try:
            await commit(message)
            self.query_one("#commit-message", Input).value = ""
            self.notify("Commit successful!", severity="information")
            self.load_data()
        except GitError as e:
            self.notify(f"Commit failed: {e}", severity="error")
