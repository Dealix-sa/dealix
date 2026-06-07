"""Doctrine-enforcing tests for the Dealix Now engine.

Fully deterministic and offline: no network, no API keys, no LLM. Every public
function in ``dealix/now`` is exercised, plus the doctrine guards (no auto-send,
approval-first, no pricing in drafts, single CTA, public-data-only).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dealix.now import (
    build_now_pack,
    check_draft_safety,
    ledger,
    load_targets,
    render_daily_brief_markdown,
    route_offer,
    score_company,
    write_company_brief,
    write_outreach_draft,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_GOLDEN = _REPO_ROOT / "apps" / "web" / "public" / "now-pack.json"

# Golden-sample companies -> (expected tier, expected total) and offer id.
_GOLDEN_TIERS = {
    "Madar Logistics": ("high", 80),
    "المجموعة الهندسية الوطنية": ("medium", 76),
    "عيادات الشفاء المتخصصة": ("medium", 66),
    "NorthStar Clinics Group": ("medium", 64),
    "سلسلة مطاعم الأصالة": ("nurture", 58),
    "وكالة إبداع للتسويق": ("nurture", 48),
}
_GOLDEN_OFFERS = {
    "Madar Logistics": "RET",
    "المجموعة الهندسية الوطنية": "PCOS",
    "عيادات الشفاء المتخصصة": "AGP",
    "NorthStar Clinics Group": "WFA",
    "سلسلة مطاعم الأصالة": "WFA",
    "وكالة إبداع للتسويق": "RAOS",
}


@pytest.fixture()
def targets() -> list[dict]:
    return load_targets()


@pytest.fixture()
def by_name(targets: list[dict]) -> dict[str, dict]:
    return {t["company_name"]: t for t in targets}


# ─────────────────────────── seed ───────────────────────────


def test_seed_skips_blank_name(targets: list[dict]) -> None:
    assert all(t["company_name"].strip() for t in targets)


def test_seed_dedupes_duplicate_company(targets: list[dict]) -> None:
    dupes = [t for t in targets if t["company_name"] == "شركة بوابة الأعمال"]
    assert len(dupes) == 1
    # Dedupe keeps the latest last_interaction (2026-04-27 over 2026-04-26).
    assert dupes[0]["last_interaction"] == "2026-04-27"


def test_seed_count_is_24(targets: list[dict]) -> None:
    # 26 data rows - 1 blank-name - 1 duplicate fold = 24.
    assert len(targets) == 24


def test_seed_rows_normalized(by_name: dict[str, dict]) -> None:
    madar = by_name["Madar Logistics"]
    assert madar["sector"] == "logistics"
    assert madar["relationship_status"] == "warm"
    assert madar["id"].startswith("lead_")


# ─────────────────────────── scoring ───────────────────────────


def test_scores_within_bounds(targets: list[dict]) -> None:
    for t in targets:
        s = score_company(t)
        assert 0 <= s["total_score"] <= 100


def test_tier_thresholds_map_correctly() -> None:
    cases = [
        (
            {
                "sector": "logistics",
                "notes": "previous diagnostic delivered; awaiting retainer",
                "relationship_status": "warm",
            },
            "high",
        ),
    ]
    for target, expected_tier in cases:
        assert score_company(target)["tier"] == expected_tier
    # Boundary mapping is exact per os/05 decision_thresholds.
    from dealix.now.scoring import _tier_for  # type: ignore[attr-defined]

    assert _tier_for(80)[0] == "high"
    assert _tier_for(79)[0] == "medium"
    assert _tier_for(60)[0] == "medium"
    assert _tier_for(59)[0] == "nurture"
    assert _tier_for(40)[0] == "nurture"
    assert _tier_for(39)[0] == "disqualified"
    assert _tier_for(0)[0] == "disqualified"


def test_fm_logistics_heavy_row_scores_high(by_name: dict[str, dict]) -> None:
    s = score_company(by_name["Madar Logistics"])
    assert s["tier"] == "high"
    assert s["total_score"] >= 80


def test_golden_six_land_on_same_tier(by_name: dict[str, dict]) -> None:
    for name, (tier, total) in _GOLDEN_TIERS.items():
        s = score_company(by_name[name])
        assert s["tier"] == tier, f"{name}: tier {s['tier']} != {tier}"
        assert abs(s["total_score"] - total) <= 2, f"{name}: {s['total_score']} vs {total}"


def test_score_output_shape(by_name: dict[str, dict]) -> None:
    s = score_company(by_name["Madar Logistics"])
    assert set(s) >= {
        "total_score",
        "tier",
        "tier_color",
        "tier_action_ar",
        "dimension_scores",
        "top_strengths",
        "top_weaknesses",
    }
    assert len(s["dimension_scores"]) == 8
    for dim in s["dimension_scores"]:
        assert set(dim) == {"id", "score", "level"}


# ─────────────────────────── offer routing ───────────────────────────


def test_offer_healthcare_zatca_routes_agp(by_name: dict[str, dict]) -> None:
    t = by_name["عيادات الشفاء المتخصصة"]
    assert route_offer(t, score_company(t))["id"] == "AGP"


def test_offer_engineering_routes_pcos(by_name: dict[str, dict]) -> None:
    t = by_name["المجموعة الهندسية الوطنية"]
    assert route_offer(t, score_company(t))["id"] == "PCOS"


def test_offer_warm_prior_diagnostic_routes_ret(by_name: dict[str, dict]) -> None:
    t = by_name["Madar Logistics"]
    assert route_offer(t, score_company(t))["id"] == "RET"


def test_offer_default_is_wfa() -> None:
    target = {
        "company_name": "Plain Co",
        "sector": "training",
        "relationship_status": "cold",
        "notes": "no strong signals",
        "id": "lead_plain",
    }
    assert route_offer(target, score_company(target))["id"] == "WFA"


def test_golden_six_route_same_offer(by_name: dict[str, dict]) -> None:
    for name, offer_id in _GOLDEN_OFFERS.items():
        t = by_name[name]
        assert route_offer(t, score_company(t))["id"] == offer_id, name


def test_offer_prices_from_catalog(by_name: dict[str, dict]) -> None:
    t = by_name["عيادات الشفاء المتخصصة"]
    offer = route_offer(t, score_company(t))
    assert offer["entry_price_sar"] == {"min": 15000, "max": 100000, "typical": 35000}
    assert offer["name_ar"]


# ─────────────────────────── brief ───────────────────────────


def test_brief_shape_and_confidence(by_name: dict[str, dict]) -> None:
    t = by_name["Madar Logistics"]
    s = score_company(t)
    brief = write_company_brief(t, s, route_offer(t, s))
    assert set(brief) == {
        "what_they_do_ar",
        "operations_complexity",
        "public_signals",
        "confidence",
    }
    assert brief["operations_complexity"] in {"low", "medium", "high"}
    assert 0.4 <= brief["confidence"] <= 0.7


def test_brief_confidence_lower_for_cold_low_data() -> None:
    warm = {
        "company_name": "Warm Co",
        "sector": "logistics",
        "relationship_status": "warm",
        "notes": "diagnostic delivered; awaiting retainer",
        "city": "Jeddah",
    }
    cold = {
        "company_name": "Cold Co",
        "sector": "logistics",
        "relationship_status": "cold",
        "notes": "data quality untested; legacy crm",
        "city": "Jeddah",
    }
    cw = write_company_brief(warm, score_company(warm), route_offer(warm, score_company(warm)))
    cc = write_company_brief(cold, score_company(cold), route_offer(cold, score_company(cold)))
    assert cc["confidence"] < cw["confidence"]


# ─────────────────────────── drafts ───────────────────────────


def _draftable(by_name: dict[str, dict]) -> list[dict]:
    out = []
    for t in by_name.values():
        s = score_company(t)
        d = write_outreach_draft(t, s, route_offer(t, s))
        if d is not None:
            out.append((t, d))
    return out


def test_draft_status_is_literal(by_name: dict[str, dict]) -> None:
    for _t, d in _draftable(by_name):
        assert d["status"] == "draft — awaiting founder approval"


def test_draft_within_length_and_single_cta(by_name: dict[str, dict]) -> None:
    for _t, d in _draftable(by_name):
        assert d["word_count"] <= 150
        assert (d["body"].count("?") + d["body"].count("؟")) == 1


def test_draft_mentions_company(by_name: dict[str, dict]) -> None:
    for t, d in _draftable(by_name):
        assert t["company_name"] in d["body"]


def test_draft_has_no_pricing_in_body(by_name: dict[str, dict]) -> None:
    money_re = re.compile(r"\d{4,}|\d{1,3}[,\.]\d{3}")
    price_words = (
        "sar",
        "ريال",
        "سعر",
        "أسعار",
        "تكلفة",
        "price",
        "cost",
        "pricing",
        "$",
        "usd",
        "ر.س",
    )
    for _t, d in _draftable(by_name):
        body_l = d["body"].lower()
        assert not money_re.search(d["body"]), d["body"]
        assert not any(w in body_l for w in price_words), d["body"]


def test_draft_contact_stub_and_channel(by_name: dict[str, dict]) -> None:
    for _t, d in _draftable(by_name):
        assert d["channel"] == "email"
        assert d["lang"] == "ar"
        assert d["contact"]["to"] == ""
        assert "Dealix لا يرسل" in d["contact"]["note_ar"]


def test_nurture_rows_produce_no_draft(by_name: dict[str, dict]) -> None:
    t = by_name["سلسلة مطاعم الأصالة"]  # nurture
    s = score_company(t)
    assert s["tier"] == "nurture"
    assert write_outreach_draft(t, s, route_offer(t, s)) is None


# ─────────────────────────── safety ───────────────────────────


def test_clean_draft_approved_for_review(by_name: dict[str, dict]) -> None:
    t = by_name["Madar Logistics"]
    s = score_company(t)
    d = write_outreach_draft(t, s, route_offer(t, s))
    assert d is not None
    result = check_draft_safety(d)
    assert result["approved_for_review"] is True
    assert all(result["checks"].values())
    assert set(result["checks"]) == {
        "mentions_company",
        "single_pain",
        "single_cta",
        "no_pricing",
        "within_length",
        "no_overclaim",
    }


def test_injected_pricing_draft_rejected() -> None:
    bad = {
        "subject": "عرض خاص",
        "body": "أهلاً، نقدم النظام بسعر 20,000 ريال شهريًا فقط — هل تشترك؟",
        "company_name": "شركة تجريبية",
        "word_count": 11,
    }
    result = check_draft_safety(bad)
    assert result["approved_for_review"] is False
    assert result["checks"]["no_pricing"] is False


def test_injected_overclaim_draft_rejected() -> None:
    bad = {
        "subject": "نحن شركة رائدة",
        "body": "نحن شركة رائدة ونضمن لك النتائج — هل نبدأ؟",
        "company_name": "شركة تجريبية",
        "word_count": 9,
    }
    result = check_draft_safety(bad)
    assert result["approved_for_review"] is False
    assert result["checks"]["no_overclaim"] is False


# ─────────────────────────── ledger ───────────────────────────


@pytest.fixture()
def ledger_env(tmp_path, monkeypatch) -> Path:
    path = tmp_path / "now_ledger.jsonl"
    monkeypatch.setenv("DEALIX_NOW_LEDGER_PATH", str(path))
    return path


def test_approve_logs_and_returns_send_links_without_sending(ledger_env: Path) -> None:
    draft = {
        "id": "draft_demo",
        "subject": "موضوع تجريبي",
        "body": "نص الرسالة التجريبي.",
        "company_name": "شركة تجريبية",
        "contact": {"to": "", "note_ar": ""},
    }
    result = ledger.approve("draft_demo", draft)
    assert result["ok"] is True
    assert "never auto-sends" in result["status"]
    assert result["mailto"].startswith("mailto:")
    assert "subject=" in result["mailto"]
    assert result["whatsapp"].startswith("https://wa.me/")
    # The ledger file got exactly one line; nothing else was produced.
    assert ledger_env.exists()
    lines = [ln for ln in ledger_env.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["draft_id"] == "draft_demo"
    assert rec["decision"] == "approved"


def test_reject_logs_only(ledger_env: Path) -> None:
    result = ledger.reject("draft_x")
    assert result["ok"] is True
    assert "nothing sent" in result["status"]
    decisions = ledger.list_decisions()
    assert any(d["draft_id"] == "draft_x" and d["decision"] == "rejected" for d in decisions)


def test_record_decision_normalizes_unknown(ledger_env: Path) -> None:
    rec = ledger.record_decision("draft_y", "sent_externally")
    # An unknown decision is never silently treated as a send.
    assert rec["decision"] == "noted"


def test_ledger_has_no_send_attribute() -> None:
    # Hard doctrine guard: the ledger module exposes no send/dispatch surface.
    forbidden = ("send", "dispatch", "deliver", "transmit", "post", "smtp", "email_send")
    public = {name for name in dir(ledger) if not name.startswith("_")}
    assert not (public & set(forbidden))


# ─────────────────────────── pack ───────────────────────────


def test_pack_has_golden_top_level_keys() -> None:
    golden = json.loads(_GOLDEN.read_text(encoding="utf-8"))
    pack = build_now_pack(today="2026-06-07")
    assert set(pack.keys()) == set(golden.keys())


def test_pack_lead_and_draft_shape_match_golden() -> None:
    golden = json.loads(_GOLDEN.read_text(encoding="utf-8"))
    pack = build_now_pack(today="2026-06-07")
    assert set(pack["leads"][0].keys()) == set(golden["leads"][0].keys())
    assert set(pack["metrics"].keys()) == set(golden["metrics"].keys())
    assert set(pack["pipeline"].keys()) == set(golden["pipeline"].keys())
    assert set(pack["drafts"][0].keys()) == set(golden["drafts"][0].keys())
    assert set(pack["priorities"][0].keys()) == set(golden["priorities"][0].keys())


def test_pack_metrics_internally_consistent() -> None:
    pack = build_now_pack(today="2026-06-07")
    m = pack["metrics"]
    assert m["leads_total"] == len(pack["leads"])
    assert (
        m["priority_high"] + m["priority_medium"] + m["nurture"] + m["disqualified"]
        == m["leads_total"]
    )
    assert m["drafts_ready"] == len(pack["drafts"])
    # Drafts only for high+medium tiers.
    assert m["drafts_ready"] == m["priority_high"] + m["priority_medium"]
    assert m["pipeline_value_sar"]["low"] <= m["pipeline_value_sar"]["high"]


def test_pack_is_not_sample_and_deterministic() -> None:
    p1 = build_now_pack(today="2026-06-07")
    p2 = build_now_pack(today="2026-06-07")
    assert p1["is_sample"] is False
    assert p1 == p2  # deterministic given the same date + seed
    assert p1["tz"] == "Asia/Riyadh"
    assert p1["date"] == "2026-06-07"


def test_pack_priorities_at_most_three() -> None:
    pack = build_now_pack(today="2026-06-07")
    assert len(pack["priorities"]) <= 3


def test_pack_doctrine_flags_true() -> None:
    pack = build_now_pack(today="2026-06-07")
    d = pack["doctrine"]
    assert d["no_auto_send"] is True
    assert d["no_scraping"] is True
    assert d["public_data_only"] is True
    assert d["approval_first"] is True


# ─────────────────────────── daily brief ───────────────────────────


def test_daily_brief_markdown_structure_and_footer() -> None:
    pack = build_now_pack(today="2026-06-07")
    md = render_daily_brief_markdown(pack)
    assert "## 1. Revenue Pipeline" in md
    assert "أولويات اليوم الثلاث" in md
    assert "Intelligence Alerts" in md
    assert md.strip().endswith(
        "*مُولَّد تلقائياً بواسطة Dealix Chief of Staff Agent — للقراءة اليومية فقط، لا يُرسل لأي طرف خارجي*"
    )


# ─────────────────────────── api smoke ───────────────────────────


def test_now_routes_registered(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./_now_smoke.db")
    from api.main import create_app

    app = create_app()
    paths = {getattr(r, "path", "") for r in app.routes}
    assert "/api/v1/now/pack" in paths
    assert "/api/v1/now/drafts/{draft_id}/approve" in paths
    assert "/api/v1/now/daily-brief" in paths
