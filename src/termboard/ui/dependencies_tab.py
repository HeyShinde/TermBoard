from textual import work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, DataTable, Input, Label

from ..core.project import get_project_metadata
from ..core.pypi import get_package_info, PyPIError
from ..core.runner import run_command


class DependenciesTab(Container):
    """The visual package manager tab."""

    def compose(self) -> ComposeResult:
        with Horizontal(id="deps-header", classes="header-bar"):
            yield Label("📦 Visual Package Manager", classes="title")
            yield Button("Refresh", id="refresh-deps", variant="primary")

        with Horizontal(id="pypi-search-bar"):
            yield Input(
                placeholder="Search PyPI for exact package name (e.g. 'requests')...",
                id="pypi-search",
            )
            yield Button("Search", id="search-btn", variant="primary")

        yield Label("Search Results", classes="section-label")
        yield DataTable(id="search-results-table", cursor_type="row")
        yield Horizontal(
            Button(
                "Install Selected", id="install-btn", variant="success", disabled=True
            ),
            id="install-bar",
        )

        yield Label("Installed Dependencies", classes="section-label")
        yield DataTable(id="deps-table", cursor_type="row")
        yield Horizontal(
            Button(
                "Uninstall Selected", id="uninstall-btn", variant="error", disabled=True
            ),
            id="uninstall-bar",
        )

    def on_mount(self) -> None:
        deps_table = self.query_one("#deps-table", DataTable)
        deps_table.add_columns("Package Name")

        search_table = self.query_one("#search-results-table", DataTable)
        search_table.add_columns("Package", "Version", "Summary")

        self.load_dependencies()

    @work(exclusive=True, thread=False)
    async def load_dependencies(self) -> None:
        table = self.query_one("#deps-table", DataTable)
        table.clear()
        meta = get_project_metadata()
        for dep in meta.dependencies:
            table.add_row(dep)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh-deps":
            self.load_dependencies()
        elif event.button.id == "search-btn":
            query = self.query_one("#pypi-search", Input).value.strip()
            if query:
                self.search_pypi(query)
        elif event.button.id == "install-btn":
            table = self.query_one("#search-results-table", DataTable)
            if table.cursor_row is not None and table.row_count > 0:
                pkg_name = table.get_row_at(table.cursor_row)[0]
                self.action_install(pkg_name)
        elif event.button.id == "uninstall-btn":
            table = self.query_one("#deps-table", DataTable)
            if table.cursor_row is not None and table.row_count > 0:
                pkg_name = table.get_row_at(table.cursor_row)[0]
                self.action_uninstall(pkg_name)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "search-results-table":
            self.query_one("#install-btn", Button).disabled = False
        elif event.data_table.id == "deps-table":
            self.query_one("#uninstall-btn", Button).disabled = False

    @work(exclusive=True, thread=False)
    async def search_pypi(self, query: str) -> None:
        table = self.query_one("#search-results-table", DataTable)
        table.clear()
        self.notify(f"Searching PyPI for '{query}'...")
        try:
            info = await get_package_info(query)
            if info:
                version = info.get("info", {}).get("version", "Unknown")
                summary = info.get("info", {}).get("summary", "")
                table.add_row(query, version, summary)
            else:
                table.add_row(query, "N/A", "Package not found.")
        except PyPIError as e:
            self.notify(f"PyPI Error: {e}", severity="error")

    @work(exclusive=True, thread=False)
    async def action_install(self, package: str) -> None:
        self.notify(f"Installing {package}...")
        meta = get_project_metadata()
        prefix = meta.env_command
        # If uv is in prefix, use uv add. Otherwise pip install.
        cmd = (
            f"uv add {package}" if "uv " in prefix else f"{prefix}pip install {package}"
        )

        async for _ in run_command(cmd):
            pass  # We just consume it for now.

        self.notify(f"Installed {package}!", severity="information")
        self.load_dependencies()

    @work(exclusive=True, thread=False)
    async def action_uninstall(self, package: str) -> None:
        self.notify(f"Uninstalling {package}...")
        meta = get_project_metadata()
        prefix = meta.env_command
        # If uv is in prefix, use uv remove. Otherwise pip uninstall -y.
        # Just grab the base package name in case it has versions (e.g. foo>=1.0)
        base_pkg = package.split(">")[0].split("<")[0].split("=")[0].strip()
        cmd = (
            f"uv remove {base_pkg}"
            if "uv " in prefix
            else f"{prefix}pip uninstall -y {base_pkg}"
        )

        async for _ in run_command(cmd):
            pass

        self.notify(f"Uninstalled {base_pkg}!", severity="information")
        self.load_dependencies()
