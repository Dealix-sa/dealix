from __future__ import annotations

import csv
from pathlib import Path

from dealix.commercial_ops import first_paid_tracker as tracker


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
