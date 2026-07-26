from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing" / "marketers.html"


FORBIDDEN_UNSUPPORTED_CLAIMS = (
    "ابدأ بـ 1 ريال",
    "99.9% Uptime",
    "34% تحسّن في ROAS",
    "18 ساعة/أسبوع",
    "60% وقت إعداد التقارير",
    "متوافق مرحلة 2",
    "4.8★",
    "دقة 88%+",
    "60% من عملائنا",
    "SOC 2 compliance",
    "SOC 2 (Q3 2026)",
    "البيانات في AWS me-south-1",
    "أسعارنا 40-60% أرخص",
    "توفّرلك 15 ساعة/أسبوع",
)

REQUIRED_GOVERNANCE_CONTRACT = (
    "تجربة مُدارة",
    "Draft-only",
    "لا يستبدل CRM",
    "لا نقدم ضمان نتائج",
    "يتوقف عند الموافقة",
    "لا تُفترض شهادات امتثال أو نتائج مالية أو تكاملات جاهزة دون دليل واختبار",
)


def test_marketers_landing_contains_no_unsupported_market_claims() -> None:
    source = LANDING.read_text(encoding="utf-8")

    for claim in FORBIDDEN_UNSUPPORTED_CLAIMS:
        assert claim not in source, f"Unsupported public claim returned: {claim}"


def test_marketers_landing_preserves_approval_first_pilot_contract() -> None:
    source = LANDING.read_text(encoding="utf-8")

    for contract in REQUIRED_GOVERNANCE_CONTRACT:
        assert contract in source, f"Missing governed landing contract: {contract}"

    assert "https://calendly.com/sami-assiri11/dealix-demo" in source
    assert "<html lang=\"ar\" dir=\"rtl\">" in source
