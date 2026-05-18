import json
import time
from urllib.parse import urlparse

from playwright.sync_api import FloatRect, Page, sync_playwright


def _wait_for_ready(page: Page) -> None:
    try:
        page.wait_for_function(
            """() => {
                const ha = document.querySelector('home-assistant');
                if (!ha || !ha.shadowRoot) return false;
                const main = ha.shadowRoot.querySelector('home-assistant-main');
                if (!main || !main.shadowRoot) return false;
                const resolver = main.shadowRoot.querySelector('partial-panel-resolver');
                if (!resolver || resolver._loading) return false;
                const panel = resolver.children[0];
                if (!panel) return false;
                if (panel._panelState !== undefined) return panel._panelState === 'loaded';
                return !panel._loading;
            }""",
            timeout=30000,
        )
    except Exception:
        pass

    try:
        page.wait_for_function(
            """() => {
                const ha = document.querySelector('home-assistant');
                if (!ha) return false;
                const h = ha.hass;
                if (!h || !h.states || Object.keys(h.states).length === 0) return false;
                if (h.connected === false) return false;
                if (h.config && h.config.state !== 'RUNNING') return false;
                return true;
            }""",
            timeout=30000,
        )
    except Exception:
        pass

    try:
        page.wait_for_function(
            """() => {
                if (document.getElementById('ha-launch-screen')) return false;
                const selectors = [
                    'ha-circular-progress', 'hass-loading-screen',
                    '.loading', '.spinner', '[loading]', 'hui-card-preview',
                ];
                function isVisible(el) {
                    const s = window.getComputedStyle(el);
                    return s.display !== 'none' && s.visibility !== 'hidden';
                }
                function hasLoading(root) {
                    for (const sel of selectors)
                        for (const el of root.querySelectorAll(sel))
                            if (isVisible(el)) return true;
                    for (const el of root.querySelectorAll('*'))
                        if (el.shadowRoot && hasLoading(el.shadowRoot)) return true;
                    return false;
                }
                return !hasLoading(document);
            }""",
            timeout=15000,
        )
    except Exception:
        pass

    try:
        page.wait_for_function(
            """() => {
                function findAll(root, sel) {
                    const found = [...root.querySelectorAll(sel)];
                    for (const el of root.querySelectorAll('*'))
                        if (el.shadowRoot) found.push(...findAll(el.shadowRoot, sel));
                    return found;
                }
                function isVisible(el) {
                    const s = window.getComputedStyle(el);
                    return s.display !== 'none' && s.visibility !== 'hidden';
                }
                const cards = findAll(document, 'calendar-card-pro');
                if (cards.length === 0) return true;
                return cards.every(c => {
                    if (!c.shadowRoot) return true;
                    const loaders = findAll(c.shadowRoot, '.loading, .loading-indicator');
                    if (loaders.some(el => isVisible(el))) return false;
                    // Defend against race: if neither loader is visible but the card
                    // has rendered nothing at all, keep waiting — Lit may not have
                    // rendered yet.  When loaded, the card always has a header-container.
                    if (!c.shadowRoot.querySelector('.header-container')) return false;
                    return true;
                });
            }""",
            timeout=30000,
        )
    except Exception:
        pass

    try:
        page.wait_for_function(
            """() => {
                function findAll(root, sel) {
                    const found = [...root.querySelectorAll(sel)];
                    for (const el of root.querySelectorAll('*'))
                        if (el.shadowRoot) found.push(...findAll(el.shadowRoot, sel));
                    return found;
                }
                const cards = findAll(document, 'hui-markdown-card');
                if (cards.length === 0) return true;
                return cards.every(c => {
                    if (!c.shadowRoot) return false;
                    const content = c.shadowRoot.querySelector(
                        'ha-markdown-element, .content, .card-content'
                    );
                    return content && content.textContent.trim().length > 0;
                });
            }""",
            timeout=15000,
        )
    except Exception:
        pass

    try:
        page.evaluate("""() => {
            const ha = document.querySelector('home-assistant');
            if (!ha || !ha.shadowRoot) return;
            const nm = ha.shadowRoot.querySelector('notification-manager');
            if (!nm || !nm.shadowRoot) return;
            nm.shadowRoot.querySelectorAll('ha-toast').forEach(t => t.close && t.close('dismiss'));
        }""")
    except Exception:
        pass

    try:
        page.evaluate(
            "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))",
        )
    except Exception:
        pass

    # Catch auth failures early rather than silently serving a login/error screenshot
    title = page.title().lower()
    if any(
        kw in title
        for kw in (
            "log in",
            "login",
            "sign in",
            "error",
            "403",
            "404",
            "unable to connect",
        )
    ):
        raise RuntimeError(
            f"Page title '{page.title()}' suggests auth failure or error — aborting capture"
        )


def take_screenshot(
    url: str,
    token: str,
    width: int,
    height: int,
    zoom: float = 1.0,
    chromium_flags: str = "",
    hide_sidebar: bool = True,
    hide_toolbar: bool = False,
    timezone_id: str | None = None,
) -> bytes:
    extra_args = chromium_flags.split() if chromium_flags else []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", *extra_args],
        )
        toolbar_height = round(56 * zoom) if hide_toolbar else 0
        context = browser.new_context(
            viewport={"width": width, "height": height + toolbar_height},
            timezone_id=timezone_id,
        )

        parsed = urlparse(url)
        hass_url = f"{parsed.scheme}://{parsed.netloc}"
        client_id = f"{hass_url}/"

        init_items = {}
        if token:
            init_items["hassTokens"] = json.dumps(
                {
                    "access_token": token,
                    "token_type": "Bearer",
                    "expires_in": 1800,
                    "refresh_token": "",
                    "expires": (time.time() + 365 * 24 * 3600) * 1000,
                    "hassUrl": hass_url,
                    "clientId": client_id,
                }
            )
        if hide_sidebar:
            init_items["dockedSidebar"] = "always_hidden"
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
        clip = (
            FloatRect(
                x=0.0,
                y=float(toolbar_height),
                width=float(width),
                height=float(height),
            )
            if hide_toolbar
            else None
        )
        data = page.screenshot(clip=clip)
        browser.close()

    return data
