#!/usr/bin/env python3
"""Create a Dealix customer workspace — the 12-file engagement spine.

Every paid (and most free) engagements get a workspace under ``customers/<slug>/``
containing a fixed set of files that carry the engagement from intake to upsell.
Each customer-facing file ends with the mandatory bilingual disclaimer.

Usage:
    python scripts/create_customer_workspace.py --name "Acme Trading"
    python scripts/create_customer_workspace.py --name "dry-run-client" --force
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CUSTOMERS_DIR = REPO / "customers"

DISCLAIMER = (
    "> Estimated value is not Verified value / "
    "القيمة التقديرية ليست قيمة مُتحقَّقة"
)

# Ordered (filename, title) — the canonical 12-file spine.
FILES: tuple[tuple[str, str], ...] = (
    ("00_intake.md", "Intake & Source Passport"),
    ("01_company_intelligence.md", "Company Intelligence"),
    ("02_diagnostic_summary.md", "Diagnostic Summary"),
    ("03_command_sprint_scope.md", "Command Sprint Scope"),
    ("04_revenue_map.md", "Revenue Map"),
    ("05_proof_register.md", "Proof Register"),
    ("06_approval_register.md", "Approval Register"),
    ("07_next_action_board.md", "Next Action Board"),
    ("08_executive_command_brief.md", "Executive Command Brief"),
    ("09_delivery_log.md", "Delivery Log"),
    ("10_proof_pack.md", "Proof Pack"),
    ("11_upsell_recommendation.md", "Upsell Recommendation"),
)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "customer"


def body_for(filename: str, display_name: str) -> str:
    """Return the markdown body (without header/disclaimer) for a workspace file."""
    if filename == "00_intake.md":
        return (
            "## Source Passport\n\n"
            "| Field | Value |\n|---|---|\n"
            "| Data origin | _to fill_ |\n"
            "| Owner / consent | _to fill_ |\n"
            "| PII present? | _to fill — no PII in logs (non-negotiable #6)_ |\n"
            "| Received on | _to fill_ |\n\n"
            "## Engagement\n\n"
            "- Offer: _free_diagnostic / sprint_499 / ..._\n"
            "- Warm path: _founder_referral / partner_intro / inbound_\n"
            "- Founder approval on file? _no — queue before any external send_\n"
        )
    if filename == "01_company_intelligence.md":
        return (
            "## What we know (sourced only)\n\n"
            "Every line must cite where it came from (non-negotiables #4, #7).\n\n"
            "- Sector: _source_\n- Size band: _source_\n- Region: _source_\n"
            "- Current commercial process: _source_\n"
        )
    if filename == "02_diagnostic_summary.md":
        return (
            "Scored with `sales/DIAGNOSTIC_SCORECARD.md` (0–5 per dimension).\n\n"
            "| Dimension | Score | Sourced observation |\n|---|---|---|\n"
            "| Data readiness | _/5_ | _ |\n"
            "| Process clarity | _/5_ | _ |\n"
            "| Decision latency | _/5_ | _ |\n"
            "| Governance | _/5_ | _ |\n"
            "| Proof culture | _/5_ | _ |\n"
            "| Revenue leak | _/5_ | _ |\n\n"
            "**Total:** _/30_  **Band:** _Foundational / Operational / Scaling_\n\n"
            "**Biggest revenue leak:** _named plainly_\n"
        )
    if filename == "03_command_sprint_scope.md":
        return (
            "Locked scope for the 7-Day Revenue Intelligence Sprint "
            "(`sales/COMMAND_SPRINT_TERMS.md`).\n\n"
            "- In scope: one company, one dataset, one revenue map.\n"
            "- Out of scope → Change Request (no silent scope creep).\n"
            "- Definition of done: Proof Pack score ≥ 70 + ≥ 1 Capital Asset.\n"
        )
    if filename == "04_revenue_map.md":
        return (
            "Scored accounts / opportunities derived from the customer's own data.\n\n"
            "| Account | Score | Opportunity | Source |\n|---|---|---|---|\n"
            "| _ | _ | _ | _ |\n\n"
            "_Estimated opportunity values are estimates, not guarantees "
            "(non-negotiable #5)._\n"
        )
    if filename == "05_proof_register.md":
        return (
            "Append-only register of evidence produced during the engagement.\n\n"
            "| ts | claim | evidence_tier | source_ref |\n|---|---|---|---|\n"
            "| _ | _ | estimated/verified/client_confirmed | _ |\n"
        )
    if filename == "06_approval_register.md":
        return (
            "Every outward-facing draft waits here for the founder "
            "(non-negotiable #8 — see `docs/governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md`).\n\n"
            "| ts | item | channel | governance_decision |\n|---|---|---|---|\n"
            "| _ | outreach draft | email/whatsapp | queued_for_approval |\n"
        )
    if filename == "07_next_action_board.md":
        return (
            "The single next move, refreshed daily by the delivery rhythm.\n\n"
            "- [ ] **Today's one move:** _to fill_\n"
            "- [ ] Blocker (if any): _to fill_\n"
        )
    if filename == "08_executive_command_brief.md":
        return (
            "One-page brief for the customer's decision-maker.\n\n"
            "1. Where you stand (diagnostic band).\n"
            "2. The biggest revenue leak.\n"
            "3. What we did this sprint.\n"
            "4. The one recommended next step (with price).\n"
        )
    if filename == "09_delivery_log.md":
        return (
            "Append-only. One line per working day (delivery rhythm).\n\n"
            "| ts | change | next |\n|---|---|---|\n"
            "| _ | workspace created | run intake |\n"
        )
    if filename == "10_proof_pack.md":
        return (
            "The deliverable that proves outcomes before any claim.\n\n"
            "- **Proof score:** _/100 (must be ≥ 70 to close)_\n"
            "- **Capital Asset produced:** _name — register in "
            "`data/revenue/proof_assets.jsonl`_\n"
            "- **Evidence tier:** estimated (label honestly)\n"
            "- **Governance decision:** approved / queued_for_approval\n"
        )
    if filename == "11_upsell_recommendation.md":
        return (
            "Chosen by what the Proof Pack actually showed "
            "(`docs/delivery/PROOF_TO_UPSELL_PLAYBOOK.md`).\n\n"
            "- Recommended next rung: _Data Pack / Managed Ops / Custom AI / Enterprise_\n"
            "- Why (sourced): _ \n"
            "- Status: queued_for_approval (never auto-sent)\n"
        )
    return "_to fill_\n"


def render(filename: str, title: str, display_name: str, today: str) -> str:
    return (
        f"# {title} — {display_name}\n\n"
        f"_Created: {today} · Workspace file `{filename}`_\n\n"
        f"{body_for(filename, display_name)}\n"
        f"---\n\n{DISCLAIMER}\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Dealix customer workspace.")
    parser.add_argument("--name", required=True, help="Customer display name.")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing workspace files."
    )
    args = parser.parse_args(argv)

    display_name = args.name.strip()
    slug = slugify(display_name)
    ws = CUSTOMERS_DIR / slug
    today = dt.date.today().isoformat()

    if ws.exists() and not args.force:
        print(f"Workspace already exists: {ws} (use --force to overwrite)")
        return 1

    ws.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for filename, title in FILES:
        target = ws / filename
        if target.exists() and not args.force:
            continue
        target.write_text(render(filename, title, display_name, today), encoding="utf-8")
        created.append(filename)

    print(f"Customer workspace ready: customers/{slug}/")
    for f in sorted(f for f, _ in FILES):
        print(f"  - {f}")
    print(f"\n{len(created)} file(s) written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
