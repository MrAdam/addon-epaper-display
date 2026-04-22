import json
import time

from playwright.sync_api import Page, sync_playwright


def _wait_for_ready(page: Page) -> None:
    # Wait for HA core data to be available (no-op on non-HA pages)
    try:
        page.wait_for_function(
            """() => {
                const ha = document.querySelector('home-assistant');
                if (!ha) return true;
                return !!(ha.hass && ha.hass.states && ha.hass.config);
            }""",
            timeout=15000,
        )
    except Exception:
        pass

    # Wait for loading indicators to clear
    try:
        page.wait_for_function(
            """() => {
                const els = document.querySelectorAll(
                    'ha-circular-progress, hass-loading-screen, .loading-screen'
                );
                return [...els].every(el => getComputedStyle(el).display === 'none');
            }""",
            timeout=10000,
        )
    except Exception:
        pass

    # Dismiss any visible toast notifications
    page.evaluate(
        "document.querySelectorAll('ha-toast').forEach(t => t.close && t.close())"
    )

    # Flush the rendering pipeline with a double requestAnimationFrame
    page.evaluate(
        "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
    )


def take_screenshot(
    url: str,
    token: str,
    width: int,
    height: int,
    zoom: float = 1.0,
    chromium_flags: str = "",
    hide_sidebar: bool = True,
    theme: str = "",
) -> bytes:
    extra_args = chromium_flags.split() if chromium_flags else []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"] + extra_args,
        )
        context = browser.new_context(viewport={"width": width, "height": height})

        init_items = {}
        if token:
            init_items["hassTokens"] = json.dumps({
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 1800,
                "refresh_token": "",
                "expires": time.time() + 365 * 24 * 3600,
            })
        if hide_sidebar:
            init_items["dockedSidebar"] = "always_hidden"
        if theme:
            init_items["selectedTheme"] = json.dumps({"theme": theme})
        if init_items:
            sets = "; ".join(
                f"localStorage.setItem({json.dumps(k)}, {json.dumps(v)})"
                for k, v in init_items.items()
            )
            context.add_init_script(sets)

        page = context.new_page()
        page.goto(url, wait_until="load")
        if zoom != 1.0:
            page.evaluate(f"document.body.style.zoom = '{zoom}'")
        _wait_for_ready(page)
        data = page.screenshot()
        browser.close()

    return data
