#!/usr/bin/env python3
"""Build the news-image-20261123 atlas entry.

Composes the final 1024x1024 PNG from the generated world-map base:
a navy banner naming the day, five numbered pins with leader lines on
the map, and a legend panel listing the five verified stories of
Monday 23 November 2026.

Run from the repository root:
    python3 build_overlay.py
Writes entry.png next to this script. Fully deterministic: fixed
inputs, fixed fonts, no timestamps, no network, no randomness.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_MAP = os.path.join(
    os.path.expanduser("~"),
    "workspace/makefun/scratch/news-image-20261123-r2",
    "media-generation-world-map-base-0-1f51e37f-c7a4-4a7a-92d1-83ad0117f660.png",
)
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
NAVY = (10, 30, 51)
GOLD = (232, 196, 105)
PARCHMENT = (247, 242, 227)
INK = (16, 36, 58)
MUTED = (74, 92, 110)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# (number, dot_x, dot_y, circle_x, circle_y, colour, place label, label side)
PINS = [
    (1, 30, 428, 58, 388, (214, 69, 69), "CALIFORNIA", "right"),
    (2, 538, 458, 575, 415, (230, 126, 34), "BENGHAZI", "left"),
    (3, 658, 425, 702, 378, (26, 158, 143), "IRAN", "right"),
    (4, 500, 346, 420, 292, (125, 91, 166), "BRUSSELS", "right"),
    (5, 140, 440, 202, 422, (46, 127, 194), "AUSTIN", "right"),
]

# (number, colour, headline, detail line)
STORIES = [
    (1, (214, 69, 69), "HUANG RETURNS TO NVIDIA",
     "Nvidia reinstates Jensen Huang as CEO; shares +31%, Nasdaq +6.5%."),
    (2, (230, 126, 34), "UKRAINE SINKS RUSSIAN WARSHIP",
     "Zelenskyy says sea drones sank corvette Merkury off Benghazi, Libya."),
    (3, (26, 158, 143), "U.S. SANCTIONS IRAN'S SHADOW BANKING",
     "Treasury hits 2 dozen+ targets; $14.7bn in suspect flows flagged."),
    (4, (125, 91, 166), "EU PROPOSES 22ND RUSSIA SANCTIONS",
     "60 banks face SWIFT cut; Russian flag banned at EU sports events."),
    (5, (46, 127, 194), "CROWDSTRIKE BUYS ZSCALER FOR $44BN",
     "Largest cybersecurity deal ever, in an all-stock takeover."),
]


def draw_pin(draw, number, dot, circle, colour, label, side="right"):
    """Numbered pin: small dot on the exact spot, leader line up to the
    numbered circle, and a small place label beside the circle."""
    dx, dy = dot
    cx, cy = circle
    draw.line([(dx, dy), (cx, cy)], fill=WHITE, width=4)
    draw.line([(dx, dy), (cx, cy)], fill=colour, width=2)
    draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=WHITE)
    draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=colour)
    r = 17
    draw.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=WHITE)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    num_font = font("DejaVuSans-Bold.ttf", 22)
    tw = draw.textlength(str(number), font=num_font)
    th = 22
    draw.text((cx - tw / 2, cy - th / 2 - 1), str(number),
              font=num_font, fill=WHITE)
    lab_font = font("DejaVuSans-Bold.ttf", 15)
    if side == "left":
        lw = draw.textlength(label, font=lab_font)
        lx = cx - r - 8 - lw
    else:
        lx = cx + r + 8
    draw.text((lx + 1, cy - 9 + 1), label, font=lab_font, fill=(0, 0, 0))
    draw.text((lx, cy - 9), label, font=lab_font, fill=WHITE)


def main():
    base = Image.open(BASE_MAP).convert("RGB")
    base = base.resize((W, H), Image.LANCZOS)
    img = base.copy()
    draw = ImageDraw.Draw(img)

    # --- Banner: navy band naming the day ---
    draw.rectangle([0, 0, W, 96], fill=NAVY)
    draw.rectangle([0, 96, W, 100], fill=GOLD)
    title_font = font("DejaVuSans-Bold.ttf", 44)
    date_font = font("DejaVuSans-Bold.ttf", 25)
    title = "WORLD NEWS ATLAS"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 10), title, font=title_font, fill=WHITE)
    date = "MONDAY  \u00b7  23 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 60), date, font=date_font, fill=GOLD)

    # --- Pins on the map ---
    for number, dx, dy, cx, cy, colour, label, side in PINS:
        draw_pin(draw, number, (dx, dy), (cx, cy), colour, label, side)

    # --- Legend panel ---
    panel_top = 696
    draw.rectangle([0, panel_top - 4, W, panel_top], fill=GOLD)
    draw.rectangle([0, panel_top, W, H], fill=PARCHMENT)
    head_font = font("DejaVuSans-Bold.ttf", 19)
    head = "THE DAY IN FIVE STORIES  \u2014  ALL REPORTED 23 NOVEMBER 2026"
    hw = draw.textlength(head, font=head_font)
    draw.text(((W - hw) / 2, panel_top + 12), head, font=head_font, fill=INK)

    row_y = panel_top + 44
    row_h = 58
    badge_font = font("DejaVuSans-Bold.ttf", 20)
    story_font = font("DejaVuSans-Bold.ttf", 22)
    detail_font = font("DejaVuSans.ttf", 18)
    for number, colour, headline, detail in STORIES:
        cy = row_y + 24
        cx = 44
        r = 15
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
        tw = draw.textlength(str(number), font=badge_font)
        draw.text((cx - tw / 2, cy - 11), str(number),
                  font=badge_font, fill=WHITE)
        draw.text((70, row_y + 2), headline, font=story_font, fill=INK)
        draw.text((70, row_y + 28), detail, font=detail_font, fill=MUTED)
        row_y += row_h

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")
    if size > 1048576:
        print("WARNING: over the 1 MiB limit", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
