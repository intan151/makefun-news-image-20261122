#!/usr/bin/env python3
"""Draw "The World in One Day" -- Sunday 22 November 2026.

A one-page newspaper front page summing up six verified world-news
stories of 22 November 2026. Drawn entirely with Pillow; no photos,
no network, no randomness -- two runs write byte-identical PNGs.

Usage:  python3 draw_news.py
Writes entry.png (1024x1024, PNG, <= 1 MiB) next to this file.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
CONTENT_W = W - 2 * MARGIN

PAPER = (250, 246, 236)
CARD = (255, 254, 249)
INK = (30, 28, 25)
MUTED = (110, 104, 94)
RED = (158, 30, 30)
BLUE = (30, 78, 116)
GREEN = (46, 110, 64)
RULE = (214, 205, 182)
ICON_BG = (236, 229, 211)
GOLD = (168, 124, 44)

# ---------------------------------------------------------------- fonts

_FONT_PATHS = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
}


def _load(kind, size):
    for path in _FONT_PATHS[kind]:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default(size=size)


def fonts():
    return {
        "masthead": _load("serif_bold", 58),
        "date": _load("sans_bold", 26),
        "lead_head": _load("serif_bold", 31),
        "head": _load("serif_bold", 21),
        "kicker": _load("sans_bold", 15),
        "body": _load("sans", 17),
        "lead_body": _load("sans", 19),
        "footer": _load("sans", 15),
        "number": _load("serif_bold", 24),
    }


# ---------------------------------------------------------------- text

def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill, leading,
                 max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons

def icon_globe(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 9
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=fg, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=fg, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160, fill=fg, width=3)


def icon_ship(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    # hull
    d.polygon([(x + 10, y + s // 2 + 6), (x + s - 10, y + s // 2 + 6),
               (x + s - 22, y + 3 * s // 4), (x + 22, y + 3 * s // 4)],
              fill=fg)
    # mast + bridge
    d.line([x + s // 2, y + s // 4, x + s // 2, y + s // 2 + 6],
           fill=fg, width=4)
    d.rectangle([x + s // 2 - 12, y + s // 3, x + s // 2 + 12,
                 y + s // 2], fill=fg)
    # waves
    for wy in (y + s - 22, y + s - 12):
        d.arc([x + 8, wy - 6, x + s // 2, wy + 6], 180, 360, fill=fg, width=3)
        d.arc([x + s // 2, wy - 6, x + s - 8, wy + 6], 180, 360,
              fill=fg, width=3)


def icon_building(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    bx, by = x + int(s * 0.28), y + int(s * 0.18)
    bw, bh = int(s * 0.44), int(s * 0.64)
    d.rectangle([bx, by, bx + bw, by + bh], outline=fg, width=4)
    # broken top corner: jagged crack
    d.line([(bx + bw // 2, by), (bx + bw // 2 + 5, by + 10),
            (bx + bw // 2 - 2, by + 20), (bx + bw // 2 + 6, by + 30)],
           fill=fg, width=3)
    # windows
    for r in range(3):
        for c in range(2):
            wx = bx + 6 + c * (bw - 12) // 2
            wy = by + int(bh * 0.52) + r * (bh // 5)
            d.rectangle([wx, wy, wx + 8, wy + 8], fill=fg)
    # rubble at the base
    d.polygon([(bx - 2, by + bh), (bx + 12, by + bh - 10),
               (bx + 26, by + bh)], fill=fg)


def icon_capitol(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    cx = x + s // 2
    r = int(s * 0.20)
    top = y + int(s * 0.30)
    # dome
    d.pieslice([cx - r, top, cx + r, top + 2 * r], 180, 360, fill=fg)
    d.line([cx, top - 6, cx, top], fill=fg, width=3)
    # base and columns
    base = top + 2 * r
    d.rectangle([cx - r - 6, base, cx + r + 6, base + 7], fill=fg)
    for k in range(-2, 3):
        d.rectangle([cx + k * 11 - 3, base + 7, cx + k * 11 + 3,
                     base + 19], fill=fg)
    d.rectangle([cx - r - 8, base + 19, cx + r + 8, base + 25], fill=fg)


def icon_orbit(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    cx, cy = x + s // 2, y + s // 2
    # elliptical orbit
    d.ellipse([x + 8, y + s // 4, x + s - 8, y + 3 * s // 4],
              outline=fg, width=3)
    # planet
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=fg)
    # satellite dot on the orbit
    d.ellipse([x + s - 16, y + s // 4 - 2, x + s - 8, y + s // 4 + 6],
              fill=fg)
    # star specks
    for sx, sy in ((x + 16, y + 20), (x + 20, y + s - 22),
                   (x + s - 24, y + s - 18)):
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=fg)


def icon_flag(d, x, y, s, fg):
    d.ellipse([x, y, x + s, y + s], fill=ICON_BG)
    # pole
    d.line([x + 16, y + 12, x + 16, y + s - 12], fill=fg, width=4)
    # checkered flag
    fx, fy, cw = x + 20, y + 16, 14
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * cw, fy + r * cw,
                             fx + (c + 1) * cw, fy + (r + 1) * cw],
                            fill=fg)
    d.rectangle([fx, fy, fx + 4 * cw, fy + 3 * cw], outline=fg, width=3)


ICONS = {
    "globe": icon_globe,
    "ship": icon_ship,
    "building": icon_building,
    "capitol": icon_capitol,
    "orbit": icon_orbit,
    "flag": icon_flag,
}

# ---------------------------------------------------------------- stories

# (number, kicker, headline, summary, icon, accent)
STORIES = [
    (1, "ANTALYA  ·  CLIMATE",
     "COP31 talks collapse with no deal",
     "The UN climate summit ended two days past its deadline — the "
     "longest ever — with no agreement. The draft made no mention of "
     "fossil fuels, and the UN chief called it deeply disappointing.",
     "globe", BLUE),
    (2, "BENGHAZI, LIBYA  ·  CONFLICT",
     "Sea drones hit Russian warship Merkury",
     "The Russian corvette Merkury, docked at Benghazi naval base, "
     "was hit by suspected Ukrainian maritime drones. No one claimed "
     "the attacks.",
     "ship", RED),
    (3, "DYMER, UKRAINE  ·  WAR",
     "Drone hits apartment block; 14 missing",
     "A Russian drone partly destroyed a five-storey block in Dymer, "
     "north of Kyiv. Fourteen missing; nine evacuated, including a "
     "child.",
     "building", RED),
    (4, "WASHINGTON  ·  U.S. POLITICS",
     "Democrats win biggest House majority since 1992",
     "Democrat Chuck Hubbard's recount win in North Carolina gave "
     "Democrats at least 258 House seats — their largest majority "
     "since 1992.",
     "capitol", BLUE),
    (5, "SPACE  ·  MERCURY",
     "BepiColombo enters orbit around Mercury",
     "The European-Japanese mission entered Mercury orbit after an "
     "eight-year journey — only the second craft ever to do so. The "
     "spacecraft is safe.",
     "orbit", GREEN),
    (6, "PORTIMAO, PORTUGAL  ·  MOTORSPORT",
     "Marquez seals record-equalling eighth MotoGP title",
     "Marc Marquez clinched the 2026 championship with eighth place "
     "at the Portuguese GP, drawing level with Giacomo Agostini. He "
     "overturned a 102-point deficit — the largest comeback in "
     "MotoGP history.",
     "flag", GOLD),
]


def number_badge(d, x, y, n, f, accent):
    d.ellipse([x, y, x + 38, y + 38], fill=accent)
    txt = str(n)
    tw = d.textlength(txt, font=f["number"])
    d.text((x + (38 - tw) / 2, y + 4), txt, font=f["number"],
           fill=(255, 255, 255))


def card(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=2)


def main():
    f = fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f["masthead"])
    d.text(((W - tw) / 2, 20), title, font=f["masthead"], fill=INK)
    d.line([(MARGIN, 98), (W - MARGIN, 98)], fill=INK, width=3)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date, font=f["date"])
    d.text(((W - dw) / 2, 106), date, font=f["date"], fill=RED)
    sub = "Six stories from around the world — as reported on 22 November 2026"
    sw = d.textlength(sub, font=f["footer"])
    d.text(((W - sw) / 2, 138), sub, font=f["footer"], fill=MUTED)
    d.line([(MARGIN, 162), (W - MARGIN, 162)], fill=INK, width=2)

    # ---- lead story (1), full width ---------------------------------
    n, kicker, head, body, icon, accent = STORIES[0]
    y0 = 176
    card(d, MARGIN, y0, W - MARGIN, y0 + 168)
    number_badge(d, MARGIN + 16, y0 + 14, n, f, accent)
    d.text((MARGIN + 66, y0 + 16), kicker, font=f["kicker"], fill=accent)
    end_y = draw_wrapped(d, MARGIN + 66, y0 + 38, head, f["lead_head"],
                         640, INK, 37)
    draw_wrapped(d, MARGIN + 66, end_y + 8, body, f["lead_body"], 640,
                 INK, 24)
    ICONS[icon](d, W - MARGIN - 128, y0 + 14, 112, accent)

    # ---- grid stories (2-5), two columns -----------------------------
    grid_y = [356, 548]
    grid_h = 180
    col_w = (CONTENT_W - 16) // 2
    for idx, (n, kicker, head, body, icon, accent) in enumerate(STORIES[1:5]):
        row, col = divmod(idx, 2)
        x0 = MARGIN + col * (col_w + 16)
        y0 = grid_y[row]
        card(d, x0, y0, x0 + col_w, y0 + grid_h)
        number_badge(d, x0 + 12, y0 + 12, n, f, accent)
        d.text((x0 + 58, y0 + 12), kicker, font=f["kicker"], fill=accent)
        ICONS[icon](d, x0 + col_w - 74, y0 + 10, 60, accent)
        head_w = col_w - 58 - 78
        end_y = draw_wrapped(d, x0 + 58, y0 + 34, head, f["head"],
                             head_w, INK, 25)
        body_y = end_y + 7
        max_body = max(1, (y0 + grid_h - 10 - body_y) // 21)
        draw_wrapped(d, x0 + 14, body_y, body, f["body"], col_w - 28,
                     INK, 21, max_lines=max_body)

    # ---- bottom story (6), full width --------------------------------
    n, kicker, head, body, icon, accent = STORIES[5]
    y0 = 740
    card(d, MARGIN, y0, W - MARGIN, y0 + 152)
    number_badge(d, MARGIN + 16, y0 + 14, n, f, accent)
    d.text((MARGIN + 66, y0 + 16), kicker, font=f["kicker"], fill=accent)
    end_y = draw_wrapped(d, MARGIN + 66, y0 + 38, head, f["head"], 700,
                         INK, 27)
    draw_wrapped(d, MARGIN + 66, end_y + 8, body, f["body"], 700, INK, 22)
    ICONS[icon](d, W - MARGIN - 128, y0 + 14, 112, accent)

    # ---- footer -------------------------------------------------------
    d.line([(MARGIN, 912), (W - MARGIN, 912)], fill=INK, width=2)
    foot1 = "Sources: BBC · Reuters · France 24 · Al Jazeera · The Guardian · MotoGP.com"
    fw = d.textlength(foot1, font=f["footer"])
    d.text(((W - fw) / 2, 922), foot1, font=f["footer"], fill=MUTED)
    foot2 = "Drawn by program — no photographs. All six stories were reported on 22 November 2026."
    fw = d.textlength(foot2, font=f["footer"])
    d.text(((W - fw) / 2, 946), foot2, font=f["footer"], fill=MUTED)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "."
        os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, os.path.getsize(path), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
