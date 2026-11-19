# Data — where every number comes from

The profile README, the SVG cards and the site pages do not contain hand-typed
numbers. They are rendered from `data/profile.json`, which is written by
`tools/fetch_stats.py` straight out of the GitHub GraphQL API.

```
GitHub GraphQL API
        │  tools/fetch_stats.py
        ▼
data/profile.json ──┬── tools/build_readme.py   → README.md
                    ├── tools/build_assets.py   → assets/hero-*.svg, assets/projects/*.svg,
                    │                             assets/highlights-*.svg
                    └── tools/build_pages.py    → 15 HTML pages, assets/copy.js
```

`tools/build_images.py` (the raster images) reads the palette from
`tools/palette.py`, not from this file, so the two colour schemes cannot drift
apart either.

## What is in `data/profile.json`

| Key | Meaning |
| --- | --- |
| `generated_at` | ISO-8601 UTC timestamp of the fetch. Kept for the record; never printed in the README |
| `user.contributions` | `contributionCalendar.totalContributions` for the last year |
| `user.public_repos` / `org_repos` | public repositories owned by the account / by the organisation |
| `user.source_repos` / `forks` | split of the above by `isFork` |
| `user.source_commits` | commit count summed over repositories the owner wrote, forks excluded |
| `user.total_stars` | stars summed over every scanned repository |
| `languages` | byte share per language, **forks excluded** |
| `languages_with_forks` | the same including forks, for anyone who wants the raw view |
| `repos[]` | one entry per repository: `repo`, `owner`, `commits`, `stars`, `forks`, `language`, `license`, `fork`, `pushed_at`, `languages[]` |

Forked repositories are listed but never counted in a total: their commits belong
to upstream, and 10 501 inherited commits should not read as work done here.

## Refresh it

```bash
python3 tools/fetch_stats.py      # needs GITHUB_TOKEN / GH_TOKEN or `gh auth login`
python3 tools/build_assets.py
python3 tools/build_pages.py
python3 tools/build_readme.py
```

`tools/build_readme.py --check` exits non-zero when `README.md` differs from a
fresh render, so a stale README fails CI instead of shipping.

## Keep it current without thinking about it

Copy the workflow into place once:

```bash
mkdir -p .github/workflows
cp tools/workflows/profile-data.yml .github/workflows/profile-data.yml
git add .github/workflows/profile-data.yml && git commit -m "ci: refresh profile data nightly" && git push
```

It runs daily at 04:17 ICT, on every push that touches `tools/**` or `data/**`,
and on demand. It renders everything and commits **only if the output changed** —
the build is deterministic (no timestamps in the output), so a quiet week
produces no commits.

`tools/workflows/` exists because a GitHub App without the `workflows`
permission cannot push into `.github/workflows/`. The same applies to
`tools/graph-art.workflow.yml`.

## What is not generated

Prose. Every sentence in `tools/build_pages.py` and `tools/build_readme.py` is
written by the owner; the pipeline only fills in the numbers inside those
sentences. Nothing here invents a metric, and nothing rounds a number in a
flattering direction.
