"""Print the Revenue Sprint Kit — the bundle of files a fresh sprint needs.

`make kit` shows where the canonical templates live.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

KIT_FILES: tuple[tuple[str, str], ...] = (
    ("docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md", "production line overview"),
    ("docs/delivery/revenue_sprint/DELIVERY_CONTROL_SYSTEM.md", "rules and metrics"),
    ("docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md", "step-by-step playbook"),
    ("docs/delivery/revenue_sprint/CLIENT_INTAKE.md", "Day 0 intake template"),
    ("docs/delivery/revenue_sprint/LEAD_TABLE_SCHEMA.md", "deliverable spreadsheet schema"),
    ("docs/delivery/revenue_sprint/SCORING_RULES.md", "scoring rubric"),
    ("docs/delivery/revenue_sprint/OUTREACH_PACK_TEMPLATE.md", "bilingual outreach"),
    ("docs/delivery/revenue_sprint/REPORT_TEMPLATE.md", "executive memo"),
    ("docs/delivery/revenue_sprint/QA_CHECKLIST.md", "Day 10 QA"),
    ("docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md", "Day 12 handoff"),
    ("docs/delivery/revenue_sprint/CASE_STUDY_CAPTURE.md", "Day 30/60 capture"),
)


def main() -> int:
    print("Revenue Sprint Kit")
    print("=" * 60)
    for path, label in KIT_FILES:
        present = "✓" if (ROOT / path).exists() else "✗"
        print(f"  {present}  {path:60s}  {label}")
    print()
    print("Private workspace per sprint:")
    print("  dealix-ops-private/clients/<client_id>/")
    print("  dealix-ops-private/delivery/reports/<sprint_id>/")
    print()
    print("Begin a sprint:")
    print("  1) Confirm payment / PO / signed scope.")
    print("  2) Copy CLIENT_INTAKE.md → dealix-ops-private/clients/<client_id>/intake.yaml")
    print("  3) Run the playbook day by day.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
