import json
import os
from pathlib import Path

OPTIONS_FILE = Path("/data/options.json")


def load_options() -> dict:
    with OPTIONS_FILE.open() as f:
        return json.load(f)


def get_timezone() -> str | None:
    """Return the TZ env var injected by the HA supervisor via with-contenv."""
    return os.environ.get("TZ")