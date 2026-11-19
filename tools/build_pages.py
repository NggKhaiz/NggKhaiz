#!/usr/bin/env python3
"""Render the static site from a single source of truth.

Everything published is a plain file: HTML, one stylesheet, one behaviour script,
one copy dictionary. No runtime framework, no client-side router — upload the
repository root to any host and it works.

Outputs
  index.html                      profile home
  work/index.html                 project index
  work/<slug>.html                project detail            (4)
  labs/index.html                 MoLik Labs home
  labs/work/index.html            MoLik Labs project index   (3)
  labs/work/<slug>.html           MoLik Labs project detail  (3)
  studio/index.html               redirect to /labs/
  404.html
  assets/copy.js                  VI/EN strings used by assets/site.js
  sitemap.xml

Usage: python3 tools/build_pages.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://nggkhaiz.js.org"
EMAIL = "nggkhaiz@proton.me"
DISCORD = "mental.arc"
GITHUB = "https://github.com/NggKhaiz"

YEAR = 2026

# ------------------------------------------------------------ github numbers
#
# data/profile.json is written by tools/fetch_stats.py from the GitHub GraphQL
# API and refreshed by .github/workflows/profile-data.yml. Every figure quoted on
# the site is read from here, so no page can drift away from the API.

DATA_FILE = ROOT / "data" / "profile.json"
try:
    DATA = json.loads(DATA_FILE.read_text(encoding="utf-8"))
except (OSError, ValueError):  # first run, before fetch_stats.py
    DATA = {"user": {}, "repos": [], "languages": []}

REPOS = {repo["repo"]: repo for repo in DATA.get("repos", [])}
ORG = DATA.get("user", {}).get("org", "MoLik-Labs")


def repo_commits(name: str) -> int:
    return int(REPOS.get(name, {}).get("commits", 0))


def repo_stars(name: str) -> int:
    return int(REPOS.get(name, {}).get("stars", 0))


def fmt(number: int, lang: str = "en") -> str:
    """4,580 in English, 4.580 in Vietnamese."""
    text = f"{int(number):,}"
    return text.replace(",", ".") if lang == "vi" else text


def stars(number: int) -> str:
    return f"{int(number)} ★"


# ---------------------------------------------------------------- projects


PROJECTS = [
    {
        "slug": "zmrig",
        "repo": "MoLik-Labs/ZMRIG",
        "url": f"{GITHUB}/../MoLik-Labs/ZMRIG",
        "live": "https://molik-labs.github.io/ZMRIG/",
        "title": "ZMRIG",
        "stack": ["C", "C++", "Zig", "Web"],
        "cover": "assets/img/covers/zmrig.png",
        "status": {"vi": "Đang phát hành", "en": "Shipping"},
        "tagline": {
            "vi": "Miner RandomX cho Monero — dev fee 3% hiện rõ và tắt được.",
            "en": "A RandomX miner for Monero — a 3% dev fee you can see and switch off.",
        },
        "intro": {
            "vi": "Một cây repo gồm miner RandomX, pool trả cho nó, proxy cho cả farm và site tài liệu. Engine bằng C/C++, phần cần tốc độ viết bằng Zig, phần web bằng HTML/JS. Bản hiện tại 6.48.0.",
            "en": "One tree holding a RandomX miner, the pool that pays it, a proxy for a whole farm and the site that documents it. Engine in C/C++, Zig where it earns its place, HTML/JS for the site. Current release 6.48.0.",
        },
        "why": {
            "vi": "Mình muốn phần phí dev phải nhìn thấy và tắt được, thay vì nằm trong chỗ không ai đọc tới.",
            "en": "I wanted the developer fee to be something you can see and switch off, not something buried where nobody looks.",
        },
        "how": {
            "vi": f"Linux x86-64, macOS, Windows. GPL-3.0. {fmt(repo_commits('MoLik-Labs/ZMRIG'), 'vi')} commit và {repo_stars('MoLik-Labs/ZMRIG')} sao — repo nhiều hoạt động nhất trong cả hai tài khoản.",
            "en": f"Linux x86-64, macOS and Windows. GPL-3.0. {fmt(repo_commits('MoLik-Labs/ZMRIG'), 'en')} commits and {repo_stars('MoLik-Labs/ZMRIG')} stars — the most active repository across both accounts.",
        },
        "facts": [
            ("fact.lang", "C · C++ · Zig"),
            ("fact.commits", "n.zmrig.commits"),
            ("fact.stars", "n.zmrig.stars"),
            ("fact.release", "6.48.0"),
            ("fact.license", "GPL-3.0"),
        ],
        "studio": {
            "tag": "A miner, nothing hidden",
            "summary": "A RandomX miner with a developer fee you can see and switch off, the pool that pays for it, a proxy for the whole farm, and the site that puts it together.",
            "ship": "Source and release builds. GPL-3.0, with the fee documented in doc/FEE.md instead of buried in code.",
        },
    },
    {
        "slug": "qfox",
        "repo": "MoLik-Labs/Q-FOX-Algorithm",
        "url": f"{GITHUB}/../MoLik-Labs/Q-FOX-Algorithm",
        "live": None,
        "title": "Q-FOX",
        "stack": ["C", "Python", "JavaScript"],
        "cover": "assets/img/covers/qfox.png",
        "status": {"vi": "Đang dựng", "en": "In progress"},
        "tagline": {
            "vi": "Phòng thí nghiệm 3×3: một engine C, 13 phương pháp đo trên cùng scramble.",
            "en": "A 3×3 laboratory: one C engine, 13 methods measured on the same scrambles.",
        },
        "intro": {
            "vi": "Một translation unit: facelets, 54 move, BFS + IDA*, và sổ tra toàn bộ vị trí last-layer. Python binding ở trên, 13 phương pháp chạy benchmark, site tĩnh sinh ra từ chính dữ liệu engine tạo.",
            "en": "One translation unit: facelets, 54 moves, BFS + IDA*, and a book of every reachable last-layer position. A Python binding on top, 13 solving methods benchmarked, and a static site generated from the engine's own data.",
        },
        "why": {
            "vi": "Để con số trên site không thể sai: algorithm lấy từ engine, bảng lấy từ benchmark, cả hai được replay qua code C trước khi ship.",
            "en": "So the numbers on the site cannot lie: the algorithms come from the engine, the tables from the benchmark, and both are replayed against the C code before they ship.",
        },
        "how": {
            "vi": "Site và test đều sinh bằng script — không có gì phải viết tay hai lần.",
            "en": "Site and tests are generated by scripts — nothing is written twice.",
        },
        "facts": [
            ("fact.lang", "C · Python · JS"),
            ("fact.commits", "n.qfox.commits"),
            ("fact.stars", "n.qfox.stars"),
            ("fact.license", "fact.none"),
        ],
        "studio": {
            "tag": "A method laboratory",
            "summary": "A 3×3 cube laboratory: a C engine with BFS and IDA*, a Python binding, thirteen methods measured against each other on the same scrambles, and a site whose tables are generated from the benchmark.",
            "ship": "Static site plus the C engine and Python package. Every published number is replayed against the engine before release.",
        },
    },
    {
        "slug": "study-site",
        "repo": "MoLik-Labs/STUDY-SITE",
        "url": f"{GITHUB}/../MoLik-Labs/STUDY-SITE",
        "live": None,
        "title": "Study Focus Fox",
        "stack": ["HTML", "JavaScript", "MIT"],
        "cover": "assets/img/covers/study-site.png",
        "status": {"vi": "Đang dùng", "en": "In use"},
        "tagline": {
            "vi": "Study Focus Fox — một file HTML để học Vật lí 9 và mọi môn.",
            "en": "Study Focus Fox — one HTML file to study Physics 9 and everything else.",
        },
        "intro": {
            "vi": "Lộ trình 52 ca Vật lí 9 và luyện chuyên Lý, thẻ ghi nhớ lặp lại cách quãng, sổ điểm, kế hoạch tuần, đấu trường pixel và góc công cụ Vật lí. Chạy offline, dữ liệu nằm trong máy bạn.",
            "en": "A 52-session Physics 9 track with olympiad practice, spaced-repetition cards, a grade book, weekly plans, a pixel arena and a physics toolbox. Runs offline; the data stays on your device.",
        },
        "why": {
            "vi": "Học trên web thường bị xao nhãng. Một file HTML chạy offline, không tài khoản, không tracking — mở ra là dùng.",
            "en": "Studying in a browser usually means distractions. One HTML file that runs offline, with no account and no tracking — open it and work.",
        },
        "how": {
            "vi": "Một tệp HTML cộng JS/CSS, mở thẳng bằng trình duyệt. MIT, nên bạn có thể sửa cho môn của mình.",
            "en": "A single HTML file plus JS/CSS, opened straight from disk. MIT, so you can rewrite it for your own subject.",
        },
        "facts": [
            ("fact.lang", "HTML · JS"),
            ("fact.commits", "n.study-site.commits"),
            ("fact.stars", "n.study-site.stars"),
            ("fact.license", "MIT"),
        ],
        "studio": {
            "tag": "A study tool, offline",
            "summary": "A single-file study environment: a 52-session Physics 9 track, spaced repetition, grade book, weekly plans and a pixel arena. Offline by default, because studying should not need an account.",
            "ship": "One HTML file. Open it, no install, no login, nothing leaves the device.",
        },
    },
    {
        "slug": "public-file",
        "repo": "NggKhaiz/PUBLIC_FILE",
        "url": f"{GITHUB}/PUBLIC_FILE",
        "live": None,
        "title": "PUBLIC_FILE",
        "stack": ["Python", "Security"],
        "cover": "assets/img/covers/public-file.png",
        "status": {"vi": "Đang dùng được", "en": "Usable"},
        "tagline": {
            "vi": "Trình quét code bị làm rối và vài công cụ file đi kèm.",
            "en": "An obfuscation scanner and a few file tools beside it.",
        },
        "intro": {
            "vi": "Mình muốn biết code bị làm rối đang giấu gì, nên viết luôn công cụ đi tìm. Repo gồm `obf-scanner.py`, một thư mục `ravenst`, `kill.txt` và LICENSE.",
            "en": "I wanted to know what obfuscated code is hiding, so I wrote the thing that looks. The repo holds `obf-scanner.py`, a `ravenst` folder, `kill.txt` and a LICENSE.",
        },
        "why": {
            "vi": "Đọc code lạ là cách nhanh nhất để hiểu một hệ thống. Viết scanner buộc mình phải hiểu từng kiểu làm rối thay vì đoán.",
            "en": "Reading unfamiliar code is the fastest way to understand a system. Writing the scanner forced me to understand each obfuscation trick instead of guessing.",
        },
        "how": {
            "vi": f"Một script Python chạy bằng CLI, không cần service. Apache-2.0, {repo_stars('NggKhaiz/PUBLIC_FILE')} sao.",
            "en": f"A Python script you run from a terminal — no service to host. Apache-2.0, {repo_stars('NggKhaiz/PUBLIC_FILE')} stars.",
        },
        "facts": [
            ("fact.lang", "Python"),
            ("fact.commits", "n.public-file.commits"),
            ("fact.stars", "n.public-file.stars"),
            ("fact.license", "Apache-2.0"),
        ],
        "studio": {
            "tag": "A tool, just a tool",
            "summary": "An obfuscation scanner and a public file shelf. Written because obfuscated code is a legitimate puzzle, and the tool that answers a question should be readable itself.",
            "ship": "Ships as a Python script. No daemon, no telemetry, no account.",
        },
    },
    {
        "slug": "molik-winlik",
        "repo": "MoLik-Labs/MOLIK_WINLIK",
        "url": f"{GITHUB}/../MoLik-Labs/MOLIK_WINLIK",
        "live": None,
        "title": "MOLIK_WINLIK",
        "stack": ["PowerShell", "Windows"],
        "cover": "assets/img/covers/molik-winlik.png",
        "status": {"vi": "Bản dựng upstream", "en": "Upstream build"},
        "tagline": {
            "vi": "Bản PowerShell để tinh chỉnh Windows — dựa trên Sophia Script.",
            "en": "A PowerShell build for tuning Windows — based on Sophia Script.",
        },
        "intro": {
            "vi": "Module PowerShell để tinh chỉnh Windows 10/11, kèm launcher batch. Đây là bản dựng lại của Sophia Script (farag2) theo MIT, giữ nguyên license và attribution của upstream.",
            "en": "A PowerShell module for tuning Windows 10 and 11, with a batch launcher. This is a build of Sophia Script by farag2 under MIT, keeping the upstream licence and attribution.",
        },
        "why": {
            "vi": "Mình dùng nó hằng ngày và cần một bản để sửa theo ý mình, không phải chờ upstream.",
            "en": "I use it daily and needed a copy I can adjust without waiting on upstream.",
        },
        "how": {
            "vi": f"PowerShell module cộng batch, chạy trên Windows 10/11. {fmt(repo_commits('MoLik-Labs/MOLIK_WINLIK'), 'vi')} commit trong bản dựng này, phần lớn lịch sử đến từ upstream.",
            "en": f"A PowerShell module plus batch files for Windows 10/11. {fmt(repo_commits('MoLik-Labs/MOLIK_WINLIK'), 'en')} commits in this build, most of that history inherited from upstream.",
        },
        "facts": [
            ("fact.lang", "PowerShell"),
            ("fact.commits", "n.molik-winlik.commits"),
            ("fact.stars", "n.molik-winlik.stars"),
            ("fact.license", "MIT"),
        ],
        "note": {
            "vi": "Dựa trên Sophia Script for Windows của farag2 (MIT). Không phải toàn bộ code trong repo là của mình.",
            "en": "Based on Sophia Script for Windows by farag2 (MIT). Not all of the code in this repository is mine.",
        },
        "studio": {
            "tag": "A build, credited",
            "summary": "A maintained PowerShell build of Sophia Script for tuning Windows 10 and 11, with the upstream licence and attribution kept intact.",
            "ship": "PowerShell module plus a batch launcher. MIT, inherited from upstream, with attribution kept in the README.",
        },
    },
    {
        "slug": "this-profile",
        "repo": "NggKhaiz/NggKhaiz",
        "url": f"{GITHUB}/NggKhaiz",
        "live": ORIGIN,
        "title": "This profile",
        "stack": ["Python", "SVG", "Pillow"],
        "cover": "assets/img/covers/this-profile.png",
        "status": {"vi": "Sinh tự động", "en": "Generated"},
        "tagline": {
            "vi": "README, ảnh SVG và toàn bộ trang này — sinh ra từ dữ liệu.",
            "en": "The README, the SVG images and these pages — all generated from data.",
        },
        "intro": {
            "vi": "Hero, card dự án, highlights và 20 ảnh raster đều do script sinh; các trang HTML cũng vậy. Sửa số liệu một chỗ, chạy lại, mọi thứ khớp nhau.",
            "en": "The hero, project cards, highlights and 20 raster images come from scripts; so do the HTML pages. Change one number, rerun, and everything stays consistent.",
        },
        "why": {
            "vi": "Profile nói về việc viết code thì bản thân nó cũng nên được làm bằng code, không phải chỉnh tay từng ảnh.",
            "en": "A profile about writing code should itself be built by code, not by hand-editing images.",
        },
        "how": {
            "vi": "Bốn script Python: SVG cho README, ảnh raster bằng Pillow, trang HTML từ dữ liệu, và font subset. Output là file tĩnh, không build lúc chạy.",
            "en": "Four Python scripts: SVG for the README, raster images with Pillow, HTML pages from data, and font subsets. Output is static; nothing builds at request time.",
        },
        "facts": [
            ("fact.lang", "Python"),
            ("fact.output", "15 pages · 20 images"),
            ("fact.fonts", "fact.selfhost"),
            ("fact.build", "fact.manual"),
        ],
        "studio": {
            "tag": "A profile, generated",
            "summary": "The README and every image behind it, produced from data so the two colour schemes stay in sync. The same source renders these pages.",
            "ship": "Static output committed to the repository. Regenerate with one command.",
        },
    },
]

SELECTED_SLUGS = ["zmrig", "qfox", "study-site", "public-file"]
LABS_SLUGS = ["zmrig", "qfox", "study-site"]

PROJECT_BY_SLUG = {p["slug"]: p for p in PROJECTS}
SELECTED = [PROJECT_BY_SLUG[slug] for slug in SELECTED_SLUGS]
LABS_PROJECTS = [PROJECT_BY_SLUG[slug] for slug in LABS_SLUGS]

# Aggregates, computed once from the same data file.
LAB_COMMITS = sum(repo_commits(project["repo"]) for project in LABS_PROJECTS)
LAB_STARS = sum(repo_stars(project["repo"]) for project in LABS_PROJECTS)
ORG_SOURCE = [r for r in DATA.get("repos", []) if r["owner"] == ORG and not r["fork"]]
ORG_COMMITS = sum(r["commits"] for r in ORG_SOURCE)
PUBLIC_REPOS = int(DATA.get("user", {}).get("public_repos", 0)) + int(
    DATA.get("user", {}).get("org_repos", 0)
)
SOURCE_REPOS = len([r for r in DATA.get("repos", []) if not r["fork"]])

# ---------------------------------------------------------------- copy (VI/EN)

COPY: dict[str, dict[str, str]] = {
    "vi": {},
    "en": {},
}


def add(key: str, vi: str, en: str) -> None:
    COPY["vi"][key] = vi
    COPY["en"][key] = en


# Per-project commit and star counts, keyed so each language keeps its own
# thousands separator (4.580 / 4,580) through the normal copy mechanism.
for _project in PROJECTS:
    _repo = _project.get("repo")
    if not _repo:
        continue
    _slug = _project["slug"]
    add(
        f"n.{_slug}.commits",
        fmt(repo_commits(_repo), "vi"),
        fmt(repo_commits(_repo), "en"),
    )
    add(f"n.{_slug}.stars", stars(repo_stars(_repo)), stars(repo_stars(_repo)))


# global
add("a11y.skip", "Bỏ qua tới nội dung", "Skip to content")
add("a11y.lang", "Đổi ngôn ngữ", "Switch language")
add("a11y.theme", "Đổi giao diện sáng/tối", "Switch light or dark theme")
add("nav.home", "Trang chủ", "Home")
add("nav.about", "Giới thiệu", "About")
add("nav.work", "Dự án", "Work")
add("nav.domains", "Lĩnh vực", "Domains")
add("nav.contact", "Liên hệ", "Contact")
add("nav.labs", "MoLik Labs", "MoLik Labs")
add("labs.kicker", "Tổ chức", "Organisation")
add(
    "labs.title",
    "Phần lớn code nằm ở <em>MoLik Labs</em>.",
    "Most of the code lives at <em>MoLik Labs</em>.",
)
add(
    "labs.lede",
    "Một tổ chức mở, một người bảo trì. Cùng một tài khoản, tách ra cho dễ đọc.",
    "An open organisation, one maintainer. Same account, split out so it reads cleanly.",
)
add(
    "labs.p1",
    "<strong>MoLik Labs</strong> là nơi mình đặt những repo đủ lớn để cần một trang riêng: <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/ZMRIG\" target=\"_blank\" rel=\"noopener noreferrer\">ZMRIG</a>, <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/Q-FOX-Algorithm\" target=\"_blank\" rel=\"noopener noreferrer\">Q-FOX</a> và <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/STUDY-SITE\" target=\"_blank\" rel=\"noopener noreferrer\">Study Focus Fox</a>. Không có công ty đứng sau, không có lịch ra bản.",
    "<strong>MoLik Labs</strong> is where the repositories large enough to need their own page live: <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/ZMRIG\" target=\"_blank\" rel=\"noopener noreferrer\">ZMRIG</a>, <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/Q-FOX-Algorithm\" target=\"_blank\" rel=\"noopener noreferrer\">Q-FOX</a> and <a class=\"inline-link\" href=\"https://github.com/MoLik-Labs/STUDY-SITE\" target=\"_blank\" rel=\"noopener noreferrer\">Study Focus Fox</a>. No company behind it, no release calendar.",
)
add(
    "labs.p2",
    "Đồ thị đóng góp trên profile này được vẽ từ một file text 53×7 nằm ngay trong repo, không phải chấm tay: <code>tools/graph_art.py</code> và <code>docs/graph-art.md</code> ghi rõ cách làm.",
    "The contribution grid on this profile is drawn from a 53×7 text file in this repository rather than by hand: <code>tools/graph_art.py</code> and <code>docs/graph-art.md</code> spell out how.",
)
add("labs.cta", "Mở MoLik Labs", "Open MoLik Labs")
add("labs.orgKey", "Tổ chức", "Organisation")
add("labs.reposKey", "Repo công khai", "Public repos")
add(
    "labs.reposValue",
    f"{len(ORG_SOURCE)} · {fmt(ORG_COMMITS, 'vi')} commit",
    f"{len(ORG_SOURCE)} · {fmt(ORG_COMMITS, 'en')} commits",
)
add("labs.licKey", "Giấy phép", "Licences")
add("lab.brand", "MoLik Labs", "MoLik Labs")
add("lab.footer", "MoLik Labs · độc lập, phi thương mại", "MoLik Labs · independent, non-commercial")
add("lab.nav.work", "Dự án", "Work")
add("lab.nav.people", "Con người", "People")
add("lab.nav.contact", "Liên hệ", "Contact")
add("lab.nav.profile", "Hồ sơ", "Profile")
add("lab.nav.profileBack", "← Hồ sơ", "← Profile")
add("lab.hero.label", "Lab phần mềm độc lập", "Independent software lab")
add(
    "lab.hero.title",
    "Độc lập.<br /><em>Mở theo thiết kế.</em>",
    "Independent.<br /><em>Open by design.</em>",
)
add(
    "lab.hero.lede",
    "MoLik Labs là nơi mình phát hành những phần mềm mình dùng thật: một miner RandomX, một phòng thí nghiệm Rubik, một app học một-file. Mã nguồn mở, không theo dõi, không quảng cáo — làm xong việc rồi tránh đường.",
    "MoLik Labs is where I publish software I actually use: a RandomX miner, a cube laboratory, a single-file study app. Source in the open, no tracking, no ads — built to do the job and then get out of the way.",
)
add("lab.hero.ctaWork", "Dự án", "Projects")
add("lab.hero.ctaOrg", "Tổ chức trên GitHub", "GitHub organisation")
add("lab.fig.head2", "Từ 2026", "Est. 2026")
add("lab.fig.big", "Phần mềm, có nguyên tắc.", "Software, with principles.")
add("lab.fig.1", "Một người bảo trì, có chủ đích", "One maintainer, on purpose")
add("lab.fig.2", "Mã mở, không giấu gì", "Open source, nothing to hide")
add("lab.fig.3", "Không telemetry, không bao giờ", "No telemetry, ever")
add("lab.fig.4", "Miễn phí dùng, miễn phí fork", "Free to use, free to fork")
add("lab.strip.left", "Ít ồn hơn. <strong>Nhiều chủ đích hơn.</strong>", "Less noise. <strong>More intent.</strong>")
add(
    "lab.strip.right",
    f"{len(LABS_PROJECTS)} dự án · {fmt(LAB_COMMITS, 'vi')} commit · {LAB_STARS} sao",
    f"{len(LABS_PROJECTS)} projects · {fmt(LAB_COMMITS, 'en')} commits · {LAB_STARS} stars",
)
add("lab.work.num", "01 / Dự án chọn lọc", "01 / Selected work")
add("lab.work.title", "Làm để dùng.", "Built to be used.")
add(
    "lab.work.lede",
    "Danh sách ngắn, vì danh sách vốn ngắn. Tất cả đều công khai.",
    "A short list, because the list is short. Everything below is public.",
)
add("lab.work.all", "Tất cả dự án", "All projects")
add("lab.readMore", "Đọc thêm", "Read more")
add("lab.sourceCode", "Mã nguồn", "Source code")
add("lab.people.num", "02 / Con người", "02 / The people")
add("lab.people.title", "Một lab một người, có chủ đích.", "A lab of one, on purpose.")
add(
    "lab.people.lede",
    "Giữ nhỏ để mọi quyết định có người chịu trách nhiệm, và code giữ được sự thật thà.",
    "Keeping it small means every decision has an owner, and the code can stay honest.",
)
add("lab.person.role", "Người sáng lập · Bảo trì · C, C++, Zig, Python, web", "Founder · Maintainer · C, C++, Zig, Python, web")
add("lab.person.contribTitle", "Đóng góp", "Contributions")
add(
    "lab.person.contribText",
    "Không tuyển người, không thuê ngoài, không áp lực roadmap. Pull request và báo lỗi thật thì luôn được chào.",
    "No hires, no contractors, no roadmap pressure. Pull requests and honest bug reports are welcome.",
)
add("lab.contact.num", "03 / Liên hệ", "03 / Get in touch")
add("lab.contact.title", "Một đường thẳng.", "A direct line.")
add(
    "lab.contact.lede",
    "Câu hỏi, báo lỗi, hay một thứ đáng làm cùng — một hộp thư, một người đọc.",
    "Questions, bug reports, or something worth building together — one inbox, read by one person.",
)
add("lab.contact.note", "Issue và pull request cũng về cùng một chỗ.", "Issues and pull requests reach the same desk.")
add("lab.contact.elsewhere", "Nơi khác", "Elsewhere")
add("lab.contact.site", "Trang này", "This site")
add("lab.contact.source", "Mã nguồn trang này", "Source of this site")
add("lab.fine.num", "04 / Chi tiết nhỏ", "04 / The fine print")
add("lab.fine.title", "Rõ ràng mặc định.", "Clear by default.")
add(
    "lab.fine.lede",
    "Cam kết viết ra, không có chữ nhỏ giả làm chữ lớn.",
    "Commitments written down, without the small print pretending to be big.",
)
add("lab.fine.1.title", "Một lab cá nhân, phi thương mại", "A personal, non-commercial lab")
add(
    "lab.fine.1a",
    "MoLik Labs là tổ chức mã nguồn mở cá nhân, không phải công ty và không đăng ký kinh doanh. Không có gì ở đây được kiếm tiền: không quảng cáo, không gói trả phí, không bán dữ liệu.",
    "MoLik Labs is a personal open-source organisation, not a company and not a registered entity. Nothing here is monetised: no advertising, no paid tiers, no data sold.",
)
add(
    "lab.fine.1b",
    "Dự án được phát hành để học, để dùng và để review. Việc bảo trì theo thời gian rảnh của một người, nên không có cam kết uptime.",
    "Projects are published for learning, for use and for review. Maintenance follows the free time of one person, so there is no uptime promise attached.",
)
add("lab.fine.2.title", "Không thu thập dữ liệu", "Zero data collection")
add(
    "lab.fine.2a",
    "Các trang này không có analytics, không có tracker quảng cáo, không telemetry. Không cookie nào được đặt để theo dõi, font phục vụ từ chính domain này.",
    "These pages ship no analytics, no advertising trackers and no telemetry. No cookies are set for tracking, and the fonts are served from this domain.",
)
add(
    "lab.fine.2b",
    "Hai tuỳ chọn được lưu trong localStorage của trình duyệt: giao diện sáng/tối và ngôn ngữ. Xoá dữ liệu trang là xoá cả hai. Link sang GitHub dẫn bạn ra khỏi trang này, theo chính sách của họ.",
    "Two preferences are stored in your browser's localStorage only: the interface theme and the language. Clearing site data removes both. Links to GitHub take you to a service outside this site, under its own policies.",
)
add("lab.fine.3.title", "Nội dung bên thứ ba và ghi công", "Third-party content and attribution")
add(
    "lab.fine.3a",
    "Các dự án là độc lập, không liên kết, không được bảo trợ và không đại diện cho bất kỳ nền tảng hay dịch vụ bên thứ ba nào trừ khi nói rõ.",
    "Projects are independent and not affiliated with, endorsed by, or representatives of any third-party platform or service unless stated explicitly.",
)
add(
    "lab.fine.3b",
    "Chỗ nào dựng trên việc của người khác thì trang dự án nói rõ. Ví dụ MOLIK_WINLIK là bản dựng Sophia Script cho Windows của farag2 theo giấy phép MIT, giữ nguyên phần ghi công.",
    "Where a project is built on someone else's work, that is stated on the project page. MOLIK_WINLIK, for example, is a build of Sophia Script for Windows by farag2 under the MIT licence, with attribution kept intact.",
)
add("lab.fine.4.title", "Giấy phép mã nguồn", "Source code licensing")
add(
    "lab.fine.4a",
    "Mã nguồn được công khai để review minh bạch. Quyền dùng, sửa, phân phối mỗi dự án chỉ theo LICENSE trong repo đó — GPL-3.0 cho ZMRIG, MIT cho STUDY-SITE và MOLIK_WINLIK, Apache-2.0 cho PUBLIC_FILE.",
    "Source is published in public repositories for transparent review. Permission to use, modify and redistribute each project is governed only by the license included in that repository — GPL-3.0 for ZMRIG, MIT for STUDY-SITE and MOLIK_WINLIK, Apache-2.0 for PUBLIC_FILE.",
)
add(
    "lab.fine.4b",
    "Đọc file LICENSE trước khi phân phối lại. Thư viện bên thứ ba giữ giấy phép và yêu cầu ghi công riêng. Font ở đây là Inter, Inter Tight và JetBrains Mono, đều theo SIL Open Font License 1.1.",
    "Check the LICENSE file before redistributing. Third-party dependencies keep their own licences and attribution requirements. The typefaces here are Inter, Inter Tight and JetBrains Mono, all under the SIL Open Font License 1.1.",
)
add("lab.wi.title", "Tất cả đều mở.", "Everything in the open.")
add(
    "lab.wi.lede",
    "Ba repo, mỗi cái đủ nhỏ để đọc trong một buổi chiều.",
    "Three repositories, each one small enough to read in an afternoon.",
)
add(
    "lab.wi.meta",
    f"0{len(LABS_PROJECTS)} dự án · {fmt(LAB_COMMITS, 'vi')} commit · {YEAR}",
    f"0{len(LABS_PROJECTS)} projects · {fmt(LAB_COMMITS, 'en')} commits · {YEAR}",
)
add("lab.d.what", "Nó là gì", "What it is")
add("lab.d.ship", "Nó ra sao", "How it ships")
add("lab.d.next", "Tiếp theo", "What is next")
add(
    "lab.d.nextText",
    "Sửa lỗi nhỏ, viết docs rõ hơn, và làm tiếp thứ ý tưởng kế tiếp cần. Không có roadmap nào ngoài thế.",
    "Small fixes, clearer docs and whatever the next idea needs. There is no roadmap beyond that, and no promise of one.",
)
add("lab.d.ask", "Hỏi về dự án này", "Ask about this project")
add("lab.d.glance", "Tóm tắt", "At a glance")
add("lab.d.repo", "Repo", "Repository")
add("lab.d.status", "Trạng thái", "Status")
add("lab.d.stack", "Stack", "Stack")

# per-project lab copy
LAB_VI = {
    "zmrig": (
        "Một miner, không giấu gì",
        "Một miner RandomX với phí dev nhìn thấy được và tắt được, cái pool trả cho nó, proxy cho cả farm, và trang web ghép mọi thứ lại.",
        "Mã nguồn cộng bản phát hành. GPL-3.0, phí ghi trong doc/FEE.md chứ không chôn trong code.",
    ),
    "qfox": (
        "Phòng thí nghiệm phương pháp",
        "Phòng thí nghiệm 3×3: engine C với BFS và IDA*, binding Python, mười ba phương pháp đo cạnh nhau trên cùng scramble, và trang bảng sinh ra từ benchmark.",
        "Trang tĩnh cộng engine C và gói Python. Mọi con số công bố đều được chạy lại trên engine trước khi phát hành.",
    ),
    "study-site": (
        "Công cụ học, offline",
        "Một môi trường học một-file: lộ trình Vật lí 9 52 buổi, ôn tập cách quãng, sổ điểm, kế hoạch tuần và đấu trường pixel. Offline mặc định, vì học không cần tài khoản.",
        "Một file HTML. Mở lên, không cài, không đăng nhập, không gì rời khỏi máy.",
    ),
}
for slug, (tag_vi, summary_vi, ship_vi) in LAB_VI.items():
    project = PROJECT_BY_SLUG[slug]
    add(f"lab.{slug}.tag", tag_vi, project["studio"]["tag"])
    add(f"lab.{slug}.summary", summary_vi, project["studio"]["summary"])
    add(f"lab.{slug}.ship", ship_vi, project["studio"]["ship"])


# hero
add("hero.kicker", "Xin chào", "Welcome")
add("hero.age", "26 tuổi", "26 years old")
add("hero.role", "Builder · C, C++, Zig, Python, web", "Builder · C, C++, Zig, Python, web")
add(
    "hero.tagline",
    "Mình làm từ tầng thấp — C, C++, Zig — tới web và trang tài liệu quanh nó. Ý tưởng cần gì thì mình học cái đó, rồi đẩy ra công khai.",
    "I work from the low layers — C, C++, Zig — up to the web and the pages around it. Whatever the idea needs, I learn it, then ship it in public.",
)
add("hero.ctaContact", "Liên hệ", "Get in touch")
add("hero.ctaWork", "Xem dự án", "View work")
add("hero.scroll", "Cuộn", "Scroll")

add("facts.fieldKey", "Lĩnh vực", "Field")
add("facts.fieldValue", "Code & thiết kế", "Code & design")
add("facts.dobKey", "Ngày sinh", "Date of birth")
add("facts.dobValue", "09/05/2000", "9 May 2000")
add("facts.locationKey", "Nơi ở", "Based in")
add("facts.locationValue", "Bắc Giang, Việt Nam", "Bắc Giang, Việt Nam")
add("facts.emailKey", "Email", "Email")
add("facts.siteKey", "Trang", "Site")
add("facts.statusKey", "Trạng thái", "Status")
add("facts.statusValue", "Học và làm công khai", "Learning in public")

# about
add("about.kicker", "Giới thiệu", "About")
add("about.title", "Chỗ giao nhau giữa tò mò và tay nghề.", "Where curiosity meets craft.")
add(
    "about.lede",
    "Mình không cố tỏ ra chuyên nghiệp. Mình cố giỏi hơn, công khai, từng dòng một.",
    "I am not trying to look senior. I am trying to get better, in public, one line at a time.",
)
add(
    "about.p1",
    "Mình là <strong>Khải</strong>, ở Bắc Giang. Mình làm một mình, và thích những repo lớn hơn một file script: một miner RandomX, một phòng thí nghiệm Rubik 3×3, một app học tập một-file. C++ là chỗ mình bắt đầu, vì trình biên dịch rất thẳng thắn: hoặc chạy, hoặc không.",
    "I am <strong>Khải</strong>, from Bắc Giang. I work on my own, and I like repositories that are bigger than a single script: a RandomX miner, a 3×3 cube laboratory, a single-file study app. C++ is where I started, because a compiler is brutally honest: it runs or it does not.",
)
add(
    "about.p2",
    "Phần lớn thời gian là đọc source của người khác rồi viết lại theo cách mình hiểu: C/C++ cho phần lõi, Zig khi cần đúng tốc độ đó, Python cho công cụ, HTML/CSS/JS cho mọi thứ người khác nhìn thấy. Trang này cũng do script sinh ra, không chỉnh tay.",
    "Most of the time goes into reading other people's source and rewriting it until I understand it: C/C++ for the core, Zig when that exact speed is needed, Python for tooling, HTML/CSS/JS for everything a visitor sees. Even this site is generated by scripts, not hand-edited.",
)
add("about.locationKey", "Vị trí", "Location")
add("about.locationValue", "Bắc Giang, Việt Nam", "Bắc Giang, Việt Nam")
add("about.focusKey", "Đang tập trung", "Focus")
add("about.focusValue", "C/C++, Zig, Python, web", "C/C++, Zig, Python, web")
add("about.learnKey", "Đang học", "Learning")
add("about.learnValue", "RandomX, engine C, build đa nền tảng", "RandomX, C engines, cross-platform builds")

# credentials
add("cred.kicker", "Năng lực", "Credentials")
add("cred.title", "Con số nhỏ, nhưng là thật.", "Small numbers, all of them real.")
add(
    "cred.lede",
    "Không có chứng chỉ để khoe. Chỉ có repo, commit và những thứ đã chạy được.",
    "No certificates to show off. Just repos, commits and things that already ran.",
)
add("cred.one.title", "Repo công khai, hai tài khoản", "Public repositories, two accounts")
add(
    "cred.one.text",
    f"{PUBLIC_REPOS} repo công khai giữa @NggKhaiz và @MoLik-Labs — {SOURCE_REPOS} cái là code gốc, phần còn lại là fork có chủ đích.",
    f"{PUBLIC_REPOS} public repositories across @NggKhaiz and @MoLik-Labs — {SOURCE_REPOS} original, the rest deliberate forks.",
)
add("cred.two.title", "Commit trong repo lớn nhất", "Commits in the largest repository")
add(
    "cred.two.text",
    f"ZMRIG: {fmt(repo_commits('MoLik-Labs/ZMRIG'), 'vi')} commit, {repo_stars('MoLik-Labs/ZMRIG')} sao, engine C/C++ cộng các mảnh Zig. Con số lấy từ GitHub API, không phải tự khai.",
    f"ZMRIG: {fmt(repo_commits('MoLik-Labs/ZMRIG'))} commits, {repo_stars('MoLik-Labs/ZMRIG')} stars, a C/C++ engine with Zig parts. Numbers read from the GitHub API, not self-reported.",
)
add("cred.three.title", "Điều đang theo đuổi", "What I am after")
add(
    "cred.three.text",
    "Viết code đọc được, để phí dev phải nhìn thấy được, và để mọi con số trên trang này kiểm chứng được bằng API.",
    "Writing readable code, keeping developer fees visible, and making every number on this site checkable against the API.",
)

# work
add("work.kicker", "Dự án", "Work")
add("work.title", "Bốn repo nhiều hoạt động nhất.", "The four most active repositories.")
add(
    "work.lede",
    "Chọn theo số commit thật, không theo cảm giác. Bản đầy đủ sáu repo nằm ở trang dự án.",
    "Picked by real commit counts, not by feeling. All six live on the work page.",
)
add("work.more", "Xem tất cả dự án", "See all projects")
add("work.open", "Mở dự án", "Open project")
add("work.count", "06 dự án", "06 projects")
add("work.index.title", "Tất cả những gì đã ship.", "Everything that shipped.")
add(
    "work.index.lede",
    "Sáu repo, sắp theo số commit. Cái nào là bản dựng từ upstream thì ghi rõ là bản dựng.",
    "Six repositories, ordered by commit count. Anything built on upstream work says so.",
)

# domains
add("domains.kicker", "Lĩnh vực", "Domains")
add("domains.title", "Những gì mình chạm tới.", "What I actually touch.")
add(
    "domains.lede",
    "Không phải bảng kỹ năng đầy đủ — chỉ là những thứ đã dùng cho một dự án thật.",
    "Not a full skill matrix — only the things that carried a real project.",
)
add(
    "domains.note",
    "Đang đọc thêm: RandomX và tối ưu bộ nhớ, build đa nền tảng cho C/Zig, và cách giữ một repo 4.500 commit còn đọc được.",
    "Currently reading up on: RandomX and memory tuning, cross-platform builds for C and Zig, and how to keep a 4,500-commit repository readable.",
)

# contact
add("contact.kicker", "Liên hệ", "Contact")
add("contact.title", "Một đường thẳng.", "A direct line.")
add("contact.note", "Mail là đường nhanh nhất. Discord thì thường trực hơn.", "Email is the fastest route. Discord is usually the fastest reply.")
add("contact.direct", "Liên hệ trực tiếp", "Direct")
add("contact.copy", "copy", "copy")
add("contact.copied", "đã copy", "copied")
add("contact.copyAria", "Copy username Discord mental.arc", "Copy the Discord username mental.arc")
add("contact.where", "Nơi khác", "Elsewhere")
add("contact.repo", "Repo của profile này", "This profile's repo")

# footer
add("footer.rights", "không framework, không bước build", "no framework, no build step")
add("footer.top", "Lên đầu trang", "Back to top")
add("footer.pages", "Trang", "Pages")
add("footer.note", "Không analytics, không cookie, không script bên thứ ba.", "No analytics, no cookies, no third-party scripts.")

# detail page labels
add("d.overview", "Tổng quan", "Overview")
add("d.why", "Vì sao có nó", "Why it exists")
add("d.how", "Cách nó chạy", "How it ships")
add("d.facts", "Thông tin", "At a glance")
add("d.links", "Đường dẫn", "Links")
add("d.source", "Mã nguồn", "Source")
add("d.live", "Bản chạy", "Live")
add("d.status", "Trạng thái", "Status")
add("d.stack", "Công nghệ", "Stack")
add("d.all", "Tất cả dự án", "All projects")
add("d.next", "Dự án tiếp theo", "Next project")
add("d.back", "Về danh sách dự án", "Back to all projects")
add("d.email", "Hỏi về dự án này", "Ask about this project")
add("d.404.title", "Không có trang này.", "This page does not exist.")
add("d.404.lede", "Có thể link cũ, có thể mình gõ sai. Về trang chủ là chắc nhất.", "Probably an old link or a typo. The home page is the safe way back.")

# per-project copy keys
for project in PROJECTS:
    slug = project["slug"]
    add(f"p.{slug}.title", project["title"], project["title"])
    add(f"p.{slug}.tagline", project["tagline"]["vi"], project["tagline"]["en"])
    add(f"p.{slug}.intro", project["intro"]["vi"], project["intro"]["en"])
    add(f"p.{slug}.why", project["why"]["vi"], project["why"]["en"])
    add(f"p.{slug}.how", project["how"]["vi"], project["how"]["en"])
    add(f"p.{slug}.status", project["status"]["vi"], project["status"]["en"])

# fact labels
add("fact.lang", "Ngôn ngữ", "Language")
add("fact.created", "Bắt đầu", "Started")
add("fact.commits", "Commit", "Commits")
add(
    "p.molik-winlik.note",
    "Ghi công: phần lõi là <a class=\"inline-link\" href=\"https://github.com/farag2/Sophia-Script-for-Windows\" target=\"_blank\" rel=\"noopener noreferrer\">Sophia Script for Windows</a> của farag2, giấy phép MIT. Repo này là bản dựng của mình, không phải bản gốc và không được upstream bảo trợ.",
    "Credit: the core is <a class=\"inline-link\" href=\"https://github.com/farag2/Sophia-Script-for-Windows\" target=\"_blank\" rel=\"noopener noreferrer\">Sophia Script for Windows</a> by farag2, MIT licensed. This repository is my build, not the original, and is not endorsed by upstream.",
)
add("fact.release", "Bản phát hành", "Release")
add("fact.stars", "Sao", "Stars")
add("fact.license", "Giấy phép", "License")
add("fact.deploy", "Triển khai", "Deploy")
add("fact.readme", "README", "README")
add("fact.fonts", "Font", "Fonts")
add("fact.tracking", "Tracking", "Tracking")
add("fact.output", "Đầu ra", "Output")
add("fact.build", "Build", "Build")

NO_README = {"vi": "chưa có", "en": "not yet"}
add("fact.readme.none", NO_README["vi"], NO_README["en"])
add("fact.none", "không", "none")
add("fact.selfhost", "tự host", "self-hosted")
add("fact.manual", "chạy tay", "manual")

# ---------------------------------------------------------------- html helpers


def t(key: str, tag: str = "span", cls: str | None = None) -> str:
    """Inline element carrying a copy key; the VI string is the static fallback."""
    attr = f' class="{cls}"' if cls else ""
    return f'<{tag}{attr} data-i18n="{key}">{COPY["vi"][key]}</{tag}>'


def th(key: str, tag: str = "p", cls: str | None = None) -> str:
    """Same, for strings containing markup."""
    attr = f' class="{cls}"' if cls else ""
    return f'<{tag}{attr} data-i18n-html="{key}">{COPY["vi"][key]}</{tag}>'


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


ICON_ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
)
ICON_SUN = (
    '<svg id="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
)
ICON_MOON = (
    '<svg id="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" aria-hidden="true" hidden><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
)


def canonical_url(path: str) -> str:
    if path.endswith("index.html"):
        return f"{ORIGIN}/{path[:-len('index.html')]}"
    return f"{ORIGIN}/{path}"


def jsonld(payload: dict) -> str:
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'  <script type="application/ld+json">{blob}</script>'


def person_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Nguyễn Gia Khải",
        "alternateName": "Ngg.Khaiz",
        "url": f"{ORIGIN}/",
        "image": f"{ORIGIN}/assets/img/social/avatar-384.jpg",
        "email": f"mailto:{EMAIL}",
        "birthDate": "2000-05-09",
        "jobTitle": "Software builder",
        "address": {"@type": "PostalAddress", "addressLocality": "Bắc Giang", "addressCountry": "VN"},
        "sameAs": [GITHUB, "https://github.com/MoLik-Labs", "https://nggkhaiz.pages.dev"],
        "knowsAbout": ["C", "C++", "Zig", "Python", "JavaScript", "RandomX", "Static sites"],
        "worksFor": {"@type": "Organization", "name": "MoLik Labs", "url": "https://github.com/MoLik-Labs"},
    }


def website_ld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Nguyễn Gia Khải",
        "url": f"{ORIGIN}/",
        "inLanguage": ["vi", "en"],
        "author": {"@type": "Person", "name": "Nguyễn Gia Khải", "url": f"{ORIGIN}/"},
    }


def project_ld(project: dict, path: str, org: bool = False) -> dict:
    license_name = next((value for key, value in project["facts"] if key == "fact.license"), None)
    payload = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": project["title"],
        "description": project["tagline"]["en"],
        "url": canonical_url(path),
        "codeRepository": project["url"],
        "programmingLanguage": project["stack"],
        "author": {"@type": "Person", "name": "Nguyễn Gia Khải", "url": f"{ORIGIN}/"},
        "isPartOf": {
            "@type": "Organization",
            "name": "MoLik Labs",
            "url": "https://github.com/MoLik-Labs",
        },
    }
    if license_name:
        payload["license"] = license_name
    if org:
        payload["maintainer"] = {"@type": "Organization", "name": "MoLik Labs"}
    return payload


def breadcrumb_ld(crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": index + 1, "name": name, "item": f"{ORIGIN}/{href}"}
            for index, (name, href) in enumerate(crumbs)
        ],
    }


def layout(
    *,
    path: str,
    title: str,
    description: str,
    body: str,
    studio: bool = False,
    og_image: str = "assets/img/social/og-profile.png",
    og_type: str = "website",
    scripts: str = "",
    structured: list[dict] | None = None,
    bilingual: bool = False,
) -> str:
    depth = len(path.split("/")) - 1  # nested folders below the host root
    prefix = "../" * depth
    lang = "en" if (studio and not bilingual) else "vi"
    lang_switch = ' data-lang-switch="on"' if (bilingual or not studio) else ""
    canonical = canonical_url(path)

    if studio:
        nav = (
            f'<a href="{prefix}labs/work/">{t("lab.nav.work")}</a>'
            f'<a href="{prefix}labs/#people">{t("lab.nav.people")}</a>'
            f'<a href="{prefix}labs/#contact">{t("lab.nav.contact")}</a>'
            f'<a href="{prefix}index.html">{t("lab.nav.profileBack")}</a>'
        )
        wordmark = f'<a class="wordmark" href="{prefix}labs/index.html"><span class="wordmark__dot" aria-hidden="true"></span><span>MoLik Labs</span></a>'
        controls = (
            (
                '<button class="control" id="lang-toggle" type="button" aria-label="Đổi ngôn ngữ">'
                '<span id="lang-current">VI</span><span class="control__lang-idle" id="lang-other">/EN</span></button>'
            )
            if bilingual
            else ""
        ) + (
            '<button class="control" id="theme-toggle" type="button" aria-label="Toggle light and dark theme">'
            f"{ICON_SUN}{ICON_MOON}</button>"
        )
        footer_links = (
            f'<a href="{prefix}labs/work/">{t("lab.nav.work")}</a>'
            f'<a href="{prefix}labs/#people">{t("lab.nav.people")}</a>'
            f'<a href="{prefix}labs/#contact">{t("lab.nav.contact")}</a>'
            f'<a href="{prefix}index.html">{t("lab.nav.profile")}</a>'
        )
    else:
        nav = (
            f'<a href="{prefix}index.html#about">{t("nav.about")}</a>'
            f'<a href="{prefix}work/">{t("nav.work")}</a>'
            f'<a href="{prefix}index.html#domains">{t("nav.domains")}</a>'
            f'<a href="{prefix}index.html#contact">{t("nav.contact")}</a>'
        )
        wordmark = f'<a class="wordmark" href="{prefix}index.html"><span class="wordmark__dot" aria-hidden="true"></span><span>Ngg.Khaiz</span></a>'
        controls = (
            '<button class="control" id="lang-toggle" type="button" aria-label="Đổi ngôn ngữ">'
            '<span id="lang-current">VI</span><span class="control__lang-idle" id="lang-other">/EN</span></button>'
            f'<button class="control" id="theme-toggle" type="button" aria-label="Đổi giao diện sáng/tối">'
            f"{ICON_SUN}{ICON_MOON}</button>"
        )
        footer_links = (
            f'<a href="{prefix}work/">{t("nav.work")}</a>'
            f'<a href="{prefix}labs/index.html">{t("nav.labs")}</a>'
            f'<a href="{prefix}index.html#contact">{t("nav.contact")}</a>'
            f'<a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub</a>'
        )

    skip = t("a11y.skip", "a", "skip-link").replace("<a ", '<a href="#main" ', 1)
    # t() renders a span; build the skip link explicitly instead
    skip = f'<a class="skip-link" href="#main" data-i18n="a11y.skip">{COPY[lang]["a11y.skip"]}</a>'

    structured_block = "\n".join(jsonld(item) for item in (structured or []))
    canonical_tag = (
        "" if path == "404.html" else f'  <link rel="canonical" href="{canonical}" />'
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="dark"{lang_switch}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="author" content="Nguyễn Gia Khải" />
  <meta name="theme-color" content="#1e1e2e" media="(prefers-color-scheme: dark)" />
  <meta name="theme-color" content="#eff1f5" media="(prefers-color-scheme: light)" />
  <meta name="color-scheme" content="dark light" />
{canonical_tag}

  <meta property="og:type" content="{og_type}" />
  <meta property="og:site_name" content="Ngg.Khaiz" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ORIGIN}/{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{esc(title)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="twitter:image" content="{ORIGIN}/{og_image}" />
  <meta name="twitter:image:alt" content="{esc(title)}" />
  <meta property="og:locale" content="{'en_US' if (studio and not bilingual) else 'vi_VN'}" />
  <meta property="og:locale:alternate" content="{'vi_VN' if (studio and not bilingual) else 'en_US'}" />
{structured_block}

  <link rel="icon" href="{prefix}assets/img/icons/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/img/icons/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="{prefix}assets/img/icons/favicon-16.png" />
  <link rel="apple-touch-icon" href="{prefix}assets/img/icons/apple-touch-icon.png" />
  <link rel="manifest" href="{prefix}site.webmanifest" />

  <script>document.documentElement.classList.add("js");</script>
  <link rel="preload" href="{prefix}assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}assets/fonts/inter-tight-var.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}assets/fonts/jetbrains-mono-var.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{prefix}assets/site.css" />
  <link rel="stylesheet" href="{prefix}assets/pages.css" />
</head>

<body id="top">
  {skip}

  <header class="site-header" id="header">
    <div class="shell site-header__inner">
      {wordmark}
      <nav class="site-nav" aria-label="{'MoLik Labs' if studio else 'Chính'}">{nav}</nav>
      <div class="header-controls">{controls}</div>
    </div>
    <div class="progress" id="progress" aria-hidden="true"></div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="shell site-footer__inner">
      <p>© <span id="year">{YEAR}</span> {t('lab.footer') if studio else 'Nguyễn Gia Khải'} · {'' if studio else t('footer.rights')}</p>
      <nav class="footer-nav" aria-label="Footer">{footer_links}</nav>
      <a class="to-top" href="#top">{t('footer.top') if not studio else 'Back to top'}
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
      </a>
    </div>
  </footer>

  <script src="{prefix}assets/copy.js" defer></script>
  <script src="{prefix}assets/site.js" defer></script>
  {scripts}
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks


def work_row(project: dict, index: int, prefix: str) -> str:
    slug = project["slug"]
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in project["stack"])
    return f"""          <a class="work__item reveal" href="{prefix}work/{slug}.html">
            <span class="work__index">{index:02d}</span>
            <span class="work__main">
              <span class="work__title">{t(f"p.{slug}.title", "span")}{ICON_ARROW}</span>
              {t(f"p.{slug}.tagline", "span", "work__desc")}
            </span>
            <span class="work__tags">{tags}</span>
          </a>"""


def work_card(project: dict, prefix: str) -> str:
    slug = project["slug"]
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in project["stack"])
    return f"""          <a class="postcard reveal" href="{prefix}work/{slug}.html">
            <span class="postcard__media">
              <img src="{prefix}{project['cover']}" alt="" width="1200" height="675" loading="lazy" />
            </span>
            <span class="postcard__body">
              <span class="postcard__head">
                <span class="postcard__title">{t(f"p.{slug}.title", "span")}</span>
                <span class="postcard__status">{t(f"p.{slug}.status")}</span>
              </span>
              <span class="postcard__text">{t(f"p.{slug}.tagline")}</span>
              <span class="postcard__tags">{tags}</span>
            </span>
          </a>"""


CONTACT_BLOCK = f"""        <div class="contact reveal">
          <div>
            <a class="contact__big" href="mailto:{EMAIL}">
              <span>{EMAIL}</span>
              {ICON_ARROW}
            </a>
            <p class="contact__note">{t("contact.note")}</p>
          </div>

          <div class="contact__grid">
            <div class="contact__block">
              <h3>{t("contact.direct")}</h3>
              <div class="contact__links" data-contact-direct>
                <a href="mailto:{EMAIL}">Email <span class="arrow">↗</span></a>
                <button class="contact__copy" type="button" data-copy="{DISCORD}" aria-label="Copy the Discord username {DISCORD}">
                  <span class="contact__copy-handle">Discord · @{DISCORD}</span>
                  <span class="contact__copy-hint">{t("contact.copy")}</span>
                </button>
              </div>
            </div>

            <div class="contact__block">
              <h3>{t("contact.where")}</h3>
              <div class="contact__links">
                <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub <span class="arrow">↗</span></a>
                <a href="{ORIGIN}" target="_blank" rel="noopener noreferrer">nggkhaiz.js.org <span class="arrow">↗</span></a>
                <a href="{{prefix}}labs/index.html">MoLik Labs <span class="arrow">↗</span></a>
                <a href="{GITHUB}/NggKhaiz" target="_blank" rel="noopener noreferrer">{t("contact.repo")}</a>
              </div>
            </div>
          </div>
        </div>"""

# ---------------------------------------------------------------- pages


def page_home() -> str:
    prefix = ""
    rows = "\n\n".join(work_row(p, i + 1, prefix) for i, p in enumerate(SELECTED))
    contact = CONTACT_BLOCK.replace("{prefix}", prefix)

    body = f"""    <!-- ============ HERO ============ -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__rings" aria-hidden="true"><span></span><span></span><span></span><span></span></div>

      <div class="shell hero__grid">
        <div class="hero__lead">
          <p class="hero__kicker label">{t("hero.kicker", "span")}</p>

          <div class="hero__portrait">
            <img src="assets/img/social/avatar-384.jpg" alt="Ảnh đại diện của Nguyễn Gia Khải"
                 width="96" height="96" />
          </div>

          <h1 id="hero-title">Nguyễn Gia Khải</h1>

          <p class="hero__meta">
            {t("hero.age")}
            <span class="sep" aria-hidden="true"></span>
            {t("hero.role")}
          </p>

          <p class="hero__tagline">{t("hero.tagline")}</p>

          <div class="hero__actions">
            <a class="btn btn--solid" href="mailto:{EMAIL}">{t("hero.ctaContact")}{ICON_ARROW}</a>
            <a class="btn btn--ghost" href="#work">{t("hero.ctaWork")}</a>
          </div>

          <a class="scroll-cue" href="#about">
            <span aria-hidden="true"></span>
            <em>{t("hero.scroll")}</em>
          </a>
        </div>

        <aside class="hero__aside">
          <dl class="facts">
            <div class="facts__row"><dt>{t("facts.fieldKey")}</dt><dd>{t("facts.fieldValue")}</dd></div>
            <div class="facts__row"><dt>{t("facts.dobKey")}</dt><dd>{t("facts.dobValue")}</dd></div>
            <div class="facts__row"><dt>{t("facts.locationKey")}</dt><dd>{t("facts.locationValue")}</dd></div>
            <div class="facts__row"><dt>{t("facts.emailKey")}</dt><dd><a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
            <div class="facts__row"><dt>{t("facts.siteKey")}</dt><dd>nggkhaiz.js.org</dd></div>
            <div class="facts__row"><dt>{t("facts.statusKey")}</dt><dd>{t("facts.statusValue")}</dd></div>
          </dl>
        </aside>
      </div>
    </section>

    <!-- ============ 01 ABOUT ============ -->
    <section class="section" id="about" aria-labelledby="about-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">01 / {t("about.kicker")}</p>
          <h2 class="section__title" id="about-title">{t("about.title", "span")}</h2>
          <p class="section__lede">{t("about.lede")}</p>
        </div>

        <div class="about__body">
          <div class="prose reveal">
            {th("about.p1")}
            {th("about.p2")}
          </div>

          <aside class="about__aside reveal" style="--d: 120ms">
            <dl>
              <div><dt class="label">{t("about.locationKey")}</dt><dd>{t("about.locationValue")}</dd></div>
              <div><dt class="label">{t("about.focusKey")}</dt><dd>{t("about.focusValue")}</dd></div>
              <div><dt class="label">{t("about.learnKey")}</dt><dd>{t("about.learnValue")}</dd></div>
            </dl>
          </aside>
        </div>
      </div>
    </section>

    <!-- ============ 02 CREDENTIALS ============ -->
    <section class="section" id="credentials" aria-labelledby="credentials-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">02 / {t("cred.kicker")}</p>
          <h2 class="section__title" id="credentials-title">{t("cred.title", "span")}</h2>
          <p class="section__lede">{t("cred.lede")}</p>
        </div>

        <div class="cards">
          <article class="card reveal">
            <p class="card__num">18</p>
            <h3 class="card__title">{t("cred.one.title")}</h3>
            <p class="card__text">{t("cred.one.text")}</p>
          </article>
          <article class="card reveal" style="--d: 90ms">
            <p class="card__num">4.580</p>
            <h3 class="card__title">{t("cred.two.title")}</h3>
            <p class="card__text">{t("cred.two.text")}</p>
          </article>
          <article class="card reveal" style="--d: 180ms">
            <p class="card__num">∞</p>
            <h3 class="card__title">{t("cred.three.title")}</h3>
            <p class="card__text">{t("cred.three.text")}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ============ 03 WORK ============ -->
    <section class="section" id="work" aria-labelledby="work-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">03 / {t("work.kicker")}</p>
          <h2 class="section__title" id="work-title">{t("work.title", "span")}</h2>
          <p class="section__lede">{t("work.lede")}</p>
        </div>

        <div class="work">
{rows}
        </div>

        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="work/">{t("work.more")}{ICON_ARROW}</a>
        </div>
      </div>
    </section>

    <!-- ============ 04 LAB ============ -->
    <section class="section" id="labs" aria-labelledby="labs-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">04 / {t("labs.kicker")}</p>
          <h2 class="section__title" id="labs-title">{t("labs.title", "span")}</h2>
          <p class="section__lede">{t("labs.lede")}</p>
        </div>

        <div class="about__body">
          <div class="prose reveal">
            {th("labs.p1")}
            {th("labs.p2")}
            <p><a class="inline-link" href="labs/index.html">{t("labs.cta")} {ICON_ARROW}</a></p>
          </div>

          <aside class="about__aside reveal" style="--d: 120ms">
            <dl>
              <div><dt class="label">{t("labs.orgKey")}</dt><dd>MoLik-Labs</dd></div>
              <div><dt class="label">{t("labs.reposKey")}</dt><dd>{t("labs.reposValue")}</dd></div>
              <div><dt class="label">{t("labs.licKey")}</dt><dd>GPL-3.0 · MIT · Apache-2.0</dd></div>
            </dl>
          </aside>
        </div>
      </div>
    </section>

    <!-- ============ 05 DOMAINS ============ -->
    <section class="section" id="domains" aria-labelledby="domains-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">05 / {t("domains.kicker")}</p>
          <h2 class="section__title" id="domains-title">{t("domains.title", "span")}</h2>
          <p class="section__lede">{t("domains.lede")}</p>
        </div>

        <ul class="domains reveal">
          <li>C</li><li>C++</li><li>Zig</li><li>Python</li><li>JavaScript</li><li>TypeScript</li>
          <li>HTML</li><li>CSS</li><li>PowerShell</li><li>Shell</li><li>Docker</li>
          <li>RandomX</li><li>Build systems</li><li>Git</li><li>Obfuscated code</li>
        </ul>

        <p class="domains__note reveal">{t("domains.note")}</p>
      </div>
    </section>

    <!-- ============ 05 CONTACT ============ -->
    <section class="section" id="contact" aria-labelledby="contact-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">06 / {t("contact.kicker")}</p>
          <h2 class="section__title" id="contact-title">{t("contact.title", "span")}</h2>
        </div>

{contact}

        <div class="signature reveal">
          <pre><span class="cm">// the first program that did what I told it to</span>
<span class="kw">#include</span> <span class="str">&lt;bits/stdc++.h&gt;</span>
<span class="kw">using namespace</span> std;

<span class="kw">int</span> main() {{
    cout &lt;&lt; <span class="str">"Love You !"</span>;
    <span class="kw">return</span> 0;
}}</pre>
        </div>
      </div>
    </section>"""

    return layout(
        path="index.html",
        title="Nguyễn Gia Khải — builder · C, C++, Zig, Python, web",
        description=(
            "Nguyễn Gia Khải (Ngg.Khaiz) — Bắc Giang, Việt Nam. Làm một mình, từ C/C++ và Zig "
            f"tới Python và web viết tay: ZMRIG, Q-FOX, Study Focus Fox. Liên hệ: {EMAIL}."
        ),
        structured=[person_ld(), website_ld()],
        body=body,
    )


def page_work_index() -> str:
    cards = "\n".join(work_card(p, "../") for p in PROJECTS)
    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">{t("nav.home")}</a><span aria-hidden="true">/</span><span>{t("nav.work")}</span>
        </nav>
        <div class="page-head__grid">
          <h1 class="page-title reveal">{t("work.index.title", "span")}</h1>
          <p class="page-lede reveal">{t("work.index.lede")}</p>
        </div>
        <p class="page-meta reveal">{t("work.count")} · {YEAR}</p>
      </div>
    </section>

    <section class="section section--tight">
      <div class="shell">
        <div class="postgrid">
{cards}
        </div>
      </div>
    </section>"""

    return layout(
        path="work/index.html",
        title="Work — Nguyễn Gia Khải",
        description="Sáu dự án công khai, xếp theo số commit: ZMRIG, Q-FOX, Study Focus Fox, PUBLIC_FILE, MOLIK_WINLIK và chính trang này.",
        structured=[breadcrumb_ld([("Trang chủ", ""), ("Dự án", "work/")])],
        body=body,
    )


def page_work_detail(project: dict, index: int) -> str:
    slug = project["slug"]
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    facts = "".join(
        f'<div><dt class="label">{t(key)}</dt><dd>{t(value) if value.startswith(("fact.", "n.")) else esc(value)}</dd></div>'
        for key, value in project["facts"]
    )
    links = [f'<a href="{project["url"]}" target="_blank" rel="noopener noreferrer">{t("d.source")} <span class="arrow">↗</span></a>']
    if project["live"]:
        links.append(f'<a href="{project["live"]}" target="_blank" rel="noopener noreferrer">{t("d.live")} <span class="arrow">↗</span></a>')
    links.append(f'<a href="mailto:{EMAIL}?subject={slug}">{t("d.email")} <span class="arrow">↗</span></a>')
    note = project.get("note")
    note_html = f'<div class="detail__note">{th(f"p.{slug}.note")}</div>' if note else ""

    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">{t("nav.home")}</a><span aria-hidden="true">/</span>
          <a href="index.html">{t("nav.work")}</a><span aria-hidden="true">/</span>
          <span>{esc(project["title"])}</span>
        </nav>

        <div class="page-head__grid">
          <h1 class="page-title reveal">{esc(project["title"])}</h1>
          <p class="page-lede reveal">{t(f"p.{slug}.tagline")}</p>
        </div>

        <dl class="inline-facts reveal">
          <div><dt>{t("d.status")}</dt><dd>{t(f"p.{slug}.status")}</dd></div>
          <div><dt>{t("d.stack")}</dt><dd>{esc(" · ".join(project["stack"]))}</dd></div>
          <div><dt>{t("d.source")}</dt><dd><a class="inline-link" href="{project["url"]}" target="_blank" rel="noopener noreferrer">{esc(project["repo"])}</a></dd></div>
        </dl>
      </div>
    </section>

    <div class="shell">
      <figure class="cover reveal">
        <img src="../{project['cover']}" alt="Cover: {esc(project['title'])}" width="1200" height="675" />
      </figure>
    </div>

    <section class="section section--tight">
      <div class="shell detail">
        <div class="detail__main">
          <article class="prose reveal">
            <h2>{t("d.overview")}</h2>
            {th(f"p.{slug}.intro")}
            <h2>{t("d.why")}</h2>
            {th(f"p.{slug}.why")}
            {note_html}
            <h2>{t("d.how")}</h2>
            {th(f"p.{slug}.how")}
          </article>
        </div>

        <aside class="detail__aside reveal" style="--d: 120ms">
          <h3 class="label">{t("d.facts")}</h3>
          <dl class="detail__facts">{facts}</dl>
          <h3 class="label">{t("d.links")}</h3>
          <div class="contact__links">{''.join(links)}</div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="shell">
        <a class="nextup reveal" href="{nxt['slug']}.html">
          <span class="label">{t("d.next")}</span>
          <span class="nextup__title">{esc(nxt["title"])}{ICON_ARROW}</span>
          <span class="nextup__text">{t(f"p.{nxt['slug']}.tagline")}</span>
        </a>
        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="index.html">{t("d.back")}</a>
        </div>
      </div>
    </section>"""

    return layout(
        path=f"work/{slug}.html",
        title=f"{project['title']} — Nguyễn Gia Khải",
        description=project["tagline"]["vi"],
        og_image=project["cover"],
        og_type="article",
        structured=[
            project_ld(project, f"work/{slug}.html"),
            breadcrumb_ld([("Home", ""), ("Work", "work/"), (project["title"], f"work/{slug}.html")]),
        ],
        body=body,
    )


def page_studio_home() -> str:
    cards = "\n".join(studio_feature(p, "") for p in LABS_PROJECTS)
    body = f"""    <section class="studio-hero">
      <div class="shell studio-hero__grid">
        <div>
          <p class="label label--accent">{t("lab.hero.label")}</p>
          <h1>{th("lab.hero.title")}</h1>
          <p class="studio-hero__lede">{t("lab.hero.lede")}</p>
          <div class="studio-hero__actions">
            <a class="btn btn--solid" href="work/">{t("lab.hero.ctaWork")}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </a>
            <a class="btn btn--ghost" href="https://github.com/MoLik-Labs" target="_blank" rel="noopener noreferrer">{t("lab.hero.ctaOrg")} {ICON_ARROW}</a>
          </div>
        </div>

        <aside class="fig reveal">
          <div class="fig__head"><span class="label">Fig. 001</span><span class="label">{t("lab.fig.head2")}</span></div>
          <div class="fig__rule"></div>
          <p class="fig__big">{t("lab.fig.big")}</p>
          <div class="fig__list">
            <span>{t("lab.fig.1")}</span>
            <span>{t("lab.fig.2")}</span>
            <span>{t("lab.fig.3")}</span>
            <span>{t("lab.fig.4")}</span>
          </div>
        </aside>
      </div>
    </section>

    <div class="shell">
      <div class="strip">
        <span>{th("lab.strip.left")}</span>
        <span>{t("lab.strip.right")}</span>
      </div>
    </div>

    <section class="section" id="work">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">{t("lab.work.num")}</p>
          <h2 class="section__title">{t("lab.work.title")}</h2>
          <p class="section__lede">{t("lab.work.lede")}</p>
        </div>
{cards}
        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="work/">{t("lab.work.all")}
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>
          </a>
        </div>
      </div>
    </section>

    <section class="section" id="people">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">{t("lab.people.num")}</p>
          <h2 class="section__title">{t("lab.people.title")}</h2>
          <p class="section__lede">{t("lab.people.lede")}</p>
        </div>

        <div class="people">
          <article class="person reveal">
            <p class="person__index">01</p>
            <img class="person__avatar" src="../assets/img/social/avatar-384.jpg" alt="Nguyễn Gia Khải"
                 width="72" height="72" loading="lazy" />
            <h3 class="person__name">Nguyễn Gia Khải</h3>
            <p class="person__role">{t("lab.person.role")}</p>
            <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">github.com/NggKhaiz ↗</a>
          </article>
          <article class="person reveal" style="--d: 90ms">
            <p class="person__index">02</p>
            <h3 class="person__name">{t("lab.person.contribTitle")}</h3>
            <p class="person__role">{t("lab.person.contribText")}</p>
            <a href="https://github.com/MoLik-Labs" target="_blank" rel="noopener noreferrer">github.com/MoLik-Labs ↗</a>
          </article>
        </div>
      </div>
    </section>

    <section class="section" id="contact">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">{t("lab.contact.num")}</p>
          <h2 class="section__title">{t("lab.contact.title")}</h2>
          <p class="section__lede">{t("lab.contact.lede")}</p>
        </div>

        <div class="contact reveal">
          <div>
            <a class="contact__big" href="mailto:{EMAIL}">
              <span>{EMAIL}</span>
              {ICON_ARROW}
            </a>
            <p class="contact__note">{t("lab.contact.note")}</p>
          </div>

          <div class="contact__grid">
            <div class="contact__block">
              <h3>{t("lab.contact.elsewhere")}</h3>
              <div class="contact__links" data-contact-direct>
                <a href="https://github.com/MoLik-Labs" target="_blank" rel="noopener noreferrer">MoLik Labs <span class="arrow">↗</span></a>
                <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub <span class="arrow">↗</span></a>
                <button class="contact__copy" type="button" data-copy="{DISCORD}" aria-label="Copy the Discord username {DISCORD}">
                  <span class="contact__copy-handle">Discord · @{DISCORD}</span>
                  <span class="contact__copy-hint">copy</span>
                </button>
              </div>
            </div>
            <div class="contact__block">
              <h3>{t("lab.contact.site")}</h3>
              <div class="contact__links">
                <a href="../index.html">{t("lab.nav.profile")} <span class="arrow">↗</span></a>
                <a href="{GITHUB}/NggKhaiz" target="_blank" rel="noopener noreferrer">{t("lab.contact.source")} <span class="arrow">↗</span></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="fine">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">{t("lab.fine.num")}</p>
          <h2 class="section__title">{t("lab.fine.title")}</h2>
          <p class="section__lede">{t("lab.fine.lede")}</p>
        </div>

        <div class="fine reveal">
          <details>
            <summary><span class="n">01</span> {t("lab.fine.1.title")} <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>{t("lab.fine.1a")}</p>
              <p>{t("lab.fine.1b")}</p>
            </div>
          </details>
          <details>
            <summary><span class="n">02</span> {t("lab.fine.2.title")} <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>{t("lab.fine.2a")}</p>
              <p>{t("lab.fine.2b")}</p>
            </div>
          </details>
          <details>
            <summary><span class="n">03</span> {t("lab.fine.3.title")} <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>{t("lab.fine.3a")}</p>
              <p>{t("lab.fine.3b")}</p>
            </div>
          </details>
          <details>
            <summary><span class="n">04</span> {t("lab.fine.4.title")} <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>{t("lab.fine.4a")}</p>
              <p>{t("lab.fine.4b")}</p>
            </div>
          </details>
        </div>
      </div>
    </section>"""

    return layout(
        path="labs/index.html",
        title="MoLik Labs — Independent, open by design",
        description="MoLik Labs: a personal, non-commercial open-source lab — a RandomX miner, a cube laboratory and a single-file study app. No tracking, no ads, source in the open.",
        og_image="assets/img/social/og-labs.png",
        studio=True,
        bilingual=True,
        structured=[
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "MoLik Labs",
                "url": "https://github.com/MoLik-Labs",
                "description": "A personal, non-commercial open-source organisation: a RandomX miner, a cube laboratory and a single-file study app.",
                "founder": {"@type": "Person", "name": "Nguyễn Gia Khải", "url": f"{ORIGIN}/"},
                "sameAs": ["https://github.com/MoLik-Labs"],
            }
        ],
        body=body,
    )


def studio_feature(project: dict, prefix: str) -> str:
    slug = project["slug"]
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in project["stack"])
    return f"""        <article class="feature reveal">
          <div>
            <p class="feature__tag">{t(f"lab.{slug}.tag")}</p>
            <h3 class="feature__title"><a href="{prefix}work/{slug}.html">{esc(project['title'])}</a></h3>
            <div class="feature__meta">{tags}</div>
            <div class="feature__links">
              <a class="btn btn--ghost" href="{prefix}work/{slug}.html">{t("lab.readMore")} {ICON_ARROW}</a>
              <a class="btn btn--ghost" href="{project['url']}" target="_blank" rel="noopener noreferrer">{t("lab.sourceCode")} {ICON_ARROW}</a>
            </div>
          </div>
          <div class="feature__body--end">
            <p class="feature__text">{t(f"lab.{slug}.summary")}</p>
          </div>
        </article>"""


def page_studio_work_index() -> str:
    cards = "\n".join(
        f"""          <a class="postcard reveal" href="{p['slug']}.html">
            <span class="postcard__media"><img src="../../{p['cover']}" alt="" width="1200" height="675" loading="lazy" /></span>
            <span class="postcard__body">
              <span class="postcard__head">
                <span class="postcard__title">{esc(p['title'])}</span>
                <span class="postcard__status">{t(f"lab.{p['slug']}.tag")}</span>
              </span>
              <span class="postcard__text">{t(f"p.{p['slug']}.tagline")}</span>
              <span class="postcard__tags">{"".join(f"<span>{esc(tag)}</span>" for tag in p['stack'])}</span>
            </span>
          </a>"""
        for p in LABS_PROJECTS
    )
    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">MoLik Labs</a><span aria-hidden="true">/</span><span>{t("lab.nav.work")}</span>
        </nav>
        <div class="page-head__grid">
          <h1 class="page-title reveal">{t("lab.wi.title")}</h1>
          <p class="page-lede reveal">{t("lab.wi.lede")}</p>
        </div>
        <p class="page-meta reveal">{t("lab.wi.meta")}</p>
      </div>
    </section>

    <section class="section section--tight">
      <div class="shell">
        <div class="postgrid">
{cards}
        </div>
      </div>
    </section>"""

    return layout(
        path="labs/work/index.html",
        title="Work — MoLik Labs",
        description="Open-source projects from MoLik Labs: a RandomX miner, a 3x3 cube laboratory and a single-file study app.",
        og_image="assets/img/social/og-labs.png",
        studio=True,
        bilingual=True,
        structured=[breadcrumb_ld([("MoLik Labs", "labs/"), ("Work", "labs/work/")])],
        body=body,
    )


def page_studio_detail(project: dict, index: int) -> str:
    slug = project["slug"]
    nxt = LABS_PROJECTS[(index + 1) % len(LABS_PROJECTS)]
    facts_rows = [
        (t("lab.d.status"), project["status"]["vi"]),
        (t("lab.d.stack"), " · ".join(project["stack"])),
        (t("lab.d.repo"), project["repo"]),
    ]
    facts = "".join(
        f"<div><dt class=\"label\">{label}</dt><dd>{esc(value)}</dd></div>" for label, value in facts_rows
    )
    live = (
        f'<a href="{project["live"]}" target="_blank" rel="noopener noreferrer">{t("d.live")} <span class="arrow">↗</span></a>'
        if project["live"]
        else ""
    )
    note = project.get("note")
    note_html = f'<div class="detail__note">{th(f"p.{slug}.note")}</div>' if note else ""

    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">MoLik Labs</a><span aria-hidden="true">/</span>
          <a href="index.html">{t("lab.nav.work")}</a><span aria-hidden="true">/</span>
          <span>{esc(project['title'])}</span>
        </nav>
        <div class="page-head__grid">
          <h1 class="page-title reveal">{esc(project['title'])}</h1>
          <p class="page-lede reveal">{t(f"p.{slug}.tagline")}</p>
        </div>
        <p class="page-meta reveal">{t(f"lab.{slug}.tag")} · {YEAR}</p>
      </div>
    </section>

    <div class="shell">
      <figure class="cover reveal">
        <img src="../../{project['cover']}" alt="Cover for {esc(project['title'])}" width="1200" height="675" />
      </figure>
    </div>

    <section class="section section--tight">
      <div class="shell detail">
        <div class="detail__main">
          <article class="prose reveal">
            <h2>{t("lab.d.what")}</h2>
            <p>{t(f"lab.{slug}.summary")}</p>
            {note_html}
            <h2>{t("lab.d.ship")}</h2>
            <p>{t(f"lab.{slug}.ship")}</p>
            <h2>{t("lab.d.next")}</h2>
            <p>{t("lab.d.nextText")}</p>
          </article>
        </div>

        <aside class="detail__aside reveal" style="--d: 120ms">
          <h3 class="label">{t("lab.d.glance")}</h3>
          <dl class="detail__facts">{facts}</dl>
          <h3 class="label">{t("d.links")}</h3>
          <div class="contact__links">
            <a href="{project['url']}" target="_blank" rel="noopener noreferrer">{t("d.source")} <span class="arrow">↗</span></a>
            {live}
            <a href="mailto:{EMAIL}?subject={slug}">{t("lab.d.ask")} <span class="arrow">↗</span></a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="shell">
        <a class="nextup reveal" href="{nxt['slug']}.html">
          <span class="label">{t("d.next")}</span>
          <span class="nextup__title">{esc(nxt['title'])}{ICON_ARROW}</span>
          <span class="nextup__text">{t(f"p.{nxt['slug']}.tagline")}</span>
        </a>
        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="index.html">{t("d.back")}</a>
        </div>
      </div>
    </section>"""

    return layout(
        path=f"labs/work/{slug}.html",
        title=f"{project['title']} — MoLik Labs",
        description=project["tagline"]["en"],
        og_image=project["cover"],
        og_type="article",
        studio=True,
        bilingual=True,
        structured=[
            project_ld(project, f"labs/work/{slug}.html", org=True),
            breadcrumb_ld([("MoLik Labs", "labs/"), ("Work", "labs/work/"), (project["title"], f"labs/work/{slug}.html")]),
        ],
        body=body,
    )


def page_studio_redirect() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MoLik Labs — moved</title>
  <meta name="robots" content="noindex" />
  <meta http-equiv="refresh" content="0; url=../labs/index.html" />
  <link rel="canonical" href="{ORIGIN}/labs/" />
  <link rel="stylesheet" href="../assets/site.css" />
</head>
<body>
  <main class="shell" style="padding-block: 30vh">
    <p class="label label--accent">Moved</p>
    <h1 class="page-title" style="margin-top: 1rem">The studio page is now MoLik Labs.</h1>
    <p class="page-lede" style="margin-top: 1rem">Taking you to the new home. If nothing happens,
      <a class="inline-link" href="../labs/index.html">open /labs/</a>.</p>
  </main>
</body>
</html>
"""


def page_404() -> str:
    body = f"""    <section class="page-head page-head--tall">
      <div class="shell">
        <p class="label label--accent">404</p>
        <div class="page-head__grid">
          <h1 class="page-title reveal">{t("d.404.title", "span")}</h1>
          <p class="page-lede reveal">{t("d.404.lede")}</p>
        </div>
        <div class="hero__actions reveal">
          <a class="btn btn--solid" href="index.html">{t("nav.home")}{ICON_ARROW}</a>
          <a class="btn btn--ghost" href="work/">{t("nav.work")}</a>
        </div>
      </div>
    </section>"""

    return layout(
        path="404.html",
        title="404 — Nguyễn Gia Khải",
        description="Không có trang này.",
        body=body,
    )


# ---------------------------------------------------------------- other outputs


def copy_js() -> str:
    import json

    def block(lang: str) -> str:
        data = {key: COPY[lang][key] for key in sorted(COPY[lang])}
        body = json.dumps(data, ensure_ascii=False, indent=6)
        return "\n".join("    " + line for line in body.splitlines()[1:-1])

    return (
        "/* Generated by tools/build_pages.py - edit the source there, not here. */\n"
        "window.NK_COPY = {\n"
        "  vi: {\n" + block("vi") + "\n  },\n"
        "  en: {\n" + block("en") + "\n  }\n"
        "};\n"
    )


MANIFEST = """{
  "name": "Nguyễn Gia Khải — nggkhaiz.js.org",
  "short_name": "Ngg.Khaiz",
  "description": "Builder — C, C++, Zig, Python and the web around it. Bắc Giang, Việt Nam.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#1e1e2e",
  "theme_color": "#1e1e2e",
  "icons": [
    { "src": "assets/img/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "assets/img/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "assets/img/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
"""


def sitemap(pages: list[str]) -> str:
    def public_url(page: str) -> str:
        path = page.replace("index.html", "")
        return f"{ORIGIN}/{path}"

    urls = "\n".join(
        f"""  <url>
    <loc>{public_url(page)}</loc>
    <lastmod>2026-11-16</lastmod>
    <priority>{'1.0' if page == 'index.html' else '0.7'}</priority>
  </url>"""
        for page in pages
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def main() -> int:
    pages: dict[str, str] = {}

    pages["index.html"] = page_home()
    pages["work/index.html"] = page_work_index()
    for i, project in enumerate(PROJECTS):
        pages[f"work/{project['slug']}.html"] = page_work_detail(project, i)

    pages["labs/index.html"] = page_studio_home()
    pages["labs/work/index.html"] = page_studio_work_index()
    for i, project in enumerate(LABS_PROJECTS):
        pages[f"labs/work/{project['slug']}.html"] = page_studio_detail(project, i)

    pages["studio/index.html"] = page_studio_redirect()

    pages["404.html"] = page_404()

    for path, html in pages.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print(f"  {path}  ({len(html) // 1024} KiB)")

    (ROOT / "assets" / "copy.js").write_text(copy_js(), encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(MANIFEST, encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n", encoding="utf-8"
    )
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    public = [p for p in pages if p not in ("404.html", "studio/index.html")]
    (ROOT / "sitemap.xml").write_text(sitemap(public), encoding="utf-8")

    print(f"{len(pages)} pages, {len(COPY['vi'])} copy keys")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
