#!/usr/bin/env python3
"""Generate the Partner Pipeline report."""

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
    primary = priv / "partners" / "partner_pipeline.csv"
    bootstrap = BOOTSTRAP_ROOT / "partners" / "partner_pipeline.csv"

    _, rows, source = load_with_fallback(primary, bootstrap)
    ctx = ReportContext(
        name="Partner Pipeline Report",
        runtime_paths_checked=[primary],
        fallback_paths_used=[] if source == "runtime" else [bootstrap],
        started_at=now_iso(),
    )

    by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_status: dict[str, int] = defaultdict(int)
    for r in rows:
        by_type[r.get("type", "other")].append(r)
        by_status[(r.get("status") or "prospect").strip() or "prospect"] += 1

    lines = ctx.header()
    lines += [
        "## Partner pipeline — status counts",
        "",
    ]
    for s in (
        "prospect",
        "intro_meeting",
        "pilot_partner",
        "active",
        "paused",
        "terminated",
    ):
        lines.append(f"- **{s}**: {by_status.get(s, 0)}")

    for partner_type in (
        "agency",
        "erp_crm",
        "cybersecurity_grc",
        "consultancy",
        "other",
    ):
        items = by_type.get(partner_type, [])
        if not items:
            continue
        lines += [
            "",
            f"## {partner_type}",
            "",
            "| Partner | Path | Offer Fit | Referral | White-label | Trust Risk | Status | Next Action |",
            "| ------- | ---- | --------- | -------- | ----------- | ---------- | ------ | ----------- |",
        ]
        for it in items:
            lines.append(
                f"| {it.get('partner_id','')} {it.get('company','')} "
                f"| {it.get('relationship_path','')} "
                f"| {it.get('offer_fit','')} "
                f"| {it.get('referral_potential','')} "
                f"| {it.get('white_label_potential','')} "
                f"| {it.get('trust_risk','')} "
                f"| {it.get('status','')} "
                f"| {it.get('next_action','')} |"
            )

    lines += [
        "",
        "## Guardrails",
        "",
        "- No revenue share outside the approved partner program.",
        "- No exclusivity without a counter-signed contract and governance row.",
        "- No customer logos without explicit permission.",
        "- White-label is governance-reviewed; never the default.",
    ]

    out = priv / "partners" / "partner_pipeline_report.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
