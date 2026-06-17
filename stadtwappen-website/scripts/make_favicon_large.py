#!/usr/bin/env python3
import colorsys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "images" / "logo-favicon.png"
FAVICON_PNG = ROOT / "assets" / "images" / "favicon.png"
FAVICON_ICO = ROOT / "assets" / "images" / "favicon.ico"


def is_clover_pixel(r, g, b, a):
    if a < 20:
        return False

    hue, saturation, value = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    degrees = hue * 360
    return 95 <= degrees <= 165 and saturation >= 0.22 and value >= 0.10


def main():
    source = Image.open(SOURCE).convert("RGBA")

    # Crop around the central clover and stem, excluding the surrounding shield.
    crop = source.crop((130, 190, 585, 690))
    pixels = crop.load()
    mask = Image.new("L", crop.size, 0)
    mask_pixels = mask.load()

    for y in range(crop.height):
        for x in range(crop.width):
            if is_clover_pixel(*pixels[x, y]):
                mask_pixels[x, y] = pixels[x, y][3]

    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError("No clover pixels found.")

    clover = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    clover.alpha_composite(crop)
    clover.putalpha(mask)
    clover = clover.crop(bbox)
    mask = mask.crop(bbox)

    # Add a light outline so the green clover stays visible on dark browser tabs.
    outline_mask = mask.filter(ImageFilter.MaxFilter(19)).filter(ImageFilter.GaussianBlur(1.2))
    outline_only = ImageChops.subtract(outline_mask, mask)

    side = max(clover.width, clover.height) + 34
    icon = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    x = (side - clover.width) // 2
    y = (side - clover.height) // 2

    outline = Image.new("RGBA", clover.size, (255, 250, 232, 255))
    outline.putalpha(outline_only)
    icon.alpha_composite(outline, (x, y))
    icon.alpha_composite(clover, (x, y))

    favicon = icon.resize((512, 512), Image.Resampling.LANCZOS)
    favicon.save(FAVICON_PNG)
    favicon.save(
        FAVICON_ICO,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )

    print(f"Saved {FAVICON_PNG.relative_to(ROOT)}")
    print(f"Saved {FAVICON_ICO.relative_to(ROOT)}")
    print(f"Clover crop: {clover.width}x{clover.height}")


if __name__ == "__main__":
    main()
