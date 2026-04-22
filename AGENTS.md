# E-Paper Display Add-on — Agent Instructions

## Project overview

A Home Assistant add-on that uses a headless Chromium browser (via Playwright) to screenshot a dashboard URL and serve the result as an e-ink optimised PNG over HTTP on port 3412.

## Stack

- **Python 3.11+** with `uv` for package management
- **Playwright** (sync API) for headless Chromium screenshots
- **Pillow + numpy** for image processing
- **croniter** for cron schedule parsing
- `http.server.HTTPServer` for the HTTP endpoint (no framework)

## Key files

- `server.py` — entire runtime: screenshot capture, image processing pipeline, HTTP server
- `config.yaml` — Home Assistant add-on metadata and config schema (defines the HA UI options)
- `build.yaml` — multi-arch Docker base images (`amd64`, `aarch64` only — Playwright does not support `armv7`)
- `pyproject.toml` + `uv.lock` — Python dependencies

## Image processing pipeline

Order matters: **gamma correction → greyscale → normalize → dither**

- `process_image()` owns all image manipulation
- `take_screenshot()` returns raw PNG bytes from the browser — no image processing
- Both functions are called together by `refresh_loop` (schedule mode) and `Handler.do_GET` (direct mode)

## Config options (HA UI)

All options are read fresh from `/data/options.json` on every capture. Changes take effect after the current sleep/request cycle ends — no restart needed.

## Conventions

- Use `uv` for all dependency management — never `pip` directly
- Regenerate `uv.lock` after any change to `pyproject.toml`
- Keep `--no-sandbox` and `--disable-dev-shm-usage` hardcoded in `take_screenshot` — they are required for Chromium in Docker and must not be removed
- Do not add a web framework — the stdlib `HTTPServer` is intentional for minimal footprint
