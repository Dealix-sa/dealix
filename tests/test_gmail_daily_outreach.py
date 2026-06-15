"""Tests for the daily Gmail outreach system.

Covers:
- angle_for and render_outreach_email (in daily_targeting)
- load_targets, filter_and_rank, pick_diversified, build_draft (in the script)
- mark_drafted updates last_contacted
- Subject format
- Fallback angle for unknown sector
- No guaranteed-outcome language in generated emails
"""

from __future__ import annotations

import json
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

from auto_client_acquisition.email.daily_targeting import (
    angle_for,
    render_outreach_email,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_target(
    id_: str = "t-001",
    sector: str = "real_estate_developer",
    status: str = "pending",
    last_contacted: str | None = None,
    priority: str = "P0",
) -> dict[str, Any]:
    return {
        "id": id_,
        "company_ar": "شركة الاختبار",
        "company_en": "Test Company",
        "sector": sector,
        "sector_ar": "اختبار",
        "city": "Riyadh",
        "city_ar": "الرياض",
        "contact_email": None,
        "contact_name": None,
        "pain_signal": "test pain",
        "priority": priority,
        "status": status,
        "last_contacted": last_contacted,
        "notes": "",
    }


def _write_targets(targets: list[dict[str, Any]], tmp_dir: Path) -> Path:
    path = tmp_dir / "targets.json"
    path.write_text(json.dumps(targets, ensure_ascii=False), encoding="utf-8")
    return path


# ── angle_for ─────────────────────────────────────────────────────────────────

def test_angle_for_real_estate_developer() -> None:
    result = angle_for("real_estate_developer")
    assert "45 ثانية" in result
    assert "lead" in result


def test_angle_for_restaurant_chain() -> None:
    result = angle_for("restaurant_chain")
    assert "Dealix" in result
    assert "45 ثانية" in result


def test_angle_for_healthcare_clinic() -> None:
    result = angle_for("healthcare_clinic")
    assert "appointment" in result or "مواعيد" in result


def test_angle_for_car_dealership() -> None:
    result = angle_for("car_dealership")
    assert "سيارة" in result or "معرض" in result


def test_angle_for_unknown_sector_returns_default() -> None:
    result = angle_for("unknown_sector_xyz")
    assert "Dealix" in result
    assert "45 ثانية" in result


def test_angle_for_none_returns_default() -> None:
    result = angle_for(None)
    assert "Dealix" in result


def test_angle_for_construction() -> None:
    result = angle_for("construction")
    assert "RFQ" in result or "تسعير" in result


def test_angle_for_logistics() -> None:
    result = angle_for("logistics")
    assert "RFQ" in result or "شحن" in result


# ── render_outreach_email ─────────────────────────────────────────────────────

def test_render_outreach_email_contains_company_name() -> None:
    target = _make_target(sector="real_estate_developer")
    result = render_outreach_email(target)
    assert "شركة الاختبار" in result["body_ar"]


def test_render_outreach_email_subject_contains_company() -> None:
    target = _make_target(sector="real_estate_developer")
    result = render_outreach_email(target)
    assert "شركة الاختبار" in result["subject_ar"]
    assert result["subject_ar"].startswith("Dealix —")


def test_render_outreach_email_subject_has_pipe_separator() -> None:
    target = _make_target(sector="hospitality")
    result = render_outreach_email(target)
    assert "|" in result["subject_ar"]


def test_render_outreach_email_body_has_pilot_cta() -> None:
    target = _make_target(sector="events")
    result = render_outreach_email(target)
    assert "499 ريال" in result["body_ar"]
    assert "Pilot 7" in result["body_ar"]


def test_render_outreach_email_body_has_command_room_bullets() -> None:
    target = _make_target(sector="logistics")
    result = render_outreach_email(target)
    body = result["body_ar"]
    assert "غرفة قيادة" in body
    assert "نظام متابعة" in body
    assert "تقرير أسبوعي" in body


def test_render_outreach_email_body_has_calendly_link() -> None:
    target = _make_target(sector="car_dealership")
    result = render_outreach_email(target)
    assert "calendly.com/sami-assiri11/dealix-demo" in result["body_ar"]


def test_render_outreach_email_body_no_guaranteed_outcome_language() -> None:
    """Emails must not contain guaranteed-outcome claims."""
    for sector in (
        "real_estate_developer", "construction", "hospitality",
        "events", "logistics", "restaurant_chain", "healthcare_clinic", "car_dealership",
    ):
        target = _make_target(sector=sector)
        result = render_outreach_email(target)
        body_lower = result["body_ar"].lower()
        # The word "نضمن" (we guarantee) must not appear in outreach body
        assert "نضمن" not in body_lower, (
            f"Sector {sector!r}: outreach body must not contain guaranteed-outcome language"
        )


def test_render_outreach_email_all_required_keys_present() -> None:
    target = _make_target(sector="construction")
    result = render_outreach_email(target)
    assert "subject_ar" in result
    assert "body_ar" in result


# ── Script-level functions ─────────────────────────────────────────────────────

def test_load_targets(tmp_path: Path) -> None:
    targets = [_make_target()]
    path = _write_targets(targets, tmp_path)
    # Import inside test to avoid module-level side-effects
    import importlib, sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    loaded = script.load_targets(path)
    assert len(loaded) == 1
    assert loaded[0]["id"] == "t-001"


def test_is_contactable_pending_no_last(tmp_path: Path) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    t = _make_target(status="pending", last_contacted=None)
    assert script.is_contactable(t, date.today()) is True


def test_is_contactable_non_pending_rejected(tmp_path: Path) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    t = _make_target(status="contacted", last_contacted=None)
    assert script.is_contactable(t, date.today()) is False


def test_is_contactable_recent_last_contacted_rejected() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    recent = (date.today() - timedelta(days=10)).isoformat()
    t = _make_target(status="pending", last_contacted=recent)
    assert script.is_contactable(t, date.today()) is False


def test_is_contactable_old_last_contacted_allowed() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    old = (date.today() - timedelta(days=31)).isoformat()
    t = _make_target(status="pending", last_contacted=old)
    assert script.is_contactable(t, date.today()) is True


def test_filter_and_rank_p0_first() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    targets = [
        _make_target(id_="t-002", priority="P1"),
        _make_target(id_="t-001", priority="P0"),
    ]
    ranked = script.filter_and_rank(targets, date.today())
    assert ranked[0]["id"] == "t-001"
    assert ranked[1]["id"] == "t-002"


def test_filter_and_rank_sector_filter() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    targets = [
        _make_target(id_="t-001", sector="real_estate_developer"),
        _make_target(id_="t-002", sector="construction"),
    ]
    ranked = script.filter_and_rank(targets, date.today(), sector_filter="construction")
    assert len(ranked) == 1
    assert ranked[0]["id"] == "t-002"


def test_pick_diversified_respects_count() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    targets = [_make_target(id_=f"t-{i:03d}", sector="real_estate_developer") for i in range(20)]
    picked = script.pick_diversified(targets, count=5, max_per_sector=10)
    assert len(picked) == 5


def test_pick_diversified_caps_per_sector() -> None:
    """Sector cap is applied in the first pass.

    When count <= max_per_sector * num_sectors, the first pass fills quota
    and the top-up pass is not needed, so caps are honoured exactly.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    targets = [
        *[_make_target(id_=f"re-{i}", sector="real_estate_developer") for i in range(6)],
        *[_make_target(id_=f"co-{i}", sector="construction") for i in range(6)],
    ]
    # count=4 with max_per_sector=2 across 2 sectors: first pass fills 4, done.
    picked = script.pick_diversified(targets, count=4, max_per_sector=2)
    re_count = sum(1 for t in picked if t["sector"] == "real_estate_developer")
    co_count = sum(1 for t in picked if t["sector"] == "construction")
    assert re_count <= 2
    assert co_count <= 2
    assert len(picked) == 4


def test_build_draft_has_expected_keys() -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    target = _make_target(sector="hospitality")
    draft = script.build_draft(target)
    for key in ("id", "company_ar", "sector", "subject_ar", "body_ar", "generated_at"):
        assert key in draft, f"Missing key: {key}"


def test_mark_drafted_updates_json(tmp_path: Path) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    targets = [_make_target(id_="t-001")]
    path = _write_targets(targets, tmp_path)
    today = date.today()
    script.mark_drafted(targets, {"t-001"}, today, path=path)
    updated = json.loads(path.read_text(encoding="utf-8"))
    assert updated[0]["last_contacted"] == today.isoformat()


def test_write_digest_creates_file(tmp_path: Path) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import importlib
    # Patch _DATA_DIR to tmp_path
    import gmail_daily_outreach as script
    original = script._DATA_DIR
    script._DATA_DIR = tmp_path
    try:
        today = date(2026, 6, 14)
        draft = script.build_draft(_make_target(sector="events"))
        out = script.write_digest([draft], today)
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["date"] == "2026-06-14"
        assert data["count"] == 1
    finally:
        script._DATA_DIR = original


def test_run_dry_run_exits_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """run() in dry-run mode should not write files and return 0."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script

    targets = [
        _make_target(id_=f"t-{i:03d}", sector=s)
        for i, s in enumerate(
            ["real_estate_developer", "construction", "hospitality",
             "events", "logistics", "restaurant_chain",
             "healthcare_clinic", "car_dealership"],
            1,
        )
    ]
    path = _write_targets(targets, tmp_path)
    code = script.run(["--targets-path", str(path), "--dry-run", "--count", "3"])
    assert code == 0
    out = capsys.readouterr().out
    assert "شركة الاختبار" in out


def test_run_missing_file_exits_nonzero(tmp_path: Path) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    import gmail_daily_outreach as script
    code = script.run(["--targets-path", str(tmp_path / "nonexistent.json"), "--dry-run"])
    assert code != 0
