#!/usr/bin/env python3
"""Generate the Authority Engine content queue report."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BOOTSTRAP_ROOT,
    ReportContext,
    load_with_fallback,
    now_iso,
    private_ops_root,
    write_markdown,
)


def main() -> int:
    priv = private_ops_root()
    sources = {
        "angles": (
            priv / "authority" / "content_angles.csv",
            BOOTSTRAP_ROOT / "authority" / "content_angles.csv",
        ),
        "insights": (
            priv / "authority" / "sector_insights.csv",
            BOOTSTRAP_ROOT / "authority" / "sector_insights.csv",
        ),
        "posts": (
            priv / "authority" / "founder_posts.csv",
            BOOTSTRAP_ROOT / "authority" / "founder_posts.csv",
        ),
        "reports": (
            priv / "authority" / "report_ideas.csv",
            BOOTSTRAP_ROOT / "authority" / "report_ideas.csv",
        ),
    }
    loaded: dict[str, list[dict[str, str]]] = {}
    fallbacks: list[Path] = []
    for key, (primary, bootstrap) in sources.items():
        _, rows, source = load_with_fallback(primary, bootstrap)
        loaded[key] = rows
        if source == "fallback":
            fallbacks.append(bootstrap)

    ctx = ReportContext(
        name="Authority Content Queue",
        runtime_paths_checked=[p for p, _ in sources.values()],
        fallback_paths_used=fallbacks,
        started_at=now_iso(),
    )

    lines = ctx.header()

    # Posts by approval
    posts_by_status: dict[str, int] = defaultdict(int)
    for p in loaded["posts"]:
        posts_by_status[(p.get("approval_status") or "pending").strip() or "pending"] += 1
    lines += [
        "## Founder posts queue",
        "",
    ]
    for s in ("pending", "approved", "held", "rejected"):
        lines.append(f"- **{s}**: {posts_by_status.get(s, 0)}")

    lines += [
        "",
        "### Posts",
        "",
        "| Post | Theme | Sector | Approval | Proof | Risk | Next Action |",
        "| ---- | ----- | ------ | -------- | ----- | ---- | ----------- |",
    ]
    for p in loaded["posts"]:
        lines.append(
            f"| {p.get('post_id','')} | {p.get('theme','')} "
            f"| {p.get('sector','')} | {p.get('approval_status','')} "
            f"| {p.get('proof_status','')} | {p.get('risk_level','')} "
            f"| {p.get('next_action','')} |"
        )

    # Insights by sector
    insights_by_sector: dict[str, list[dict[str, str]]] = defaultdict(list)
    for i in loaded["insights"]:
        insights_by_sector[i.get("sector", "unknown")].append(i)
    lines += [
        "",
        "## Sector insights (validated / draft)",
        "",
    ]
    for sector, items in sorted(insights_by_sector.items()):
        lines.append(f"### {sector}")
        lines.append("")
        for it in items:
            evidence = (it.get("evidence") or "").strip() or "_missing_"
            lines.append(
                f"- ({it.get('status','draft')}) {it.get('insight','')} "
                f"— evidence: {evidence} — public: {it.get('approved_for_public','no')}"
            )
        lines.append("")

    # Angles
    lines += [
        "## Content angles",
        "",
        "| Angle | Theme | Sector | Claim | Evidence Needed | Risk | Status |",
        "| ----- | ----- | ------ | ----- | --------------- | ---- | ------ |",
    ]
    for a in loaded["angles"]:
        lines.append(
            f"| {a.get('angle_id','')} | {a.get('theme','')} "
            f"| {a.get('sector','')} | {a.get('claim','')} "
            f"| {a.get('evidence_needed','')} | {a.get('risk_level','')} "
            f"| {a.get('status','')} |"
        )

    # Reports
    lines += [
        "",
        "## Sector report pipeline",
        "",
        "| Report | Sector | Title | Hypothesis | Data Needed | Approval | Next Action |",
        "| ------ | ------ | ----- | ---------- | ----------- | -------- | ----------- |",
    ]
    for r in loaded["reports"]:
        lines.append(
            f"| {r.get('report_id','')} | {r.get('sector','')} "
            f"| {r.get('title','')} | {r.get('hypothesis','')} "
            f"| {r.get('data_needed','')} | {r.get('approval_status','')} "
            f"| {r.get('next_action','')} |"
        )

    lines += [
        "",
        "## Doctrine",
        "",
        "- No post is published without `approval_status=approved`.",
        "- No claim without evidence linked.",
        "- No customer logos without permission rows.",
        "- LinkedIn first; other public channels only after this one produces signal.",
    ]

    out = priv / "authority" / "authority_content_queue.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
