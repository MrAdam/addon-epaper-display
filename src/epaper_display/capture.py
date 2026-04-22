import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def take_screenshot(
    url: str,
    token: str,
    width: int,
    height: int,
    zoom: float = 1.0,
    chromium_flags: str = "",
) -> bytes:
    extra_args = chromium_flags.split() if chromium_flags else []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"] + extra_args,
        )
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()

        if token:
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            page.goto(base_url, wait_until="load")
            page.evaluate(
                "payload => localStorage.setItem('hassTokens', JSON.stringify(payload))",
                {
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": 1800,
                    "refresh_token": "refresh",
                    "expires_at": time.time() + 365 * 24 * 3600,
                },
            )

        page.goto(url, wait_until="load")
        if zoom != 1.0:
            page.evaluate(f"document.body.style.zoom = '{zoom}'")
        page.wait_for_timeout(3000)
        data = page.screenshot()
        browser.close()

    return data
