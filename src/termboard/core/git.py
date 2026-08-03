import asyncio
from typing import List, Tuple


class GitError(Exception):
    pass


async def _run_git(args: List[str]) -> str:
    process = await asyncio.create_subprocess_exec(
        "git", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise GitError(stderr.decode().strip())
    return stdout.decode().strip()


async def get_status() -> Tuple[List[str], List[str]]:
    """Returns a tuple of (staged_files, unstaged_files)."""
    try:
        output = await _run_git(["status", "--porcelain"])
    except GitError:
        return [], []

    staged = []
    unstaged = []

    if not output:
        return staged, unstaged

    for line in output.split("\n"):
        if len(line) < 3:
            continue
        x = line[0]  # Index status
        y = line[1]  # Working tree status
        path = line[3:].strip()

        if x in ("M", "A", "D", "R", "C"):
            staged.append(f"{x} {path}")
        if y in ("M", "A", "D", "R", "C", "?"):
            # ?? means untracked
            status_char = "U" if y == "?" else y
            unstaged.append(f"{status_char} {path}")

    return staged, unstaged


async def stage_file(filepath: str) -> None:
    # Remove status prefix if present
    clean_path = filepath.split(" ", 1)[-1] if " " in filepath else filepath
    await _run_git(["add", clean_path])


async def unstage_file(filepath: str) -> None:
    clean_path = filepath.split(" ", 1)[-1] if " " in filepath else filepath
    await _run_git(["restore", "--staged", clean_path])


async def stage_all() -> None:
    await _run_git(["add", "."])


async def unstage_all() -> None:
    await _run_git(["restore", "--staged", "."])


async def commit(message: str) -> None:
    if not message.strip():
        raise GitError("Commit message cannot be empty")
    await _run_git(["commit", "-m", message])
