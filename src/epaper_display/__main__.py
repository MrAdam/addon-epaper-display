import datetime
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from croniter import croniter

from .capture import take_screenshot
from .config import load_options
from .image import process_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

PORT = 3412

_lock = threading.Lock()
_screenshot: bytes | None = None


def _capture(options: dict) -> bytes:
    raw = take_screenshot(
        options["url"],
        options.get("token", ""),
        options.get("width", 800),
        options.get("height", 480),
        options.get("zoom", 1.0),
        options.get("chromium_flags", ""),
    )
    return process_image(raw, options)


def refresh_loop() -> None:
    global _screenshot
    while True:
        options = load_options()
        if options.get("direct", False):
            time.sleep(60)
            continue

        try:
            log.info("Capturing %s", options["url"])
            data = _capture(options)
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
                data = _capture(options)
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
