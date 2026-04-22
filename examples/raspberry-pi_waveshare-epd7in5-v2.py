#!/usr/bin/env python3
# Device:  Raspberry Pi Zero 2 W
# Display: Waveshare 7.5" e-Paper HAT V2 (epd7in5_V2) — 800×480, black/white
#
# Prerequisites:
#   sudo apt install fonts-noto python3-pillow
#   git clone https://github.com/waveshare/e-Paper /opt/e-Paper
#
# Run on a schedule (e.g. every 5 minutes) with cron or a systemd timer to
# match the refresh interval configured in the E-Paper Display add-on.
import io
import logging
import os
import sys
import urllib.request

libdir = '/opt/e-Paper/RaspberryPi_JetsonNano/python/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image
from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.INFO)

ADDON_URL = 'http://10.4.0.100:3412/screenshot.png'

try:
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    logging.info("Fetching screenshot from add-on...")
    with urllib.request.urlopen(ADDON_URL) as response:
        image = Image.open(io.BytesIO(response.read())).convert('1')

    epd.display(epd.getbuffer(image))
    epd.sleep()

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
