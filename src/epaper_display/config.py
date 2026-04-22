import json
import os
import urllib.request
from pathlib import Path

OPTIONS_FILE = Path("/data/options.json")


def load_options() -> dict:
    with OPTIONS_FILE.open() as f:
        return json.load(f)


def get_supervisor_timezone() -> str | None:
    import logging
    log = logging.getLogger(__name__)
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        log.debug("SUPERVISOR_TOKEN not set")
        return None
    try:
        req = urllib.request.Request(
            "http://supervisor/core/api/config",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.load(resp).get("time_zone")
    except Exception as e:
        log.warning("Failed to fetch timezone from supervisor: %s", e)
        return None
