#!/usr/bin/env python3
"""Render the static site from a single source of truth.

Everything published is a plain file: HTML, one stylesheet, one behaviour script,
one copy dictionary. No runtime framework, no client-side router — upload the
repository root to any host and it works.

Outputs
  index.html                      profile home
  work/index.html                 project index
  work/<slug>.html                project detail            (4)
  studio/index.html               studio home
  studio/work/index.html          studio project index
  studio/work/<slug>.html         studio project detail      (3)
  404.html
  assets/copy.js                  VI/EN strings used by assets/site.js
  sitemap.xml

Usage: python3 tools/build_pages.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://nggkhaiz.js.org"
EMAIL = "nggkhaiz@proton.me"
DISCORD = "mental.arc"
GITHUB = "https://github.com/NggKhaiz"

YEAR = 2026

# ---------------------------------------------------------------- projects


PROJECTS = [
    {
        "slug": "public-file",
        "repo": "NggKhaiz/PUBLIC_FILE",
        "url": f"{GITHUB}/PUBLIC_FILE",
        "live": None,
        "title": "PUBLIC_FILE",
        "stack": ["Python", "CLI", "Obfuscation"],
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
            "vi": "Một script Python chạy được bằng CLI, không cần service. Đẩy lên GitHub là dùng được, không có bước build.",
            "en": "A Python script you run from a terminal — no service to host. Clone it and it works; there is no build step.",
        },
        "facts": [
            ("fact.lang", "Python"),
            ("fact.created", "05/2026"),
            ("fact.stars", "4 ★"),
            ("fact.license", "LICENSE"),
        ],
        "studio": {
            "tag": "A tool, just a tool",
            "summary": "An obfuscation scanner and a public file shelf. Written because obfuscated code is a legitimate puzzle, and because the tool that answers a question should be readable itself.",
            "ship": "Ships as a Python script. No daemon, no telemetry, no account.",
        },
    },
    {
        "slug": "rhlz-panel",
        "repo": "NggKhaiz/RHLZ-PANEL",
        "url": f"{GITHUB}/RHLZ-PANEL",
        "live": None,
        "title": "RHLZ Panel",
        "stack": ["TypeScript", "Docker", "Shell"],
        "cover": "assets/img/covers/rhlz-panel.png",
        "status": {"vi": "Thử nghiệm", "en": "Experimental"},
        "tagline": {
            "vi": "Panel tự host, đóng gói Docker, chạy được từ Procfile.",
            "en": "A self-hosted panel, Docker-packaged, deployable from a Procfile.",
        },
        "intro": {
            "vi": "Một bảng điều khiển nhỏ viết bằng TypeScript, có Dockerfile và Procfile để đẩy lên bất kỳ host container nào. Repo chưa có README — code là tài liệu duy nhất.",
            "en": "A small control panel in TypeScript with a Dockerfile and a Procfile, so it runs on any container host. The repo has no README yet — the code is the documentation.",
        },
        "why": {
            "vi": "Làm để xem một panel nhỏ có thể đi xa tới đâu trước khi nó cần một framework thật sự.",
            "en": "Built to find out how far a small panel can go before it needs a real framework.",
        },
        "how": {
            "vi": "Đóng gói container, cấu hình qua biến môi trường, chạy sau reverse proxy. Không phụ thuộc dịch vụ bên ngoài.",
            "en": "Ships as a container, configured through environment variables, meant to sit behind a reverse proxy. No external services required.",
        },
        "facts": [
            ("fact.lang", "TypeScript"),
            ("fact.created", "08/2026"),
            ("fact.deploy", "Docker · Procfile"),
            ("fact.readme", "fact.readme.none"),
        ],
        "studio": {
            "tag": "A panel, nothing more",
            "summary": "A self-hosted control panel that deploys from a Procfile and runs anywhere Docker does. Built to find the point where a small panel stops being small.",
            "ship": "Container image, environment variables, reverse proxy. Nothing to sign up for.",
        },
    },
    {
        "slug": "nggkhaiz-site",
        "repo": "NggKhaiz/NggKhaiz",
        "url": f"{GITHUB}/NggKhaiz",
        "live": ORIGIN,
        "title": "nggkhaiz.js.org",
        "stack": ["HTML", "CSS", "JavaScript"],
        "cover": "assets/img/covers/nggkhaiz-site.png",
        "status": {"vi": "Đang chạy", "en": "Live"},
        "tagline": {
            "vi": "Trang bạn đang đọc: HTML và CSS viết tay, không framework.",
            "en": "The page you are reading: hand-written HTML and CSS, no framework.",
        },
        "intro": {
            "vi": "Một stylesheet, một file JS, font tự host. Không bundler, không router, không dependency nào phải cập nhật.",
            "en": "One stylesheet, one script, self-hosted fonts. No bundler, no router, no dependency to keep updating.",
        },
        "why": {
            "vi": "Mình muốn một trang mở ra là thấy ngay, kể cả mạng chậm, và đọc được cả khi JavaScript bị tắt.",
            "en": "I wanted a page that opens instantly, even on a bad connection, and still reads with JavaScript switched off.",
        },
        "how": {
            "vi": "Deploy bằng GitHub Pages từ một nhánh. Sáng/tối và VI/EN lưu trong localStorage, không có cookie, không analytics.",
            "en": "Deployed with GitHub Pages from one branch. Theme and language live in localStorage — no cookies, no analytics.",
        },
        "facts": [
            ("fact.lang", "HTML · CSS"),
            ("fact.deploy", "GitHub Pages"),
            ("fact.fonts", "fact.selfhost"),
            ("fact.tracking", "fact.none"),
        ],
        "studio": {
            "tag": "A site, hand-written",
            "summary": "This site and the page behind this one: two files of markup, one stylesheet, one script. No framework to keep alive, nothing to rebuild next year.",
            "ship": "Static files on GitHub Pages. Loads without a build step and without third-party scripts.",
        },
    },
    {
        "slug": "this-profile",
        "repo": "NggKhaiz/NggKhaiz",
        "url": f"{GITHUB}/NggKhaiz",
        "live": None,
        "title": "This profile",
        "stack": ["Python", "SVG", "Images"],
        "cover": "assets/img/covers/this-profile.png",
        "status": {"vi": "Sinh tự động", "en": "Generated"},
        "tagline": {
            "vi": "README và toàn bộ ảnh SVG, sinh từ ba script Python.",
            "en": "The README and every SVG, produced by three Python scripts.",
        },
        "intro": {
            "vi": "Hero, card dự án và bảng highlights đều là SVG sinh ra từ `tools/build_assets.py`, nên bản sáng và bản tối không bao giờ lệch nhau.",
            "en": "The hero, project cards and highlights strip are SVG generated by `tools/build_assets.py`, so the dark and light versions can never drift apart.",
        },
        "why": {
            "vi": "Sửa số liệu ở một chỗ, chạy lại script, mọi ảnh tự cập nhật. Không chỉnh tay từng file SVG.",
            "en": "Change a number in one place, rerun the script, every image follows. No hand-editing SVG.",
        },
        "how": {
            "vi": "Ba script: ảnh SVG cho README, ảnh raster (icon, OG, cover) bằng Pillow, và trang HTML từ dữ liệu.",
            "en": "Three scripts: SVG for the README, raster images (icons, OG, covers) with Pillow, and the HTML pages from data.",
        },
        "facts": [
            ("fact.lang", "Python"),
            ("fact.output", "12 pages · 19 images"),
            ("fact.fonts", "Inter · JetBrains Mono"),
            ("fact.build", "fact.manual"),
        ],
        "studio": {
            "tag": "A profile, generated",
            "summary": "The README and every image behind it, produced from data so the two colour schemes stay in sync. The same source renders these pages.",
            "ship": "Static output committed to the repository. Regenerate with one command.",
        },
    },
]

PROFILE_PROJECTS = PROJECTS  # profile pages show all four
STUDIO_PROJECTS = [p for p in PROJECTS if p["slug"] != "this-profile"]

PROJECT_BY_SLUG = {p["slug"]: p for p in PROJECTS}

# ---------------------------------------------------------------- copy (VI/EN)

COPY: dict[str, dict[str, str]] = {
    "vi": {},
    "en": {},
}


def add(key: str, vi: str, en: str) -> None:
    COPY["vi"][key] = vi
    COPY["en"][key] = en


# global
add("a11y.skip", "Bỏ qua tới nội dung", "Skip to content")
add("a11y.lang", "Đổi ngôn ngữ", "Switch language")
add("a11y.theme", "Đổi giao diện sáng/tối", "Switch light or dark theme")
add("nav.home", "Trang chủ", "Home")
add("nav.about", "Giới thiệu", "About")
add("nav.work", "Dự án", "Work")
add("nav.domains", "Lĩnh vực", "Domains")
add("nav.contact", "Liên hệ", "Contact")
add("nav.studio", "Studio", "Studio")

# hero
add("hero.kicker", "Xin chào", "Welcome")
add("hero.age", "26 tuổi", "26 years old")
add("hero.role", "Lập trình viên · Builder", "Developer · Builder")
add(
    "hero.tagline",
    "Mình viết code, phá thử, rồi ghép lại — để một ý tưởng thành thứ người khác chạy được thật.",
    "I write code, break it on purpose, and put it back together — so an idea becomes something you can actually run.",
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
    "Mình là <strong>Khải</strong>, ở Bắc Giang. Mình bắt đầu với C++ vì trình biên dịch rất thẳng thắn: hoặc chạy, hoặc không. Thói quen đó ở lại — mình thích chương trình nhỏ, dự án thật, và code có thể giải thích từng dòng.",
    "I am <strong>Khải</strong>, from Bắc Giang. I started with C++ because a compiler is brutally honest: it runs or it does not. The habit stuck — I like small programs, real projects and code I can explain line by line.",
)
add(
    "about.p2",
    "Phần lớn thứ mình làm nằm công khai: một trình quét code bị làm rối bằng Python, một panel chạy được bằng Docker, và trang này — HTML/CSS viết tay, không framework, không bước build. Mình thích cảm giác đẩy lên rồi xem nó có sống không.",
    "Most of what I build lives in public: a Python scanner for obfuscated code, a Docker-ready panel, and this site — hand-written HTML and CSS, no framework, no build step. I like pushing something live and finding out whether it survives.",
)
add("about.locationKey", "Vị trí", "Location")
add("about.locationValue", "Bắc Giang, Việt Nam", "Bắc Giang, Việt Nam")
add("about.focusKey", "Đang tập trung", "Focus")
add("about.focusValue", "C++, Python, web thuần", "C++, Python, plain web")
add("about.learnKey", "Đang học", "Learning")
add("about.learnValue", "Hệ thống, bảo mật cơ bản", "Systems, security basics")

# credentials
add("cred.kicker", "Năng lực", "Credentials")
add("cred.title", "Con số nhỏ, nhưng là thật.", "Small numbers, all of them real.")
add(
    "cred.lede",
    "Không có chứng chỉ để khoe. Chỉ có repo, commit và những thứ đã chạy được.",
    "No certificates to show off. Just repos, commits and things that already ran.",
)
add("cred.one.title", "Repo công khai", "Public repositories")
add(
    "cred.one.text",
    "Từ tháng 12/2025, mỗi repo là một lý do để học thêm: công cụ, thử nghiệm, panel nhỏ.",
    "Since December 2025 every repo has been a reason to learn something: tools, experiments, small panels.",
)
add("cred.two.title", "Ngôn ngữ trong repo", "Languages in my repos")
add(
    "cred.two.text",
    "C++, Python, TypeScript, JavaScript, HTML/CSS, Rust — chọn theo việc cần làm, không theo mốt.",
    "C++, Python, TypeScript, JavaScript, HTML/CSS, Rust — picked per job, not per trend.",
)
add("cred.three.title", "Điều đang theo đuổi", "What I am after")
add(
    "cred.three.text",
    "Hiểu máy chạy thế nào, viết code đọc được, và giữ thói quen đẩy sản phẩm ra ngoài.",
    "Understanding how the machine actually works, writing readable code, and keeping the habit of shipping.",
)

# work
add("work.kicker", "Dự án", "Work")
add("work.title", "Vài thứ đã làm xong.", "A few things, finished.")
add(
    "work.lede",
    "Chọn lọc, không phải tất cả. Cái nào cũng có link để bạn tự kiểm tra.",
    "Selected, not everything. Each one links somewhere you can check.",
)
add("work.more", "Xem tất cả dự án", "See all projects")
add("work.open", "Mở dự án", "Open project")
add("work.count", "04 dự án", "04 projects")
add("work.index.title", "Tất cả những gì đã ship.", "Everything that shipped.")
add(
    "work.index.lede",
    "Bốn repo, mỗi cái một lý do để học. Cái nào chưa xong mình vẫn ghi rõ là chưa xong.",
    "Four repositories, each one a reason to learn. The unfinished ones are labelled unfinished.",
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
    "Thứ mình đang đọc thêm: cách CPU và bộ nhớ làm việc, cách một request đi qua một hệ thống, và cách viết giao diện ít nhưng đúng.",
    "Currently reading up on: how CPU and memory work, how a request travels through a system, and how to write interfaces that say less but mean more.",
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
add("contact.telegram", "Telegram", "Telegram")

# footer
add("footer.rights", "làm bằng tay", "made by hand")
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
) -> str:
    depth = len(path.split("/")) - 1  # nested folders below the host root
    prefix = "../" * depth
    lang = "en" if studio else "vi"
    lang_switch = "" if studio else ' data-lang-switch="on"'
    canonical = f"{ORIGIN}/{path}"

    if studio:
        nav = (
            f'<a href="{prefix}studio/work/">{t("nav.work", "span") if False else "Work"}</a>'
            f'<a href="{prefix}studio/#people">People</a>'
            f'<a href="{prefix}studio/#contact">Contact</a>'
            f'<a href="{prefix}index.html">← Profile</a>'
        )
        wordmark = f'<a class="wordmark" href="{prefix}studio/index.html"><span class="wordmark__dot" aria-hidden="true"></span><span>NggKhaiz Studio</span></a>'
        controls = (
            '<button class="control" id="theme-toggle" type="button" aria-label="Toggle light and dark theme">'
            f"{ICON_SUN}{ICON_MOON}</button>"
        )
        footer_links = (
            f'<a href="{prefix}studio/work/">Work</a>'
            f'<a href="{prefix}studio/#people">People</a>'
            f'<a href="{prefix}studio/#contact">Contact</a>'
            f'<a href="{prefix}index.html">Profile</a>'
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
            f'<a href="{prefix}studio/index.html">{t("nav.studio")}</a>'
            f'<a href="{prefix}index.html#contact">{t("nav.contact")}</a>'
            f'<a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub</a>'
        )

    skip = t("a11y.skip", "a", "skip-link").replace("<a ", '<a href="#main" ', 1)
    # t() renders a span; build the skip link explicitly instead
    skip = f'<a class="skip-link" href="#main" data-i18n="a11y.skip">{COPY["vi"]["a11y.skip"] if not studio else COPY["en"]["a11y.skip"]}</a>'

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="dark"{lang_switch}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="author" content="Nguyễn Gia Khải" />
  <meta name="theme-color" content="#0a0a0b" />
  <link rel="canonical" href="{canonical}" />

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
  <meta name="twitter:image" content="{ORIGIN}/{og_image}" />

  <link rel="icon" href="{prefix}assets/img/icons/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/img/icons/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="{prefix}assets/img/icons/favicon-16.png" />
  <link rel="apple-touch-icon" href="{prefix}assets/img/icons/apple-touch-icon.png" />
  <link rel="manifest" href="{prefix}site.webmanifest" />

  <script>document.documentElement.classList.add("js");</script>
  <link rel="preload" href="{prefix}assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}assets/fonts/inter-tight-var.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{prefix}assets/site.css" />
  <link rel="stylesheet" href="{prefix}assets/pages.css" />
</head>

<body id="top">
  {skip}

  <header class="site-header" id="header">
    <div class="shell site-header__inner">
      {wordmark}
      <nav class="site-nav" aria-label="{'Studio' if studio else 'Chính'}">{nav}</nav>
      <div class="header-controls">{controls}</div>
    </div>
    <div class="progress" id="progress" aria-hidden="true"></div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="shell site-footer__inner">
      <p>© <span id="year">{YEAR}</span> {'NggKhaiz Studio · independent, non-commercial' if studio else 'Nguyễn Gia Khải'} · {'' if studio else t('footer.rights')}</p>
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
                <a href="{{prefix}}studio/index.html">Studio <span class="arrow">↗</span></a>
                <a href="{GITHUB}/NggKhaiz" target="_blank" rel="noopener noreferrer">{t("contact.repo")}</a>
              </div>
            </div>
          </div>
        </div>"""

# ---------------------------------------------------------------- pages


def page_home() -> str:
    prefix = ""
    rows = "\n\n".join(work_row(p, i + 1, prefix) for i, p in enumerate(PROJECTS))
    contact = CONTACT_BLOCK.replace("{prefix}", prefix)

    body = f"""    <!-- ============ HERO ============ -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__rings" aria-hidden="true"><span></span><span></span><span></span><span></span></div>

      <div class="shell hero__grid">
        <div class="hero__lead">
          <p class="hero__kicker label">{t("hero.kicker", "span")}</p>

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
            <p class="card__num">12</p>
            <h3 class="card__title">{t("cred.one.title")}</h3>
            <p class="card__text">{t("cred.one.text")}</p>
          </article>
          <article class="card reveal" style="--d: 90ms">
            <p class="card__num">06</p>
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

    <!-- ============ 04 DOMAINS ============ -->
    <section class="section" id="domains" aria-labelledby="domains-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">04 / {t("domains.kicker")}</p>
          <h2 class="section__title" id="domains-title">{t("domains.title", "span")}</h2>
          <p class="section__lede">{t("domains.lede")}</p>
        </div>

        <ul class="domains reveal">
          <li>C++</li><li>Python</li><li>TypeScript</li><li>JavaScript</li><li>HTML</li><li>CSS</li>
          <li>Rust</li><li>Shell</li><li>PowerShell</li><li>Docker</li><li>Cloudflare Workers</li>
          <li>Git</li><li>Obfuscated code</li><li>UI &amp; typography</li>
        </ul>

        <p class="domains__note reveal">{t("domains.note")}</p>
      </div>
    </section>

    <!-- ============ 05 CONTACT ============ -->
    <section class="section" id="contact" aria-labelledby="contact-title">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">05 / {t("contact.kicker")}</p>
          <h2 class="section__title" id="contact-title">{t("contact.title", "span")}</h2>
        </div>

{contact}

        <div class="signature reveal">
          <pre><span class="cm">// dấu vết cá nhân, giữ nguyên từ bản cũ</span>
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
        title="Nguyễn Gia Khải — developer, builder",
        description=(
            "Nguyễn Gia Khải (Ngg.Khaiz) — Bắc Giang, Việt Nam. C++, Python, TypeScript và web viết tay. "
            f"Xây những thứ chạy được thật. Liên hệ: {EMAIL}."
        ),
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
        description="Bốn dự án công khai: trình quét code bị làm rối, panel tự host, trang web này và bộ sinh ảnh profile.",
        body=body,
    )


def page_work_detail(project: dict, index: int) -> str:
    slug = project["slug"]
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    facts = "".join(
        f'<div><dt class="label">{t(key)}</dt><dd>{t(value) if value.startswith("fact.") else esc(value)}</dd></div>'
        for key, value in project["facts"]
    )
    links = [f'<a href="{project["url"]}" target="_blank" rel="noopener noreferrer">{t("d.source")} <span class="arrow">↗</span></a>']
    if project["live"]:
        links.append(f'<a href="{project["live"]}" target="_blank" rel="noopener noreferrer">{t("d.live")} <span class="arrow">↗</span></a>')
    links.append(f'<a href="mailto:{EMAIL}?subject={slug}">{t("d.email")} <span class="arrow">↗</span></a>')

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
        <img src="../{project['cover']}" alt="Cover cho dự án {esc(project['title'])}" width="1200" height="675" />
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
        body=body,
    )


def page_studio_home() -> str:
    cards = "\n".join(studio_feature(p, "") for p in STUDIO_PROJECTS)
    body = f"""    <section class="studio-hero">
      <div class="shell studio-hero__grid">
        <div>
          <p class="label label--accent">Independent software studio</p>
          <h1>Independent.<br /><em>Open by design.</em></h1>
          <p class="studio-hero__lede">
            Software that respects you. Source in the open, no tracking, no ads — made to do its job well
            and then get out of the way.
          </p>
          <div class="studio-hero__actions">
            <a class="btn btn--solid" href="work/">Projects
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </a>
            <a class="btn btn--ghost" href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub {ICON_ARROW}</a>
          </div>
        </div>

        <aside class="fig reveal">
          <div class="fig__head"><span class="label">Fig. 001</span><span class="label">Est. 2025</span></div>
          <div class="fig__rule"></div>
          <p class="fig__big">Software, with principles.</p>
          <div class="fig__list">
            <span>One person, on purpose</span>
            <span>Open source, nothing to hide</span>
            <span>No telemetry, ever</span>
            <span>Free to use, free to fork</span>
          </div>
        </aside>
      </div>
    </section>

    <div class="shell">
      <div class="strip">
        <span>Less noise. <strong>More intent.</strong></span>
        <span>Small output · Deliberate work</span>
      </div>
    </div>

    <section class="section" id="work">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">01 / Selected work</p>
          <h2 class="section__title">Built to be used.</h2>
          <p class="section__lede">A short list, because the list is short. Everything below is public.</p>
        </div>
{cards}
        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="work/">All projects
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>
          </a>
        </div>
      </div>
    </section>

    <section class="section" id="people">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">02 / The people</p>
          <h2 class="section__title">A team of one, on purpose.</h2>
          <p class="section__lede">Keeping it small means every decision has an owner, and the code can stay honest.</p>
        </div>

        <div class="people">
          <article class="person reveal">
            <p class="person__index">01</p>
            <h3 class="person__name">Nguyễn Gia Khải</h3>
            <p class="person__role">Founder · Code, security curiosity, design</p>
            <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">github.com/NggKhaiz ↗</a>
          </article>
          <article class="person reveal" style="--d: 90ms">
            <p class="person__index">02</p>
            <h3 class="person__name">Open chairs</h3>
            <p class="person__role">No hires, no contractors, no roadmap pressure. Contributions by pull request are welcome.</p>
            <a href="{GITHUB}?tab=repositories" target="_blank" rel="noopener noreferrer">Browse repositories ↗</a>
          </article>
        </div>
      </div>
    </section>

    <section class="section" id="contact">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">03 / Get in touch</p>
          <h2 class="section__title">A direct line.</h2>
          <p class="section__lede">Questions, bug reports, or something worth building together — one inbox, read by one person.</p>
        </div>

        <div class="contact reveal">
          <div>
            <a class="contact__big" href="mailto:{EMAIL}">
              <span>{EMAIL}</span>
              {ICON_ARROW}
            </a>
            <p class="contact__note">Issues and pull requests reach the same desk.</p>
          </div>

          <div class="contact__grid">
            <div class="contact__block">
              <h3>Elsewhere</h3>
              <div class="contact__links" data-contact-direct>
                <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub <span class="arrow">↗</span></a>
                <button class="contact__copy" type="button" data-copy="{DISCORD}" aria-label="Copy the Discord username {DISCORD}">
                  <span class="contact__copy-handle">Discord · @{DISCORD}</span>
                  <span class="contact__copy-hint">copy</span>
                </button>
                <a href="{ORIGIN}" target="_blank" rel="noopener noreferrer">nggkhaiz.js.org <span class="arrow">↗</span></a>
              </div>
            </div>
            <div class="contact__block">
              <h3>This site</h3>
              <div class="contact__links">
                <a href="../index.html">Profile <span class="arrow">↗</span></a>
                <a href="{GITHUB}/NggKhaiz" target="_blank" rel="noopener noreferrer">Source of this site <span class="arrow">↗</span></a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="fine">
      <div class="shell">
        <div class="section__head reveal">
          <p class="section__num">04 / The fine print</p>
          <h2 class="section__title">Clear by default.</h2>
          <p class="section__lede">Commitments written down, without the small print pretending to be big.</p>
        </div>

        <div class="fine reveal">
          <details>
            <summary><span class="n">01</span> A personal, non-commercial initiative <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>NggKhaiz Studio is a personal open-source effort, not a company and not a registered organisation. Nothing here is monetised: no advertising, no paid tiers, no data sold.</p>
              <p>Projects are published for learning, for use, and for review. Maintenance and support follow the free time of one person, so there is no uptime promise attached.</p>
            </div>
          </details>
          <details>
            <summary><span class="n">02</span> Zero data collection <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>These pages ship no analytics, no advertising trackers and no telemetry. No cookies are set for tracking, and the fonts are served from this domain.</p>
              <p>Two preferences are stored in your browser's localStorage only: the interface theme and the language. Clearing site data removes both. Links to GitHub take you to a service outside this site, under its own policies.</p>
            </div>
          </details>
          <details>
            <summary><span class="n">03</span> Third-party content and services <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>Projects are independent and not affiliated with, endorsed by, or representatives of any third-party platform or service unless stated explicitly.</p>
              <p>Third-party services may change or disappear at any time. Software is provided as available, without guarantee of uninterrupted service.</p>
            </div>
          </details>
          <details>
            <summary><span class="n">04</span> Source code licensing <span class="plus">+</span></summary>
            <div class="fine__body">
              <p>Source is published in public repositories for transparent review. Permission to use, modify and redistribute each project is governed only by the license included in that repository.</p>
              <p>Check the LICENSE file before redistributing. Third-party dependencies keep their own licenses and attribution requirements. The typefaces here are Inter, Inter Tight and JetBrains Mono, all under the SIL Open Font License 1.1.</p>
            </div>
          </details>
        </div>
      </div>
    </section>"""

    return layout(
        path="studio/index.html",
        title="NggKhaiz Studio — Independent, open by design",
        description="An independent, non-commercial open-source initiative. Software with no tracking, no ads and the source in the open.",
        og_image="assets/img/social/og-studio.png",
        studio=True,
        body=body,
    )


def studio_feature(project: dict, prefix: str) -> str:
    tags = "".join(f"<span>{esc(tag)}</span>" for tag in project["stack"])
    return f"""        <article class="feature reveal">
          <div>
            <p class="feature__tag">{esc(project['studio']['tag'])}</p>
            <h3 class="feature__title"><a href="{prefix}work/{project['slug']}.html">{esc(project['title'])}</a></h3>
            <div class="feature__meta">{tags}</div>
            <div class="feature__links">
              <a class="btn btn--ghost" href="{prefix}work/{project['slug']}.html">Read more {ICON_ARROW}</a>
              <a class="btn btn--ghost" href="{project['url']}" target="_blank" rel="noopener noreferrer">Source code {ICON_ARROW}</a>
            </div>
          </div>
          <div class="feature__body--end">
            <p class="feature__text">{esc(project['studio']['summary'])}</p>
          </div>
        </article>"""


def page_studio_work_index() -> str:
    cards = "\n".join(
        f"""          <a class="postcard reveal" href="{p['slug']}.html">
            <span class="postcard__media"><img src="../../{p['cover']}" alt="" width="1200" height="675" loading="lazy" /></span>
            <span class="postcard__body">
              <span class="postcard__head">
                <span class="postcard__title">{esc(p['title'])}</span>
                <span class="postcard__status">{esc(p['studio']['tag'])}</span>
              </span>
              <span class="postcard__text">{esc(p['tagline']['en'])}</span>
              <span class="postcard__tags">{"".join(f"<span>{esc(tag)}</span>" for tag in p['stack'])}</span>
            </span>
          </a>"""
        for p in STUDIO_PROJECTS
    )
    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">Studio</a><span aria-hidden="true">/</span><span>Work</span>
        </nav>
        <div class="page-head__grid">
          <h1 class="page-title reveal">Everything in the open.</h1>
          <p class="page-lede reveal">Three projects, each one small enough to read in an afternoon.</p>
        </div>
        <p class="page-meta reveal">03 projects · {YEAR}</p>
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
        path="studio/work/index.html",
        title="Work — NggKhaiz Studio",
        description="Open-source projects from NggKhaiz Studio: an obfuscation scanner, a self-hosted panel and this site.",
        studio=True,
        body=body,
    )


def page_studio_detail(project: dict, index: int) -> str:
    slug = project["slug"]
    nxt = STUDIO_PROJECTS[(index + 1) % len(STUDIO_PROJECTS)]
    facts = "".join(
        f'<div><dt class="label">{esc(key)}</dt><dd>{esc(value)}</dd></div>'
        for key, value in [
            ("Status", project["status"]["en"]),
            ("Stack", " · ".join(project["stack"])),
            ("Repository", project["repo"]),
        ]
    )
    live = (
        f'<a href="{project["live"]}" target="_blank" rel="noopener noreferrer">Live <span class="arrow">↗</span></a>'
        if project["live"]
        else ""
    )
    body = f"""    <section class="page-head">
      <div class="shell">
        <nav class="crumbs reveal" aria-label="Breadcrumb">
          <a href="../index.html">Studio</a><span aria-hidden="true">/</span>
          <a href="index.html">Work</a><span aria-hidden="true">/</span>
          <span>{esc(project['title'])}</span>
        </nav>
        <div class="page-head__grid">
          <h1 class="page-title reveal">{esc(project['title'])}</h1>
          <p class="page-lede reveal">{esc(project['tagline']['en'])}</p>
        </div>
        <p class="page-meta reveal">{esc(project['studio']['tag'])} · {YEAR}</p>
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
            <h2>What it is</h2>
            <p>{esc(project['studio']['summary'])}</p>
            <h2>How it ships</h2>
            <p>{esc(project['studio']['ship'])}</p>
            <h2>What is next</h2>
            <p>Small fixes, clearer docs and whatever the next idea needs. There is no roadmap beyond that, and no promise of one.</p>
          </article>
        </div>

        <aside class="detail__aside reveal" style="--d: 120ms">
          <h3 class="label">At a glance</h3>
          <dl class="detail__facts">{facts}</dl>
          <h3 class="label">Links</h3>
          <div class="contact__links">
            <a href="{project['url']}" target="_blank" rel="noopener noreferrer">Source <span class="arrow">↗</span></a>
            {live}
            <a href="mailto:{EMAIL}?subject={slug}">Ask about this project <span class="arrow">↗</span></a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="shell">
        <a class="nextup reveal" href="{nxt['slug']}.html">
          <span class="label">Next project</span>
          <span class="nextup__title">{esc(nxt['title'])}{ICON_ARROW}</span>
          <span class="nextup__text">{esc(nxt['tagline']['en'])}</span>
        </a>
        <div class="section__foot reveal">
          <a class="btn btn--ghost" href="index.html">Back to all projects</a>
        </div>
      </div>
    </section>"""

    return layout(
        path=f"studio/work/{slug}.html",
        title=f"{project['title']} — NggKhaiz Studio",
        description=project["tagline"]["en"],
        og_image=project["cover"],
        og_type="article",
        studio=True,
        body=body,
    )


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
  "description": "Developer, builder, Bắc Giang, Việt Nam.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#0a0a0b",
  "theme_color": "#0a0a0b",
  "icons": [
    { "src": "/assets/img/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/assets/img/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/assets/img/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
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

    pages["studio/index.html"] = page_studio_home()
    pages["studio/work/index.html"] = page_studio_work_index()
    for i, project in enumerate(STUDIO_PROJECTS):
        pages[f"studio/work/{project['slug']}.html"] = page_studio_detail(project, i)

    pages["404.html"] = page_404()

    for path, html in pages.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print(f"  {path}  ({len(html) // 1024} KiB)")

    (ROOT / "assets" / "copy.js").write_text(copy_js(), encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(MANIFEST, encoding="utf-8")

    public = [p for p in pages if p != "404.html"]
    (ROOT / "sitemap.xml").write_text(sitemap(public), encoding="utf-8")

    print(f"{len(pages)} pages, {len(COPY['vi'])} copy keys")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
