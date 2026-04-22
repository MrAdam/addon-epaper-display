import json
import os
from pathlib import Path

OPTIONS_FILE = Path("/data/options.json")


def load_options() -> dict:
    with OPTIONS_FILE.open() as f:
        return json.load(f)


def get_timezone() -> str | None:
    """Return the timezone injected by the HA supervisor (TZ env var)."""
    return os.environ.get("TZ")