#!/usr/bin/env python3
"""Fetch the three families the site uses and emit self-hosted woff2 subsets.

Sources are the official Google Fonts repository (SIL Open Font License 1.1):

    ofl/inter/Inter[opsz,wght].ttf
    ofl/intertight/InterTight[wght].ttf
    ofl/jetbrainsmono/JetBrainsMono[wght].ttf

Downloads land in .cache/fonts (git-ignored), the generated woff2 files and the
licences land in assets/fonts. Subsets cover Latin, Latin Extended and
Vietnamese, which is what the copy in this repository actually needs.

Requires: pip install fonttools brotli
Usage:   python3 tools/fetch_fonts.py [--force]
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "fonts"
OUT = ROOT / "assets" / "fonts"

FAMILIES = [
    ("Inter", "ofl/inter/Inter%5Bopsz,wght%5D.ttf", "inter-var.woff2"),
    ("InterTight", "ofl/intertight/InterTight%5Bwght%5D.ttf", "inter-tight-var.woff2"),
    ("JetBrainsMono", "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf", "jetbrains-mono-var.woff2"),
]

LICENSES = [
    ("OFL-inter.txt", "ofl/inter/OFL.txt"),
    ("OFL-intertight.txt", "ofl/intertight/OFL.txt"),
    ("OFL-jetbrainsmono.txt", "ofl/jetbrainsmono/OFL.txt"),
]

# Latin, Latin Extended, Vietnamese, punctuation, arrows, symbols used in the UI.
UNICODES = (
    "U+0000-024F,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
    "U+1E00-1EFF,U+2000-206F,U+20AB,U+20AC,U+2122,U+2190-21FF,"
    "U+2C60-2C7F,U+A720-A7FF,U+FEFF,U+FFFD"
)

API = "https://api.github.com/repos/google/fonts/contents/{path}?ref=main"


def fetch(path: str) -> bytes:
    request = urllib.request.Request(API.format(path=path), headers={"User-Agent": "build-profile"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.load(response)
    if "content" not in payload:
        raise RuntimeError(f"GitHub returned no inline content for {path} ({payload.get('size')} bytes)")
    return base64.b64decode(payload["content"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="re-download and re-subset everything")
    args = parser.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    for name, path, target in FAMILIES:
        ttf = CACHE / f"{name}.ttf"
        if args.force or not ttf.exists():
            ttf.write_bytes(fetch(path))
            print(f"downloaded {name} ({ttf.stat().st_size // 1024} KiB)")

        woff2 = OUT / target
        if args.force or not woff2.exists():
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "fontTools.subset",
                    str(ttf),
                    f"--unicodes={UNICODES}",
                    "--layout-features=*",
                    "--flavor=woff2",
                    f"--output-file={woff2}",
                ],
                check=True,
            )
            print(f"subset {target} ({woff2.stat().st_size // 1024} KiB)")

    for target, path in LICENSES:
        (OUT / target).write_bytes(fetch(path))
        print(f"licence {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
