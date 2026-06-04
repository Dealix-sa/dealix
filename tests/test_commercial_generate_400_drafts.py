"""Tests for the 400/day commercial draft factory."""

from __future__ import annotations

from dealix.commercial_launch.engine import (
    REQUIRED_DRAFT_FIELDS,
    generate_drafts,
    load_config,
    validate_draft_invariants,
)


def test_generates_at_least_400_drafts() -> None:
    result = generate_drafts(target=400, seed=1, run_date="2026-01-01")
    assert result.total_accepted >= 400


def test_every_draft_has_required_fields() -> None:
    result = generate_drafts(target=400, seed=2, run_date="2026-01-01")
    for d in result.accepted[:50]:
        for f in REQUIRED_DRAFT_FIELDS:
            assert f in d, f"missing field {f}"


def test_every_draft_is_review_only() -> None:
    result = generate_drafts(target=400, seed=3, run_date="2026-01-01")
    for d in result.accepted:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["status"] in ("founder_review", "manual_review_only")
        assert validate_draft_invariants(d) == []


def test_no_banned_send_flags_present() -> None:
    result = generate_drafts(target=400, seed=4, run_date="2026-01-01")
    for d in result.accepted:
        for banned in ("auto_send", "smtp_send", "whatsapp_send", "linkedin_send", "api_send"):
            assert banned not in d or not d.get(banned)


def test_scores_and_opt_out_present() -> None:
    result = generate_drafts(target=400, seed=5, run_date="2026-01-01")
    for d in result.accepted:
        assert 70 <= d["quality_score"] <= 100
        assert 70 <= d["compliance_score"] <= 100
        body = d["body"]
        assert ("STOP" in body) or ("إيقاف" in body)


def test_channel_targets_met() -> None:
    cfg = load_config()
    result = generate_drafts(target=400, config=cfg, seed=6, run_date="2026-01-01")
    counts: dict[str, int] = {}
    for d in result.accepted:
        counts[d["channel"]] = counts.get(d["channel"], 0) + 1
    targets = cfg["launch"]["daily_targets_by_channel"]
    for channel, target in targets.items():
        assert counts.get(channel, 0) >= target, f"{channel}: {counts.get(channel, 0)} < {target}"


def test_five_verticals_all_represented() -> None:
    cfg = load_config()
    result = generate_drafts(target=400, config=cfg, seed=7, run_date="2026-01-01")
    verts = {d["vertical"] for d in result.accepted}
    expected = {v["id"] for v in cfg["verticals"]["verticals"]}
    assert len(expected) == 5
    assert expected.issubset(verts)


def test_bilingual_output() -> None:
    result = generate_drafts(target=400, seed=8, run_date="2026-01-01")
    langs = {d["language"] for d in result.accepted}
    assert "ar" in langs and "en" in langs


def test_runs_without_real_leads() -> None:
    # Passing an explicit empty lead list forces placeholder mode.
    result = generate_drafts(target=400, leads=[], seed=9, run_date="2026-01-01")
    assert result.used_real_leads is False
    assert result.total_accepted >= 400
    assert any("placeholder" in w.lower() for w in result.warnings)
    # placeholders must be flagged for research
    assert all(d["research_required"] for d in result.accepted)
