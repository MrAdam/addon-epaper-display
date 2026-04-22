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

import numpy as np
from croniter import croniter
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

OPTIONS_FILE = Path("/data/options.json")
PORT = 8099

# sRGB → linear gamma LUT (γ = 2.2 approximation), repeated 3× for RGB point()
_GAMMA_LUT = [int(((i / 255.0) ** 2.2) * 255 + 0.5) for i in range(256)] * 3

# 8×8 Bayer threshold matrix normalised to [0, 1)
_BAYER = np.array([
    [ 0, 32,  8, 40,  2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44,  4, 36, 14, 46,  6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [ 3, 35, 11, 43,  1, 33,  9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
], dtype=np.float32) / 64.0


def _bayer_dither(img: Image.Image) -> Image.Image:
    arr = np.array(img, dtype=np.float32) / 255.0
    h, w = arr.shape
    threshold = np.tile(_BAYER, (h // 8 + 1, w // 8 + 1))[:h, :w]
    return Image.fromarray(((arr > threshold) * 255).astype(np.uint8), mode="L")


def process_image(raw: bytes, options: dict) -> bytes:
    img = Image.open(BytesIO(raw))

    if options.get("gamma_correction", True):
        img = img.convert("RGB").point(_GAMMA_LUT)

    img = img.convert("L")

    if options.get("normalize", True):
        img = ImageOps.autocontrast(img)

    dithering = options.get("dithering", "floyd-steinberg")
    if dithering == "floyd-steinberg":
        img = img.convert("1", dither=Image.Dither.FLOYDSTEINBERG).convert("L")
    elif dithering == "ordered":
        img = _bayer_dither(img)
    else:
        img = img.convert("1", dither=Image.Dither.NONE).convert("L")

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


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

    return data


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
            raw = take_screenshot(
                options["url"],
                options.get("token", ""),
                options.get("width", 800),
                options.get("height", 480),
            )
            data = process_image(raw, options)
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
                raw = take_screenshot(
                    options["url"],
                    options.get("token", ""),
                    options.get("width", 800),
                    options.get("height", 480),
                )
                data = process_image(raw, options)
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
