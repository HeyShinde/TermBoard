from textual.app import ComposeResult
from textual.widgets import (
    TabbedContent,
    TabPane,
    Markdown,
    Button,
    RichLog,
    Static,
    DataTable,
)
from textual.containers import Vertical, Horizontal, HorizontalScroll
from textual import work, on

from termboard.core.project import get_project_metadata
from termboard.core.runner import run_command
from termboard.core.config import load_config
from termboard.ui.settings import SettingsWidget, ConfigUpdated


class ProjectInfoWidget(Static):
    def compose(self) -> ComposeResult:
        meta = get_project_metadata()
        md = f"""
# {meta.name}
- **Version:** {meta.version}
- **Description:** {meta.description}
- **Python:** {meta.python_version}
- **Virtual Environment:** {"✅ Active (.venv)" if meta.has_venv else "❌ Missing"}
"""
        yield Markdown(md)


class DependenciesWidget(Static):
    def compose(self) -> ComposeResult:
        yield DataTable(id="deps_table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Package Name")
        meta = get_project_metadata()
        for dep in meta.dependencies:
            table.add_row(dep)


class TasksWidget(Static):
    def compose(self) -> ComposeResult:
        config = load_config()
        with HorizontalScroll(id="buttons"):
            for name in config.tasks.keys():
                # Textual IDs can't have spaces or parens easily, so we slugify
                safe_id = "".join(c if c.isalnum() else "_" for c in name)
                yield Button(name, id=f"task_{safe_id}", variant="primary")
        yield RichLog(id="task_log", highlight=True, markup=True)

    async def reload_buttons(self) -> None:
        buttons = self.query_one("#buttons")
        await buttons.remove()

        config = load_config()
        buttons_layout = HorizontalScroll(id="buttons")
        await self.mount(buttons_layout, before="#task_log")

        for name in config.tasks.keys():
            safe_id = "".join(c if c.isalnum() else "_" for c in name)
            await buttons_layout.mount(
                Button(name, id=f"task_{safe_id}", variant="primary")
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not event.button.id or not event.button.id.startswith("task_"):
            return

        log = self.query_one(RichLog)
        meta = get_project_metadata()
        config = load_config()
        prefix = config.env_command or meta.env_command

        # Find the matching task by safe_id
        task_name = event.button.label.plain
        if task_name not in config.tasks:
            return

        cmd = config.tasks[task_name]
        log.write(f"[bold green]Running {task_name} (Prefix: {prefix})...[/]")
        self.run_task(f"{prefix}{cmd}")

    @work(exclusive=True)
    async def run_task(self, cmd: str) -> None:
        log = self.query_one(RichLog)
        async for line in run_command(cmd):
            log.write(line.strip())
        log.write("[bold]Done.[/]")


class Dashboard(Static):
    def compose(self) -> ComposeResult:
        with TabbedContent(initial="project-tab"):
            with TabPane("Project Info", id="project-tab"):
                yield ProjectInfoWidget()
            with TabPane("Dependencies", id="deps-tab"):
                yield DependenciesWidget()
            with TabPane("Tasks", id="tasks-tab"):
                yield TasksWidget()
            with TabPane("Settings", id="settings-tab"):
                yield SettingsWidget()

    @on(ConfigUpdated)
    async def on_config_updated(self, event: ConfigUpdated) -> None:
        tasks_widget = self.query_one(TasksWidget)
        await tasks_widget.reload_buttons()
