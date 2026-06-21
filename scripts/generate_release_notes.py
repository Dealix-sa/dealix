#!/usr/bin/env python3
"""Generate release notes from git log since the last release tag (or last N days).

Outputs reports/releases/release-notes-YYYY-MM-DD.md.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "reports" / "releases"


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return ""


def _last_tag() -> str:
    return _run(["git", "describe", "--tags", "--abbrev=0"])


def _commits_since(ref: str | None, days: int) -> list[str]:
    if ref:
        rng = f"{ref}..HEAD"
        out = _run(["git", "log", "--no-merges", "--pretty=format:%h %s", rng])
    else:
        since = (_dt.date.today() - _dt.timedelta(days=days)).isoformat()
        out = _run(
            ["git", "log", "--no-merges", "--pretty=format:%h %s", f"--since={since}"]
        )
    return [line for line in out.split("\n") if line.strip()]


CATEGORIES = {
    "feat": "Features",
    "fix": "Fixes",
    "chore": "Chores",
    "docs": "Docs",
    "refactor": "Refactors",
    "test": "Tests",
    "ci": "CI / Build",
    "perf": "Performance",
}


def _categorize(commits: list[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {label: [] for label in CATEGORIES.values()}
    buckets["Other"] = []
    for line in commits:
        try:
            _sha, msg = line.split(" ", 1)
        except ValueError:
            continue
        prefix = msg.split("(", 1)[0].split(":", 1)[0].strip()
        label = CATEGORIES.get(prefix, "Other")
        buckets[label].append(line)
    return buckets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = _last_tag()
    commits = _commits_since(tag, args.days)
    buckets = _categorize(commits)

    date = _dt.date.today().isoformat()
    lines = [
        f"# Release notes — {date}",
        "",
        f"_Source: {'tag ' + tag if tag else f'last {args.days} days'}_",
        "",
        f"_{len(commits)} commits considered._",
        "",
    ]
    for label, items in buckets.items():
        if not items:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for it in items:
            lines.append(f"- {it}")
        lines.append("")

    out = OUT_DIR / f"release-notes-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out} ({len(commits)} commits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
