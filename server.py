#!/usr/bin/env python3
import datetime
import json
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

from croniter import croniter

from PIL import Image
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

OPTIONS_FILE = Path("/data/options.json")
PORT = 8099


def load_options() -> dict:
    with OPTIONS_FILE.open() as f:
        return json.load(f)


def take_screenshot(url: str, token: str, width: int, height: int) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()

        if token:
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            page.goto(base_url, wait_until="load")
            token_payload = {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 1800,
                "refresh_token": "refresh",
                "expires_at": time.time() + 365 * 24 * 3600,
            }
            page.evaluate(
                "payload => localStorage.setItem('hassTokens', JSON.stringify(payload))",
                token_payload,
            )

        page.goto(url, wait_until="load")
        page.wait_for_timeout(3000)
        data = page.screenshot()
        browser.close()

    img = Image.open(BytesIO(data)).convert("L")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


_lock = threading.Lock()
_screenshot: bytes | None = None


def refresh_loop() -> None:
    global _screenshot
    while True:
        options = load_options()
        if options.get("direct", False):
            time.sleep(60)
            continue

        try:
            log.info("Capturing %s", options["url"])
            data = take_screenshot(
                options["url"],
                options.get("token", ""),
                options.get("width", 800),
                options.get("height", 480),
            )
            with _lock:
                _screenshot = data
            log.info("Screenshot updated (%d bytes)", len(data))
        except Exception:
            log.exception("Screenshot failed")

        cron_expr = options.get("cron", "*/5 * * * *")
        next_run = croniter(cron_expr, datetime.datetime.now()).get_next(datetime.datetime)
        sleep_secs = (next_run - datetime.datetime.now()).total_seconds()
        log.info("Next capture at %s", next_run.strftime("%H:%M:%S"))
        time.sleep(max(0, sleep_secs))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/screenshot.png":
            self.send_response(404)
            self.end_headers()
            return

        options = load_options()
        if options.get("direct", False):
            try:
                data = take_screenshot(
                    options["url"],
                    options.get("token", ""),
                    options.get("width", 800),
                    options.get("height", 480),
                )
            except Exception:
                log.exception("Direct screenshot failed")
                self.send_response(500)
                self.end_headers()
                return
        else:
            with _lock:
                data = _screenshot
            if data is None:
                self.send_response(503)
                self.end_headers()
                return

        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args) -> None:
        log.info("HTTP " + fmt, *args)


if __name__ == "__main__":
    threading.Thread(target=refresh_loop, daemon=True).start()
    log.info("Listening on port %d", PORT)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
