"""Safety & compliance audit over a generated draft queue.

PASS criteria (all must hold):
- send_allowed == False for every draft               (0 send-allowed)
- external_send_blocked == True for every draft        (0 unblocked)
- no_auto_send == True for every draft                 (0 auto-send)
- requires_founder_approval == True for every draft
- no forbidden / overclaim language in any body
- no routable contact fields (email/phone) on any draft
"""

from __future__ import annotations

import json
from pathlib import Path

from .compliance import find_forbidden_claims

_CONTACT_FIELDS = ("email", "phone", "mobile", "whatsapp", "to_address", "recipient_email")


def load_drafts(queue_path: Path) -> list[dict]:
    drafts: list[dict] = []
    with queue_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                drafts.append(json.loads(line))
    return drafts


def audit(drafts: list[dict]) -> dict:
    """Run the safety audit and return a structured result dict."""
    n = len(drafts)
    send_allowed_true = sum(1 for d in drafts if d.get("send_allowed") is True)
    external_blocked_false = sum(1 for d in drafts if d.get("external_send_blocked") is not True)
    no_auto_send_false = sum(1 for d in drafts if d.get("no_auto_send") is not True)
    needs_approval_false = sum(1 for d in drafts if d.get("requires_founder_approval") is not True)

    overclaim_drafts: list[str] = []
    contact_field_drafts: list[str] = []
    for d in drafts:
        body = f"{d.get('subject_en','')} {d.get('subject_ar','')} {d.get('body_en','')} {d.get('body_ar','')}"
        if find_forbidden_claims(body):
            overclaim_drafts.append(d.get("draft_id", "?"))
        if any(f in d for f in _CONTACT_FIELDS):
            contact_field_drafts.append(d.get("draft_id", "?"))

    checks = {
        "draft_count_ge_1": n >= 1,
        "send_allowed_true_count_is_zero": send_allowed_true == 0,
        "external_send_blocked_false_count_is_zero": external_blocked_false == 0,
        "no_auto_send_false_count_is_zero": no_auto_send_false == 0,
        "requires_founder_approval_all_true": needs_approval_false == 0,
        "no_overclaim_language": len(overclaim_drafts) == 0,
        "no_routable_contact_fields": len(contact_field_drafts) == 0,
    }
    passed = all(checks.values())

    return {
        "pass": passed,
        "total_drafts": n,
        "counts": {
            "send_allowed_true": send_allowed_true,
            "external_send_blocked_false": external_blocked_false,
            "no_auto_send_false": no_auto_send_false,
            "requires_founder_approval_false": needs_approval_false,
            "overclaim_drafts": len(overclaim_drafts),
            "contact_field_drafts": len(contact_field_drafts),
        },
        "checks": checks,
        "offending": {
            "overclaim_drafts": overclaim_drafts[:25],
            "contact_field_drafts": contact_field_drafts[:25],
        },
    }


def audit_queue(queue_path: Path) -> dict:
    return audit(load_drafts(queue_path))
