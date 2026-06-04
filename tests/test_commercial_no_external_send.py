"""Hard contract: the Commercial Launch OS can never send anything externally."""

from __future__ import annotations

from scripts.commercial_launch_core import (
    FORBIDDEN_STATUSES,
    MANDATORY_FLAGS,
    generate_drafts,
    load_all_configs,
    load_seed_leads,
)
from scripts.commercial_safety_audit import run_safety_audit


def test_all_drafts_are_unsendable():
    result = generate_drafts(target=400, leads=load_seed_leads(), cfg=load_all_configs())
    assert len(result.drafts) >= 400
    for d in result.drafts:
        for flag, expected in MANDATORY_FLAGS.items():
            assert d[flag] is expected
        assert d["status"] not in FORBIDDEN_STATUSES


def test_mandatory_flags_are_the_safe_values():
    assert MANDATORY_FLAGS["send_allowed"] is False
    assert MANDATORY_FLAGS["external_send_blocked"] is True
    assert MANDATORY_FLAGS["requires_founder_approval"] is True
    assert MANDATORY_FLAGS["no_auto_send"] is True


def test_safety_audit_finds_no_send_capability():
    # Ensure outputs exist so the audit has data to scan.
    generate_drafts(target=400, leads=load_seed_leads())
    report = run_safety_audit()
    assert report["pass"] is True, report["violations"]
    assert report["violations"] == []
