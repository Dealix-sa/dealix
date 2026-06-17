#!/usr/bin/env python3
"""Triage open pull requests into actionable buckets.

Reads the open PR list via the ``gh`` CLI (available on GitHub Actions runners and
locally when installed/authenticated), sorts each PR into exactly one bucket per
``docs/agents/PR_TRIAGE_POLICY.md``, and writes a triage report. Humans decide what
to merge — this tool never merges, closes, or comments.

Outputs:
  - reports/pr_triage/OPEN_PR_TRIAGE.md
  - reports/pr_triage/open_pr_triage.json
  - stdout line: ``DEALIX_PR_TRIAGE=PASS|SKIPPED``

Always exits 0 — triage is informational and must never break a build.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "pr_triage"

# Bucket order matters: first match wins.
BUCKET_ORDER = ("draft", "security", "dependencies", "agent", "docs", "needs_review")

PER_BUCKET_LIMIT = 50


def _labels(pr: dict) -> str:
    return " ".join(label.get("name", "").lower() for label in pr.get("labels", []))


def classify(pr: dict) -> str:
    """Return the single bucket a PR belongs to (first match wins)."""
    title = (pr.get("title") or "").lower()
    labels = _labels(pr)
    author = (pr.get("author") or {}).get("login", "").lower()

    if pr.get("isDraft"):
        return "draft"
    if any(word in title or word in labels for word in ("security", "auth", "secret", "vuln")):
        return "security"
    if "dependabot" in author or "deps" in labels or any(
        word in title for word in ("bump ", "dependabot", "dependency", "upgrade ")
    ):
        return "dependencies"
    if any(word in title for word in ("claude", "codex", "agent")):
        return "agent"
    if "docs" in labels or title.startswith("docs") or "documentation" in title:
        return "docs"
    return "needs_review"


def fetch_prs() -> list[dict] | None:
    """Return the open PR list via ``gh``, or ``None`` when gh is unavailable."""
    if shutil.which("gh") is None:
        return None
    try:
        raw = subprocess.check_output(
            [
                "gh", "pr", "list",
                "--state", "open",
                "--limit", "500",
                "--json", "number,title,author,createdAt,updatedAt,labels,isDraft",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw)
    except Exception:
        return None


def build_buckets(prs: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {name: [] for name in BUCKET_ORDER}
    for pr in prs:
        buckets[classify(pr)].append(pr)
    for items in buckets.values():
        items.sort(key=lambda pr: pr.get("updatedAt", ""))  # most stale first
    return buckets


def render_markdown(buckets: dict[str, list[dict]], total: int) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = ["# Open PR Triage", "", f"- Generated: `{now}`", f"- Open PRs: {total}", ""]
    lines.append("See policy: `docs/agents/PR_TRIAGE_POLICY.md`. Agents never merge.")
    lines.append("")
    for name in BUCKET_ORDER:
        items = buckets[name]
        lines.append(f"## {name} ({len(items)})")
        if not items:
            lines.append("- none")
        for pr in items[:PER_BUCKET_LIMIT]:
            num = pr.get("number")
            title = pr.get("title", "")
            updated = pr.get("updatedAt", "")
            lines.append(f"- #{num} {title} — updated {updated}")
        if len(items) > PER_BUCKET_LIMIT:
            lines.append(f"- … and {len(items) - PER_BUCKET_LIMIT} more")
        lines.append("")
    return "\n".join(lines)


def write_skipped_report(reason: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "OPEN_PR_TRIAGE.md").write_text(
        "# Open PR Triage\n\n"
        f"Status: **SKIPPED** — {reason}\n\n"
        "Populate by either:\n"
        "- running where the `gh` CLI is installed and authenticated "
        "(`GITHUB_TOKEN` set), or\n"
        "- from an agent session with GitHub MCP tools, using `list_pull_requests` "
        "and applying `docs/agents/PR_TRIAGE_POLICY.md`.\n",
        encoding="utf-8",
    )
    (OUT_DIR / "open_pr_triage.json").write_text(
        json.dumps({"status": "SKIPPED", "reason": reason}, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    prs = fetch_prs()
    if prs is None:
        write_skipped_report("gh CLI unavailable or PR list could not be read")
        print("DEALIX_PR_TRIAGE=SKIPPED")
        return 0

    buckets = build_buckets(prs)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "OPEN_PR_TRIAGE.md").write_text(
        render_markdown(buckets, len(prs)), encoding="utf-8"
    )
    summary = {
        "status": "PASS",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_open": len(prs),
        "buckets": {name: len(items) for name, items in buckets.items()},
    }
    (OUT_DIR / "open_pr_triage.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("DEALIX_PR_TRIAGE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
