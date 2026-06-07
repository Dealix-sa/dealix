"""Doctrine guards + behaviour for the Saudi B2B target universe & daily draft pack.

These tests fail loudly if anyone (human or agent) introduces an un-sourced row,
PII, a cold channel, or a draft that is not approval-gated.
"""

from __future__ import annotations

from datetime import date

import pytest

from scripts.dealix_target_universe import (
    ALLOWED_CHANNELS,
    ALLOWED_SOURCE_TYPES,
    BLOCKED_SOURCE_TYPES,
    daily_selection,
    load_accounts,
    ranked,
)


@pytest.fixture(scope="module")
def accounts():
    return load_accounts()


def test_universe_non_empty(accounts):
    assert len(accounts) >= 10, "target universe should have a real seed of accounts"


def test_every_account_is_sourced(accounts):
    # Non-negotiable #4/#7 — no un-sourced claims.
    for a in accounts:
        assert a.source_url.startswith("http"), f"{a.company}: source_url must be a public URL"


def test_no_pii_stored(accounts):
    # Non-negotiable #6 — company-level public info only; no personal contact.
    for a in accounts:
        assert a.raw.get("contact", "").strip() == "", f"{a.company}: contact must be empty (no PII)"
        assert a.contact_status == "needs_warm_intro"


def test_only_approval_first_channels(accounts):
    # Non-negotiables #1-3, #8 — no cold/scraping/automation channels.
    for a in accounts:
        assert a.channel in ALLOWED_CHANNELS, f"{a.company}: channel {a.channel!r} not approval-first"


def test_no_blocked_sources(accounts):
    for a in accounts:
        assert a.source_type not in BLOCKED_SOURCE_TYPES
        assert a.source_type in ALLOWED_SOURCE_TYPES


def test_scores_in_range(accounts):
    for a in accounts:
        s = a.icp_score()
        assert 0 <= s <= 100


def test_ranked_is_descending(accounts):
    scores = [a.icp_score() for a in ranked(accounts)]
    assert scores == sorted(scores, reverse=True)


def test_daily_selection_defaults_to_top(accounts):
    sel = daily_selection(accounts, top_n=5)
    top5 = ranked(accounts)[:5]
    assert [a.company for a in sel] == [a.company for a in top5]


def test_rotation_covers_whole_universe(accounts):
    n = 5
    seen: set[str] = set()
    base = date(2026, 6, 1)
    # Walk enough days to cover every rotation window.
    for offset in range(0, (len(accounts) // n + 2)):
        d = date.fromordinal(base.toordinal() + offset)
        for a in daily_selection(accounts, top_n=n, on_date=d, rotate=True):
            seen.add(a.company)
    assert seen == {a.company for a in accounts}


def test_loader_rejects_unsourced(tmp_path):
    from scripts.dealix_target_universe import UniverseError
    from scripts.dealix_target_universe import load_accounts as load

    bad = tmp_path / "bad.csv"
    bad.write_text(
        "company,contact,segment,channel,source_type,source_url,status\n"
        "NoSource Co,,saas,warm_intro,public_business_info,,not_contacted\n",
        encoding="utf-8",
    )
    with pytest.raises(UniverseError):
        load(bad)


def test_loader_rejects_pii(tmp_path):
    from scripts.dealix_target_universe import UniverseError
    from scripts.dealix_target_universe import load_accounts as load

    bad = tmp_path / "pii.csv"
    bad.write_text(
        "company,contact,segment,channel,source_type,source_url,status\n"
        "PII Co,ceo@example.sa,saas,warm_intro,public_business_info,https://x.co,not_contacted\n",
        encoding="utf-8",
    )
    with pytest.raises(UniverseError):
        load(bad)


def test_loader_rejects_cold_channel(tmp_path):
    from scripts.dealix_target_universe import UniverseError
    from scripts.dealix_target_universe import load_accounts as load

    bad = tmp_path / "cold.csv"
    bad.write_text(
        "company,contact,segment,channel,source_type,source_url,status\n"
        "Cold Co,,saas,cold_whatsapp,public_business_info,https://x.co,not_contacted\n",
        encoding="utf-8",
    )
    with pytest.raises(UniverseError):
        load(bad)


def test_draft_pack_is_approval_gated(tmp_path):
    from scripts.dealix_daily_draft_pack import build_pack

    pack = build_pack(top_n=4, on_date=date(2026, 6, 7), founder="بسام", out_root=tmp_path)
    assert pack["batch_size"] == 4
    assert len(pack["items"]) == 4
    for item in pack["items"]:
        assert item["approval_status"] == "approval_required"
        assert item["governance_decision"] == "research_only"
        assert item["draft_count"] >= 1

    out_dir = tmp_path / "2026-06-07"
    index = (out_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "Estimated value is not Verified value" in index
    assert "no cold" in index.lower()

    # Every account file is approval-gated, carries the disclaimer, and has no PII.
    for item in pack["items"]:
        md = (out_dir / item["drafts_file"]).read_text(encoding="utf-8")
        assert "approval_required" in md
        assert "Estimated value is not Verified value" in md
        assert "NO COLD SEND" in md
