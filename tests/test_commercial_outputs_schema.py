"""Daily outputs hold a stable schema and safe flags."""

from __future__ import annotations

import json

from scripts.commercial_generate_400_drafts import build_outputs

REQUIRED_FIELDS = [
    "draft_id",
    "batch_id",
    "created_at",
    "company_name",
    "source_lead_id",
    "vertical",
    "country",
    "channel",
    "language",
    "buyer_persona",
    "buyer_title",
    "offer_stage",
    "offer_name",
    "pain_angle",
    "trigger_event",
    "subject",
    "body",
    "cta",
    "opt_out",
    "quality_score",
    "compliance_score",
    "fit_score",
    "priority_score",
    "risk_level",
    "research_required",
    "founder_notes",
    "rejection_reason",
    "status",
    "send_allowed",
    "external_send_blocked",
    "requires_founder_approval",
    "no_auto_send",
]


def _drafts(tmp_path):
    out_dir = tmp_path / "d"
    build_outputs(400, None, "2026-06-04", out_dir)
    return out_dir, [
        json.loads(ln)
        for ln in (out_dir / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def test_every_draft_has_required_fields(tmp_path):
    _, drafts = _drafts(tmp_path)
    for d in drafts:
        for field in REQUIRED_FIELDS:
            assert field in d, f"{d.get('draft_id')} missing {field}"


def test_no_internal_hint_keys_leak(tmp_path):
    _, drafts = _drafts(tmp_path)
    for d in drafts:
        assert not any(k.startswith("_") for k in d)


def test_rejected_records_have_reason(tmp_path):
    out_dir, _ = _drafts(tmp_path)
    rejected = [
        json.loads(ln)
        for ln in (out_dir / "rejected_drafts.jsonl").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    for d in rejected:
        assert "rejection_reason" in d
        assert d["rejection_reason"]


def test_daily_metrics_revenue_not_assumed(tmp_path):
    out_dir, _ = _drafts(tmp_path)
    metrics = json.loads((out_dir / "daily_metrics.json").read_text(encoding="utf-8"))
    assert metrics["drafts_generated"] >= 400
    assert metrics["safety_flags_invariant"]["send_allowed"] is False
