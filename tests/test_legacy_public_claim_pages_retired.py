from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_PAGES = [
    ROOT / "landing/roi.html",
    ROOT / "landing/case-study.html",
    ROOT / "landing/compare.html",
    ROOT / "landing/launchpad.html",
]

UNSAFE_LEGACY_CLAIMS = [
    "499 ريال",
    "999 ريال",
    "5,000 SAR",
    "12,000 SAR",
    "3.2x",
    "45 ثانية",
    "45 ث",
    "استرجاع 100%",
    "استرجاع كامل",
    "100% refund",
    "PDPL-compliant",
    "14-day deploy",
    "اشتر اليوم",
    "ابدأ بكره",
    "KPI lift",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_retired_public_claim_pages_are_noindex_and_corrective() -> None:
    for path in RETIRED_PAGES:
        assert path.is_file(), path
        text = _read(path)
        assert 'content="noindex,nofollow"' in text, path
        assert "/diagnostic.html" in text or "/pricing.html" in text or "/proof.html" in text
        for unsafe_claim in UNSAFE_LEGACY_CLAIMS:
            assert unsafe_claim not in text, f"{path}: {unsafe_claim}"


def test_sitemap_excludes_retired_claim_pages_and_uses_canonical_domain() -> None:
    sitemap = _read(ROOT / "landing/sitemap.xml")

    assert "https://dealix.me/" in sitemap
    for retired_name in ["roi.html", "case-study.html", "compare.html", "launchpad.html"]:
        assert retired_name not in sitemap


def test_retired_pages_do_not_offer_checkout_or_fixed_price_purchase() -> None:
    for path in RETIRED_PAGES:
        text = _read(path)
        assert "/checkout.html" not in text, path
        assert "tier=" not in text, path
        assert "عرض سعر" in text or "دليل" in text or "إثبات" in text, path
