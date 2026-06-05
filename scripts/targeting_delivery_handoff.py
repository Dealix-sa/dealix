#!/usr/bin/env python3
"""Delivery handoff — converts a PAID target into a structured customer folder.

The targeting OS does not stop at sales. The moment a company pays, this script
materializes ``customers/{slug}/`` with the full delivery + proof scaffold so the
engagement is governed from day one. Every file carries the standard front-matter
block (source / evidence / assumption / confidence / recommendation /
approval_required / next_action / owner / due_date).

Hard rule: a handoff is only created for a company whose outcome stage is
``paid``. This function never charges anyone and never sends anything.

Usage:
    python scripts/targeting_delivery_handoff.py \\
        --company "Manar Performance Agency" \\
        --offer command_sprint
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from scripts.targeting_common import (
    CUSTOMERS_DIR,
    load_companies_jsonl,
    load_outcomes,
    slugify,
)
from scripts.targeting_offer_router import OFFERS, route_offer

# The canonical customer folder layout (filename → human title).
CUSTOMER_FILES = [
    ("00_intake.md", "Intake"),
    ("01_company_intelligence.md", "Company Intelligence"),
    ("02_diagnostic_summary.md", "Diagnostic Summary"),
    ("03_command_sprint_scope.md", "Command Sprint Scope"),
    ("04_revenue_map.md", "Revenue Map"),
    ("05_proof_register.md", "Proof Register"),
    ("06_next_action_board.md", "Next Action Board"),
    ("07_executive_command_brief.md", "Executive Command Brief"),
    ("08_delivery_log.md", "Delivery Log"),
    ("09_proof_pack.md", "Proof Pack"),
    ("10_upsell_recommendation.md", "Upsell Recommendation"),
]


def _front_matter(
    title: str, company: str, *, owner: str, due: str, next_action: str, confidence: str = "medium"
) -> str:
    """The standard governance block every customer artifact must carry."""
    return (
        f"# {title} — {company}\n\n"
        f"- **source:** delivery handoff (paid conversion)\n"
        f"- **evidence:** see customer intelligence + outcomes ledger\n"
        f"- **assumption:** to be confirmed with the client\n"
        f"- **confidence:** {confidence}\n"
        f"- **recommendation:** populate during delivery; do not overclaim\n"
        f"- **approval_required:** founder\n"
        f"- **next_action:** {next_action}\n"
        f"- **owner:** {owner}\n"
        f"- **due_date:** {due}\n\n"
        f"---\n\n"
    )


def create_handoff(
    company: dict[str, Any],
    *,
    offer_id: str | None = None,
    owner: str = "founder",
    base_dir: Path | None = None,
) -> dict[str, Any]:
    """Create the customer folder for a paid company. Returns paths + metadata.

    Raises ValueError if the company is not a real, named record.
    """
    name = (company.get("company_name") or "").strip()
    if not name:
        raise ValueError("cannot create a delivery handoff without a company name")

    base_dir = base_dir or CUSTOMERS_DIR
    slug = slugify(name)
    folder = base_dir / slug
    folder.mkdir(parents=True, exist_ok=True)

    routed = route_offer(company)
    offer_id = offer_id or routed["offer_id"]
    offer = OFFERS.get(offer_id, OFFERS["command_sprint"])
    today = date.today()
    due = (today + timedelta(days=7)).isoformat()

    created: list[str] = []
    for filename, title in CUSTOMER_FILES:
        path = folder / filename
        next_action = {
            "00_intake.md": "confirm scope + access with client",
            "02_diagnostic_summary.md": "review diagnostic findings with client",
            "04_revenue_map.md": "map opportunities + leakage points",
            "05_proof_register.md": "log claims with evidence (L1→L3)",
            "08_delivery_log.md": "record each delivery step + artifact",
            "09_proof_pack.md": "assemble proof pack at L2/L3",
            "10_upsell_recommendation.md": "decide upsell after proof",
        }.get(filename, "populate during delivery")
        body = _front_matter(title, name, owner=owner, due=due, next_action=next_action)

        if filename == "00_intake.md":
            body += (
                f"- **Company:** {name}\n"
                f"- **Sector:** {company.get('sector', '—')}\n"
                f"- **City:** {company.get('city', '—')}\n"
                f"- **Offer:** {offer['name_en']} ({offer.get('price_sar', 0)} SAR)\n"
                f"- **Primary weakness:** {routed['primary_weakness']} → {routed['primary_os_angle']}\n"
                f"- **Paid date:** {today.isoformat()}\n"
            )
        elif filename == "03_command_sprint_scope.md":
            body += "## Deliverables\n" + "\n".join(f"- {x}" for x in offer["includes"]) + "\n"
        elif filename == "09_proof_pack.md":
            body += (
                "## Proof levels\n"
                "- L1 artifact created\n- L2 client reviewed\n- L3 client approved\n"
                "- L4 client used\n- L5 measurable impact\n\n"
                "> First target: L2/L3. Then pursue L4/L5.\n"
            )
        path.write_text(body, encoding="utf-8")
        created.append(
            str(path.relative_to(base_dir.parent) if base_dir.parent in path.parents else path)
        )

    return {
        "company_name": name,
        "slug": slug,
        "folder": str(folder),
        "offer_id": offer_id,
        "files_created": [f for f, _ in CUSTOMER_FILES],
        "proof_pack": str(folder / "09_proof_pack.md"),
    }


def handoff_paid_from_outcomes(base_dir: Path | None = None) -> list[dict[str, Any]]:
    """Create handoffs for every company whose latest outcome stage is 'paid'."""
    outcomes = load_outcomes()
    companies = {c.get("company_name"): c for c in load_companies_jsonl()}
    paid_names = {o["company_name"] for o in outcomes if o.get("stage") == "paid"}
    results = []
    for name in sorted(paid_names):
        company = companies.get(name, {"company_name": name})
        results.append(create_handoff(company, base_dir=base_dir))
    return results


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix targeting → delivery handoff")
    ap.add_argument("--company", help="company name; if omitted, processes all paid outcomes")
    ap.add_argument("--offer", default=None)
    args = ap.parse_args(argv)

    if args.company:
        companies = {c.get("company_name"): c for c in load_companies_jsonl()}
        company = companies.get(args.company, {"company_name": args.company})
        result = create_handoff(company, offer_id=args.offer)
        print(f"handoff → {result['folder']} ({len(result['files_created'])} files)")
    else:
        results = handoff_paid_from_outcomes()
        for r in results:
            print(f"handoff → {r['folder']} ({len(r['files_created'])} files)")
        if not results:
            print("no paid outcomes found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
