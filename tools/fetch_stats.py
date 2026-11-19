#!/usr/bin/env python3
"""Fetch the GitHub numbers the profile shows and write data/profile.json.

Everything the README and the SVG cards state — contributions, repositories,
stars, per-project commit counts, languages — comes from here, so the numbers
are always the API's, never typed by hand.

Auth: GITHUB_TOKEN / GH_TOKEN, otherwise `gh auth token`.
Usage: python3 tools/fetch_stats.py [--login NggKhaiz] [--org MoLik-Labs]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "profile.json"
API = "https://api.github.com/graphql"

QUERY = """
query ($login: String!, $org: String!) {
  user(login: $login) {
    name
    login
    bio
    location
    followers { totalCount }
    following { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions }
    }
    repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { ...repo }
    }
  }
  organization(login: $org) {
    repositories(first: 60, privacy: PUBLIC, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { ...repo }
    }
  }
}

fragment repo on Repository {
  name
  nameWithOwner
  description
  stargazerCount
  forkCount
  isFork
  pushedAt
  createdAt
  primaryLanguage { name }
  licenseInfo { spdxId }
  owner { login }
  defaultBranchRef { target { ... on Commit { history { totalCount } } } }
  languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
    edges { size node { name } }
  }
}
"""


def token() -> str:
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        value = os.environ.get(key)
        if value:
            return value
    try:
        return subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit("No GitHub token: set GITHUB_TOKEN or run `gh auth login`.")


def graphql(query: str, variables: dict, auth: str) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"bearer {auth}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": "nggkhaiz-profile-stats",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    if "errors" in payload:
        raise SystemExit("GitHub API error: " + json.dumps(payload["errors"])[:600])
    return payload["data"]


def shape(node: dict) -> dict:
    history = ((node.get("defaultBranchRef") or {}).get("target") or {}).get("history") or {}
    languages = [
        {"name": edge["node"]["name"], "bytes": edge["size"]}
        for edge in (node.get("languages") or {}).get("edges", [])
        if edge.get("size")
    ]
    return {
        "name": node["name"],
        "repo": node["nameWithOwner"],
        "owner": (node.get("owner") or {}).get("login", ""),
        "description": node.get("description") or "",
        "stars": node.get("stargazerCount") or 0,
        "forks": node.get("forkCount") or 0,
        "commits": history.get("totalCount") or 0,
        "language": ((node.get("primaryLanguage") or {}).get("name")) or "",
        "license": ((node.get("licenseInfo") or {}).get("spdxId")) or "",
        "fork": bool(node.get("isFork")),
        "pushed_at": node.get("pushedAt") or "",
        "created_at": node.get("createdAt") or "",
        "languages": languages,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--login", default="NggKhaiz")
    parser.add_argument("--org", default="MoLik-Labs")
    args = parser.parse_args()

    data = graphql(QUERY, {"login": args.login, "org": args.org}, token())
    user = data["user"]
    owned = [shape(node) for node in user["repositories"]["nodes"]]
    organisation = [shape(node) for node in (data.get("organization") or {}).get(
        "repositories", {}
    ).get("nodes", [])]

    repos = sorted(owned + organisation, key=lambda repo: repo["commits"], reverse=True)

    # Forks carry someone else's commit history and language mix, so they are
    # counted in the repository list but never in the totals or percentages.
    source = [repo for repo in repos if not repo["fork"]]

    def language_mix(items: list[dict]) -> list[dict]:
        sizes: dict[str, int] = {}
        for repo in items:
            for language in repo["languages"]:
                sizes[language["name"]] = sizes.get(language["name"], 0) + language["bytes"]
        total = sum(sizes.values()) or 1
        return [
            {"name": name, "bytes": size, "percent": round(size * 100 / total, 1)}
            for name, size in sorted(sizes.items(), key=lambda item: item[1], reverse=True)
        ]

    languages = language_mix(source)
    languages_with_forks = language_mix(repos)

    payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": "https://api.github.com/graphql",
        "user": {
            "login": user["login"],
            "name": user["name"],
            "bio": user.get("bio") or "",
            "location": user.get("location") or "",
            "followers": user["followers"]["totalCount"],
            "following": user["following"]["totalCount"],
            "public_repos": user["repositories"]["totalCount"],
            "source_repos": len([repo for repo in owned if not repo["fork"]]),
            "forks": len([repo for repo in owned if repo["fork"]]),
            "org_repos": (data.get("organization") or {}).get("repositories", {}).get(
                "totalCount", 0
            ),
            "org": args.org,
            "contributions": user["contributionsCollection"]["contributionCalendar"][
                "totalContributions"
            ],
            "total_stars": sum(repo["stars"] for repo in repos),
            "source_commits": sum(repo["commits"] for repo in source),
            "top_language": languages[0]["name"] if languages else "",
        },
        "languages": languages,
        "languages_with_forks": languages_with_forks,
        "repos": repos,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    totals = payload["user"]
    print(
        f"{totals['contributions']} contributions · {totals['public_repos']} public repos · "
        f"{totals['total_stars']} stars · {totals['source_repos']} source repos + "
        f"{totals['forks']} forks + {totals['org_repos']} in {totals['org']} · "
        f"{len(languages)} languages"
    )
    for repo in repos[:6]:
        print(f"  {repo['repo']:<28} {repo['commits']:>5} commits  {repo['stars']:>3}★  {repo['language']}")


if __name__ == "__main__":
    main()
