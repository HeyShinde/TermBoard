from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Input,
    Label,
    Markdown,
    Static,
    Switch,
    TabbedContent,
    TabPane,
)

from termboard.core.config import (
    load_global_config,
    load_local_config,
    save_global_config,
    save_local_config,
)


class ConfigUpdated(Message):
    """Fired when the user saves new configurations."""


class ConfirmDeleteScreen(ModalScreen[bool]):
    """Screen with a dialog to confirm deletion."""

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm_dialog"):
            yield Label(
                "Are you sure you want to delete this task?", id="confirm_label"
            )
            with Horizontal(id="confirm_buttons"):
                yield Button("Cancel", variant="primary", id="btn_cancel")
                yield Button("Delete", variant="error", id="btn_confirm_delete")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_confirm_delete":
            self.dismiss(True)
        else:
            self.dismiss(False)


class SettingsWidget(Static):
    def compose(self) -> ComposeResult:
        with TabbedContent(initial="project-settings"):
            with TabPane("Project Settings", id="project-settings"):
                with VerticalScroll():
                    yield Markdown("## Project Settings (`./termboard.toml`)")
                    yield Label("Project Environment Command (overrides global):")
                    yield Input(id="input_project_env")

                    with Horizontal(classes="switch_container"):
                        yield Label(
                            "Ignore Global Tasks (Only show tasks defined in this project)",
                            classes="switch_label",
                        )
                        yield Switch(id="ignore_global_tasks_switch")

                    with Horizontal(classes="switch_container"):
                        yield Label(
                            "Run Tasks Interactively (Suspends UI)",
                            classes="switch_label",
                        )
                        yield Switch(id="project_interactive_switch")

                    yield Label("Project Tasks:", classes="tasks_label")
                    yield Vertical(
                        id="project_tasks_container", classes="tasks_container"
                    )

                    with Horizontal(classes="settings_buttons"):
                        yield Button(
                            "Add Project Task", id="btn_add_project", variant="primary"
                        )
                        yield Button(
                            "Save Project Configurations",
                            id="btn_save_project",
                            variant="success",
                        )

            with TabPane("Global Settings", id="global-settings"):
                with VerticalScroll():
                    yield Markdown("## Global Settings (`~/.termboard.toml`)")
                    yield Label("Environment Command (e.g., `uv run `):")
                    yield Input(id="input_global_env")

                    with Horizontal(classes="switch_container"):
                        yield Label(
                            "Run Tasks Interactively (Suspends UI)",
                            classes="switch_label",
                        )
                        yield Switch(id="global_interactive_switch")

                    yield Label("Global Tasks:", classes="tasks_label")
                    yield Vertical(
                        id="global_tasks_container", classes="tasks_container"
                    )

                    with Horizontal(classes="settings_buttons"):
                        yield Button(
                            "Add Global Task", id="btn_add_global", variant="primary"
                        )
                        yield Button(
                            "Save Global Configurations",
                            id="btn_save_global",
                            variant="success",
                        )

    def on_mount(self) -> None:
        self.load_settings_into_ui()

    def create_task_row(self, name: str = "", cmd: str = "") -> Horizontal:
        return Horizontal(
            Input(value=name, placeholder="Task Name", classes="task_name"),
            Input(value=cmd, placeholder="Command", classes="task_cmd"),
            Button("X", variant="error", classes="btn_delete_task"),
            classes="task_row",
        )

    def load_settings_into_ui(self) -> None:
        global_config = load_global_config()
        local_config = load_local_config()

        self.query_one("#input_global_env", Input).value = global_config.env_command
        self.query_one(
            "#global_interactive_switch", Switch
        ).value = global_config.interactive_tasks

        global_container = self.query_one("#global_tasks_container")
        for name, cmd in global_config.tasks.items():
            global_container.mount(self.create_task_row(name, cmd))

        self.query_one("#input_project_env", Input).value = local_config.env_command
        self.query_one(
            "#ignore_global_tasks_switch", Switch
        ).value = local_config.ignore_global_tasks
        self.query_one(
            "#project_interactive_switch", Switch
        ).value = local_config.interactive_tasks

        project_container = self.query_one("#project_tasks_container")
        for name, cmd in local_config.tasks.items():
            project_container.mount(self.create_task_row(name, cmd))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_add_global":
            self.query_one("#global_tasks_container").mount(self.create_task_row())

        elif event.button.id == "btn_add_project":
            self.query_one("#project_tasks_container").mount(self.create_task_row())

        elif event.button.id == "btn_save_global":
            self.save_global_settings()

        elif event.button.id == "btn_save_project":
            self.save_project_settings()

        elif event.button.has_class("btn_delete_task"):
            row = event.button.parent

            def check_delete(confirm: bool) -> None:
                if confirm and row:
                    row.remove()

            self.app.push_screen(ConfirmDeleteScreen(), check_delete)

    def save_global_settings(self) -> None:
        global_env = self.query_one("#input_global_env", Input).value
        global_tasks = {}
        for row in self.query_one("#global_tasks_container").query(".task_row"):
            name = row.query(".task_name").first(Input).value
            cmd = row.query(".task_cmd").first(Input).value
            if name.strip() and cmd.strip():
                global_tasks[name.strip()] = cmd.strip()

        global_config = load_global_config()
        global_config.env_command = global_env
        global_config.tasks = global_tasks
        global_config.interactive_tasks = self.query_one(
            "#global_interactive_switch", Switch
        ).value
        save_global_config(global_config)

        self.app.notify("Global settings saved! UI updated.")
        self.post_message(ConfigUpdated())

    def save_project_settings(self) -> None:
        project_env = self.query_one("#input_project_env", Input).value
        ignore_global_tasks = self.query_one(
            "#ignore_global_tasks_switch", Switch
        ).value

        project_tasks = {}
        for row in self.query_one("#project_tasks_container").query(".task_row"):
            name = row.query(".task_name").first(Input).value
            cmd = row.query(".task_cmd").first(Input).value
            if name.strip() and cmd.strip():
                project_tasks[name.strip()] = cmd.strip()

        local_config = load_local_config()
        local_config.env_command = project_env
        local_config.ignore_global_tasks = ignore_global_tasks
        local_config.tasks = project_tasks
        local_config.interactive_tasks = self.query_one(
            "#project_interactive_switch", Switch
        ).value
        save_local_config(local_config)

        self.app.notify("Project settings saved! UI updated.")
        self.post_message(ConfigUpdated())
