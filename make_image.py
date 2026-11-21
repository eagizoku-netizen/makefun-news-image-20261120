#!/usr/bin/env python3
"""Render the news-image-20261120 entry image.

Draws a flat editorial collage of six verified world-news stories from
Friday 20 November 2026 onto a 1024x1024 canvas and saves it as
news.png beside this file.  Every shape is drawn with Pillow primitives
and every word is set in DejaVu Sans, so the output is deterministic:
running this program always produces the same bytes.

Usage: python3 make_image.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

WIDTH = 1024
HEIGHT = 1024
BACKGROUND = "#0f1b2d"
INK = "#f2eee3"
GOLD = "#d9a441"
MUTED_TEXT = "#aebfd2"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REGULAR = str(FONT_DIR / "DejaVuSans.ttf")

MARGIN = 24
GAP = 16
GRID_TOP = 156
GRID_BOTTOM = 958
PANEL_W = (WIDTH - 2 * MARGIN - 2 * GAP) // 3          # 314
PANEL_H = (GRID_BOTTOM - GRID_TOP - GAP) // 2          # 393
SCENE_H = 188
BAR_H = 46


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, cy, text, fnt, fill):
    draw.text((cx, cy), text, font=fnt, fill=fill, anchor="mm")


def fitted_font(draw, text, path, size, max_width):
    """Shrink a bold headline until it fits its bar."""
    fnt = font(path, size)
    while size > 12 and draw.textlength(text, font=fnt) > max_width:
        size -= 1
        fnt = font(path, size)
    return fnt


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph widths."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def star_points(cx, cy, r_outer, r_inner=None):
    r_inner = r_inner or r_outer * 0.45
    points = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


# ---------------------------------------------------------------- scenes
# Each scene draws inside the rectangle (x, y, x+PANEL_W-24, y+SCENE_H).

def scene_summit(draw, x, y):
    """Three flags above a summit table."""
    w = PANEL_W - 24
    flags = [(x + 6, y + 34), (x + 105, y + 34), (x + 204, y + 34)]
    fw, fh = 80, 54
    for fx, fy in flags:  # poles
        draw.line([(fx - 4, fy - 8), (fx - 4, fy + fh + 42)],
                  fill="#8d99a6", width=3)
    # United States: stripes + blue canton with dot stars
    fx, fy = flags[0]
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill="#f0ead8")
    stripe = fh / 7
    for i in range(0, 7, 2):
        draw.rectangle([fx, fy + i * stripe, fx + fw, fy + (i + 1) * stripe],
                       fill="#b73a48")
    draw.rectangle([fx, fy, fx + 36, fy + stripe * 4], fill="#2c3e70")
    for row in range(3):
        for col in range(4):
            cx, cy = fx + 6 + col * 9, fy + 6 + row * 9
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill="#f0ead8")
    # China: red field, one large star and four small ones
    fx, fy = flags[1]
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill="#c93a30")
    draw.polygon(star_points(fx + 17, fy + 16, 10), fill="#f5d13d")
    for dx, dy in [(34, 7), (38, 17), (38, 28), (34, 38)]:
        draw.polygon(star_points(fx + dx, fy + dy, 4), fill="#f5d13d")
    # Russia: white, blue, red horizontal bands
    fx, fy = flags[2]
    draw.rectangle([fx, fy, fx + fw, fy + fh // 3], fill="#eef0ee")
    draw.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3],
                   fill="#2b59a2")
    draw.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill="#c93a30")
    # summit table
    ty = y + 138
    draw.rectangle([x + 18, ty, x + w - 18, ty + 11], fill="#8a6642")
    draw.rectangle([x + 30, ty + 11, x + 38, ty + 34], fill="#6f5133")
    draw.rectangle([x + w - 38, ty + 11, x + w - 30, ty + 34],
                   fill="#6f5133")


def scene_court(draw, x, y):
    """Courthouse with the scales of justice above it."""
    cx = x + (PANEL_W - 24) // 2
    stone = "#cfc8b8"
    stone_dark = "#b3ab99"
    # scales of justice
    draw.line([(cx, y + 8), (cx, y + 46)], fill="#e8dfc8", width=4)
    draw.line([(cx - 40, y + 14), (cx + 40, y + 14)], fill="#e8dfc8", width=4)
    for sx in (cx - 40, cx + 40):
        draw.line([(sx, y + 14), (sx - 11, y + 34)], fill="#e8dfc8", width=2)
        draw.line([(sx, y + 14), (sx + 11, y + 34)], fill="#e8dfc8", width=2)
        draw.ellipse([sx - 15, y + 32, sx + 15, y + 42], fill="#e8dfc8")
    draw.ellipse([cx - 6, y + 44, cx + 6, y + 54], fill="#e8dfc8")
    # pediment, frieze, columns, steps
    draw.polygon([(cx, y + 58), (x + 22, y + 92), (x + 268, y + 92)],
                 fill=stone)
    draw.rectangle([x + 30, y + 92, x + 260, y + 104], fill=stone_dark)
    for i in range(4):
        col_x = x + 48 + i * 56
        draw.rectangle([col_x, y + 104, col_x + 18, y + 158], fill=stone)
    draw.rectangle([x + 34, y + 158, x + 256, y + 168], fill=stone_dark)
    draw.rectangle([x + 24, y + 168, x + 266, y + 180], fill=stone)


def scene_kyiv(draw, x, y):
    """Night skyline, searchlight beams and drones. Sober, no gore."""
    w = PANEL_W - 24
    draw.ellipse([x + w - 52, y + 12, x + w - 24, y + 40], fill="#d8d3c3")
    # searchlight beams (drawn first, buildings stand over them)
    draw.polygon([(x + 42, y + SCENE_H), (x + 140, y),
                  (x + 168, y), (x + 96, y + SCENE_H)], fill="#33506e")
    draw.polygon([(x + 238, y + SCENE_H), (x + 104, y),
                  (x + 132, y), (x + 268, y + SCENE_H)], fill="#2b4660")
    # drones
    for dx, dy in [(58, 44), (158, 28), (228, 60)]:
        for rx, ry in [(-13, -7), (13, -7), (-13, 7), (13, 7)]:
            draw.ellipse([x + dx + rx - 3, y + dy + ry - 3,
                          x + dx + rx + 3, y + dy + ry + 3], fill="#9fb3c8")
        draw.ellipse([x + dx - 9, y + dy - 4, x + dx + 9, y + dy + 4],
                     fill="#9fb3c8")
        draw.ellipse([x + dx - 2, y + dy + 5, x + dx + 2, y + dy + 9],
                     fill="#e5484d")
    # skyline silhouette with a few lit windows
    buildings = [(0, 96, 52), (48, 74, 62), (106, 108, 48), (150, 84, 58),
                 (204, 100, 44), (244, 78, 46)]
    for bx, top, bw in buildings:
        draw.rectangle([x + bx, y + top, x + bx + bw, y + SCENE_H],
                       fill="#070b11")
        for row in range(3):
            for col in range(2):
                if (row * 2 + col + bx) % 3 == 0:
                    wx = x + bx + 9 + col * 20
                    wy = y + top + 12 + row * 22
                    draw.rectangle([wx, wy, wx + 6, wy + 8], fill="#d9a441")


def scene_stocks(draw, x, y):
    """A chart whose line falls steeply, with a down arrow."""
    left, right = x + 34, x + 262
    top, bottom = y + 22, y + 158
    for i in range(4):  # gridlines
        gy = top + i * (bottom - top) // 3
        draw.line([(left, gy), (right, gy)], fill="#3a5f55", width=1)
    draw.line([(left, top), (left, bottom)], fill="#cfe0d8", width=3)
    draw.line([(left, bottom), (right, bottom)], fill="#cfe0d8", width=3)
    points = [(left + 6, top + 16), (left + 48, top + 30),
              (left + 84, top + 24), (left + 120, top + 58),
              (left + 154, top + 52), (left + 188, top + 92),
              (right - 6, bottom - 8)]
    draw.line(points, fill="#e5484d", width=6, joint="curve")
    for px, py in points:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill="#e5484d")
    ex, ey = points[-1]  # arrowhead at the end of the fall
    draw.polygon([(ex + 14, ey + 2), (ex - 8, ey - 8), (ex - 2, ey + 14)],
                 fill="#e5484d")


def scene_climate(draw, x, y):
    """Globe with a thermometer and a leaf."""
    cx, cy, r = x + 102, y + 96, 68
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#2e6da4")
    land = "#3f9e63"
    draw.ellipse([cx - 52, cy - 44, cx - 8, cy - 8], fill=land)
    draw.ellipse([cx + 6, cy - 30, cx + 48, cy + 2], fill=land)
    draw.ellipse([cx - 30, cy + 12, cx + 14, cy + 50], fill=land)
    draw.ellipse([cx + 22, cy + 26, cx + 52, cy + 52], fill=land)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline="#bcd6ea", width=3)
    # thermometer
    tx = x + 208
    draw.rounded_rectangle([tx, y + 26, tx + 22, y + 138], radius=11,
                           fill="#d8d3c3")
    draw.rectangle([tx + 6, y + 84, tx + 16, y + 132], fill="#d84a35")
    draw.ellipse([tx - 6, y + 128, tx + 28, y + 162], fill="#d84a35")
    for i in range(4):
        ty = y + 42 + i * 22
        draw.line([(tx + 28, ty), (tx + 38, ty)], fill="#d8d3c3", width=3)
    # leaf: a pointed oval built from a sine width profile along a
    # diagonal axis, with a vein and a short stem
    bx, by = x + 238, y + 52          # leaf base
    tx2, ty2 = x + 276, y + 16        # leaf tip
    axis_x, axis_y = tx2 - bx, ty2 - by
    length = math.hypot(axis_x, axis_y)
    ux, uy = axis_x / length, axis_y / length
    perp_x, perp_y = -uy, ux
    outline = []
    for i in range(13):
        t = i / 12
        wdt = 13 * math.sin(math.pi * t)
        outline.append((bx + axis_x * t + perp_x * wdt,
                        by + axis_y * t + perp_y * wdt))
    for i in range(11, -1, -1):
        t = i / 12
        wdt = 13 * math.sin(math.pi * t)
        outline.append((bx + axis_x * t - perp_x * wdt,
                        by + axis_y * t - perp_y * wdt))
    draw.polygon(outline, fill="#57b06a")
    draw.line([(bx, by), (tx2, ty2)], fill="#2c6e3f", width=3)
    draw.line([(bx, by), (bx - 8, by + 10)], fill="#2c6e3f", width=3)


def scene_ebola(draw, x, y):
    """A rising sun behind a hospital marked with a cross."""
    cx = x + (PANEL_W - 24) // 2
    horizon = y + 148
    # sun (a semicircle) and its rays, drawn before the building; the
    # disc is wider and taller than the hospital so the rising sun
    # stays visible above the roof and at both sides
    draw.pieslice([cx - 92, horizon - 92, cx + 92, horizon + 92],
                  start=180, end=360, fill="#e8a33d")
    for angle in (195, 225, 255, 285, 315, 345):
        rad = math.radians(angle)
        x1 = cx + 102 * math.cos(rad)
        y1 = horizon + 102 * math.sin(rad)
        x2 = cx + 118 * math.cos(rad)
        y2 = horizon + 118 * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill="#e8a33d", width=5)
    # hospital building, low and narrow in front of the sun
    draw.rectangle([cx - 64, y + 106, cx + 64, y + 180], fill="#e8e4da")
    draw.rectangle([cx - 72, y + 97, cx + 72, y + 108], fill="#b9b2a2")
    # red cross on the upper wall
    draw.rectangle([cx - 7, y + 114, cx + 7, y + 146], fill="#c93a30")
    draw.rectangle([cx - 17, y + 123, cx + 17, y + 137], fill="#c93a30")
    for wx in (cx - 52, cx + 32):  # windows
        draw.rectangle([wx, y + 120, wx + 18, y + 134], fill="#7d94a8")
    draw.rectangle([cx - 12, y + 156, cx + 12, y + 180], fill="#5a6a78")
    draw.rectangle([x, horizon + 30, x + PANEL_W - 24, y + SCENE_H],
                   fill="#5a4128")


# ---------------------------------------------------------------- panels

STORIES = [
    ("#33566e", "#26455c", scene_summit, "SHENZHEN SUMMIT",
     "US, China and Russia's leaders hold their first three-way summit "
     "and sign a peace declaration"),
    ("#5a4a63", "#463850", scene_court, "GENOCIDE RULING",
     "The World Court finds Myanmar committed genocide against the "
     "Rohingya, a first ruling of its kind against a state"),
    ("#223140", "#182635", scene_kyiv, "MASS ATTACK ON KYIV",
     "Over 400 drones and 110 missiles strike Ukraine; embassies in "
     "Kyiv are damaged and missiles fall in Poland"),
    ("#2f4f4a", "#23403b", scene_stocks, "AI DOUBTS SINK STOCKS",
     "The Nikkei falls 4.8% and the S&P 500 drops 2% in a fifth "
     "straight day of losses"),
    ("#2c5d50", "#20473d", scene_climate, "COP31 GOES OVERTIME",
     "Climate talks in Antalya stall as the draft deal drops any "
     "call to phase out fossil fuels"),
    ("#7a5c3e", "#63482f", scene_ebola, "EBOLA'S LAST PATIENT",
     "Kenya discharges its last Ebola patient, 37 days after the "
     "first case"),
]


def draw_panel(draw, col, row, story):
    panel_fill, scene_fill, scene_fn, headline, sub = story
    px = MARGIN + col * (PANEL_W + GAP)
    py = GRID_TOP + row * (PANEL_H + GAP)
    draw.rounded_rectangle([px, py, px + PANEL_W, py + PANEL_H], radius=12,
                           fill=panel_fill)
    sx, sy = px + 12, py + 12
    draw.rounded_rectangle([sx, sy, sx + PANEL_W - 24, sy + SCENE_H],
                           radius=8, fill=scene_fill)
    scene_fn(draw, sx, sy)
    bar_y = sy + SCENE_H + 10
    draw.rounded_rectangle([px + 12, bar_y, px + PANEL_W - 12, bar_y + BAR_H],
                           radius=8, fill="#101c2c")
    headline_font = fitted_font(draw, headline, BOLD, 21, PANEL_W - 44)
    centered(draw, px + PANEL_W // 2, bar_y + BAR_H // 2, headline,
             headline_font, INK)
    sub_font = font(REGULAR, 17)
    lines = wrap(draw, sub, sub_font, PANEL_W - 28)
    ly = bar_y + BAR_H + 12
    for line in lines:
        draw.text((px + 14, ly), line, font=sub_font, fill=INK)
        ly += 23


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    # header
    centered(draw, WIDTH // 2, 40, "THE WORLD IN ONE DAY",
             font(BOLD, 25), GOLD)
    centered(draw, WIDTH // 2, 96, "FRIDAY 20 NOVEMBER 2026",
             font(BOLD, 54), INK)
    draw.line([(MARGIN, 138), (WIDTH - MARGIN, 138)], fill=GOLD, width=3)
    # panels
    for index, story in enumerate(STORIES):
        draw_panel(draw, index % 3, index // 3, story)
    # footer
    centered(draw, WIDTH // 2, 986,
             "Six stories of one day · compiled from news reports "
             "of 20 November 2026", font(REGULAR, 19), MUTED_TEXT)
    out = Path(__file__).resolve().parent / "news.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
