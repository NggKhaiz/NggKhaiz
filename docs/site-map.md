# Page map

Every page is a static file. Relative links only, so the repository root can be
uploaded to any host (GitHub Pages, Netlify, Cloudflare Pages, a VPS) without a
base-path setting.

| URL | File | Language | Purpose |
| --- | --- | --- | --- |
| `/` | `index.html` | VI / EN | profile: hero, about, credentials, work, lab, domains, contact |
| `/work/` | `work/index.html` | VI / EN | all six projects, cover cards |
| `/work/zmrig.html` | `work/zmrig.html` | VI / EN | project detail |
| `/work/qfox.html` | `work/qfox.html` | VI / EN | project detail |
| `/work/study-site.html` | `work/study-site.html` | VI / EN | project detail |
| `/work/public-file.html` | `work/public-file.html` | VI / EN | project detail |
| `/work/molik-winlik.html` | `work/molik-winlik.html` | VI / EN | project detail, with the upstream credit note |
| `/work/this-profile.html` | `work/this-profile.html` | VI / EN | how this site is generated |
| `/labs/` | `labs/index.html` | VI / EN | MoLik Labs: work, people, contact, fine print |
| `/labs/work/` | `labs/work/index.html` | VI / EN | lab project index (three) |
| `/labs/work/zmrig.html` | `labs/work/zmrig.html` | VI / EN | lab project detail |
| `/labs/work/qfox.html` | `labs/work/qfox.html` | VI / EN | lab project detail |
| `/labs/work/study-site.html` | `labs/work/study-site.html` | VI / EN | lab project detail |
| `/studio/` | `studio/index.html` | — | redirect stub to `/labs/` (kept so old links land somewhere) |
| `/404.html` | `404.html` | VI / EN | not found (no canonical, `noindex`) |
| `/robots.txt` | `robots.txt` | — | allow all + sitemap pointer |
| `/sitemap.xml` | `sitemap.xml` | — | 13 public URLs, `lastmod` set |

Metadata: every page carries a canonical URL (directory form, no `/index.html`),
OpenGraph and Twitter cards with an absolute image, `og:locale` plus the alternate,
and JSON-LD — `Person` + `WebSite` on the profile, `SoftwareSourceCode` and
`BreadcrumbList` on each project, `Organization` on MoLik Labs. The 404 page is
`noindex` and deliberately has no canonical.

`.nojekyll` keeps GitHub Pages from running Jekyll over the output, so folders that
start with an underscore would still be served if they ever appear.

Language: every page defaults to Vietnamese and carries a VI/EN toggle
(`assets/copy.js` + `data-lang-switch`). The lab pages used to be English-only like the
reference studio; they now share the same toggle and the same dictionary, so no string
exists in one language only.

Assets

| Path | What |
| --- | --- |
| `assets/site.css` | tokens, type scale, layout, components |
| `assets/pages.css` | inner-page furniture + lab sections |
| `assets/site.js` | theme, language, reveal, copy-to-clipboard |
| `assets/copy.js` | VI/EN strings (generated) |
| `assets/fonts/*.woff2` | Inter, Inter Tight, JetBrains Mono — self-hosted, OFL 1.1 |
| `assets/img/icons/` | favicon.ico, 16/32/48 png, apple-touch-icon, PWA 192/512 |
| `assets/img/social/` | OG cards, GitHub social preview, X header, Discord banner, avatars |
| `assets/img/covers/` | 1200×675 cover per project |
| `assets/*.svg` | profile README images (hero, project cards, highlights) |

Regeneration

```bash
python3 tools/fetch_fonts.py    # woff2 subsets (needs fonttools + brotli, network)
python3 tools/build_images.py   # raster images (needs pillow + fonts in .cache)
python3 tools/build_assets.py   # README SVGs
python3 tools/build_pages.py    # HTML, copy.js, sitemap.xml, site.webmanifest
python3 tools/graph_art.py plan # rebuild the contribution-art plan (optional)
```

Nothing in `assets/` or the HTML is meant to be edited by hand: change the
Python sources in `tools/` and re-run them.
