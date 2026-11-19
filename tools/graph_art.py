#!/usr/bin/env python3
"""Paint the GitHub contribution graph from a text pattern.

The contribution calendar is 53 columns (weeks, Sunday first) by 7 rows
(Sunday first). Any 53x7 block of characters therefore maps onto real dates,
and a date gets as many commits as its character says.

    python3 tools/graph_art.py render          # print the grid as ASCII
    python3 tools/graph_art.py plan            # rebuild tools/graph-art.plan.json
    python3 tools/graph_art.py verify          # compare the plan with git history
    python3 tools/graph_art.py apply --yes     # create the missing commits

The plan is frozen: dates and counts are written to tools/graph-art.plan.json
and committed, so the same history can be reproduced from any clone and the
scheduled workflow never drifts when the calendar slides forward.

Intensities, matching the four shades GitHub draws:

    ' ' or '.'   nothing / one commit
    '-'          two
    '+'          three
    '#'          four

Nothing here is hidden: every commit carries the message
"chore: graph art YYYY-MM-DD (n/m)" and the pattern lives in this file.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = ROOT / "tools" / "graph-art.txt"
PLAN = ROOT / "tools" / "graph-art.plan.json"

WEEKS = 53
DAYS = 7
TZ = dt.timezone(dt.timedelta(hours=7))  # Asia/Ho_Chi_Minh
COMMIT_HOUR = 12
MESSAGE = "chore: graph art {date} ({i}/{n})"

#: character -> commits that day
LEVELS = {
    " ": 0,
    ".": 1,
    "·": 1,
    "-": 2,
    "+": 3,
    "#": 4,
}


# ----------------------------------------------------------------- pattern


@dataclass
class Pattern:
    anchor: dt.date  # Sunday of the first column
    rows: list[str]  # 7 strings, row 0 = Sunday

    @property
    def width(self) -> int:
        return len(self.rows[0])


def parse_pattern(text: str) -> Pattern:
    """Read the pattern file.

    `//` starts a comment, `anchor: YYYY-MM-DD` sets the first Sunday, and the
    remaining non-empty lines are the seven rows of the grid. Rows are used
    verbatim (spaces matter), padded to 53 columns on the right.
    """
    anchor: dt.date | None = None
    rows: list[str] = []
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        if stripped.lower().startswith("anchor:"):
            anchor = dt.date.fromisoformat(stripped.split(":", 1)[1].strip())
            continue
        if set(stripped) - set(LEVELS):
            raise SystemExit(f"unknown pattern characters in {stripped!r}")
        rows.append(line)
    if anchor is None:
        raise SystemExit("pattern needs an `anchor: YYYY-MM-DD` line")
    if anchor.weekday() != 6:
        raise SystemExit(f"anchor must be a Sunday, {anchor} is {anchor:%A}")
    if len(rows) != DAYS:
        raise SystemExit(f"pattern needs exactly {DAYS} rows, found {len(rows)}")
    if any(len(row) > WEEKS for row in rows):
        widest = max(len(row) for row in rows)
        raise SystemExit(f"pattern rows must be at most {WEEKS} columns, widest is {widest}")
    rows = [row.ljust(WEEKS) for row in rows]
    return Pattern(anchor=anchor, rows=rows)


def load_pattern(path: Path = PATTERN) -> Pattern:
    return parse_pattern(path.read_text(encoding="utf-8"))


def grid_date(pattern: Pattern, week: int, day: int) -> dt.date:
    return pattern.anchor + dt.timedelta(days=week * DAYS + day)


# --------------------------------------------------------------------- plan


def build_plan(pattern: Pattern) -> list[dict]:
    """One entry per date that carries at least one commit."""
    entries: list[dict] = []
    for day, row in enumerate(pattern.rows):
        for week, char in enumerate(row):
            count = LEVELS[char]
            if count == 0:
                continue
            date = grid_date(pattern, week, day)
            entries.append({"date": date.isoformat(), "commits": count})
    entries.sort(key=lambda e: e["date"])
    return entries


def plan_document(pattern: Pattern, entries: list[dict]) -> dict:
    return {
        "generated_by": "tools/graph_art.py",
        "anchor": pattern.anchor.isoformat(),
        "weeks": WEEKS,
        "days": DAYS,
        "timezone": "+07:00",
        "total_commits": sum(e["commits"] for e in entries),
        "active_days": len(entries),
        "entries": entries,
    }


def write_plan(document: dict, path: Path = PLAN) -> None:
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")


def load_plan(path: Path = PLAN) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# -------------------------------------------------------------------- render


def render(document: dict) -> str:
    """ASCII preview, using the same characters as the pattern."""
    counts = {e["date"]: e["commits"] for e in document["entries"]}
    anchor = dt.date.fromisoformat(document["anchor"])
    shade = {0: " ", 1: ".", 2: "-", 3: "+", 4: "#"}
    lines = []
    for day in range(DAYS):
        cells = []
        for week in range(WEEKS):
            date = anchor + dt.timedelta(days=week * DAYS + day)
            cells.append(shade.get(counts.get(date.isoformat(), 0), "#"))
        lines.append("".join(cells).rstrip())
    return "\n".join(lines)


# ---------------------------------------------------------------- git state


def git(*args: str, env: dict | None = None) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env={**os.environ, **(env or {})},
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed:\n{proc.stderr.strip()}")
    return proc.stdout


def painted_counts() -> dict[str, int]:
    """How many graph-art commits already exist per date."""
    message = git("log", "--all", "--format=%s")
    counts: dict[str, int] = {}
    for line in message.splitlines():
        if not line.startswith("chore: graph art "):
            continue
        try:
            date = line.split()[3]
            dt.date.fromisoformat(date)
        except (IndexError, ValueError):
            continue
        counts[date] = counts.get(date, 0) + 1
    return counts


def status(document: dict) -> tuple[int, int]:
    painted = painted_counts()
    missing = 0
    for entry in document["entries"]:
        have = painted.get(entry["date"], 0)
        if have < entry["commits"]:
            missing += entry["commits"] - have
    return missing, len(document["entries"])


# --------------------------------------------------------------------- apply


def apply_plan(
    document: dict,
    *,
    author_name: str,
    author_email: str,
    push: bool = False,
    limit: int | None = None,
) -> int:
    painted = painted_counts()
    created = 0
    for entry in document["entries"]:
        date = entry["date"]
        have = painted.get(date, 0)
        want = entry["commits"]
        if have >= want:
            continue
        day = dt.date.fromisoformat(date)
        for index in range(have + 1, want + 1):
            if limit is not None and created >= limit:
                print(f"stopping at the {limit}-commit limit; rerun to continue")
                return created
            stamp = dt.datetime(
                day.year, day.month, day.day, COMMIT_HOUR, 0, index - 1, tzinfo=TZ
            ).isoformat()
            env = {
                "GIT_AUTHOR_DATE": stamp,
                "GIT_COMMITTER_DATE": stamp,
                "GIT_AUTHOR_NAME": author_name,
                "GIT_AUTHOR_EMAIL": author_email,
                "GIT_COMMITTER_NAME": author_name,
                "GIT_COMMITTER_EMAIL": author_email,
            }
            git(
                "commit",
                "--allow-empty",
                "--no-verify",  # keep the message exactly as documented
                "-q",
                "-m",
                MESSAGE.format(date=date, i=index, n=want),
                env=env,
            )
            created += 1
        print(f"  {date}  {have} -> {want}")

    if push and created:
        git("push", "origin", "HEAD")
    return created


# ----------------------------------------------------------------------- cli


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Contribution-graph art from a text pattern.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("render", help="print the frozen plan as ASCII")

    plan_cmd = sub.add_parser("plan", help="rebuild the plan file from the pattern")
    plan_cmd.add_argument("--dry-run", action="store_true")

    sub.add_parser("verify", help="report how much of the plan is already committed")

    apply_cmd = sub.add_parser("apply", help="create the missing commits")
    apply_cmd.add_argument("--yes", action="store_true", help="actually write commits")
    apply_cmd.add_argument("--push", action="store_true", help="push to origin after writing")
    apply_cmd.add_argument("--limit", type=int, default=None, help="stop after N new commits")
    apply_cmd.add_argument(
        "--author",
        default=os.environ.get("GRAPH_ART_AUTHOR", ""),
        help="Name <email> used for the commits; defaults to GRAPH_ART_AUTHOR",
    )

    args = parser.parse_args(argv)

    if args.command == "render":
        print(render(load_plan()))
        return 0

    if args.command == "plan":
        pattern = load_pattern()
        entries = build_plan(pattern)
        document = plan_document(pattern, entries)
        print(f"{document['active_days']} active days, {document['total_commits']} commits")
        print(render(document))
        if not args.dry_run:
            write_plan(document)
            print(f"wrote {PLAN.relative_to(ROOT)}")
        return 0

    document = load_plan()

    if args.command == "verify":
        missing, active = status(document)
        print(f"plan: {active} active days, {document['total_commits']} commits")
        print(f"missing: {missing} commits")
        print(render(document))
        return 0 if missing == 0 else 1

    # apply
    missing, _ = status(document)
    if missing == 0:
        print("nothing to do: the plan is fully painted")
        return 0
    if not args.yes:
        print(f"would create {missing} commits; rerun with --yes")
        return 0
    author = args.author.strip()
    if "<" not in author or not author.endswith(">"):
        raise SystemExit("pass --author 'Your Name <you@example.com>' or set GRAPH_ART_AUTHOR")
    name, email = author.split("<", 1)
    created = apply_plan(
        document,
        author_name=name.strip(),
        author_email=email.rstrip(">").strip(),
        push=args.push,
        limit=args.limit,
    )
    print(f"created {created} commits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
