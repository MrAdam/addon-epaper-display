# E-Paper Display — Home Assistant Add-on

A Home Assistant add-on that renders a dashboard screenshot and serves it as a PNG over HTTP, optimised for e-paper displays.

A headless Chromium browser captures the configured dashboard URL on a cron schedule (or on every request in direct mode), converts it to greyscale, and exposes it at `GET /screenshot.png` on port 8099.

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
2. Add this repository URL
3. Install **E-Paper Display** from the list

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | URL | — | Dashboard URL to screenshot |
| `token` | password | — | HA long-lived access token (Settings → Profile → Security) |
| `direct` | bool | `false` | If enabled, captures a fresh screenshot on every request instead of serving a cached one |
| `cron` | string | `*/5 * * * *` | Capture schedule (ignored when `direct` is enabled) |
| `width` | int | `800` | Viewport width in pixels |
| `height` | int | `480` | Viewport height in pixels |

## Usage

Once the add-on is running, fetch the screenshot from any HTTP client:

```
http://<ha-host>:8099/screenshot.png
```

### Raspberry Pi

The companion script at [`dashboard.py`](https://github.com/MrAdam/addon-epaper-display) fetches the screenshot and pushes it to a Waveshare 7.5" e-paper display:

```python
HA_URL = 'http://<ha-host>:8099/screenshot.png'
```

Run it on a schedule with a systemd timer or cron to match the add-on's refresh interval.

## Architecture notes

- Supports `amd64` and `aarch64` only — Playwright does not support `armv7`
- In schedule mode the last successful screenshot is always cached, so the Pi gets an instant response even if a render is in progress
- In direct mode the Pi waits for the full render (~10–30 s depending on dashboard complexity)
