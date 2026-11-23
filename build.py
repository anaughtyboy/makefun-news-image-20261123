#!/usr/bin/env python3
"""Draw the Monday 23 November 2026 front page of THE MONDAY GLOBE.

A single 1024x1024 PNG newspaper front page, drawn entirely with Pillow
shapes and text. No network, no downloads: every glyph comes from the
system Noto fonts and every picture is vector art drawn in code.
Run:  python3 build.py   (writes entry.png next to this file)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # content width

PAPER = (247, 242, 231)
INK = (24, 24, 24)
FAINT = (90, 86, 76)
RED = (163, 29, 29)
NAVY = (44, 74, 110)
GREEN = (61, 107, 53)
GOLD = (176, 128, 30)
SKY = (126, 164, 196)
SEA = (52, 96, 128)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def vrule(draw, x, y0, y1, w=1, fill=INK):
    draw.line([(x, y0), (x, y1)], fill=fill, width=w)


def kicker(draw, x, y, text):
    f = font(SANS_B, 17)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 24


def headline(draw, x, y, text, size, max_w, leading=None):
    f = font(SERIF, size)
    leading = leading or int(size * 1.12)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, INK, leading)


def body(draw, x, y, text, size, max_w, leading=None):
    f = font(SANS, size)
    leading = leading or int(size * 1.38)
    lines = wrap(draw, text, f, max_w)
    return draw_lines(draw, lines, x, y, f, (48, 48, 44), leading)


# ---- wordless illustrations (all drawn with shapes, no text) ----

def art_globe_crack(draw, box):
    """A globe split by a jagged crack, over a row of small flags."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    r = min(x1 - x0, y1 - y0) // 2 - 12
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 231, 240),
                 outline=NAVY, width=4)
    for k in (-0.55, 0.0, 0.55):
        rx = int(r * 0.62)
        ry = r
        draw.arc([cx - rx, cy - ry, cx + rx, cy + ry],
                 start=90 - 55, end=90 + 55, fill=NAVY, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
             start=200, end=340, fill=NAVY, width=2)
    # jagged crack from top to bottom
    pts = [(cx - 8, cy - r + 4), (cx + 14, cy - r // 2), (cx - 12, cy - 4),
           (cx + 16, cy + r // 3), (cx - 6, cy + r - 6)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    # small flags below the globe
    fy = y1 - 26
    cols = [NAVY, GREEN, GOLD, RED, SEA]
    fw, gap = 26, 12
    total = 5 * fw + 4 * gap
    fx = cx - total // 2
    for i, c in enumerate(cols):
        draw.rectangle([fx, fy, fx + fw, fy + 18], fill=c)
        draw.line([(fx, fy), (fx, fy + 24)], fill=INK, width=2)
        fx += fw + gap


def art_shield_chart(draw, box):
    """A shield with rising bars: a takeover, drawn as a climbing chart.
    Drawn in a 300x130 design space, scaled to fit the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / 300.0, bh / 130.0, 1.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - 150 * s, cy - 65 * s
    def X(v):
        return ox + v * s
    def Y(v):
        return oy + v * s
    pts = [(X(75), Y(30)), (X(75), Y(98)), (X(150), Y(125)),
           (X(225), Y(98)), (X(225), Y(30)), (X(150), Y(6))]
    draw.polygon(pts, fill=(226, 236, 244), outline=NAVY, width=4)
    # rising bars inside the shield
    base = Y(108)
    for bx0, bhgt in ((100, 30), (137, 46), (174, 66)):
        draw.rectangle([X(bx0), base - bhgt * s, X(bx0 + 26), base], fill=NAVY)
    # small red up-arrow above the bars
    draw.line([(X(92), Y(26)), (X(208), Y(14))], fill=RED, width=4)
    draw.polygon([(X(196), Y(8)), (X(212), Y(12)), (X(200), Y(26))], fill=RED)


def art_capitol(draw, box):
    """US Capitol dome over a ballot box with a tick.
    Drawn in a 300x130 design space, scaled to fit the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / 300.0, bh / 130.0, 1.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - 150 * s, cy - 65 * s
    def X(v):
        return ox + v * s
    def Y(v):
        return oy + v * s
    # finial
    draw.line([(X(150), Y(16)), (X(150), Y(4))], fill=INK, width=3)
    draw.ellipse([X(145), Y(0), X(155), Y(10)], fill=INK)
    # dome: top half of a wide ellipse
    draw.pieslice([X(70), Y(16), X(230), Y(116)], start=180, end=360,
                  fill=(210, 208, 198), outline=INK, width=3)
    # drum under the dome
    draw.rectangle([X(70), Y(62), X(230), Y(76)], fill=(210, 208, 198),
                   outline=INK, width=2)
    # columns
    for dx in (84, 120, 180, 216):
        draw.rectangle([X(dx - 6), Y(76), X(dx + 6), Y(116)], fill=INK)
    # base
    draw.rectangle([X(60), Y(116), X(240), Y(128)], fill=(210, 208, 198),
                   outline=INK, width=2)
    # ballot box bottom-right, in front of the base
    bx0, by0 = X(238), Y(94)
    draw.rectangle([bx0, by0, bx0 + 54 * s, by0 + 32 * s],
                   fill=(232, 226, 210), outline=INK, width=3)
    draw.line([(bx0 - 8 * s, by0), (bx0 + 62 * s, by0)], fill=INK, width=3)
    draw.line([(bx0 + 12 * s, by0 + 18 * s), (bx0 + 26 * s, by0 + 30 * s),
               (bx0 + 50 * s, by0 + 4 * s)], fill=GREEN, width=5, joint="curve")


def art_satellite(draw, box):
    """A satellite on an orbit ring around a slice of Earth, with a star.
    Drawn in a 240x150 design space, scaled to fit the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / 240.0, bh / 150.0, 1.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - 120 * s, cy - 75 * s
    def X(v):
        return ox + v * s
    def Y(v):
        return oy + v * s
    # orbit ellipse
    draw.ellipse([X(8), Y(24), X(232), Y(126)], outline=FAINT, width=2)
    # earth slice bottom-left
    draw.pieslice([X(-20), Y(96), X(96), Y(176)], start=270, end=360,
                  fill=(126, 164, 196), outline=NAVY, width=3)
    # star top-right
    sx, sy = X(212), Y(20)
    r = 12 * s
    draw.polygon([(sx, sy - r), (sx + r * 0.33, sy - r * 0.33),
                  (sx + r, sy), (sx + r * 0.33, sy + r * 0.33),
                  (sx, sy + r), (sx - r * 0.33, sy + r * 0.33),
                  (sx - r, sy), (sx - r * 0.33, sy - r * 0.33)], fill=RED)
    # satellite body top-right of the ring
    bx, by = X(150), Y(52)
    draw.rectangle([bx - 16 * s, by - 10 * s, bx + 16 * s, by + 10 * s],
                   fill=(200, 200, 192), outline=INK, width=3)
    draw.rectangle([bx - 46 * s, by - 6 * s, bx - 18 * s, by + 6 * s],
                   fill=NAVY, outline=INK, width=2)
    draw.rectangle([bx + 18 * s, by - 6 * s, bx + 46 * s, by + 6 * s],
                   fill=NAVY, outline=INK, width=2)
    draw.line([(bx, by - 10 * s), (bx, by - 26 * s)], fill=INK, width=3)
    draw.ellipse([bx - 4 * s, by - 32 * s, bx + 4 * s, by - 24 * s], fill=RED)


def art_ship_drones(draw, box):
    """A warship on waves, circled by two small drone boats.
    Drawn in a 240x130 design space, scaled to fit the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / 240.0, bh / 130.0, 1.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - 120 * s, cy - 65 * s
    def X(v):
        return ox + v * s
    def Y(v):
        return oy + v * s
    wy = Y(96)  # waterline
    # waves
    for yy in (wy, wy + 12 * s, wy + 24 * s):
        for k in range(4):
            xa = X(8 + k * 58)
            draw.arc([xa, yy - 8 * s, xa + 44 * s, yy + 10 * s],
                     start=200, end=340, fill=SEA, width=3)
    # hull
    draw.polygon([(X(28), wy - 6 * s), (X(212), wy - 6 * s),
                  (X(194), wy + 16 * s), (X(46), wy + 16 * s)],
                 fill=(64, 64, 60), outline=INK, width=2)
    # superstructure + mast
    draw.rectangle([X(86), wy - 40 * s, X(150), wy - 6 * s],
                   fill=(96, 96, 90), outline=INK, width=2)
    draw.line([(X(128), wy - 40 * s), (X(128), wy - 66 * s)], fill=INK, width=3)
    draw.ellipse([X(122), wy - 74 * s, X(134), wy - 62 * s], fill=RED)
    # drone boats with wakes
    for dx in (2, 238):
        px = X(dx)
        draw.polygon([(px - 16 * s, wy), (px + 16 * s, wy),
                      (px + 10 * s, wy + 8 * s), (px - 10 * s, wy + 8 * s)],
                     fill=NAVY)
        draw.line([(px - 26 * s, wy + 12 * s), (px - 44 * s, wy + 16 * s)],
                  fill=FAINT, width=2)


def art_court(draw, box):
    """Courthouse columns with a gavel: an arrest on return.
    Drawn in a 240x150 design space, scaled to fit the box."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    s = min(bw / 240.0, bh / 150.0, 1.0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - 120 * s, cy - 75 * s
    def X(v):
        return ox + v * s
    def Y(v):
        return oy + v * s
    base = Y(138)
    # pediment
    draw.polygon([(X(42), Y(42)), (X(198), Y(42)), (X(120), Y(12))],
                 fill=(210, 208, 198), outline=INK, width=3)
    draw.rectangle([X(42), Y(42), X(198), Y(52)],
                   fill=(210, 208, 198), outline=INK, width=2)
    # columns
    for dx in (62, 100, 140, 178):
        draw.rectangle([X(dx - 7), Y(52), X(dx + 7), base - 12 * s],
                       fill=(232, 226, 210), outline=INK, width=2)
    draw.rectangle([X(36), base - 12 * s, X(204), base],
                   fill=(210, 208, 198), outline=INK, width=2)
    # gavel bottom-right
    gx, gy = X(196), Y(122)
    draw.line([(gx - 26 * s, gy + 8 * s), (gx + 22 * s, gy - 16 * s)],
              fill=(122, 82, 40), width=7)
    draw.rectangle([gx - 2 * s, gy - 26 * s, gx + 30 * s, gy - 8 * s],
                   fill=(122, 82, 40), outline=INK, width=2)


# ---- page assembly ----

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    name = "THE MONDAY GLOBE"
    nf = font(DISPLAY, 86)
    nw = d.textlength(name, font=nf)
    d.text(((W - nw) / 2, 26), name, font=nf, fill=INK)
    rule(d, MARGIN, W - MARGIN, 132, w=4)
    rule(d, MARGIN, W - MARGIN, 138, w=1)
    date = "MONDAY 23 NOVEMBER 2026"
    df = font(SANS_B, 25)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 148), date, font=df, fill=INK)
    lf = font(SANS, 16)
    d.text((MARGIN, 152), "WORLD NEWS IN ONE PAGE", font=lf, fill=FAINT)
    tag = "No. 327  ·  MONDAY EDITION"
    d.text((W - MARGIN - d.textlength(tag, font=lf), 152), tag, font=lf, fill=FAINT)

    y = 186
    # ---- lead: COP31 collapses (full width) ----
    lead_top = y
    y = kicker(d, MARGIN, y, "CLIMATE SUMMIT  ·  ANTALYA")
    art_w = 300
    text_w = CW - art_w - 28
    y = headline(d, MARGIN, y, "COP31 collapses as climate talks end with no deal",
                 42, text_w, leading=47)
    y = body(d, MARGIN, y + 6,
             "The summit closed on Sunday without an agreement — the first "
             "failed UN climate summit since Copenhagen in 2009, and the "
             "longest on record. The EU, Panama and island nations rejected "
             "a final text that never mentioned moving away from fossil fuels.",
             19, text_w)
    art_globe_crack(d, (W - MARGIN - art_w, lead_top + 8, W - MARGIN, 426))
    y = 434
    rule(d, MARGIN, W - MARGIN, y, w=3)
    y += 12

    # ---- row 2: two half panels, art in a fixed band at the bottom ----
    row2_top = y
    row2_h = 240
    art_h2 = 90
    half_w = (CW - 28) // 2
    # left: CrowdStrike / Zscaler
    x = MARGIN
    yy = kicker(d, x, y, "TECH  ·  CYBERSECURITY")
    yy = headline(d, x, yy, "CrowdStrike buys Zscaler in $43.9bn all-stock deal",
                  27, half_w, leading=31)
    yy = body(d, x, yy + 4,
              "The biggest cybersecurity acquisition on record. Zscaler "
              "holders get 1.135 CrowdStrike shares each, about $260.41 a "
              "share — a premium of about 34%.",
              16, half_w)
    art_shield_chart(d, (x, row2_top + row2_h - art_h2, x + half_w,
                         row2_top + row2_h))
    # right: Democrats House majority
    x = MARGIN + half_w + 28
    yy = kicker(d, x, y, "US POLITICS  ·  WASHINGTON")
    yy = headline(d, x, yy, "Democrats clinch biggest House majority since 1992",
                  27, half_w, leading=31)
    yy = body(d, x, yy + 4,
              "At least 258 of 435 seats after Chuck Hubbard beat "
              "Republican Virginia Foxx in North Carolina on Sunday. Four "
              "races are still uncalled.",
              16, half_w)
    art_capitol(d, (x, row2_top + row2_h - art_h2, x + half_w,
                    row2_top + row2_h))
    vrule(d, MARGIN + half_w + 14, row2_top, row2_top + row2_h,
          w=1, fill=(200, 194, 178))
    y = row2_top + row2_h
    rule(d, MARGIN, W - MARGIN, y, w=3)
    y += 12

    # ---- row 3: three third panels, art in a fixed band at the bottom ----
    row3_top = y
    row3_h = 290
    art_h3 = 90
    third_w = (CW - 2 * 24) // 3
    panels = [
        ("SPACE  ·  DEFENCE",
         "NATO believes Russia ready to launch nuclear-armed satellite",
         "German media reported on Monday that Western services concluded "
         "Russia plans to orbit Sputnik-S, assembled years ago and stored "
         "near Moscow, this year — possibly in December. The Kremlin "
         "dismissed the reports.",
         art_satellite),
        ("UKRAINE  ·  LIBYA",
         "Ukraine says it sank a Russian warship off Libya",
         "Kyiv says sea drones struck a Russian warship docked at a Libyan "
         "base, 2,400 km from the front line.",
         art_ship_drones),
        ("BANGLADESH  ·  DHAKA",
         "Bangladesh vows to arrest Hasina if she returns from India",
         "Dhaka says the former prime minister will be arrested if she "
         "comes back from India.",
         art_court),
    ]
    for i, (kick, head, txt, art) in enumerate(panels):
        x = MARGIN + i * (third_w + 24)
        yy = kicker(d, x, y, kick)
        yy = headline(d, x, yy, head, 22, third_w, leading=25)
        yy = body(d, x, yy + 4, txt, 15, third_w)
        art(d, (x, row3_top + row3_h - art_h3, x + third_w,
                row3_top + row3_h))
        if i < 2:
            vrule(d, x + third_w + 12, row3_top,
                  row3_top + row3_h, w=1, fill=(200, 194, 178))
    y = row3_top + row3_h
    rule(d, MARGIN, W - MARGIN, y + 8, w=3)

    # footer
    ff = font(SANS, 14)
    foot = "THE MONDAY GLOBE  ·  Monday 23 November 2026  ·  All six stories reported on 23 November 2026"
    d.text(((W - d.textlength(foot, font=ff)) / 2, y + 18), foot, font=ff, fill=FAINT)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
