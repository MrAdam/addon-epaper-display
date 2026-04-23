from io import BytesIO

import numpy as np
from PIL import Image, ImageOps

# sRGB → linear gamma LUT (γ = 2.2 approximation), repeated 3× for RGB point()
_GAMMA_LUT = [int(((i / 255.0) ** 2.2) * 255 + 0.5) for i in range(256)] * 3

# 8×8 Bayer threshold matrix normalised to [0, 1)
_BAYER = (
    np.array(
        [
            [0, 32, 8, 40, 2, 34, 10, 42],
            [48, 16, 56, 24, 50, 18, 58, 26],
            [12, 44, 4, 36, 14, 46, 6, 38],
            [60, 28, 52, 20, 62, 30, 54, 22],
            [3, 35, 11, 43, 1, 33, 9, 41],
            [51, 19, 59, 27, 49, 17, 57, 25],
            [15, 47, 7, 39, 13, 45, 5, 37],
            [63, 31, 55, 23, 61, 29, 53, 21],
        ],
        dtype=np.float32,
    )
    / 64.0
)


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
