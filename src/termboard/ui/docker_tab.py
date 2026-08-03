from textual import work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, DataTable, Label

from ..core.docker import (
    DockerError,
    get_containers,
    remove_container,
    start_container,
    stop_container,
)


class DockerTab(Container):
    """The Docker services integration tab."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="docker-header", classes="header-bar"):
            yield Label("🐳 Docker Services", classes="title")
            yield Button("Refresh", id="refresh-docker", variant="primary")

        yield Label("Containers (Select a row to manage)", classes="section-label")
        yield DataTable(id="docker-table", cursor_type="row")

        with Horizontal(id="docker-actions-bar"):
            yield Button("Start", id="start-btn", variant="success", disabled=True)
            yield Button("Stop", id="stop-btn", variant="warning", disabled=True)
            yield Button("Delete", id="delete-btn", variant="error", disabled=True)

    def on_mount(self) -> None:
        table = self.query_one("#docker-table", DataTable)
        table.add_columns("ID", "Names", "Image", "State", "Status")
        self.load_data()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh-docker":
            self.load_data()
            return

        table = self.query_one("#docker-table", DataTable)
        if table.cursor_row is not None and table.row_count > 0:
            container_id = table.get_row_at(table.cursor_row)[0]
            if container_id == "N/A" or container_id == "Error":
                return

            if event.button.id == "start-btn":
                self.action_start(container_id)
            elif event.button.id == "stop-btn":
                self.action_stop(container_id)
            elif event.button.id == "delete-btn":
                self.action_delete(container_id)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.query_one("#start-btn", Button).disabled = False
        self.query_one("#stop-btn", Button).disabled = False
        self.query_one("#delete-btn", Button).disabled = False

    @work(exclusive=True, thread=False)
    async def load_data(self) -> None:
        table = self.query_one("#docker-table", DataTable)
        table.clear()

        self.query_one("#start-btn", Button).disabled = True
        self.query_one("#stop-btn", Button).disabled = True
        self.query_one("#delete-btn", Button).disabled = True

        try:
            containers = await get_containers()
            for c in containers:
                table.add_row(
                    c.get("ID", "Unknown"),
                    c.get("Names", "Unknown"),
                    c.get("Image", "Unknown"),
                    c.get("State", "Unknown"),
                    c.get("Status", "Unknown"),
                )
            if not containers:
                table.add_row("N/A", "No containers found.", "", "", "")
        except DockerError as e:
            table.add_row("Error", str(e), "", "", "")

    @work(exclusive=True, thread=False)
    async def action_start(self, container_id: str) -> None:
        try:
            await start_container(container_id)
            self.notify(f"Started {container_id}")
            self.load_data()
        except DockerError as e:
            self.notify(f"Failed to start: {e}", severity="error")

    @work(exclusive=True, thread=False)
    async def action_stop(self, container_id: str) -> None:
        try:
            await stop_container(container_id)
            self.notify(f"Stopped {container_id}")
            self.load_data()
        except DockerError as e:
            self.notify(f"Failed to stop: {e}", severity="error")

    @work(exclusive=True, thread=False)
    async def action_delete(self, container_id: str) -> None:
        try:
            await remove_container(container_id)
            self.notify(f"Deleted {container_id}")
            self.load_data()
        except DockerError as e:
            self.notify(f"Failed to delete: {e}", severity="error")
