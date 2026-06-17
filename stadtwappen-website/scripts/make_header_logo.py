#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "images" / "logo-favicon.png"
OUTPUT = ROOT / "assets" / "images" / "logo-header.png"

BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"


def text_size(draw, position, text, font):
    bbox = draw.textbbox(position, text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def main():
    crest = Image.open(SOURCE).convert("RGBA")
    bbox = crest.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Header crest source has no visible pixels.")

    scale = 3
    crest = crest.crop(bbox)

    canvas = Image.new("RGBA", (900 * scale, 300 * scale), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)

    title = ImageFont.truetype(BOLD, 58 * scale)
    small = ImageFont.truetype(REGULAR, 35 * scale)
    subtitle = ImageFont.truetype(BOLD, 50 * scale)

    gold = (214, 167, 72, 255)
    cream = (248, 240, 223, 255)
    text_x = 230 * scale

    text_parts = [
        draw.textbbox((text_x, 45 * scale), "GASTSTÄTTE", font=title),
        (text_x, 143 * scale, text_x + 112 * scale, 147 * scale),
        draw.textbbox((text_x + 130 * scale, 122 * scale), "zum", font=small),
        draw.textbbox((text_x, 180 * scale), "STADTWAPPEN", font=subtitle),
    ]
    text_top = min(part[1] for part in text_parts)
    text_bottom = max(part[3] for part in text_parts)
    crest.thumbnail((260 * scale, text_bottom - text_top), Image.Resampling.LANCZOS)

    crest_x = 26 * scale
    crest_y = text_top + ((text_bottom - text_top) - crest.height) // 2
    shadow = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    shadow.alpha_composite(crest, (crest_x, crest_y))
    shadow = shadow.filter(ImageFilter.GaussianBlur(7 * scale))
    canvas.alpha_composite(Image.new("RGBA", canvas.size, (0, 0, 0, 0)))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(crest, (crest_x, crest_y))

    draw.text((text_x, 45 * scale), "GASTSTÄTTE", font=title, fill=cream)
    line_y = 145 * scale
    draw.line((text_x, line_y, text_x + 112 * scale, line_y), fill=gold, width=4 * scale)
    draw.text((text_x + 130 * scale, 122 * scale), "zum", font=small, fill=cream)
    draw.text((text_x, 180 * scale), "STADTWAPPEN", font=subtitle, fill=gold)

    bbox = canvas.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("Generated header logo has no visible pixels.")

    left, top, right, bottom = bbox
    pad = 20 * scale
    cropped = canvas.crop(
        (
            max(0, left - pad),
            max(0, top - pad),
            min(canvas.width, right + pad),
            min(canvas.height, bottom + pad),
        )
    )
    cropped = cropped.resize((cropped.width // scale, cropped.height // scale), Image.Resampling.LANCZOS)
    cropped.save(OUTPUT)
    print(f"Saved {OUTPUT.relative_to(ROOT)}")
    print(f"Size: {cropped.width}x{cropped.height}")


if __name__ == "__main__":
    main()
