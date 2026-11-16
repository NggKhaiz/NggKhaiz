# Clone notes — what was observed, what was inferred

This repository is a rebuild of three references, with all identity content replaced by
Nguyễn Gia Khải's. Method follows the evidence-first workflow of
[`morluto/rea` → `reverse-engineer-anything`](https://github.com/morluto/rea): collect the
shipped artifact, record observations separately from inferences, and keep the unknowns
visible instead of filling them in silently.

Sources

- `https://github.com/Sakayorii/Sakayorii` — profile README and its SVG assets (raw files read via the GitHub API)
- `https://sakayori.dev/` — personal site (text content only)
- `https://sakayori.studio/` — studio site (text content only)
- `https://api.github.com/users/NggKhaiz`, `/repos`, and a GraphQL `contributionsCollection` query for the real numbers

---

## 1. Observed — profile README (verbatim structure)

Read from `Sakayorii/Sakayorii@main`. These are measurements of the actual artifact, not guesses:

| Element | Observation |
| --- | --- |
| README skeleton | `<picture>` hero → 3 badge row → rule → **About me** → **Selected work** (2×2 cards) → **Toolbox** (flat-square badge row) → **Activity** (streak) → **Highlights** → rule → `<sub>` footer |
| Hero SVG | `1600×360`, background `#131313`, avatar plate `circle(172,180,r=97)` white with `avatarClip r=94`, decorative rings right at `cx=1680` (`r=215/330/445`, `stroke #262626`, `stroke-width 34`), name at `x=305 y=198` `104px/800/-2` `#f5f5f5`, tagline `x=310 y=256` `29px/300` `#a3a3a3`, four feature cells at `(965,78) (1260,78) (965,218) (1260,218)` with Lucide icons scaled `1.9` |
| Light hero | Same geometry; background `#fafafa`, rings `#efefef`/`#e7e7e7`, text `#111111`/`#737373` |
| Project card | `520×176`, `rect x=1 y=1 518×174 rx=14`, mono repo label `12px` + `open ↗` `13px`, title `22px/700`, description `14px`, language pills at `y=126 h=26 rx=7`, pill width `27.6 + 6.6 × len(text)`, next pill `+8` |
| Dark card | fill `#0d1117`, stroke `#30363d`, label `#8b949e`, title `#f0f6fc`, pill `#161b22` |
| Light card | fill `#ffffff`, stroke `#d0d7de`, label `#656d76`, title `#1f2328`, pill `#f6f8fa` |
| Highlights | `1160×190`, mono caption `GITHUB HIGHLIGHTS`, four `30px/700` values at `x = 28 + 285·i`, `13px` captions below |
| Badges | `style=for-the-badge`, site `#111827`, secondary `#6F4320`, handle `#181717`; toolbox uses `flat-square` with `0D1117`/`F6F8FA` and `logoColor` white/`111111` |
| Theme handling | Every image is a `<picture>` with `prefers-color-scheme: dark` and `light` sources |

## 2. Observed — the two sites (structure)

`sakayori.dev`: `Welcome` label → name → age → role → tagline → two CTAs → facts table
(`Field`, `Date of birth`, `Studio`) → `Scroll` → **01 About** (statement + two paragraphs +
`Location` / `Date of birth`) → **02 Credentials and expertise** (three cards with large
numerals: `04yrs`, `08yrs`, `∞`) → **03 Selected work** (numbered rows: title, category,
description) → **04 Technical domains** (flat list).

`sakayori.studio`: studio label → hero *“Independent. Open by design.”* + two CTAs →
`Fig. 001` caption card with three claim lines → `LESS NOISE. MORE INTENT.` strip →
**01 Selected work** (featured project with mono category, title, tag chips, two links) →
**02 The people** (numbered person cards) → **03 Get in touch** → **04 The fine print**
(4 numbered disclosures: non-profit, zero data collection, third-party, licensing).

## 3. Observed — Khải's own data (GitHub API, 2026-11-16)

- login `NggKhaiz`, name `Ngg.Khaiz`, location `Viet Nam`, blog `nggkhaiz.pages.dev`, no public email in the API
- 12 public repositories, 5 stars total, top repo `PUBLIC_FILE` with 4 stars, account created 2025-12-22
- repo languages: `D, HTML, JavaScript, Python, Rust, TypeScript`; `RHLZ-PANEL` adds `Shell`, `CSS`, `Dockerfile`
- contributions in the last year: **464**
- `PUBLIC_FILE` contains `obf-scanner.py`, `ravenst`, `kill.txt` → an obfuscation scanner, not a generic “file host”
- site domain comes from `CNAME`: `nggkhaiz.js.org`

## 4. Inferred — not verifiable from the available evidence

- **Fonts on sakayori.dev / .studio.** CSS was never served to this environment (only rendered
  text). The rebuild uses `Inter Tight` (display), `Inter` (text), `JetBrains Mono` (labels):
  a modern grotesk pairing consistent with the reference's tight, lowercase-and-caps mix.
- **Colour values of the sites.** Only the SVG assets expose exact hex values; those were
  reused (`#131313`, mono text ramp). The website palette (`#0a0a0b` / `#f4f2f0` + warm
  accent `#d9a06b`) is a deliberate interpretation of the same monochrome-plus-warm-badge language.
- **Motion.** Reveal-on-scroll, scroll progress, active-nav tracking and the sticky blur header
  are additions in that spirit; they are hidden from `prefers-reduced-motion`.
- **The `/studio/` page.** sakayori.studio describes a studio with two people and a legal
  fine-print section. This version is written as a personal, non-commercial initiative of one
  person — no invented co-founder, no invented company registration. Delete the folder if you
  do not want it.

## 5. Deliberately not cloned

The reference is a security analyst with certifications and eight years of experience. Copying
that copy verbatim would make this profile lie. The structure, type scale and section rhythm are
cloned; **the claims are Khải's own**: born 9 May 2000, 12 public repositories, real languages,
real projects. No fake certificates, no fake employers, no invented metrics.

## 6. Identity data — supplied by the owner

| Field | Value | Where it appears |
| --- | --- | --- |
| Date of birth | 09-05-2000 (9 May 2000, DD-MM-YYYY) | site facts table (`facts.dobValue`) |
| Age | derived: 26 | hero, both languages |
| Email | `nggkhaiz@proton.me` | README badge, hero CTA, contact block, studio page, `<meta name="description">` |
| Discord | `mental.arc` | README badge, contact block with copy-to-clipboard |
| Telegram | **withheld by request** | nowhere. `TELEGRAM_HANDLE = ""` in `assets/site.js` keeps the link out of the page; fill it in when you want it visible |
| Avatar | monogram `K` | hero SVG plate, app icons, `assets/img/social/avatar*.png` |

## 7. Unknowns — fill these in yourself

- the Telegram handle, whenever it should go live
- a real avatar photo for the hero: base64-encode a square image and set `AVATAR_DATA_URI`
  in `tools/build_assets.py`, then rebuild — the monogram plate disappears automatically
- whether `nggkhaiz.pages.dev` (profile blog) should be the primary URL instead of `nggkhaiz.js.org`

## 8. Structure

The site is 12 static pages (see `docs/site-map.md`) served from the repository root, so deploying
is "upload this folder". Profile pages are bilingual (VI default, EN toggle); studio pages stay in
English like the reference, and their `<html>` has no `data-lang-switch`, so the language script
never touches them.

Fonts are self-hosted: `tools/fetch_fonts.py` pulls Inter, Inter Tight and JetBrains Mono from the
Google Fonts repository and subsets them to Latin + Vietnamese (320 KiB total, OFL 1.1 licences kept
in `assets/fonts`). No request leaves the domain for type, and there is no third-party script.

## 9. Images

`tools/build_images.py` renders every raster asset with Pillow from the same design tokens as the
CSS: favicon set, apple-touch-icon, PWA 192/512, OG cards (profile + studio, dark + light), GitHub
social preview 1280×640, X header 1500×500, Discord banner 960×540, square avatars, and one
1200×675 cover per project. The covers are deliberately abstract UI studies — they are *not*
presented as screenshots of software that does not exist.

## 10. Rebuild

```bash
python3 tools/fetch_fonts.py    # woff2 subsets        (fonttools, brotli, network)
python3 tools/build_images.py   # 19 raster images     (pillow, fonts in .cache/fonts)
python3 tools/build_assets.py   # README SVGs
python3 tools/build_pages.py    # HTML + copy.js + sitemap + manifest
python3 -m http.server 8000     # preview http://localhost:8000
```

SVG content lives in `CONTENT` at the top of `tools/build_assets.py`; page copy and the project
records live in `tools/build_pages.py`, which also emits `assets/copy.js` so the two languages can
never drift apart. Nothing is fetched at runtime.
