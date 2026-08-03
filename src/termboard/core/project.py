import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectMetadata:
    name: str
    version: str
    description: str
    has_venv: bool
    python_version: str
    dependencies: list[str]
    env_command: str


def get_project_metadata(path: Path | None = None) -> ProjectMetadata:
    """Parses pyproject.toml and checks for .venv in the given path."""
    project_path = path or Path.cwd()
    pyproject_file = project_path / "pyproject.toml"
    venv_dir = project_path / ".venv"

    env_command = ""
    if (project_path / "uv.lock").exists():
        env_command = "uv run "
    elif (project_path / "poetry.lock").exists():
        env_command = "poetry run "
    elif (project_path / "Pipfile.lock").exists():
        env_command = "pipenv run "
    elif venv_dir.exists():
        env_command = f"{venv_dir / 'bin'}/"

    if not pyproject_file.exists():
        return ProjectMetadata(
            name="Unknown",
            version="0.0.0",
            description="No pyproject.toml found",
            has_venv=venv_dir.exists(),
            python_version="Unknown",
            dependencies=[],
            env_command=env_command,
        )

    with pyproject_file.open("rb") as f:
        data = tomllib.load(f)

    project_data = data.get("project", {})
    return ProjectMetadata(
        name=project_data.get("name", "Unknown"),
        version=project_data.get("version", "0.0.0"),
        description=project_data.get("description", ""),
        has_venv=venv_dir.exists(),
        python_version=project_data.get("requires-python", "Unknown"),
        dependencies=project_data.get("dependencies", []),
        env_command=env_command,
    )
