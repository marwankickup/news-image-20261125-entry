#!/usr/bin/env python3
"""Draw "The World on Wednesday" — a newspaper front page summing up the
world news of Wednesday 25 November 2026. Deterministic: fixed fonts,
fixed geometry, no timestamps, no randomness. Output: 1024x1024 PNG.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
BLUE = (30, 64, 120)
GREY = (110, 105, 95)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(d, x, y, w, h, tag, tag_color, headline, sub, picto):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(200, 192, 172), width=2)
    # tag bar
    d.rectangle([x, y, x + w, y + 34], fill=tag_color)
    d.text((x + 12, y + 7), tag, font=SANS_B(20), fill=(255, 255, 255))
    # pictogram zone on the right
    px, py = x + w - 118, y + 46
    picto(d, px, py)
    # headline + sub on the left
    tx = x + 12
    tw = w - 150
    lines = wrap(d, headline, SANS_B(27), tw)
    cy = y + 48
    for ln in lines:
        d.text((tx, cy), ln, font=SANS_B(27), fill=INK)
        cy += 32
    cy += 6
    for ln in wrap(d, sub, SANS(19), tw):
        d.text((tx, cy), ln, font=SANS(19), fill=(70, 66, 58))
        cy += 24


# ---- pictograms (simple flat shapes, drawn in a ~110x110 box) ----

def pic_tariffs(d, x, y):
    # rising bar chart with an upward arrow
    d.rectangle([x + 12, y + 66, x + 28, y + 100], fill=INK)
    d.rectangle([x + 34, y + 48, x + 50, y + 100], fill=RED)
    d.rectangle([x + 56, y + 30, x + 72, y + 100], fill=BLUE)
    d.rectangle([x + 78, y + 12, x + 94, y + 100], fill=(255, 196, 0))
    d.line([x + 6, y + 100, x + 100, y + 100], fill=INK, width=3)
    # upward arrow above the bars
    d.line([x + 16, y + 58, x + 62, y + 14], fill=RED, width=5)
    d.polygon([(x + 52, y + 8), (x + 72, y + 6), (x + 66, y + 26)],
              fill=RED)


def pic_hormuz(d, x, y):
    # tanker on waves with a blast burst above it
    d.rectangle([x + 10, y + 62, x + 96, y + 84], fill=(60, 60, 60))
    d.rectangle([x + 62, y + 44, x + 84, y + 62], fill=(90, 90, 90))
    d.line([x + 84, y + 30, x + 84, y + 44], fill=INK, width=4)
    cx, cy = x + 52, y + 26
    for k in range(8):
        a = math.pi * k / 4
        x2 = cx + int(30 * math.cos(a))
        y2 = cy + int(30 * math.sin(a))
        d.line([cx, cy, x2, y2], fill=RED, width=5)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 196, 0))
    d.arc([x + 4, y + 86, x + 106, y + 104], 0, 180, fill=BLUE, width=4)
    d.arc([x + 20, y + 92, x + 90, y + 108], 0, 180, fill=BLUE, width=3)


def pic_shenzhou(d, x, y):
    # rocket rising toward a ringed station
    d.ellipse([x + 66, y + 6, x + 106, y + 46], outline=BLUE, width=4)
    d.ellipse([x + 78, y + 18, x + 94, y + 34], fill=(90, 90, 90))
    d.polygon([(x + 28, y + 20), (x + 40, y + 20), (x + 46, y + 60),
               (x + 22, y + 60)], fill=INK)
    d.polygon([(x + 34, y + 8), (x + 40, y + 20), (x + 28, y + 20)],
              fill=RED)
    d.polygon([(x + 22, y + 60), (x + 46, y + 60), (x + 40, y + 74),
               (x + 28, y + 74)], fill=RED)
    d.ellipse([x + 30, y + 30, x + 38, y + 38], fill=(255, 255, 255))
    d.line([x + 34, y + 78, x + 34, y + 94], fill=(255, 196, 0), width=5)
    # flame: a small orange triangle under the engine
    d.polygon([(x + 26, y + 74), (x + 42, y + 74), (x + 34, y + 96)],
              fill=(255, 140, 0))
    d.rectangle([x + 8, y + 94, x + 100, y + 100], fill=(120, 110, 95))


def pic_canary(d, x, y):
    # crowded wooden boat on waves
    d.polygon([(x + 10, y + 56), (x + 98, y + 56), (x + 88, y + 84),
               (x + 20, y + 84)], fill=(120, 72, 30))
    d.line([x + 10, y + 56, x + 98, y + 56], fill=INK, width=3)
    for j, cx in enumerate((x + 24, x + 40, x + 56, x + 72, x + 86)):
        d.ellipse([cx - 6, y + 44, cx + 6, y + 56],
                  fill=RED if j % 2 == 0 else BLUE)
    d.arc([x + 4, y + 88, x + 106, y + 104], 0, 180, fill=BLUE, width=4)
    d.arc([x + 20, y + 94, x + 90, y + 110], 0, 180, fill=BLUE, width=3)
    d.ellipse([x + 46, y + 8, x + 60, y + 22], fill=(255, 196, 0))


def pic_inflation(d, x, y):
    # price tag with a rising arrow over a dinner plate
    d.ellipse([x + 8, y + 58, x + 92, y + 98], fill=(255, 255, 255),
              outline=INK, width=3)
    d.ellipse([x + 34, y + 70, x + 66, y + 86], fill=(120, 72, 30))
    d.polygon([(x + 62, y + 8), (x + 96, y + 8), (x + 96, y + 40),
               (x + 62, y + 40), (x + 50, y + 24)], fill=RED)
    d.ellipse([x + 56, y + 18, x + 66, y + 28], fill=(255, 255, 255))
    # rising arrow on the left, clear of the tag
    d.line([x + 12, y + 52, x + 44, y + 24], fill=INK, width=5)
    d.polygon([(x + 34, y + 16), (x + 50, y + 14), (x + 46, y + 34)],
              fill=INK)
    d.text((x + 14, y + 100), "6%", font=SANS_B(22), fill=RED)


def pic_abrego(d, x, y):
    # plane flying away over Spain's red-yellow-red stripes
    d.rectangle([x + 8, y + 82, x + 102, y + 88], fill=(178, 34, 34))
    d.rectangle([x + 8, y + 88, x + 102, y + 96], fill=(255, 196, 0))
    d.rectangle([x + 8, y + 96, x + 102, y + 102], fill=(178, 34, 34))
    d.polygon([(x + 12, y + 46), (x + 98, y + 46), (x + 84, y + 56),
               (x + 26, y + 56)], fill=INK)
    d.polygon([(x + 52, y + 26), (x + 62, y + 46), (x + 48, y + 46)],
              fill=INK)
    d.polygon([(x + 32, y + 56), (x + 42, y + 56), (x + 36, y + 70)],
              fill=INK)
    d.polygon([(x + 68, y + 56), (x + 78, y + 56), (x + 74, y + 70)],
              fill=INK)
    # dotted flight path trailing the plane
    for dx in (x + 8, x + 20, x + 32):
        d.ellipse([dx, y + 34, dx + 5, y + 39], fill=BLUE)


PANELS = [
    ("US TARIFFS", RED,
     "US proposes tariffs on 14 trading partners",
     "Highest rates hit China, +20% on its goods; EU, Japan, South Korea also named.",
     pic_tariffs),
    ("HORMUZ", (0, 90, 80),
     "Tankers hit mines in the Strait of Hormuz",
     "Iran says tankers exploded and caught fire on an unofficial route.",
     pic_hormuz),
    ("SPACE", BLUE,
     "Shenzhou 24 lifts off for Tiangong",
     "Crew of three includes Pakistan's Muhammad Zeeshan Ali, the first foreigner aboard.",
     pic_shenzhou),
    ("CANARY ISLANDS", (120, 60, 30),
     "Record 2,100 migrants reach Canaries",
     "Over 24 hours in crowded boats, most landing on El Hierro island.",
     pic_canary),
    ("US INFLATION", (90, 60, 10),
     "Thanksgiving dinner costs 6% more",
     "US prices stayed high in October; the classic feast is $58.63 for ten.",
     pic_inflation),
    ("IMMIGRATION", (60, 40, 90),
     "Abrego Garcia leaves US for Spain",
     "Wrongfully deported migrant departs voluntarily, landing in Madrid.",
     pic_abrego),
]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2, 18), "THE WORLD", font=SERIF_B(76), fill=INK, anchor="ma")
    d.text((W // 2, 102), "on Wednesday", font=SERIF(34), fill=RED, anchor="ma")
    d.rectangle([32, 148, W - 32, 150], fill=INK)
    d.text((W // 2, 158), "WEDNESDAY, 25 NOVEMBER 2026",
           font=SANS_B(30), fill=INK, anchor="ma")
    d.rectangle([32, 196, W - 32, 198], fill=INK)

    # grid: 2 columns x 3 rows
    gx, gy = 32, 214
    pw, ph, gap = 468, 240, 24
    for i, (tag, color, head, sub, picto) in enumerate(PANELS):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + 14)
        draw_panel(d, x, y, pw, ph, tag, color, head, sub, picto)

    # footer
    d.rectangle([32, 968, W - 32, 970], fill=INK)
    d.text((W // 2, 978), "Six stories from Wednesday 25 November 2026 \u2022 compiled from wire reports",
           font=SANS(18), fill=GREY, anchor="ma")

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
