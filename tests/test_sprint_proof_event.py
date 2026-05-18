"""Sprint records a ProofEvent into the ledger after step 6.

Covers C3: ``run_sprint`` writes a ``sprint_proof_pack`` proof event whose
level is derived from the real evidence signals — a thin/empty run stays
weak_proof (L1) and is never fabricated.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from auto_client_acquisition.delivery_factory.delivery_sprint import (
    _proof_level_from_signals,
    run_sprint,
)


def test_proof_level_thin_run_stays_l1() -> None:
    assert _proof_level_from_signals(evidence_signals=0, governance_blocked=False) == "L1"
    assert _proof_level_from_signals(evidence_signals=1, governance_blocked=False) == "L1"


def test_proof_level_scales_with_signals() -> None:
    assert _proof_level_from_signals(evidence_signals=2, governance_blocked=False) == "L2"
    assert _proof_level_from_signals(evidence_signals=3, governance_blocked=False) == "L3"
    assert _proof_level_from_signals(evidence_signals=4, governance_blocked=False) == "L4"


def test_proof_level_never_l5_and_block_caps_at_l1() -> None:
    # No signal count produces L5 — that rung is revenue-only.
    for n in range(0, 5):
        assert _proof_level_from_signals(
            evidence_signals=n, governance_blocked=False
        ) != "L5"
    # A governance block caps the level at L1.
    assert _proof_level_from_signals(evidence_signals=4, governance_blocked=True) == "L1"


@pytest.fixture
def captured_events() -> list:
    return []


def _patched_ledger(sink: list):
    class _FakeLedger:
        def record(self, event):  # noqa: ANN001
            sink.append(event)
            return event

    return _FakeLedger()


def test_run_sprint_records_proof_event(captured_events: list) -> None:
    """A real run with input data records exactly one sprint_proof_pack event."""
    passport = {
        "source_id": "TEST-SPRINT-001",
        "source_type": "client_upload",
        "owner": "dealix",
        "allowed_use": ["internal_analysis", "scoring"],
        "contains_pii": False,
        "sensitivity": "low",
        "ai_access_allowed": True,
        "external_use_allowed": False,
        "retention_policy": "project_duration",
    }
    csv = (
        "company,sector,relationship_status\n"
        "Acme,retail,warm\n"
        "Globex,logistics,cold\n"
    )
    accounts = [
        {"company": "Acme", "sector": "retail", "relationship_status": "warm"},
        {"company": "Globex", "sector": "logistics", "relationship_status": "cold"},
    ]
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_patched_ledger(captured_events),
    ):
        run = run_sprint(
            engagement_id="eng_test_001",
            customer_id="cust_test",
            source_passport=passport,
            raw_csv=csv,
            accounts=accounts,
            problem_summary="Rank Saudi B2B accounts.",
        )

    assert run.proof_pack is not None
    sprint_events = [
        e for e in captured_events
        if (e.payload or {}).get("kind") == "sprint_proof_pack"
    ]
    assert len(sprint_events) == 1
    ev = sprint_events[0]
    assert ev.service_id == "eng_test_001"
    assert ev.customer_visible is False
    assert ev.publish_consent is False
    assert ev.approved_by is None
    assert ev.level in ("L1", "L2", "L3", "L4")


def test_empty_run_proof_event_stays_l1(captured_events: list) -> None:
    """A run with no input data must stay weak_proof (L1) — never fabricated."""
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_patched_ledger(captured_events),
    ):
        run_sprint(
            engagement_id="eng_empty_001",
            customer_id="cust_empty",
            source_passport=None,
            raw_csv=b"",
            accounts=[],
        )
    sprint_events = [
        e for e in captured_events
        if (e.payload or {}).get("kind") == "sprint_proof_pack"
    ]
    assert len(sprint_events) == 1
    assert sprint_events[0].level == "L1"
