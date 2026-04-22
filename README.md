# E-Paper Display — Home Assistant Add-on

A Home Assistant add-on that renders a dashboard screenshot and serves it as a PNG over HTTP, optimised for e-paper displays.

A headless Chromium browser captures the configured dashboard URL on a cron schedule (or on every request in direct mode), applies e-ink optimised image processing, and exposes the result at `GET /screenshot.png` on port 3412.

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
2. Add this repository URL
3. Install **E-Paper Display** from the list

## Configuration

### Capture

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url` | URL | — | Dashboard URL to screenshot |
| `token` | password | — | HA long-lived access token (Settings → Profile → Security) |
| `direct` | bool | `false` | Capture a fresh screenshot on every request instead of serving a cached one |
| `cron` | string | `*/5 * * * *` | Capture schedule in cron syntax (ignored when `direct` is enabled) |
| `width` | int | `800` | Viewport width in pixels |
| `height` | int | `480` | Viewport height in pixels |
| `zoom` | float | `1.0` | Browser zoom level (0.25–4.0) |
| `chromium_flags` | string | see below | Space-separated Chromium launch flags |

Default `chromium_flags`: `--hide-scrollbars --disable-notifications --disable-extensions --disable-sync --disable-background-timer-throttling`

`--no-sandbox` and `--disable-dev-shm-usage` are always applied and cannot be overridden — they are required to run Chromium inside Docker.

### Image processing

All processing steps run in this order: gamma correction → greyscale → normalize → dither.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `gamma_correction` | bool | `true` | Convert sRGB to linear light before greyscale conversion — improves tonal accuracy on e-ink |
| `normalize` | bool | `true` | Stretch histogram to full 0–255 range — prevents washed-out grey output |
| `dithering` | dropdown | `floyd-steinberg` | Dithering algorithm: `floyd-steinberg` (best for gradients), `ordered` (Bayer matrix, faster, better for UI elements), `none` (hard threshold) |

## Usage

Once the add-on is running, fetch the screenshot from any HTTP client:

```
http://<ha-host>:3412/screenshot.png
```

### Raspberry Pi

The companion script fetches the screenshot and pushes it to a Waveshare 7.5" e-paper display:

```python
HA_URL = 'http://<ha-host>:3412/screenshot.png'
```

Run it on a schedule with a systemd timer or cron to match the add-on's capture schedule.

## Architecture notes

- Supports `amd64` and `aarch64` only — Playwright does not support `armv7`
- In schedule mode the last successful screenshot is always cached, so the Pi gets an instant response even if a render is in progress
- In direct mode the Pi waits for the full render (~10–30 s depending on dashboard complexity)
