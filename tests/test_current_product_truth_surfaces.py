from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_SURFACES = [
    ROOT / "landing/index.html",
    ROOT / "landing/llms.txt",
    ROOT / "landing/pricing.html",
    ROOT / ".claude/agents/dealix-sales.md",
    ROOT / ".claude/agents/dealix-pm.md",
    ROOT / ".claude/agents/dealix-delivery.md",
]

RETIRED_OR_UNSUPPORTED_TEXT = [
    "499 SAR",
    "499 <small>",
    "1,500 SAR",
    "1,500 <small>",
    "2,999 SAR",
    "2,999 <small>",
    "7,999 <small>",
    "12,000 <small>",
    "2,999-4,999",
    "2,999–4,999",
    "5,000-25,000",
    "5,000–25,000",
    "25K-50K",
    "25,000–50,000",
    "7-Day Revenue",
    "7-day Revenue",
    "full refund",
    "استرجاع كامل",
    "10-20-30%",
    "8-15K SAR MRR",
    "50/50 payment terms",
    "claude/dealix-layers-40-200-HSWI8",
    "/checkout.html",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_authority_surfaces_exist_and_use_current_pilot() -> None:
    for path in AUTHORITY_SURFACES:
        assert path.is_file(), path
        text = _read(path)
        assert "Revenue Command Pilot" in text, path
        assert "approval" in text.lower(), path


def test_retired_commercial_terms_are_absent_from_authority_surfaces() -> None:
    for path in AUTHORITY_SURFACES:
        text = _read(path)
        for retired_text in RETIRED_OR_UNSUPPORTED_TEXT:
            assert retired_text not in text, f"{path}: {retired_text}"


def test_public_homepage_has_current_paths_and_no_private_contact_or_retired_links() -> None:
    text = _read(ROOT / "landing/index.html")

    assert "Free Mini Diagnostic" in text
    assert "Revenue Command Pilot — 30 days" in text
    assert "href=\"/diagnostic.html\"" in text
    assert "href=\"/pricing.html\"" in text
    assert "sami.assiri11@gmail.com" not in text

    retired_links = [
        "/roi.html",
        "/compare.html",
        "/launchpad.html",
        "/case-study.html",
    ]
    for retired_link in retired_links:
        assert retired_link not in text

    unsupported_homepage_claims = [
        "5 وكلاء AI جاهزين",
        "8 بوّابات أمان مقفلة",
        "PDPL Saudi-first",
        "امتثال + لغة سعوديّة",
    ]
    for claim in unsupported_homepage_claims:
        assert claim not in text


def test_public_llms_surface_is_quote_only_and_evidence_bounded() -> None:
    text = _read(ROOT / "landing/llms.txt")

    assert "Free Mini Diagnostic" in text
    assert "quote_only" in text
    assert "internal_experiment" in text
    assert "Revenue requires payment evidence" in text
    assert "Completed delivery requires proof evidence" in text

    unsupported_positive_claims = [
        "built on Saudi Cloud",
        "TLS 1.3 in transit",
        "AES-256 at rest",
        "HSM key management",
        "Pricing is transparent",
        "6-tier transparent ladder",
        "data residency inside KSA",
    ]
    for claim in unsupported_positive_claims:
        assert claim not in text


def test_public_pricing_has_only_current_entry_path() -> None:
    text = _read(ROOT / "landing/pricing.html")

    assert "Free Mini Diagnostic" in text
    assert "free_entry" in text
    assert "Revenue Command Pilot — 30 days" in text
    assert "quote_only" in text
    assert "عرض سعر بعد الاكتشاف" in text
    assert "/checkout.html" not in text
    assert "لا يوجد سعر عام ثابت" in text


def test_sales_and_pm_agents_name_canonical_commercial_sources() -> None:
    for relative_path in [
        ".claude/agents/dealix-sales.md",
        ".claude/agents/dealix-pm.md",
    ]:
        text = _read(ROOT / relative_path)
        assert "docs/DEALIX_BUSINESS_MODEL.md" in text
        assert "auto_client_acquisition/service_catalog/registry.py" in text
        assert "quote_only" in text
