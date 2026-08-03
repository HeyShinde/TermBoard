import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TermBoardConfig:
    env_command: str = ""
    theme: str = "textual-dark"
    ignore_global_tasks: bool = False
    tasks: dict[str, str] = field(default_factory=dict)


def get_global_config_path() -> Path:
    return Path.home() / ".termboard.toml"


def get_local_config_path() -> Path:
    return Path.cwd() / "termboard.toml"


def _load_from_path(path: Path) -> TermBoardConfig:
    config = TermBoardConfig()
    if path.exists():
        with path.open("rb") as f:
            data = tomllib.load(f)
        settings = data.get("settings", {})
        if "env_command" in settings:
            config.env_command = settings["env_command"]
        elif "command_prefix" in settings:
            config.env_command = settings["command_prefix"]

        if "theme" in settings:
            config.theme = settings["theme"]

        if "ignore_global_tasks" in settings:
            config.ignore_global_tasks = settings["ignore_global_tasks"]

        if "tasks" in data:
            config.tasks.update(data["tasks"])
    return config


def load_global_config() -> TermBoardConfig:
    return _load_from_path(get_global_config_path())


def load_local_config() -> TermBoardConfig:
    return _load_from_path(get_local_config_path())


def load_config() -> TermBoardConfig:
    """Loads the merged configuration for execution."""
    config = load_global_config()
    local_config = load_local_config()

    if local_config.env_command:
        config.env_command = local_config.env_command

    if local_config.ignore_global_tasks:
        config.tasks = {}

    config.ignore_global_tasks = local_config.ignore_global_tasks

    # Local tasks take precedence in merged view
    config.tasks.update(local_config.tasks)

    return config


def _save_to_path(config: TermBoardConfig, path: Path) -> None:
    toml_str = "[settings]\n"
    toml_str += f'env_command = "{config.env_command}"\n'
    toml_str += f'theme = "{config.theme}"\n'

    if config.ignore_global_tasks:
        toml_str += "ignore_global_tasks = true\n"

    toml_str += "\n"

    if config.tasks:
        toml_str += "[tasks]\n"
        for name, cmd in config.tasks.items():
            cmd = cmd.replace('"', '\\"')
            toml_str += f'"{name}" = "{cmd}"\n'

    path.write_text(toml_str)


def save_global_config(config: TermBoardConfig) -> None:
    _save_to_path(config, get_global_config_path())


def save_local_config(config: TermBoardConfig) -> None:
    _save_to_path(config, get_local_config_path())


def update_global_theme(theme: str) -> None:
    config = load_global_config()
    config.theme = theme
    save_global_config(config)
