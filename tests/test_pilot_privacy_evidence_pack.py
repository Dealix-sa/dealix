"""Fail-closed contracts for the Pilot privacy evidence pack."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "docs" / "compliance"
LEDGER = COMPLIANCE / "PILOT_PRIVACY_EVIDENCE_LEDGER.csv"
RUNBOOK = COMPLIANCE / "PILOT_PRIVACY_DRILL_RUNBOOK.md"


def _ledger_rows() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_privacy_evidence_ledger_is_complete_and_fail_closed() -> None:
    rows = _ledger_rows()
    assert [row["Evidence ID"] for row in rows] == [
        f"PE-{number:03d}" for number in range(1, 13)
    ]

    required_columns = {
        "Evidence ID",
        "Gate",
        "Status",
        "Data Scope",
        "Environment",
        "Verification Method",
        "Pass Criteria",
        "Required Output",
        "Owner",
        "Reviewer",
        "Evidence Link",
        "Executed At",
        "Blocker",
        "Launch Effect",
    }
    assert required_columns <= set(rows[0])
    assert all(row["Gate"] for row in rows)
    assert all(row["Owner"] and row["Reviewer"] for row in rows)
    assert all(row["Status"] in {"blocked", "counsel_required"} for row in rows)
    assert not any(row["Status"] == "passed" for row in rows)
    assert all(row["Evidence Link"] == "" for row in rows)
    assert all(row["Executed At"] == "" for row in rows)
    assert all(row["Blocker"] for row in rows)
    assert all(row["Launch Effect"] in {"NO_REAL_CUSTOMER_DATA", "NO_LIVE_SEND"} for row in rows)


def test_legal_and_provider_decisions_cannot_be_implied_by_engineering() -> None:
    rows = {row["Evidence ID"]: row for row in _ledger_rows()}
    for evidence_id in ("PE-009", "PE-010", "PE-011"):
        assert rows[evidence_id]["Status"] == "counsel_required"
        assert rows[evidence_id]["Data Scope"] == "NO_CUSTOMER_DATA"
    for evidence_id in ("PE-002", "PE-012"):
        assert rows[evidence_id]["Status"] == "blocked"
        assert "evidence" in rows[evidence_id]["Pass Criteria"].lower() or "register" in rows[evidence_id]["Pass Criteria"].lower()


def test_technical_drills_are_synthetic_and_non_production() -> None:
    rows = {row["Evidence ID"]: row for row in _ledger_rows()}
    for evidence_id in ("PE-003", "PE-004", "PE-005", "PE-006", "PE-007", "PE-008"):
        row = rows[evidence_id]
        assert row["Data Scope"] == "SYNTHETIC_ONLY"
        assert "production" in row["Environment"].lower() or "tabletop" in row["Environment"].lower()
        assert row["Status"] == "blocked"


def test_runbook_preserves_hard_release_boundaries() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    for marker in (
        "#918",
        "SYNTHETIC_ONLY",
        "FAIL_CLOSED",
        "NO_REAL_CUSTOMER_DATA",
        "NO_LIVE_SEND",
        "NO_PRODUCTION_MUTATION",
        "Tenant isolation drill",
        "Export drill",
        "Deletion drill",
        "Suppression and opt-out drill",
        "Breach-response tabletop",
        "Backup, restore, deletion, and suppression interaction",
        "does not authorize launch",
    ):
        assert marker in text

    assert "not legal advice" in text
    assert "No gate may be marked `passed`" in text
    assert "do not change production" in text
    assert "do not send email, WhatsApp, LinkedIn, SMS" in text


def test_runbook_verification_is_contract_only() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "tests/test_pilot_launch_pack.py" in text
    assert "tests/test_pilot_privacy_evidence_pack.py" in text
    assert "does not execute provider, legal, production, or customer-data drills" in text
