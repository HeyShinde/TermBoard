import asyncio
from typing import AsyncGenerator


async def run_command(cmd: str) -> AsyncGenerator[str, None]:
    """Runs a shell command asynchronously and yields its output line by line."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )

    if process.stdout:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            yield line.decode("utf-8")

    await process.wait()
