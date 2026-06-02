#!/usr/bin/env python3
"""Product Distribution OS — draft queue review.

Reads the append-only draft ledger and renders a founder-facing review so the
human can approve / edit / reject before any manual send. Read-only: this
script never sends, edits, or deletes drafts.

Run:
    python scripts/review_draft_queue.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "data" / "drafts" / "drafts.jsonl"
REPORT = ROOT / "reports" / "distribution" / "DRAFT_QUEUE_REVIEW.md"


def read_drafts(path: Path = DRAFTS) -> list[dict[str, Any]]:
    """Read drafts from the JSONL ledger (skips blank lines)."""
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def render_review(drafts: list[dict[str, Any]]) -> str:
    """Render the markdown queue-review report."""
    by_status = Counter(d.get("status", "unknown") for d in drafts)
    pending = [d for d in drafts if d.get("status") == "pending_approval"]
    needs_edit = [d for d in drafts if d.get("status") == "needs_edit"]

    lines = [
        "# Dealix Draft Queue Review",
        "",
        f"Total drafts: {len(drafts)}",
        "",
        "## Status counts",
    ]
    if not by_status:
        lines.append("- (queue empty)")
    for status, count in sorted(by_status.items()):
        lines.append(f"- {status}: {count}")

    lines += ["", "## Pending approval"]
    if not pending:
        lines.append("- None")
    for draft in pending[:50]:
        lines.append(
            f"- `{draft['id']}` — {draft.get('company')} — "
            f"{draft.get('draft_type')} — {draft.get('channel')} — "
            f"evidence {draft.get('evidence_level')} / risk {draft.get('risk_level')}"
        )

    if needs_edit:
        lines += ["", "## Needs edit (guard tripped — do not approve as-is)"]
        for draft in needs_edit[:50]:
            lines.append(
                f"- `{draft['id']}` — {draft.get('company')} — "
                f"{', '.join(draft.get('policy_issues', []))}"
            )

    lines += [
        "",
        "## Founder action",
        "- Approve, edit, or reject each pending draft.",
        "- Manual channels only: copy approved text yourself. No auto-send.",
        "- Resolve `needs_edit` drafts before they can be approved.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    drafts = read_drafts()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_review(drafts), encoding="utf-8")

    pending = sum(1 for d in drafts if d.get("status") == "pending_approval")
    needs_edit = sum(1 for d in drafts if d.get("status") == "needs_edit")
    print(f"DEALIX_DRAFT_QUEUE_PENDING={pending}")
    print(f"DEALIX_DRAFT_QUEUE_NEEDS_EDIT={needs_edit}")


if __name__ == "__main__":
    main()
