"""Acceptance contract for the sample-company operating loop.

These tests prevent a false-green daily run where generated artifacts disagree
with the CEO brief or the review queue consumed by the web application.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from scripts import generate_daily_ceo_brief as ceo_brief
from scripts import generate_outreach_drafts as outreach


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_generated_draft_matches_canonical_review_contract() -> None:
    draft = outreach.build_draft(
        {
            "id": "sample-logistics-001",
            "name": "Najd Fleet Logistics",
            "segment": "logistics",
            "demo": True,
        },
        "ar",
        "whatsapp",
        generated_at="2026-07-25T12:00:00Z",
    )

    assert draft["id"] == "draft-sample-logistics-001-ar"
    assert draft["accountId"] == "sample-logistics-001"
    assert draft["reviewStatus"] == "draft_pending_human_review"
    assert draft["demo"] is True
    assert "human_review_required" in draft["safetyFlags"]
    assert draft["disclaimer"] == "DRAFT — Do not send without human review."


def test_write_outputs_keeps_one_canonical_queue_and_compatibility_export(
    tmp_path: Path,
    monkeypatch,
) -> None:
    canonical = tmp_path / "business" / "_data" / "outreach_review_queue.json"
    exports = tmp_path / "business" / "persuasion" / "exports"
    monkeypatch.setattr(outreach, "CANONICAL_QUEUE_PATH", canonical)
    monkeypatch.setattr(outreach, "EXPORT_DIR", exports)

    draft = outreach.build_draft(
        {"id": "sample-001", "name": "Sample Co", "segment": "b2b_services"},
        "en",
        "email",
        generated_at="2026-07-25T12:00:00Z",
    )
    canonical_path, compatibility_path = outreach.write_outputs(
        [draft],
        "demo",
        date=dt.date(2026, 7, 25),
    )

    canonical_payload = json.loads(canonical_path.read_text(encoding="utf-8"))
    compatibility_payload = json.loads(compatibility_path.read_text(encoding="utf-8"))

    assert canonical_payload["drafts"][0]["reviewStatus"] == "draft_pending_human_review"
    assert canonical_payload["notice"].startswith("Draft only")
    assert compatibility_payload[0]["review_status"] == "pending_review"
    assert canonical_path.name == "outreach_review_queue.json"


def test_ceo_brief_uses_runtime_queue_and_followup_counts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    leads_path = tmp_path / "leads.json"
    queue_path = tmp_path / "outreach_review_queue.json"
    monkeypatch.setattr(ceo_brief, "LEADS_PATH", leads_path)
    monkeypatch.setattr(ceo_brief, "OUTREACH_QUEUE_PATH", queue_path)

    _write_json(
        leads_path,
        {
            "accounts": [
                {"id": "a", "nextActionDate": "2026-07-25"},
                {"id": "b", "nextActionDate": "2026-07-27"},
                {"id": "c", "nextActionDate": "2026-08-10"},
                {"id": "d", "nextActionDate": "not-a-date"},
            ]
        },
    )
    _write_json(
        queue_path,
        {
            "drafts": [
                {"reviewStatus": "draft_pending_human_review"},
                {"reviewStatus": "draft_pending_human_review"},
                {"reviewStatus": "approved"},
            ]
        },
    )

    date = dt.date(2026, 7, 25)
    metrics = ceo_brief.load_operating_metrics(date)
    report = ceo_brief.render_brief(date, metrics)

    assert metrics == {
        "drafts_pending_review": 2,
        "followups_due_today": 1,
        "followups_upcoming_7d": 1,
    }
    assert "Drafts awaiting human review: 2" in report
    assert "Follow-ups due now: 1" in report
    assert "Follow-ups in next 7 days: 1" in report
    assert "current 14" not in report
    assert "current 8" not in report


def test_ceo_brief_reports_zero_when_runtime_artifacts_are_missing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(ceo_brief, "LEADS_PATH", tmp_path / "missing-leads.json")
    monkeypatch.setattr(ceo_brief, "OUTREACH_QUEUE_PATH", tmp_path / "missing-queue.json")

    metrics = ceo_brief.load_operating_metrics(dt.date(2026, 7, 25))

    assert metrics == {
        "drafts_pending_review": 0,
        "followups_due_today": 0,
        "followups_upcoming_7d": 0,
    }
