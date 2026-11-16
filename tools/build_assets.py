#!/usr/bin/env python3
"""Generate the SVG assets used by the profile README.

The layout, type scale and colour tokens are taken from the reference profile
(Sakayorii/Sakayorii): a 1600x360 hero, 520x176 project cards and a
1160x190 highlights strip, each with a dark and a light variant so the README
can follow the reader's colour scheme through <picture>.

Content lives in CONTENT below. Run `python3 tools/build_assets.py` after
editing it; nothing else in the repository needs to change.

Avatar: the hero draws a monogram plate. To use a photo instead, base64-encode
a square JPEG/PNG and set AVATAR_DATA_URI to "data:image/jpeg;base64,...".
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"
SANS = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"

# Empty string = draw the monogram plate instead of a photo.
AVATAR_DATA_URI = ""

CONTENT = {
    "name": "Ngg.Khaiz",
    "tagline": "Turning weird ideas into things that actually run",
    # (icon, label, value) - rendered in the right half, 2x2 grid.
    "quadrants": [
        ("rocket", "Focus", "C++ & Python"),
        ("shield", "Mindset", "Break, then fix"),
        ("code", "Toolbox", "TS, Rust, Docker"),
        ("globe", "Based in", "Việt Nam"),
    ],
    "monogram": "K",
    "highlights_label": "GITHUB HIGHLIGHTS",
    "highlights": [
        ("464", "contributions"),
        ("12", "public repositories"),
        ("4", "stars, top repository"),
        ("6", "languages in public repos"),
    ],
    "projects": [
        {
            "slug": "public-file",
            "repo": "NggKhaiz/PUBLIC_FILE",
            "title": "PUBLIC_FILE",
            "desc": "Obfuscation scanner and file tools",
            "langs": ["Python"],
        },
        {
            "slug": "rhlz-panel",
            "repo": "NggKhaiz/RHLZ-PANEL",
            "title": "RHLZ Panel",
            "desc": "Self-hosted panel, Docker-ready",
            "langs": ["TypeScript", "Shell"],
        },
        {
            "slug": "nggkhaiz-site",
            "repo": "NggKhaiz/NggKhaiz",
            "title": "nggkhaiz.js.org",
            "desc": "Hand-written site, no framework",
            "langs": ["HTML", "CSS"],
        },
        {
            "slug": "this-profile",
            "repo": "NggKhaiz/NggKhaiz",
            "title": "This profile",
            "desc": "README, SVG assets, build script",
            "langs": ["Python", "SVG"],
        },
    ],
}

THEMES = {
    "dark": {
        "hero_bg": "#131313",
        "hero_ring_far": "#1e1e1e",
        "hero_ring_near": "#262626",
        "hero_stroke": "#262626",
        "hero_plate": "#ffffff",
        "hero_mono_bg": "#1c1c1c",
        "hero_mono_fg": "#f5f5f5",
        "hero_title": "#f5f5f5",
        "hero_muted": "#a3a3a3",
        "hero_icon": "#f5f5f5",
        "card_bg": "#0d1117",
        "card_stroke": "#30363d",
        "card_label": "#8b949e",
        "card_link": "#dde6f0",
        "card_title": "#f0f6fc",
        "card_desc": "#8b949e",
        "pill_bg": "#161b22",
        "pill_text": "#f0f6fc",
    },
    "light": {
        "hero_bg": "#fafafa",
        "hero_ring_far": "#efefef",
        "hero_ring_near": "#e7e7e7",
        "hero_stroke": "#e7e7e7",
        "hero_plate": "#ffffff",
        "hero_mono_bg": "#111111",
        "hero_mono_fg": "#fafafa",
        "hero_title": "#111111",
        "hero_muted": "#737373",
        "hero_icon": "#111111",
        "card_bg": "#ffffff",
        "card_stroke": "#d0d7de",
        "card_label": "#656d76",
        "card_link": "#57606a",
        "card_title": "#1f2328",
        "card_desc": "#656d76",
        "pill_bg": "#f6f8fa",
        "pill_text": "#1f2328",
    },
}

# Lucide icon paths, 24x24 grid, stroke-based.
ICONS = {
    "rocket": [
        "M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z",
        "m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z",
        "M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0",
        "M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5",
    ],
    "shield": [
        "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z",
        "m9 12 2 2 4-4",
    ],
    "code": ["m16 18 6-6-6-6", "m8 6-6 6 6 6"],
    "globe": [
        "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z",
        "M2 12h20",
        "M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z",
    ],
}

PILL_PAD = 27.6
PILL_CHAR = 6.6
PILL_GAP = 8


def hero(theme: dict) -> str:
    t = theme
    quadrants = []
    positions = [(965, 78), (1260, 78), (965, 218), (1260, 218)]
    for (icon, label, value), (x, y) in zip(CONTENT["quadrants"], positions):
        paths = "".join(f'<path d="{d}"/>' for d in ICONS[icon])
        quadrants.append(
            f'  <g transform="translate({x},{y})">\n'
            f'    <g transform="scale(1.9)" fill="none" stroke="{t["hero_icon"]}" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{paths}</g>\n'
            f'    <text x="60" y="10" font-size="20" font-family="{SANS}" '
            f'fill="{t["hero_muted"]}">{escape(label)}</text>\n'
            f'    <text x="60" y="44" font-size="27" font-weight="700" font-family="{SANS}" '
            f'fill="{t["hero_title"]}">{escape(value)}</text>\n'
            f'  </g>\n'
        )

    if AVATAR_DATA_URI:
        avatar = (
            '  <circle cx="172" cy="180" r="97" fill="' + t["hero_plate"] + '"/>\n'
            '  <image x="78" y="86" width="188" height="188" clip-path="url(#avatarClip)" '
            f'xlink:href="{AVATAR_DATA_URI}"/>\n'
        )
    else:
        avatar = (
            f'  <circle cx="172" cy="180" r="97" fill="{t["hero_plate"]}"/>\n'
            f'  <circle cx="172" cy="180" r="88" fill="{t["hero_mono_bg"]}"/>\n'
            f'  <text x="172" y="212" text-anchor="middle" font-size="86" font-weight="800" '
            f'letter-spacing="-3" font-family="{SANS}" fill="{t["hero_mono_fg"]}">'
            f'{escape(CONTENT["monogram"])}</text>\n'
        )

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="1600" height="360" viewBox="0 0 1600 360" role="img" '
        f'aria-label="{escape(CONTENT["name"])} - {escape(CONTENT["tagline"])}">\n'
        "  <defs>\n"
        '    <clipPath id="avatarClip"><circle cx="172" cy="180" r="94"/></clipPath>\n'
        "  </defs>\n"
        f'  <rect width="1600" height="360" fill="{t["hero_bg"]}"/>\n'
        f'  <circle cx="90" cy="185" r="235" fill="{t["hero_ring_far"]}"/>\n'
        f'  <circle cx="172" cy="180" r="150" fill="{t["hero_ring_near"]}" opacity=".55"/>\n'
        f'  <g fill="none" stroke="{t["hero_stroke"]}" stroke-width="34" opacity=".8">\n'
        '    <circle cx="1680" cy="180" r="215"/>\n'
        '    <circle cx="1680" cy="180" r="330"/>\n'
        '    <circle cx="1680" cy="180" r="445"/>\n'
        "  </g>\n"
        + avatar
        + f'  <text x="305" y="198" font-size="96" font-weight="800" letter-spacing="-2" '
        f'font-family="{SANS}" fill="{t["hero_title"]}">{escape(CONTENT["name"])}</text>\n'
        f'  <text x="310" y="256" font-size="29" font-weight="300" font-family="{SANS}" '
        f'fill="{t["hero_muted"]}">{escape(CONTENT["tagline"])}</text>\n'
        "\n" + "".join(quadrants) + "</svg>\n"
    )


def highlights(theme: dict) -> str:
    t = theme
    cells = []
    for i, (value, label) in enumerate(CONTENT["highlights"]):
        x = 28 + i * 285
        cells.append(
            f'  <text x="{x}" y="90" font-size="30" font-weight="700" font-family="{SANS}" '
            f'fill="{t["card_title"]}">{escape(value)}</text>\n'
            f'  <text x="{x}" y="118" font-size="13" font-family="{SANS}" '
            f'fill="{t["card_label"]}">{escape(label)}</text>\n'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="190" '
        'viewBox="0 0 1160 190" role="img" aria-label="GitHub highlights">\n'
        f'  <rect x="1" y="1" width="1158" height="188" rx="14" fill="{t["card_bg"]}" '
        f'stroke="{t["card_stroke"]}"/>\n'
        f'  <text x="28" y="34" font-size="12" font-family="{MONO}" '
        f'fill="{t["card_label"]}">{escape(CONTENT["highlights_label"])}</text>\n\n'
        + "".join(cells)
        + "</svg>\n"
    )


def project_card(project: dict, theme: dict) -> str:
    t = theme
    pills = []
    x = 28.0
    for lang in project["langs"]:
        w = PILL_PAD + PILL_CHAR * len(lang)
        pills.append(
            f'<rect x="{x}" y="126" rx="7" ry="7" width="{w}" height="26" '
            f'fill="{t["pill_bg"]}" stroke="{t["card_stroke"]}"/>'
            f'<text x="{x + 12}" y="144" font-size="12" font-family="{MONO}" '
            f'fill="{t["pill_text"]}">{escape(lang)}</text>'
        )
        x += w + PILL_GAP
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="520" height="176" '
        'viewBox="0 0 520 176" role="img" '
        f'aria-label="{escape(project["title"])}">\n'
        f'  <rect x="1" y="1" width="518" height="174" rx="14" fill="{t["card_bg"]}" '
        f'stroke="{t["card_stroke"]}"/>\n'
        f'  <text x="28" y="34" font-size="12" font-family="{MONO}" '
        f'fill="{t["card_label"]}">{escape(project["repo"])}</text>\n'
        f'  <text x="492" y="34" text-anchor="end" font-size="13" font-family="{MONO}" '
        f'fill="{t["card_link"]}">open ↗</text>\n'
        f'  <text x="28" y="72" font-size="22" font-weight="700" font-family="{SANS}" '
        f'fill="{t["card_title"]}">{escape(project["title"])}</text>\n'
        f'  <text x="28" y="101" font-size="14" font-family="{SANS}" '
        f'fill="{t["card_desc"]}">{escape(project["desc"])}</text>\n'
        f'  {"".join(pills)}\n'
        "</svg>\n"
    )


def main() -> None:
    (ASSETS / "projects").mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"hero-{name}.svg").write_text(hero(theme), encoding="utf-8")
        (ASSETS / f"highlights-{name}.svg").write_text(highlights(theme), encoding="utf-8")
        for project in CONTENT["projects"]:
            out = ASSETS / "projects" / f"{project['slug']}-{name}.svg"
            out.write_text(project_card(project, theme), encoding="utf-8")
    print("wrote assets:", len(list(ASSETS.rglob("*.svg"))), "svg files")


if __name__ == "__main__":
    main()
