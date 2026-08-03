import asyncio
import json


class GitHubError(Exception):
    pass


async def _run_gh_json(args: list[str]) -> list:
    """Run a gh command that outputs JSON and parse it."""
    try:
        process = await asyncio.create_subprocess_exec(
            "gh", *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode().strip()
            raise GitHubError(f"GitHub CLI error: {err_msg}")

        output = stdout.decode().strip()
        if not output:
            return []
        return json.loads(output)
    except FileNotFoundError:
        raise GitHubError(
            "GitHub CLI ('gh') is not installed. Please install it to use this feature."
        )


async def get_pull_requests() -> list:
    """Fetch open pull requests."""
    return await _run_gh_json(
        [
            "pr",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,author,url,state,statusCheckRollup",
            "--limit",
            "20",
        ]
    )


async def get_issues() -> list:
    """Fetch open issues."""
    return await _run_gh_json(
        [
            "issue",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,author,url,state",
            "--limit",
            "20",
        ]
    )


async def get_actions() -> list:
    """Fetch recent GitHub Actions runs."""
    return await _run_gh_json(
        [
            "run",
            "list",
            "--json",
            "databaseId,name,status,conclusion,url",
            "--limit",
            "20",
        ]
    )


async def checkout_pr(pr_number: str) -> None:
    """Check out a PR by number."""
    process = await asyncio.create_subprocess_exec(
        "gh",
        "pr",
        "checkout",
        str(pr_number),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise GitHubError(stderr.decode().strip())
