"""Verify the Delivery & Client Success Operating System v1 is in place.

This script checks that every required doctrine document, template file, and
operational log for the OS exists and has non-trivial content. It is wired
into CI via .github/workflows/dealix-delivery-client-success.yml and exposed
via `make delivery-verify`.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    "docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md",
    "docs/delivery/KICKOFF_PROTOCOL.md",
    "docs/delivery/LEAD_TABLE_STANDARD.md",
    "docs/delivery/DELIVERY_QA_SCORE.md",
    "docs/delivery/HANDOFF_PROTOCOL.md",
    "docs/delivery/DELIVERY_OPERATING_ROUTINE.md",
    "docs/client_success/FEEDBACK_RETENTION_SYSTEM.md",
    "docs/client_success/CLIENT_HEALTH_SCORE_V2.md",
    "docs/client_success/RETAINER_PACKAGING_SYSTEM.md",
    "docs/content/PROOF_APPROVAL_SYSTEM.md",
    "docs/product/DELIVERY_TO_PRODUCTIZATION_LOOP.md",
]

REQUIRED_TEMPLATES = [
    "clients/_template/client_os.md",
    "clients/_template/intake.md",
    "clients/_template/proposal.md",
    "clients/_template/kickoff.md",
    "clients/_template/research_notes.md",
    "clients/_template/lead_table.csv",
    "clients/_template/outreach_pack.md",
    "clients/_template/delivery_report.md",
    "clients/_template/qa_checklist.md",
    "clients/_template/handoff.md",
    "clients/_template/feedback.md",
    "clients/_template/health_score.md",
    "clients/_template/retainer_offer.md",
    "clients/_template/proof_approval.md",
    "clients/_template/renewal.md",
]

REQUIRED_LOGS = [
    "delivery/qa_score_log.csv",
    "client_success/retention_tracker.csv",
    "client_success/client_success_dashboard.md",
]

EXPECTED_QA_HEADER = (
    "date,client,icp_fit,evidence_quality,lead_relevance,"
    "outreach_usefulness,summary_clarity,trust_safety,"
    "next_action_clarity,total_score,status,notes"
)

EXPECTED_RETENTION_HEADER = (
    "client,delivery_date,feedback_received,health_score,"
    "retainer_ask_sent,retainer_status,proof_status,next_action"
)

EXPECTED_LEAD_HEADER = (
    "company,sector,website,buyer_title,why_relevant,priority,"
    "evidence,suggested_angle,source,notes"
)

MIN_DOC_BYTES = 150
MIN_TEMPLATE_BYTES = 40


def _check(path_rel: str, min_size: int) -> str | None:
    path = REPO_ROOT / path_rel
    if not path.exists():
        return f"Missing: {path_rel}"
    if path.stat().st_size < min_size:
        return f"Too short ({path.stat().st_size} bytes < {min_size}): {path_rel}"
    return None


def _check_header(path_rel: str, expected_header: str) -> str | None:
    path = REPO_ROOT / path_rel
    if not path.exists():
        return f"Missing: {path_rel}"
    first_line = path.read_text(encoding="utf-8").splitlines()[:1]
    actual = first_line[0].strip() if first_line else ""
    if actual != expected_header:
        return (
            f"Wrong header in {path_rel}:\n"
            f"  expected: {expected_header}\n"
            f"  actual:   {actual}"
        )
    return None


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_DOCS:
        err = _check(rel, MIN_DOC_BYTES)
        if err:
            failures.append(err)

    for rel in REQUIRED_TEMPLATES:
        err = _check(rel, MIN_TEMPLATE_BYTES)
        if err:
            failures.append(err)

    for rel in REQUIRED_LOGS:
        err = _check(rel, MIN_TEMPLATE_BYTES)
        if err:
            failures.append(err)

    header_checks = [
        ("delivery/qa_score_log.csv", EXPECTED_QA_HEADER),
        ("client_success/retention_tracker.csv", EXPECTED_RETENTION_HEADER),
        ("clients/_template/lead_table.csv", EXPECTED_LEAD_HEADER),
    ]
    for rel, header in header_checks:
        err = _check_header(rel, header)
        if err:
            failures.append(err)

    if failures:
        print("Delivery & Client Success OS verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Delivery & Client Success OS is ready.")
    print(f"  docs:      {len(REQUIRED_DOCS)} required, all present")
    print(f"  templates: {len(REQUIRED_TEMPLATES)} required, all present")
    print(f"  logs:      {len(REQUIRED_LOGS)} required, all present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
