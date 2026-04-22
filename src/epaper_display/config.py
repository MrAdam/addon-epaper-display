import json
import logging
import os
import urllib.request
from pathlib import Path

log = logging.getLogger(__name__)

OPTIONS_FILE = Path("/data/options.json")


def load_options() -> dict:
    with OPTIONS_FILE.open() as f:
        return json.load(f)


def get_timezone() -> str | None:
    """Return the container timezone.

    Tries in order:
    1. TZ env var — set by the supervisor in most installations.
    2. GET http://supervisor/supervisor/info — correct supervisor-tier endpoint
       that accepts SUPERVISOR_TOKEN, returns {data: {timezone: ...}}.
    """
    if tz := os.environ.get("TZ"):
        return tz

    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        log.debug("SUPERVISOR_TOKEN not set, cannot fetch timezone from supervisor")
        return None
    try:
        req = urllib.request.Request(
            "http://supervisor/supervisor/info",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.load(resp).get("data", {}).get("timezone")
    except Exception as e:
        log.warning("Failed to fetch timezone from supervisor: %s", e)
        return None