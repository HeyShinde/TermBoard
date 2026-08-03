import asyncio
import json
from typing import List, Dict, Any


class DockerError(Exception):
    pass


async def _run_docker(args: List[str]) -> str:
    try:
        process = await asyncio.create_subprocess_exec(
            "docker",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise DockerError(
                stderr.decode().strip() or f"Docker exited with {process.returncode}"
            )
        return stdout.decode().strip()
    except FileNotFoundError:
        raise DockerError("Docker is not installed or not in PATH.")


async def get_containers() -> List[Dict[str, Any]]:
    try:
        # Note: older docker versions output json per line instead of an array.
        output = await _run_docker(["ps", "-a", "--format", "{{json .}}"])
    except DockerError:
        return []

    containers = []
    for line in output.split("\n"):
        line = line.strip()
        if line:
            try:
                containers.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return containers


async def start_container(container_id: str) -> None:
    await _run_docker(["start", container_id])


async def stop_container(container_id: str) -> None:
    await _run_docker(["stop", container_id])


async def remove_container(container_id: str) -> None:
    await _run_docker(["rm", "-f", container_id])
