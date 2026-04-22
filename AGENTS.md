# E-Paper Display Add-on — Agent Instructions

## Project overview

A Home Assistant add-on that uses a headless Chromium browser (via Playwright) to screenshot a dashboard URL and serve the result as an e-ink optimised PNG over HTTP on port 3412.

## Stack

- **Python 3.11+** with `uv` for package management
- **Playwright** (sync API) for headless Chromium screenshots
- **Pillow + numpy** for image processing
- **croniter** for cron schedule parsing
- `http.server.HTTPServer` for the HTTP endpoint (no framework)

## Structure

```
src/epaper_display/
├── __main__.py   # Entry point: HTTPServer, cron loop, cached state
├── capture.py    # take_screenshot() — all Playwright/browser logic
├── image.py      # process_image() — all Pillow/numpy image processing
└── config.py     # load_options() — reads /data/options.json
```

Other key files:

- `config.yaml` — Home Assistant add-on metadata and config schema (defines the HA UI options)
- `translations/en.yaml` — human-readable names and descriptions for every option in `config.yaml`; must be kept in sync whenever options are added, removed, or renamed
- `build.yaml` — multi-arch Docker base images (`amd64`, `aarch64` only — Playwright does not support `armv7`)
- `pyproject.toml` + `uv.lock` — Python dependencies; hatchling is the build backend

## Image processing pipeline

Order matters: **gamma correction → greyscale → normalize → dither**

- `process_image()` in `image.py` owns all image manipulation
- `take_screenshot()` in `capture.py` returns raw PNG bytes from the browser — no image processing
- `_capture()` in `__main__.py` composes both calls; used by both the cron loop and the direct HTTP handler

## Config options (HA UI)

All options are read fresh from `/data/options.json` on every capture. Changes take effect after the current sleep/request cycle ends — no restart needed.

## Releases and versioning

Releases are managed by [release-please](https://github.com/googleapis/release-please). Never manually bump the version in `pyproject.toml` or `config.yaml`, and never create tags by hand.

When `feat` or `fix` commits land on `main`, release-please opens a PR that bumps both files and generates `CHANGELOG.md`. Merging that PR creates the GitHub release and tag automatically.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <description>
```

Common types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`. Examples:

```
feat(capture): add sidebar hiding via localStorage
fix(image): correct gamma LUT length for RGB images
chore: regenerate uv.lock
docs: update README with hide_sidebar option
```

## Examples

Client scripts live in `examples/` and are named `{device}_{display}.py`, e.g. `raspberry-pi_waveshare-epd7in5-v2.py`. Each file must include a header comment stating the device, display model, resolution, and prerequisites. Scripts should fetch from `ADDON_URL` and handle `IOError` and `KeyboardInterrupt` — see the existing example as a template.

## Local testing

Build and run the add-on exactly as it runs in production using Docker:

```bash
# Build (uses the same base image as the real add-on)
docker build \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:bookworm \
  -t epaper-display-dev .

# Run — mount a local options.json so the add-on picks up your config
docker run --rm -p 3412:3412 \
  -v /path/to/options.json:/data/options.json \
  epaper-display-dev
```

Minimal `options.json`:
```json
{
  "url": "http://10.4.0.100:8123/e-ink-dashboard/0",
  "token": "<long-lived HA token>",
  "cron": "*/5 * * * *",
  "width": 800,
  "height": 480,
  "direct": true
}
```

With `direct: true` the add-on captures on every request — no need to wait for a cron tick. Once running, fetch the screenshot with:

```bash
curl http://localhost:3412/screenshot.png -o /tmp/test.png && open /tmp/test.png
```

## Conventions

- Always work on a feature branch — never commit directly to `main`
- Use `uv` for all dependency management — never `pip` directly
- Regenerate `uv.lock` after any change to `pyproject.toml`
- Keep `--no-sandbox` and `--disable-dev-shm-usage` hardcoded in `take_screenshot` — they are required for Chromium in Docker and must not be removed
- Do not add a web framework — the stdlib `HTTPServer` is intentional for minimal footprint
- Run with `python -m epaper_display`
