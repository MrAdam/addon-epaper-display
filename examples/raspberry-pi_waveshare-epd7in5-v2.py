#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "gpiozero",
#   "lgpio",
#   "pillow",
#   "waveshare-epaper",
# ]
# ///
# Device:  Raspberry Pi Zero 2 W
# Display: Waveshare 7.5" e-Paper HAT V2 (epd7in5_V2) — 800×480, black/white
#
# Prerequisites (one-time, on the Pi):
#   sudo apt install -y swig liblgpio-dev
#
# Run on a schedule with cron to match the refresh interval in the add-on config.
# Edit your crontab with: crontab -e
#
#   */15 * * * * $HOME/.local/bin/uv run $HOME/epaper/raspberry-pi_waveshare-epd7in5-v2.py >> $HOME/epaper/display.log 2>&1
#
# Cron expands $HOME so no hardcoded path is needed. Adjust the interval to match your setup.
import io
import logging
import textwrap
import urllib.error
import urllib.request

import epaper
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)

ADDON_URL = "http://10.4.0.100:3412/screenshot.png"
TIMEOUT = 60  # seconds

EPD_WIDTH = 800
EPD_HEIGHT = 480

PAD = 20


def fetch_image() -> Image.Image:
    with urllib.request.urlopen(ADDON_URL, timeout=TIMEOUT) as response:
        return Image.open(io.BytesIO(response.read())).convert("1")


def error_image(message: str) -> Image.Image:
    img = Image.new("1", (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.load_default(size=64)
    font_body = ImageFont.load_default(size=32)

    # Border
    draw.rectangle(
        [PAD, PAD, EPD_WIDTH - PAD - 1, EPD_HEIGHT - PAD - 1], outline=0, width=3
    )

    # Title
    title = "Display Error"
    tw = draw.textlength(title, font=font_title)
    draw.text(((EPD_WIDTH - tw) / 2, PAD + 20), title, font=font_title, fill=0)

    # Separator
    sep_y = PAD + 20 + 64 + 16
    draw.line([(PAD * 2, sep_y), (EPD_WIDTH - PAD * 2, sep_y)], fill=0, width=2)

    # Word-wrapped message
    wrapped = textwrap.fill(str(message), width=42)
    draw.text(
        (EPD_WIDTH // 2, sep_y + 24), wrapped, font=font_body, fill=0, anchor="ma"
    )

    return img


try:
    epd_module = epaper.epaper("epd7in5_V2")
    epd = epd_module.EPD()
    epd.init()
    epd.Clear()

    try:
        logging.info("Fetching screenshot from add-on...")
        image = fetch_image()
        logging.info("Displaying image...")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        logging.error("Add-on returned HTTP %s: %s — body: %s", e.code, e.reason, body)
        image = error_image(f"HTTP {e.code}: {e.reason}")
    except TimeoutError as e:
        logging.error("Request timed out after %ss: %s", TIMEOUT, e)
        image = error_image(f"Timed out after {TIMEOUT}s")
    except Exception as e:
        logging.error("Failed to fetch screenshot: %s", e)
        image = error_image(str(e))

    epd.display(epd.getbuffer(image))
    epd.sleep()

except OSError as e:
    logging.error(e)

except KeyboardInterrupt:
    epd_module.epdconfig.module_exit(cleanup=True)
    exit()
