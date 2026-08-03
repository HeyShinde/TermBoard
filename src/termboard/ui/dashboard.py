from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalScroll
from textual.widgets import (
    Button,
    Markdown,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from termboard.core.config import load_config
from termboard.core.project import get_project_metadata
from termboard.core.runner import run_command
from termboard.ui.github_tab import GitHubTab
from termboard.ui.git_tab import GitTab
from termboard.ui.dependencies_tab import DependenciesTab
from termboard.ui.docker_tab import DockerTab
from termboard.ui.settings import ConfigUpdated, SettingsWidget


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
        config = load_config()
        if config.interactive_tasks:
            import subprocess

            with self.app.suspend():
                subprocess.run(cmd, shell=True)
        else:
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
                yield DependenciesTab()
            with TabPane("Git Status", id="git-tab"):
                yield GitTab()
            with TabPane("Services", id="docker-tab"):
                yield DockerTab()
            with TabPane("Tasks", id="tasks-tab"):
                yield TasksWidget()
            with TabPane("GitHub", id="github-tab"):
                yield GitHubTab()
            with TabPane("Settings", id="settings-tab"):
                yield SettingsWidget()

    @on(ConfigUpdated)
    async def on_config_updated(self, event: ConfigUpdated) -> None:
        tasks_widget = self.query_one(TasksWidget)
        await tasks_widget.reload_buttons()
