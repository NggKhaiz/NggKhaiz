#!/usr/bin/env python3
"""Generate every raster image the site needs.

Outputs (all committed, so deploying needs no build step):

  assets/img/icons/      favicon 16/32/48, apple-touch-icon, PWA 192/512, favicon.ico
  assets/img/social/     og-profile (+light), og-labs, github-social, x-header,
                         discord-banner, avatar, avatar-384
  assets/img/covers/     one 16:9 cover per project

Requires: pip install pillow, plus the variable fonts from tools/fetch_fonts.py
(cached in .cache/fonts).
Usage:    python3 tools/build_images.py
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / ".cache" / "fonts"
OUT = ROOT / "assets" / "img"

PORTRAIT = ROOT / "tools" / "src" / "portrait.png"

INTER = FONTS / "Inter.ttf"
TIGHT = FONTS / "InterTight.ttf"
MONO = FONTS / "JetBrainsMono.ttf"

DARK = {
    "bg": (10, 10, 11),
    "panel": (16, 16, 18),
    "panel2": (22, 22, 25),
    "line": (38, 38, 42),
    "line_soft": (28, 28, 31),
    "text": (244, 242, 238),
    "muted": (154, 150, 143),
    "faint": (111, 107, 100),
    "accent": (217, 160, 107),
}
LIGHT = {
    "bg": (246, 244, 240),
    "panel": (255, 255, 255),
    "panel2": (239, 236, 231),
    "line": (216, 211, 203),
    "line_soft": (228, 224, 217),
    "text": (19, 18, 17),
    "muted": (93, 90, 85),
    "faint": (139, 135, 127),
    "accent": (138, 82, 32),
}


# ---------------------------------------------------------------- type helpers


def typeface(path: Path, size: int, weight: int = 400, optical: float | None = None) -> ImageFont.FreeTypeFont:
    """Load a variable font and pin its axes."""
    font = ImageFont.truetype(str(path), size)
    try:
        axes = font.get_variation_axes()
    except OSError:
        return font
    values = []
    for axis in axes:
        name = axis["name"] if isinstance(axis, dict) else axis.name
        if isinstance(name, (bytes, bytearray)):
            name = name.decode("utf-8", "ignore")
        name = name.lower()
        if "weight" in name or name == "wght":
            values.append(weight)
        elif "optical" in name or name == "opsz":
            values.append(optical if optical is not None else size)
        else:
            values.append(axis["default"] if isinstance(axis, dict) else axis.default)
    font.set_variation_by_axes(values)
    return font


def span(text: str, font: ImageFont.FreeTypeFont, tracking: float = 0.0) -> float:
    if not text:
        return 0.0
    return sum(font.getlength(ch) for ch in text) + tracking * (len(text) - 1)


def write(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill,
    tracking: float = 0.0,
    anchor: str = "left",
) -> float:
    """Baseline-anchored text with manual tracking. Returns the end x."""
    width = span(text, font, tracking)
    x, y = xy
    if anchor == "center":
        x -= width / 2
    elif anchor == "right":
        x -= width
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + tracking
    return x


# ---------------------------------------------------------------- shape helpers


def rounded(draw: ImageDraw.ImageDraw, box, radius: int, fill=None, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def rings(canvas: Image.Image, cx: float, cy: float, radii: list[int], colour, width: int = 2) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for r in radii:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour + (255,), width=width)
    canvas.alpha_composite(layer)


def monogram(size: int, theme: dict, letter: str = "K") -> Image.Image:
    """Circular mark: ringed plate, letter, and one accent dot on the ring."""
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    plate_r = size * 0.44
    centre = size / 2
    draw.ellipse(
        [centre - plate_r, centre - plate_r, centre + plate_r, centre + plate_r],
        fill=theme["panel2"] + (255,),
        outline=theme["line"] + (255,),
        width=max(2, size // 150),
    )
    face = typeface(TIGHT, int(size * 0.46), 800)
    write(draw, (centre, centre + size * 0.165), letter, face, theme["text"], tracking=-size * 0.015, anchor="center")

    dot_r = max(2.0, size * 0.022)
    dx = centre + plate_r * 0.72
    dy = centre - plate_r * 0.72
    draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=theme["accent"] + (255,))
    return canvas


def portrait(size: int) -> Image.Image:
    """Circular crop of the illustration that stands in for a photo."""
    image = Image.open(PORTRAIT).convert("RGB")
    side = min(image.size)
    image = image.crop(((image.width - side) // 2, (image.height - side) // 2, (image.width + side) // 2, (image.height + side) // 2))
    image = image.resize((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    canvas.paste(image, (0, 0), mask)
    return canvas


def app_icon(size: int, theme: dict) -> Image.Image:
    """Squircle icon. The accent dot only appears once there is room for it."""
    scale = 4
    big = size * scale
    canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    rounded(draw, [0, 0, big - 1, big - 1], int(big * 0.23), fill=theme["bg"] + (255,))
    face = typeface(TIGHT, int(big * 0.56), 800)
    write(draw, (big / 2, big * 0.68), "K", face, theme["text"], tracking=-big * 0.015, anchor="center")
    if size >= 128:
        dot_r = big * 0.019
        dx, dy = big * 0.795, big * 0.205
        draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=theme["accent"] + (255,))
    return canvas.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- social cards


def og_profile(theme: dict) -> Image.Image:
    W, H = 1200, 630
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    rings(canvas, W + 40, 250, [520, 400, 290, 190], theme["line"], 2)
    draw = ImageDraw.Draw(canvas)

    # monogram plate, top left
    canvas.alpha_composite(portrait(150), (72, 66))

    mono = typeface(MONO, 20, 500)
    write(draw, (250, 112), "NGGKHAIZ.JS.ORG", mono, theme["muted"], tracking=3)
    write(draw, (250, 148), "BẮC GIANG · VIỆT NAM", mono, theme["faint"], tracking=3)

    title = typeface(TIGHT, 92, 600)
    write(draw, (72, 350), "Nguyễn Gia Khải", title, theme["text"], tracking=-4)

    line = typeface(INTER, 32, 400)
    write(draw, (76, 410), "C · C++ · Zig · Python · web", line, theme["muted"], tracking=-0.4)

    rule_y = 470
    draw.line([72, rule_y, W - 72, rule_y], fill=theme["line"], width=1)

    small = typeface(MONO, 20, 400)
    write(draw, (76, 530), "nggkhaiz@proton.me", small, theme["text"], tracking=0.5)
    write(draw, (W - 76, 530), "Discord · mental.arc", small, theme["muted"], tracking=0.5, anchor="right")

    draw.ellipse([76, 566, 86, 576], fill=theme["accent"] + (255,))
    write(draw, (98, 578), "C, C++, Zig and Python — and the site around it", small, theme["faint"])
    return canvas.convert("RGB")


def og_labs(theme: dict) -> Image.Image:
    W, H = 1200, 630
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    rings(canvas, W + 90, 470, [560, 430, 310], theme["line"], 2)
    draw = ImageDraw.Draw(canvas)

    mono = typeface(MONO, 20, 500)
    write(draw, (76, 96), "MOLIK LABS · INDEPENDENT", mono, theme["accent"], tracking=4)

    title = typeface(TIGHT, 88, 600)
    write(draw, (72, 240), "Independent.", title, theme["text"], tracking=-4)
    write(draw, (72, 340), "Open by design.", title, theme["muted"], tracking=-4)

    body = typeface(INTER, 26, 400)
    write(draw, (76, 410), "Open source. No tracking. No ads. Built to do its job well.", body, theme["muted"], tracking=-0.3)

    draw.line([76, 470, W - 76, 470], fill=theme["line"], width=1)
    write(draw, (76, 530), "MOLIK LABS", mono, theme["text"], tracking=3)
    write(draw, (W - 76, 530), "github.com/MoLik-Labs", mono, theme["faint"], tracking=1, anchor="right")
    return canvas.convert("RGB")


def github_social(theme: dict) -> Image.Image:
    W, H = 1280, 640
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    rings(canvas, W - 120, 120, [430, 320, 230], theme["line"], 2)
    draw = ImageDraw.Draw(canvas)

    mono = typeface(MONO, 22, 500)
    write(draw, (80, 120), "GITHUB · @NGGKHAIZ", mono, theme["muted"], tracking=4)

    title = typeface(TIGHT, 104, 600)
    write(draw, (76, 300), "Ngg.Khaiz", title, theme["text"], tracking=-5)

    body = typeface(INTER, 34, 400)
    write(draw, (80, 360), "C · C++ · Zig · Python · hand-written web", body, theme["muted"], tracking=-0.4)

    draw.line([80, 430, W - 80, 430], fill=theme["line"], width=1)
    small = typeface(MONO, 22, 400)
    write(draw, (80, 500), "nggkhaiz.js.org", small, theme["text"], tracking=0.5)
    write(draw, (W - 80, 500), "nggkhaiz@proton.me", small, theme["faint"], tracking=0.5, anchor="right")
    return canvas.convert("RGB")


def x_header(theme: dict) -> Image.Image:
    W, H = 1500, 500
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    rings(canvas, W - 80, H + 60, [420, 320, 230, 150], theme["line"], 2)
    draw = ImageDraw.Draw(canvas)

    mono = typeface(MONO, 20, 500)
    write(draw, (72, 96), "NGGKHAIZ.JS.ORG", mono, theme["muted"], tracking=4)

    title = typeface(TIGHT, 76, 600)
    write(draw, (68, 250), "Nguyễn Gia Khải", title, theme["text"], tracking=-3.4)

    body = typeface(INTER, 26, 400)
    write(draw, (72, 300), "Builder · C, C++, Zig, Python · Bắc Giang, Việt Nam", body, theme["muted"], tracking=-0.3)
    return canvas.convert("RGB")


def discord_banner(theme: dict) -> Image.Image:
    W, H = 960, 540
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    rings(canvas, W / 2, H / 2, [300, 220, 150], theme["line"], 2)
    draw = ImageDraw.Draw(canvas)

    title = typeface(TIGHT, 84, 600)
    write(draw, (W / 2, 270), "Ngg.Khaiz", title, theme["text"], tracking=-4, anchor="center")

    mono = typeface(MONO, 20, 500)
    write(draw, (W / 2, 320), "C · C++ · ZIG · PYTHON · WEB", mono, theme["muted"], tracking=5, anchor="center")
    return canvas.convert("RGB")


# ---------------------------------------------------------------- project covers

PROJECTS = [
    {
        "slug": "zmrig",
        "repo": "MoLik-Labs / ZMRIG",
        "title": "ZMRIG",
        "sub": "RandomX miner, pool and proxy in one tree",
        "tags": ["C", "C++", "Zig"],
        "accent_lines": [1, 5],
        "glyph": "code",
    },
    {
        "slug": "qfox",
        "repo": "MoLik-Labs / Q-FOX-Algorithm",
        "title": "Q-FOX",
        "sub": "A 3x3 method laboratory, one C engine",
        "tags": ["JavaScript", "Python", "C"],
        "accent_lines": [2, 6],
        "glyph": "code",
    },
    {
        "slug": "study-site",
        "repo": "MoLik-Labs / STUDY-SITE",
        "title": "Study Focus Fox",
        "sub": "One HTML file to study everything",
        "tags": ["HTML", "JavaScript", "MIT"],
        "accent_lines": [0, 4],
        "glyph": "browser",
    },
    {
        "slug": "public-file",
        "repo": "NggKhaiz / PUBLIC_FILE",
        "title": "PUBLIC_FILE",
        "sub": "Obfuscation scanner and file tools",
        "tags": ["Python", "Apache-2.0"],
        "accent_lines": [3, 7],
        "glyph": "shell",
    },
    {
        "slug": "molik-winlik",
        "repo": "MoLik-Labs / MOLIK_WINLIK",
        "title": "MOLIK_WINLIK",
        "sub": "PowerShell build of Sophia Script",
        "tags": ["PowerShell", "Windows", "MIT"],
        "accent_lines": [2, 7],
        "glyph": "dashboard",
    },
    {
        "slug": "this-profile",
        "repo": "NggKhaiz / NggKhaiz",
        "title": "This profile",
        "sub": "README, SVG, raster and pages from data",
        "tags": ["Python", "SVG", "Pillow"],
        "accent_lines": [1, 6],
        "glyph": "code",
    },
]


def cover(project: dict, theme: dict) -> Image.Image:
    W, H = 1200, 675
    canvas = Image.new("RGBA", (W, H), theme["bg"] + (255,))
    draw = ImageDraw.Draw(canvas)

    # frame
    rounded(draw, [24, 24, W - 25, H - 25], 18, fill=theme["panel"] + (255,), outline=theme["line"], width=1)
    draw.line([24, 96, W - 25, 96], fill=theme["line"], width=1)

    mono = typeface(MONO, 18, 500)
    write(draw, (56, 70), project["repo"], mono, theme["faint"], tracking=1)
    write(draw, (W - 56, 70), "OPEN  ↗", mono, theme["muted"], tracking=2, anchor="right")

    # left: type
    title = typeface(TIGHT, 64, 600)
    title_text = project["title"]
    size = 64
    while span(title_text, title) > 500 and size > 34:
        size -= 2
        title = typeface(TIGHT, size, 600)
    write(draw, (56, 215), title_text, title, theme["text"], tracking=-2)

    body = typeface(INTER, 24, 400)
    write(draw, (58, 262), project["sub"], body, theme["muted"], tracking=-0.3)

    # tags
    x = 56
    tagfont = typeface(MONO, 16, 500)
    for tag in project["tags"]:
        w = span(tag, tagfont) + 28
        rounded(draw, [x, 310, x + w, 350], 20, fill=theme["panel2"] + (255,), outline=theme["line"], width=1)
        write(draw, (x + 14, 337), tag, tagfont, theme["text"])
        x += w + 10

    write(draw, (56, H - 62), "nggkhaiz.js.org", mono, theme["faint"], tracking=1)

    # right: abstract UI mock
    mx0, my0, mx1, my1 = 640, 140, W - 64, H - 96
    rounded(draw, [mx0, my0, mx1, my1], 14, fill=theme["panel2"] + (255,), outline=theme["line"], width=1)
    draw.line([mx0, my0 + 44, mx1, my0 + 44], fill=theme["line"], width=1)
    for i, colour in enumerate([theme["line"], theme["line"], theme["line"]]):
        cx = mx0 + 26 + i * 20
        draw.ellipse([cx - 5, my0 + 17, cx + 5, my0 + 27], fill=colour + (255,))

    # content rows
    row_y = my0 + 78
    widths = [0.62, 0.44, 0.72, 0.38, 0.56, 0.5, 0.68, 0.34]
    accent = {i for i in project["accent_lines"] if i < len(widths)}
    for i, ratio in enumerate(widths):
        bar_w = (mx1 - mx0 - 96) * ratio
        colour = theme["accent"] if i in accent else theme["line"]
        draw.rounded_rectangle([mx0 + 32, row_y, mx0 + 32 + bar_w, row_y + 10], radius=5, fill=colour + (255,))
        if ratio < 0.5:
            draw.rounded_rectangle(
                [mx0 + 44 + bar_w, row_y, mx0 + 44 + bar_w + 60, row_y + 10],
                radius=5,
                fill=theme["faint"] + (160,),
            )
        row_y += 34

    # glyph strip bottom right
    gx, gy = mx1 - 150, my1 - 74
    rounded(draw, [gx, gy, gx + 118, gy + 48], 10, fill=theme["panel"] + (255,), outline=theme["line"], width=1)
    code = typeface(MONO, 15, 500)
    write(draw, (gx + 14, gy + 30), "</>" if project["glyph"] == "code" else "> _", code, theme["muted"], tracking=1)

    return canvas.convert("RGB")


# ---------------------------------------------------------------- main


def main() -> int:
    icons = OUT / "icons"
    social = OUT / "social"
    covers = OUT / "covers"
    for folder in (icons, social, covers):
        folder.mkdir(parents=True, exist_ok=True)

    # icons
    master = app_icon(512, DARK)
    master.save(icons / "icon-512.png")
    master.resize((192, 192), Image.LANCZOS).save(icons / "icon-192.png")
    master.resize((180, 180), Image.LANCZOS).save(icons / "apple-touch-icon.png")
    master.resize((48, 48), Image.LANCZOS).save(icons / "favicon-48.png")
    master.resize((32, 32), Image.LANCZOS).save(icons / "favicon-32.png")
    master.resize((16, 16), Image.LANCZOS).save(icons / "favicon-16.png")
    master.resize((64, 64), Image.LANCZOS).save(icons / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    # social
    og_profile(DARK).save(social / "og-profile.png", optimize=True)
    og_profile(LIGHT).save(social / "og-profile-light.png", optimize=True)
    og_labs(DARK).save(social / "og-labs.png", optimize=True)
    github_social(DARK).save(social / "github-social.png", optimize=True)
    x_header(DARK).save(social / "x-header.png", optimize=True)
    discord_banner(DARK).save(social / "discord-banner.png", optimize=True)
    avatar = Image.new("RGBA", (512, 512), DARK["bg"] + (255,))
    avatar.alpha_composite(portrait(512))
    avatar.convert("RGB").save(social / "avatar.png", optimize=True)

    # 384 px square, used as the embedded avatar inside the README SVGs
    portrait(384).convert("RGB").save(social / "avatar-384.jpg", quality=90, optimize=True)

    # covers
    for project in PROJECTS:
        cover(project, DARK).save(covers / f"{project['slug']}.png", optimize=True)

    produced = sorted(p.relative_to(ROOT) for p in OUT.rglob("*.png")) + [Path("assets/img/icons/favicon.ico")]
    for path in produced:
        print(f"  {path}")
    print(f"{len(produced)} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
