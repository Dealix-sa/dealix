#!/usr/bin/env python3
"""Create a Command Sprint customer workspace (Wave 6).

Triggered when a sprint is paid (payment_status = paid in
data/revenue/payments.jsonl). Scaffolds customers/<slug>/ with the 12
Wave 6 delivery files so Day 1 delivery can start.

Reference:
  - docs/04_delivery/PAID_SPRINT_HANDOFF.md
  - docs/04_delivery/DELIVERY_DAILY_RHYTHM.md
  - Proof Pack template: docs/delivery/PROOF_PACK_TEMPLATE.md

Usage:
  python scripts/create_customer_workspace.py --name "company-name"
  python scripts/create_customer_workspace.py --name "company-name" --dry-run
  python scripts/create_customer_workspace.py --name "company-name" --idempotent

Exit codes:
  0  workspace created (or already existed and --idempotent passed)
  1  workspace already exists (and --idempotent not passed)
  2  validation error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")

# filename -> heading. Order matters (Day 1 -> Day 7 rhythm).
WORKSPACE_FILES: tuple[tuple[str, str], ...] = (
    ("00_intake.md", "Intake — الاستلام"),
    ("01_company_intelligence.md", "Company Intelligence — معلومات الشركة"),
    ("02_diagnostic_summary.md", "Diagnostic Summary — ملخص التشخيص"),
    ("03_command_sprint_scope.md", "Command Sprint Scope — نطاق العمل"),
    ("04_revenue_map.md", "Revenue Map — خريطة الإيراد"),
    ("05_proof_register.md", "Proof Register — سجل الإثبات"),
    ("06_approval_register.md", "Approval Register — سجل الموافقات"),
    ("07_next_action_board.md", "Next Action Board — لوحة الإجراءات"),
    ("08_executive_command_brief.md", "Executive Command Brief — موجز تنفيذي"),
    ("09_delivery_log.md", "Delivery Log — سجل التسليم"),
    ("10_proof_pack.md", "Proof Pack — حزمة الإثبات"),
    ("11_upsell_recommendation.md", "Upsell Recommendation — توصية التوسعة"),
)

DOCTRINE = (
    "> Rules: no auto-send · founder approval for every external action · "
    "no guaranteed revenue · no fake proof · no customer data for model training · "
    "no public case study without written approval.\n"
)


def _slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def _body(slug: str, filename: str, heading: str) -> str:
    lines = [
        f"# {heading}",
        "",
        f"Customer: `{slug}`  ·  Owner: founder",
        "",
        DOCTRINE,
        "",
    ]
    if filename == "10_proof_pack.md":
        lines += [
            "> Use the master template: `docs/delivery/PROOF_PACK_TEMPLATE.md`.",
            "> Every finding must cite evidence or be marked explicitly missing (مفقود).",
            "",
            "## Five upsell questions (see PROOF_TO_UPSELL_PLAYBOOK.md)",
            "1. What became clearer?",
            "2. What should continue weekly?",
            "3. Which Dealix OS module is the next expansion?",
            "4. Is this client fit for Managed Business OS?",
            "5. Recommended upsell: none / Starter Command / Business Ops / Executive OS",
        ]
    elif filename == "11_upsell_recommendation.md":
        lines += [
            "recommended_upsell: none | starter_command | business_ops | executive_os",
            "",
            "Reference: `sales/MANAGED_BUSINESS_OS_OFFER.md`. No upgrade before documented proof.",
        ]
    elif filename == "09_delivery_log.md":
        lines += [
            "| day | deliverable | status | blocker | approval_needed |",
            "|-----|-------------|--------|---------|-----------------|",
            "| 1 | Intake + Company Intelligence |  |  |  |",
        ]
    else:
        lines += ["_(to be filled during delivery)_"]
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True, help="company name or slug, e.g. 'acme-agency'")
    p.add_argument("--dry-run", action="store_true", help="print what would be created without writing")
    p.add_argument("--idempotent", action="store_true", help="exit 0 if workspace already exists")
    args = p.parse_args()

    slug = _slugify(args.name)
    if not SLUG_RE.match(slug):
        print(f"ERROR: could not derive a valid slug from {args.name!r} (got {slug!r})", file=sys.stderr)
        return 2

    workspace = REPO_ROOT / "customers" / slug

    if workspace.exists():
        if args.idempotent:
            print(f"OK: workspace already exists (idempotent): customers/{slug}/")
            return 0
        print(f"ERROR: workspace already exists: customers/{slug}/ (pass --idempotent to allow)", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"DRY-RUN: would create customers/{slug}/ with {len(WORKSPACE_FILES)} files:")
        for filename, _ in WORKSPACE_FILES:
            print(f"  customers/{slug}/{filename}")
        return 0

    workspace.mkdir(parents=True, exist_ok=False)
    for filename, heading in WORKSPACE_FILES:
        (workspace / filename).write_text(_body(slug, filename, heading), encoding="utf-8")

    print(f"OK: created customers/{slug}/ with {len(WORKSPACE_FILES)} files.")
    print("Next steps:")
    print(f"  1. Fill customers/{slug}/00_intake.md (Day 1).")
    print(f"  2. Add '{slug}' to reports/delivery/active_sprints.md, stage -> delivery_started.")
    print("  3. Follow docs/04_delivery/DELIVERY_DAILY_RHYTHM.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
