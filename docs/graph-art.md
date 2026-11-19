# Graph art

The contribution calendar on the profile is drawn on purpose. This page explains
exactly how, so nobody has to guess.

## What it is

GitHub renders one square per day: 53 columns of weeks, 7 rows of days. That is
a 53×7 bitmap, so a text file with 53 characters on each of 7 lines is enough to
describe a picture. `tools/graph-art.txt` holds that picture; `tools/graph_art.py`
maps it onto real dates and creates one empty commit per pixel of shade.

Every commit is dated **12:00 +07:00** on its day and carries the message

```
chore: graph art 2026-04-19 (2/4)
```

so `git log --grep "graph art"` lists the whole drawing. Nothing is disguised as
real work: the commits are empty, the messages say what they are, and the tool
that makes them is in this repository.

## The characters

| Character | Commits that day | Shade |
| --- | --- | --- |
| space | 0 | empty |
| `.` | 1 | lightest |
| `-` | 2 | light |
| `+` | 3 | medium |
| `#` | 4 | darkest |

Four is enough: GitHub scales the shades against your own busiest day, so a day
with four commits already sits at the top of the scale for an account with
sparse activity.

## The frozen plan

`tools/graph-art.plan.json` is generated from the pattern and **committed**. It
holds explicit `{date, commits}` entries:

```json
{
  "anchor": "2026-01-04",
  "weeks": 53,
  "total_commits": 332,
  "entries": [{ "date": "2026-04-19", "commits": 4 }, ...]
}
```

Why freeze the dates instead of recomputing them on every run: the calendar
slides forward one week at a time, so a relative mapping would repaint different
days every Sunday and scramble the drawing. With absolute dates the schedule is
idempotent — it skips every cell that already has its commits — and the drawing
scrolls left out of the 53-week window on its own, like any old contribution.

New art means a new pattern and a new anchor:

```bash
python3 tools/graph_art.py plan      # rewrites the plan from tools/graph-art.txt
python3 tools/graph_art.py render    # ASCII preview of the frozen plan
python3 tools/graph_art.py verify    # how many commits are still missing
```

## Status

Painted on **2026-11-16**: 332 commits from plan v1 (the glyph `KHAI`, anchor
2026-01-04, cells between 2026-04-19 and 2026-09-26), authored as
`Nguyễn Gia Khải <251014756+NggKhaiz@users.noreply.github.com>` so the squares
land on the profile rather than on a bot.

Two consequences worth knowing:

- the painting lives in the branch history, so **merge the pull request with a merge
  commit, not with squash** — a squash collapses the 332 commits into one and the
  drawing disappears from the calendar;
- if it is squashed anyway, nothing is lost: the plan is committed, so installing the
  workflow and running it once repaints every cell on the default branch.

## Painting

```bash
python3 tools/graph_art.py apply \
  --author "Nguyễn Gia Khải <12345678+NggKhaiz@users.noreply.github.com>" \
  --yes --push
```

Without `--yes` it only reports what it would do. `--limit N` stops after N new
commits, which is handy when you would rather not dump 300 commits in one go.

The author identity matters: GitHub only counts a commit towards your calendar
when the author email belongs to your account. Use the `users.noreply.github.com`
address from **Settings → Emails**, not a random one.

## The workflow

The job ships as `tools/graph-art.workflow.yml` instead of being active in place, because
GitHub refuses to let an app token without the `workflows` permission create files under
`.github/workflows/`. Install it once:

```bash
mkdir -p .github/workflows
cp tools/graph-art.workflow.yml .github/workflows/graph-art.yml
git add .github/workflows/graph-art.yml && git commit -m "ci: enable graph art" && git push
```

After that it runs weekly and on demand:

- it exits quietly on forks and mirrors (`github.repository_owner == 'NggKhaiz'`);
- it needs the repository variable `GRAPH_ART_AUTHOR` (`Name <id+user@users.noreply.github.com>`)
  and warns instead of committing under a wrong identity when it is missing;
- it verifies, paints the missing cells, and pushes to the checked-out branch.

Set the variable once, then either wait for the schedule or run
**Actions → graph art → Run workflow** with an optional commit limit.

## Turning it off

Delete `.github/workflows/graph-art.yml` and stop running `apply`. The commits
already made stay in history — they are real commits — but nothing new appears.
If you want no trace of the drawing at all, you would have to rewrite that part
of the history; this project deliberately does not, because the point is to keep
the trick visible.

## Why bother

The same reason the rest of the site is honest about numbers: a contribution
graph is decoration, and decoration that pretends to be a productivity metric is
worse than decoration that says what it is. This one is a bitmap, and the bitmap
ships with its source.
