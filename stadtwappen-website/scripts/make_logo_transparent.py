#!/usr/bin/env python3
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "assets" / "images" / "logo-schild.png"
BACKUP_PATH = ROOT / "assets" / "images" / "logo-schild-transparent.png"
PADDING = 24


def is_background(pixel):
    r, g, b, a = pixel
    if a == 0:
        return False

    return is_light_neutral(r, g, b)


def is_light_neutral(r, g, b):
    # The fake checkerboard is very light and nearly neutral grey/white.
    # The shield interior is also light, but warmer, so keep it opaque.
    return r >= 220 and g >= 220 and b >= 220 and (max(r, g, b) - min(r, g, b)) <= 22


def is_edge_traversable(pixel):
    r, g, b, a = pixel
    return a == 0 or is_light_neutral(r, g, b)


def flood_fill_background(image):
    width, height = image.size
    pixels = image.load()
    queue = deque()
    seen = set()

    def enqueue(x, y):
        if (x, y) in seen:
            return
        seen.add((x, y))
        if is_background(pixels[x, y]):
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)

    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)

        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                enqueue(nx, ny)

    return image


def is_protected_shield_fill(x, y, width, height):
    nx = x / width
    ny = y / height

    in_main_shield = 0.02 <= nx <= 0.98 and 0.31 <= ny <= 0.84
    in_top_crest = 0.40 <= nx <= 0.60 and 0.04 <= ny <= 0.38

    return in_main_shield or in_top_crest


def remove_embedded_checkerboard(image):
    pixels = image.load()
    width, height = image.size
    edge_reachable = set()
    queue = deque()

    def enqueue(x, y):
        if (x, y) in edge_reachable:
            return
        if not is_edge_traversable(pixels[x, y]):
            return
        edge_reachable.add((x, y))
        queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)

    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                enqueue(nx, ny)

    for y in range(height):
        for x in range(width):
            r, g, b, _ = pixels[x, y]
            if not is_light_neutral(r, g, b):
                continue

            if (x, y) in edge_reachable:
                pixels[x, y] = (r, g, b, 0)
            elif is_protected_shield_fill(x, y, width, height):
                pixels[x, y] = (r, g, b, 255)
            else:
                pixels[x, y] = (r, g, b, 0)

    return image


def crop_with_padding(image):
    bbox = image.getbbox()
    if bbox is None:
        raise RuntimeError("No non-transparent pixels left after background removal.")

    cropped = image.crop(bbox)
    result = Image.new(
        "RGBA",
        (cropped.width + PADDING * 2, cropped.height + PADDING * 2),
        (255, 255, 255, 0),
    )
    result.alpha_composite(cropped, (PADDING, PADDING))
    return result


def main():
    image = Image.open(LOGO_PATH).convert("RGBA")
    transparent = flood_fill_background(image)
    transparent = crop_with_padding(transparent)
    transparent = remove_embedded_checkerboard(transparent)
    transparent = crop_with_padding(transparent)

    transparent.save(LOGO_PATH)
    transparent.save(BACKUP_PATH)

    print(f"Saved {LOGO_PATH.relative_to(ROOT)}")
    print(f"Saved {BACKUP_PATH.relative_to(ROOT)}")
    print(f"Size: {transparent.width}x{transparent.height}")


if __name__ == "__main__":
    main()
