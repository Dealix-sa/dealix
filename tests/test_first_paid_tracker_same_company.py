from __future__ import annotations

import csv
from pathlib import Path

from dealix.commercial_ops import evidence_append
from dealix.commercial_ops import first_paid_tracker as tracker
from dealix.commercial_ops import moyasar_payment_sync as payment_sync
from dealix.revenue_ops_autopilot import store as autopilot_store
from dealix.revenue_ops_autopilot.schemas import FunnelLeadRecord


def _configure_tracker(
    monkeypatch,
    tmp_path: Path,
    rows: list[dict[str, str]],
    *,
    crm_pending: bool = False,
) -> None:
    evidence = tmp_path / "docs/commercial/operations/evidence_events_tracker.csv"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    with evidence.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["event_type", "company", "notes"])
        writer.writeheader()
        writer.writerows(rows)

    kpi = tmp_path / "dealix/transformation/kpi_founder_commercial_import.yaml"
    kpi.parent.mkdir(parents=True, exist_ok=True)
    kpi.write_text(
        "status: pending_founder_export\n" if crm_pending else "status: synced\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(tracker, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(tracker, "EVIDENCE", evidence)
    monkeypatch.setattr(tracker, "KPI_YAML", kpi)
    monkeypatch.setattr(
        tracker,
        "DOD_DOC",
        tmp_path / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
    )
    monkeypatch.setattr(
        tracker,
        "SOFT_LAUNCH_TRACKER",
        tmp_path / "docs/commercial/operations/soft_launch_meetings_tracker.yaml",
    )


def test_different_companies_do_not_create_a_false_close(monkeypatch, tmp_path: Path) -> None:
    _configure_tracker(
        monkeypatch,
        tmp_path,
        [
            {"event_type": "payment_received", "company": "Company Alpha", "notes": "real"},
            {"event_type": "proof_pack_delivered", "company": "Company Beta", "notes": "real"},
        ],
    )

    result = tracker.analyze_first_paid_diagnostic()

    assert result["verdict"] == "IN_PROGRESS"
    assert result["first_close_ready"] is False
    assert result["matching_close_real"] == 0
    assert result["payment_without_proof_companies"] == ["Company Alpha"]
    assert result["proof_without_payment_companies"] == ["Company Beta"]


def test_same_company_payment_and_proof_can_close_after_kpi_sync(
    monkeypatch, tmp_path: Path
) -> None:
    _configure_tracker(
        monkeypatch,
        tmp_path,
        [
            {"event_type": "payment_received", "company": "  ACME Saudi ", "notes": "real"},
            {"event_type": "proof_pack_delivered", "company": "acme   saudi", "notes": "real"},
        ],
    )

    result = tracker.analyze_first_paid_diagnostic()

    assert result["verdict"] == "CLOSED"
    assert result["first_close_ready"] is True
    assert result["matching_close_real"] == 1
    assert result["matching_close_companies"] == ["ACME Saudi"]


def test_same_company_close_remains_blocked_while_crm_kpi_is_pending(
    monkeypatch, tmp_path: Path
) -> None:
    _configure_tracker(
        monkeypatch,
        tmp_path,
        [
            {"event_type": "payment_received", "company": "Company Alpha", "notes": "real"},
            {"event_type": "proof_pack_delivered", "company": "Company Alpha", "notes": "real"},
        ],
        crm_pending=True,
    )

    result = tracker.analyze_first_paid_diagnostic()

    assert result["verdict"] == "IN_PROGRESS"
    assert result["first_close_ready"] is False
    assert result["matching_close_real"] == 1
    assert result["crm_kpi_pending"] is True


def test_payment_evidence_resolves_checkout_lead_id_to_company(
    monkeypatch, tmp_path: Path
) -> None:
    store = autopilot_store.reset_autopilot_store_for_tests(tmp_path / "autopilot.json")
    store.upsert_lead(
        FunnelLeadRecord(
            id="lead-123",
            company="ACME Saudi",
            email="ops@acme.example",
            stage="invoice_sent",
        )
    )
    captured: dict[str, object] = {}

    def _capture_evidence(**kwargs):
        captured.update(kwargs)
        return kwargs

    monkeypatch.setattr(evidence_append, "append_evidence_row", _capture_evidence)
    try:
        result = payment_sync.append_payment_evidence(
            payment={
                "status": "paid",
                "amount": 499900,
                "metadata": {
                    "lead_id": "lead-123",
                    "email": "ops@acme.example",
                    "plan": "diagnostic",
                },
            },
            event_type="payment_paid",
        )
    finally:
        autopilot_store.clear_autopilot_store_singleton_for_tests()

    assert captured["company"] == "ACME Saudi"
    assert captured["contact"] == "ops@acme.example"
    assert result["identity_source"] == "lead_record"
    assert result["lead_id"] == "lead-123"


def test_canonical_lead_company_overrides_conflicting_payment_metadata(
    monkeypatch, tmp_path: Path
) -> None:
    store = autopilot_store.reset_autopilot_store_for_tests(tmp_path / "autopilot.json")
    store.upsert_lead(
        FunnelLeadRecord(
            id="lead-456",
            company="Canonical Company",
            email="owner@canonical.example",
            stage="invoice_sent",
        )
    )
    captured: dict[str, object] = {}

    def _capture_evidence(**kwargs):
        captured.update(kwargs)
        return kwargs

    monkeypatch.setattr(evidence_append, "append_evidence_row", _capture_evidence)
    try:
        result = payment_sync.append_payment_evidence(
            payment={
                "status": "paid",
                "amount": 499900,
                "metadata": {
                    "lead_id": "lead-456",
                    "email": "owner@canonical.example",
                    "company": "Conflicting Metadata Company",
                },
            },
            event_type="payment_paid",
        )
    finally:
        autopilot_store.clear_autopilot_store_singleton_for_tests()

    assert captured["company"] == "Canonical Company"
    assert result["identity_source"] == "lead_record"


def test_payment_evidence_does_not_treat_email_as_company(tmp_path: Path) -> None:
    autopilot_store.reset_autopilot_store_for_tests(tmp_path / "empty-autopilot.json")
    try:
        result = payment_sync.append_payment_evidence(
            payment={
                "status": "paid",
                "amount": 499900,
                "metadata": {"email": "unknown@example.com", "plan": "diagnostic"},
            },
            event_type="payment_paid",
        )
    finally:
        autopilot_store.clear_autopilot_store_singleton_for_tests()

    assert result == {"skipped": True, "reason": "no_resolved_company_identity"}
