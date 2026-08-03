import asyncio
import json
import urllib.request
from urllib.error import HTTPError
from typing import Optional, Dict, Any


class PyPIError(Exception):
    pass


async def get_package_info(package_name: str) -> Optional[Dict[str, Any]]:
    """Fetches package information from PyPI JSON API."""
    url = f"https://pypi.org/pypi/{package_name}/json"

    def fetch():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "termboard/1.0.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
        except HTTPError as e:
            if e.code == 404:
                return None
            raise PyPIError(f"HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            raise PyPIError(str(e))

    return await asyncio.to_thread(fetch)
