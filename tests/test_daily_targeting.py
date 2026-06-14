"""Tests for the daily targeting engine and email composer."""

from __future__ import annotations

from dealix.daily_targeting.email_composer import EmailComposer
from dealix.daily_targeting.daily_engine import (
    DailyTargetingEngine,
    DailyReport,
    SAMPLE_ACCOUNTS,
)


# ---------------------------------------------------------------------------
# EmailComposer
# ---------------------------------------------------------------------------


def test_email_composer_compose_returns_required_keys() -> None:
    composer = EmailComposer()
    account = {
        "company_name": "Test Real Estate",
        "contact_name": "Ahmad",
        "email": "ahmad@test.sa",
        "sector": "real_estate",
        "region": "Riyadh",
    }
    result = composer.compose(account, score=80)
    assert "subject" in result
    assert "body_ar" in result
    assert "body_html" in result
    assert "offer_matched" in result
    assert "pain_points_used" in result
    assert "to_email" in result


def test_email_composer_high_score_maps_to_ai_os_offer() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Big Co", "contact_name": "Ali", "email": "a@b.sa",
         "sector": "real_estate", "region": "Riyadh"},
        score=80,
    )
    assert result["offer_matched"] == "نظام التشغيل بالذكاء الاصطناعي"


def test_email_composer_low_score_maps_to_free_diagnostic() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Small Co", "contact_name": "Ali", "email": "a@b.sa",
         "sector": "marketing_agency", "region": "Jeddah"},
        score=10,
    )
    assert result["offer_matched"] == "التشخيص المجاني"


def test_email_composer_mid_score_maps_to_managed_ops() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Mid Co", "contact_name": "Sara", "email": "s@mid.sa",
         "sector": "medical", "region": "Dammam"},
        score=60,
    )
    assert result["offer_matched"] == "حزمة العمليات المُدارة"


def test_email_composer_uses_two_pain_points() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Clinic A", "contact_name": "Doc", "email": "doc@clinic.sa",
         "sector": "medical", "region": "Riyadh"},
        score=55,
    )
    assert len(result["pain_points_used"]) == 2


def test_email_composer_sector_normalisation_arabic() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "عقارات الخليج", "contact_name": "خالد", "email": "k@gulf.sa",
         "sector": "عقار", "region": "الرياض"},
        score=70,
    )
    # Should pick real estate pain points
    pains = EmailComposer.SECTOR_PAIN_POINTS["real_estate"]
    assert result["pain_points_used"][0] in pains


def test_email_composer_body_contains_contact_name() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Test", "contact_name": "ناصر", "email": "n@t.sa",
         "sector": "training", "region": "Riyadh"},
        score=40,
    )
    assert "ناصر" in result["body_ar"]


def test_email_composer_signature_present() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Test", "contact_name": "Ali", "email": "a@t.sa",
         "sector": "default", "region": ""},
        score=45,
    )
    assert "Dealix" in result["body_ar"]
    assert "نظام تشغيل البيانات" in result["body_ar"]


def test_email_composer_html_contains_rtl_dir() -> None:
    composer = EmailComposer()
    result = composer.compose(
        {"company_name": "Test", "contact_name": "Ali", "email": "a@t.sa",
         "sector": "marketing_agency", "region": "Jeddah"},
        score=55,
    )
    assert "rtl" in result["body_html"]


def test_email_composer_subject_is_non_empty() -> None:
    composer = EmailComposer()
    for sector in ["real_estate", "medical", "training", "marketing_agency", "default"]:
        result = composer.compose(
            {"company_name": "X", "contact_name": "Y", "email": "y@x.sa",
             "sector": sector, "region": ""},
            score=50,
        )
        assert result["subject"], f"Empty subject for sector={sector}"


# ---------------------------------------------------------------------------
# DailyTargetingEngine
# ---------------------------------------------------------------------------


def test_daily_engine_loads_sample_accounts() -> None:
    engine = DailyTargetingEngine(dry_run=True)
    accounts = engine._load_accounts()
    assert len(accounts) >= 20


def test_daily_engine_score_all_returns_sorted_list() -> None:
    engine = DailyTargetingEngine(dry_run=True)
    accounts = engine._load_accounts()
    scored = engine._score_all(accounts)
    assert len(scored) == len(accounts)
    # Should be sorted descending
    for i in range(len(scored) - 1):
        assert scored[i].total >= scored[i + 1].total


def test_daily_engine_pick_targets_max_10() -> None:
    engine = DailyTargetingEngine(dry_run=True)
    accounts = engine._load_accounts()
    scored = engine._score_all(accounts)
    top = engine._pick_daily_targets(scored)
    assert len(top) <= 10


def test_daily_engine_pick_targets_skips_dq() -> None:
    engine = DailyTargetingEngine(dry_run=True)
    accounts = engine._load_accounts()
    scored = engine._score_all(accounts)
    top = engine._pick_daily_targets(scored)
    for t in top:
        assert t.tier != "DQ"
        assert t.total >= engine._MIN_SCORE


def test_daily_engine_run_returns_daily_report(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.daily_targeting.daily_engine.DailyTargetingEngine._REPORTS_DIR",
        tmp_path,
    )
    engine = DailyTargetingEngine(dry_run=True)
    report = engine.run()
    assert isinstance(report, DailyReport)
    assert report.dry_run is True
    assert report.total_accounts_loaded >= 20
    assert isinstance(report.top_targets, list)
    assert len(report.top_targets) <= 10


def test_daily_engine_run_saves_report_json(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.daily_targeting.daily_engine.DailyTargetingEngine._REPORTS_DIR",
        tmp_path,
    )
    engine = DailyTargetingEngine(dry_run=True)
    report = engine.run()
    saved = list(tmp_path.glob("*.json"))
    assert len(saved) == 1
    assert saved[0].name == f"{report.date}.json"


def test_daily_report_to_dict_has_required_keys(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.daily_targeting.daily_engine.DailyTargetingEngine._REPORTS_DIR",
        tmp_path,
    )
    engine = DailyTargetingEngine(dry_run=True)
    report = engine.run()
    d = report.to_dict()
    for key in ("date", "run_at", "dry_run", "top_targets", "tier_counts", "drafts_created"):
        assert key in d, f"Missing key: {key}"


def test_daily_engine_compose_emails_for_all_targets(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "dealix.daily_targeting.daily_engine.DailyTargetingEngine._REPORTS_DIR",
        tmp_path,
    )
    engine = DailyTargetingEngine(dry_run=True)
    accounts = engine._load_accounts()
    account_map = {a["account_id"]: a for a in accounts}
    scored = engine._score_all(accounts)
    top10 = engine._pick_daily_targets(scored)
    emails = engine._compose_emails(top10, account_map)
    assert len(emails) == len(top10)
    for email in emails:
        assert "subject" in email
        assert "body_ar" in email


def test_sample_accounts_count() -> None:
    assert len(SAMPLE_ACCOUNTS) == 20


def test_sample_accounts_sector_distribution() -> None:
    sectors = [a["sector"] for a in SAMPLE_ACCOUNTS]
    assert sectors.count("real_estate") == 5
    assert sectors.count("medical") == 5
    assert sectors.count("training") == 5
    assert sectors.count("marketing_agency") == 5


def test_sample_accounts_have_required_fields() -> None:
    required = {"account_id", "company_name", "contact_name", "email", "sector", "region"}
    for acc in SAMPLE_ACCOUNTS:
        for field in required:
            assert field in acc, f"Missing field '{field}' in account {acc.get('account_id')}"
