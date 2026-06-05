#!/usr/bin/env python3
"""Render a partner distribution plan from data/growth/partner_targets.csv.

Offline, deterministic. Partner targets are CATEGORIES (not scraped contacts).
No scraping, no purchased lists (non-negotiable #1). Outreach is warm and
founder-approved.
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "growth" / "partner_targets.csv"
OUT = ROOT / "reports" / "growth"


def main() -> int:
    if not DATA.exists():
        print("DEALIX_GROWTH_PARTNERS=SKIP (no data file)")
        return 0
    rows = list(csv.DictReader(DATA.read_text(encoding="utf-8").splitlines()))
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Partner Distribution Plan — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Source: `data/growth/partner_targets.csv` ({len(rows)} categories)",
        "",
        "> Categories, not scraped contacts. No scraping, no purchased lists.",
        "> Outreach is warm and founder-approved. Partners get the Partner Kit.",
        "",
        "| Category | Tier | Why fit | Offer angle | Status |",
        "|---|---|---|---|---|",
    ]
    by_tier: dict[str, int] = {}
    for r in rows:
        tier = r.get("partner_tier", "")
        by_tier[tier] = by_tier.get(tier, 0) + 1
        lines.append(
            "| {cat} | {tier} | {why} | {angle} | {status} |".format(
                cat=r.get("category", ""),
                tier=tier,
                why=r.get("why_fit", "").replace("|", "/"),
                angle=r.get("offer_angle", "").replace("|", "/"),
                status=r.get("status", ""),
            )
        )
    lines += ["", "## By tier", ""]
    for tier, count in sorted(by_tier.items()):
        lines.append(f"- **{tier}**: {count}")
    lines += [
        "",
        "## Partner Kit (each partner receives)",
        "",
        "- `partner_one_pager` — what Dealix is + co-sell value",
        "- `partner_pitch` — talking points",
        "- `command_sprint_overview` — the entry offer",
        "- `referral_terms` — credit / reward terms (see REFERRAL_SYSTEM.md)",
        "- `co_delivery_process` — how co-delivery works",
        "",
        "## Tiers",
        "",
        "- **referral** — sends a lead.",
        "- **co-sell** — joins the sale.",
        "- **co-deliver** — helps execute.",
        "",
    ]
    (OUT / "PARTNER_TARGETS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_PARTNERS=PASS ({len(rows)} categories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
