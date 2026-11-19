#!/usr/bin/env python3
"""Render README.md from data/profile.json.

The numbers in the profile (contributions, repositories, stars, per-project
commit counts) are the GitHub API's, refreshed by `tools/fetch_stats.py` and a
scheduled workflow. Nothing here is typed by hand except the prose, so the
profile cannot go stale.

Usage:  python3 tools/build_readme.py [--check]
        --check exits 1 when README.md differs from a fresh render (CI guard).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from palette import LATTE, MOCHA  # noqa: E402  (single source of truth)
DATA = ROOT / "data" / "profile.json"
README = ROOT / "README.md"

RAW = "https://raw.githubusercontent.com/NggKhaiz/NggKhaiz/main/assets"
SITE = "https://nggkhaiz.js.org"
LABS = f"{SITE}/labs/"
MAIL = "nggkhaiz@proton.me"

# shields.io and the summary-card API both take bare hex, no `#`.
BASE = MOCHA["base"].lstrip("#")
MANTLE = MOCHA["mantle"].lstrip("#")
MAUVE = MOCHA["mauve"].lstrip("#")
PEACH = MOCHA["peach"].lstrip("#")
TEXT = MOCHA["text"].lstrip("#")

# Headline projects: repository -> (slug of the card in assets/projects, what it is).
CARDS = [
    ("MoLik-Labs/ZMRIG", "zmrig", "RandomX miner, pool and proxy"),
    ("MoLik-Labs/MOLIK_WINLIK", "molik-winlik", "PowerShell build of Sophia Script"),
    ("MoLik-Labs/Q-FOX-Algorithm", "qfox", "3×3 method laboratory"),
    ("MoLik-Labs/STUDY-SITE", "study-site", "Single-file study app"),
]

# Repositories that carry someone else's history: named, never counted as work.
FORKS_NOTE = (
    "Forks are visible on the account and excluded from every total below — "
    "their commits are upstream's, not mine."
)


def badge(alt: str, href: str, label: str, message: str, logo: str, accent: str = MAUVE) -> str:
    """flat-square chip: mauve label, Mocha value — readable on either theme."""
    return (
        f'  <a href="{href}"><img alt="{alt}" '
        f'src="https://img.shields.io/badge/{label}-{message}-{BASE}?style=flat-square'
        f"&labelColor={accent}&color={BASE}&logo={logo}&logoColor={TEXT}\" /></a>"
    )


def picture(name: str, alt: str, width: str = "100%") -> str:
    return f'''  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{RAW}/{name}-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="{RAW}/{name}-light.svg">
    <img width="{width}" alt="{alt}" src="{RAW}/{name}-dark.svg">
  </picture>'''


def summary_card() -> str:
    """Live card pair: the service takes explicit hex, so it is our palette too."""
    base = "https://github-profile-summary-cards.vercel.app/api/cards/profile-details"

    def url(palette: dict[str, str]) -> str:
        colors = dict(
            bg_color=palette["base"],
            title_color=palette["mauve"],
            text_color=palette["subtext0"],
            icon_color=palette["mauve"],
            chart_color=palette["peach"],
            border_color=palette["surface1"],
        )
        query = "&".join(f"{key}={value.lstrip('#')}" for key, value in colors.items())
        return f"{base}?username=NggKhaiz&hide_border=false&utcOffset=7&{query}"

    dark, light = url(MOCHA), url(LATTE)
    return f'''  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{dark}">
    <source media="(prefers-color-scheme: light)" srcset="{light}">
    <img width="62%" alt="NggKhaiz — commits, pull requests, issues and stars, live from the GitHub API" src="{dark}">
  </picture>'''


def repo_by_name(data: dict) -> dict[str, dict]:
    return {repo["repo"]: repo for repo in data["repos"]}


def render(data: dict) -> str:
    user = data["user"]
    repos = repo_by_name(data)
    languages = ", ".join(item["name"] for item in data["languages"][:6])

    cards = []
    for repo_name, slug, pitch in CARDS:
        repo = repos.get(repo_name, {})
        cards.append(
            f'''<a href="https://github.com/{repo_name}">
{picture(f"projects/{slug}", pitch, "49%")}
</a>'''
        )
    card_grid = "\n".join(cards)

    source = [repo for repo in data["repos"] if not repo["fork"]]
    source.sort(key=lambda repo: repo["commits"], reverse=True)
    minor = [repo for repo in source if repo["repo"] not in {name for name, _, _ in CARDS}]

    def line(repo: dict) -> str:
        stars = f" · {repo['stars']}★" if repo["stars"] else ""
        language = f" · {repo['language']}" if repo["language"] else ""
        commits = f"{repo['commits']:,} " + ("commit" if repo["commits"] == 1 else "commits")
        return f"- [`{repo['repo']}`](https://github.com/{repo['repo']}) — {commits}{language}{stars}"

    minor_list = "\n".join(line(repo) for repo in minor[:6])

    commits_total = f"{user['source_commits']:,}"
    contributions = f"{user['contributions']:,}"
    repos_total = user["public_repos"] + user["org_repos"]

    return f'''<div align="center">

{picture("hero", "Ngg.Khaiz — C, C++, Zig and Python, and the site around it")}

<p>
{badge("nggkhaiz.js.org", SITE, "site", "nggkhaiz.js.org", "githubpages")}
{badge("MoLik Labs", LABS, "lab", "MoLik_Labs", "github", PEACH)}
{badge(MAIL, f"mailto:{MAIL}", "mail", "nggkhaiz%40proton.me", "protonmail")}
</p>

</div>

### `$ whoami`

```console
nggkhaiz        Nguyễn Gia Khải · he/him · Bắc Giang, Việt Nam
role            independent developer, one maintainer, no roadmap
writes          C · C++ · Zig for the core, Python for the tooling,
                hand-written HTML/CSS/JS for what people actually touch
criteria        read the source, then the changelog
contact         {MAIL} · Discord mental.arc
sites           {SITE} · lab: {LABS}
```

I build tools that stay small enough to read: a RandomX miner, a 3×3 cube
laboratory, a study app that fits in one HTML file. I would rather ship a small
honest tool than a large empty one, and every number on this profile and on my
site can be checked against the GitHub API — the figures below are fetched, not
typed.

### `$ ls ~/projects`

<div align="center">

{card_grid}

</div>

Everything else that is mine:

{minor_list}

{FORKS_NOTE}

### `$ cat ~/stack`

| layer | contents |
| :-- | :-- |
| **systems** | C · C++ · Zig · assembly when the compiler stops helping |
| **scripting** | Python · PowerShell · Bash |
| **web** | TypeScript · JavaScript · hand-written HTML and CSS, no framework |
| **data** | SQLite · JSON · plain text files that survive a reinstall |
| **shipping** | git · CMake · Docker · GitHub Actions · GitHub Pages |
| **in the trees** | {languages} |

<sub>Language mix is measured in bytes across my own repositories only.</sub>

### `$ gh api graphql --jq .data.user`

<div align="center">

{picture("highlights", "GitHub numbers: contributions, public repositories, stars, largest repository")}

{summary_card()}

</div>

{contributions} contributions in the last year, {commits_total} commits in
repositories I own outright, {repos_total} of them public across two accounts.
The strip is drawn by `tools/build_assets.py` from `data/profile.json`; the card
is served live by github-profile-summary-cards with the same hex values. Both
read the GitHub API, so neither can drift.

### `$ tree ~/molik-labs`

The larger work lives in [MoLik-Labs](https://github.com/MoLik-Labs), kept
separate so each repository carries its own documentation, releases and licence:

- **[ZMRIG](https://github.com/MoLik-Labs/ZMRIG)** — RandomX miner, pool and proxy · C / C++ / Zig · GPL-3.0
- **[MOLIK_WINLIK](https://github.com/MoLik-Labs/MOLIK_WINLIK)** — PowerShell build of [Sophia Script](https://github.com/farag2/Sophia-Script-for-Windows) for Windows 10/11 · MIT, upstream credited
- **[Q-FOX](https://github.com/MoLik-Labs/Q-FOX-Algorithm)** — 3×3 method laboratory, one C translation unit · C / Python / JS
- **[Study Focus Fox](https://github.com/MoLik-Labs/STUDY-SITE)** — single-file study app · HTML / JS · MIT

Personal, non-commercial, one maintainer: [{LABS.replace("https://", "")}]({LABS}).

### `$ cat Makefile`

This profile and [{SITE.replace("https://", "")}]({SITE}) are one static site,
generated end to end — the HTML, the SVG cards and every raster image come out
of `tools/`, so nothing under `assets/` is hand-edited.

```bash
python3 tools/fetch_stats.py    # data/profile.json from the GitHub GraphQL API
python3 tools/build_readme.py   # this file
python3 tools/build_assets.py   # hero + project SVGs (Catppuccin Mocha / Latte)
python3 tools/build_images.py   # raster images              (needs pillow)
python3 tools/build_pages.py    # 15 HTML pages, sitemap, manifest, robots
```

Deploying is "upload the repository root": GitHub Pages serves it from `CNAME`,
there is no runtime build and no framework in the bundle. Page map:
[`docs/site-map.md`](docs/site-map.md) · where the numbers come from:
[`docs/data.md`](docs/data.md) · what came from the references and what did not:
[`docs/clone-notes.md`](docs/clone-notes.md) · the contribution graph:
[`docs/graph-art.md`](docs/graph-art.md).

MIT for the code ([`LICENSE`](LICENSE)); the name, portrait and write-ups stay
mine, and each project keeps its own licence.

---

<div align="center">
  <sub>README, cards and site are regenerated by a scheduled workflow — the
  numbers come from the GitHub API and the palette from
  <a href="https://github.com/NggKhaiz/NggKhaiz/blob/main/tools/palette.py">tools/palette.py</a>.</sub>
  <br />
  <sub>The contribution grid is painted by <a href="https://github.com/NggKhaiz/NggKhaiz/blob/main/tools/graph_art.py">tools/graph_art.py</a>
  from a 53×7 text file and a scheduled workflow — nothing hidden, see
  <a href="https://github.com/NggKhaiz/NggKhaiz/blob/main/docs/graph-art.md">docs/graph-art.md</a>.</sub>
  <br />
  <sub>sometimes C++, sometimes Zig, sometimes whatever gets the idea working</sub>
</div>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    output = render(data)

    if args.check:
        current = README.read_text(encoding="utf-8") if README.exists() else ""
        if current != output:
            print("README.md is out of date — run python3 tools/build_readme.py")
            sys.exit(1)
        print("README.md is up to date")
        return

    README.write_text(output, encoding="utf-8")
    print(f"wrote README.md  ({output.count(chr(10))} lines, {len(output):,} bytes)")


if __name__ == "__main__":
    main()
