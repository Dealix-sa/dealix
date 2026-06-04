#!/usr/bin/env python3
"""
Dealix Commercial Launch Readiness.

Aggregates the draft factory + safety audit results into:
  - outputs/commercial_launch/latest/daily_metrics.json   (enriched)
  - docs/commercial-launch/99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md

Read-only with respect to external systems. No sending.
Exit 0 if commercially ready (drafts>=400 and safety pass), 1 otherwise.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "outputs" / "commercial_launch" / "latest"
REPORT = REPO / "docs" / "commercial-launch" / "99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> int:
    metrics = read_json(OUT_DIR / "daily_metrics.json")
    safety = read_json(OUT_DIR / "safety_audit.json")

    draft_count = int(metrics.get("draft_count", 0))
    safety_pass = bool(safety.get("pass", False))
    ready = draft_count >= 400 and safety_pass

    metrics.update(
        {
            "readiness_computed_at": datetime.now(timezone.utc).isoformat(),
            "safety_pass": safety_pass,
            "commercially_ready": ready,
            "go_decision": "GO (review-only drafts + manual approved outreach)" if ready else "NO-GO",
        }
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "daily_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    by_vertical = metrics.get("by_vertical", {})
    lines = [
        "# 99 — Final Commercial Launch Readiness Report",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        "## Result",
        f"- Draft count: **{draft_count}** (target ≥ 400)",
        f"- Safety audit: **{'PASS' if safety_pass else 'FAIL'}**",
        f"- Send allowed (any draft): **{metrics.get('send_allowed_true_count', 'n/a')}**",
        f"- Commercially ready: **{'YES' if ready else 'NO'}**",
        f"- Decision: **{metrics['go_decision']}**",
        "",
        "## Drafts by vertical",
    ]
    for v, c in sorted(by_vertical.items()):
        lines.append(f"- {v}: {c}")
    lines += [
        "",
        "## What this authorizes (GO)",
        "- Generation of ≥400 review-only drafts.",
        "- Founder manual review and editing.",
        "- Manual, approved outreach by the founder.",
        "- Paid diagnostics, discovery calls, proposal creation, pilot planning.",
        "",
        "## What this does NOT authorize (NO-GO)",
        "- Automated email sending.",
        "- Cold messaging automation on any platform.",
        "- Professional-network automation.",
        "- Website form auto-submit.",
        "- Bulk sending.",
        "- External sending from GitHub Actions.",
        "",
        "_All outputs are artifacts for human review. No external send occurs anywhere in this pipeline._",
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"[readiness] draft_count={draft_count} safety_pass={safety_pass} ready={ready}")
    print(f"[readiness] report -> {REPORT.relative_to(REPO)}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
