# Page map

Every page is a static file. Relative links only, so the repository root can be
uploaded to any host (GitHub Pages, Netlify, Cloudflare Pages, a VPS) without a
base-path setting.

| URL | File | Language | Purpose |
| --- | --- | --- | --- |
| `/` | `index.html` | VI / EN | profile: hero, about, credentials, work, domains, contact |
| `/work/` | `work/index.html` | VI / EN | all four projects, cover cards |
| `/work/public-file.html` | `work/public-file.html` | VI / EN | project detail |
| `/work/rhlz-panel.html` | `work/rhlz-panel.html` | VI / EN | project detail |
| `/work/nggkhaiz-site.html` | `work/nggkhaiz-site.html` | VI / EN | project detail |
| `/work/this-profile.html` | `work/this-profile.html` | VI / EN | project detail |
| `/studio/` | `studio/index.html` | EN | studio: work, people, contact, fine print |
| `/studio/work/` | `studio/work/index.html` | EN | studio project index |
| `/studio/work/public-file.html` | `studio/work/public-file.html` | EN | studio project detail |
| `/studio/work/rhlz-panel.html` | `studio/work/rhlz-panel.html` | EN | studio project detail |
| `/studio/work/nggkhaiz-site.html` | `studio/work/nggkhaiz-site.html` | EN | studio project detail |
| `/404.html` | `404.html` | VI / EN | not found |

Assets

| Path | What |
| --- | --- |
| `assets/site.css` | tokens, type scale, layout, components |
| `assets/pages.css` | inner-page furniture + studio sections |
| `assets/site.js` | theme, language, reveal, copy-to-clipboard, optional Telegram link |
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
```
