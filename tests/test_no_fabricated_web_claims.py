"""Doctrine guard — public marketing surfaces must not display fabricated proof.

Dealix is pre-revenue / founding-cohort. Non-negotiables #4 (no fake /
un-sourced claims) and #5 (no guaranteed outcomes) apply to the website, not
just to outreach drafts. This perimeter test fails if removed fabricated
content — invented client logos, made-up testimonials/case studies, false
consent claims, or claimed-but-unmeasured metrics — ever reappears across the
key public components.

When real, consented, sourced customer results exist, publish them via the
Proof Pack / Trust Center surfaces with evidence — never as hard-coded
marketing strings.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FE = REPO_ROOT / "frontend" / "src"

HOME = FE / "components" / "gtm" / "CommercialLaunchHome.tsx"

# Public marketing components scanned for fabricated proof.
SCANNED = [
    HOME,
    FE / "components" / "gtm" / "TestimonialsSection.tsx",
    FE / "components" / "gtm" / "CaseStudiesSection.tsx",
    FE / "components" / "gtm" / "DealixDiagnosticLanding.tsx",
    FE / "components" / "trust" / "TrustCenter.tsx",
]

# High-signal strings from the removed fabricated content. Their absence proves
# we have not regressed to fake logos / metrics / testimonials / case studies /
# false consent claims / claimed-but-unmeasured security metrics.
_FORBIDDEN: tuple[tuple[str, str], ...] = (
    # Fake home logos / metrics / testimonial structure
    ("نماء للاستثمار", "fabricated client logo"),
    ("Oasis Tech", "fabricated client / testimonial company"),
    ("واحة التقنية", "fabricated client logo"),
    ("عميل راضٍ", "invented 'happy clients' metric"),
    ("Happy Clients", "invented 'happy clients' metric"),
    ("quoteAr", "fabricated testimonial structure"),
    ("quoteEn", "fabricated testimonial structure"),
    # Guaranteed-outcome language (#5)
    ("Guaranteed SLA", "guaranteed-outcome language"),
    ("SLA مضمون", "guaranteed-outcome language"),
    # Fabricated diagnostic / case-study "results" + false consent claims (#4)
    ("كشف تسرّب إيراد 18%", "fabricated diagnostic result"),
    ("Results from Real Saudi Companies", "fabricated case-study claim"),
    ("نتائج من شركات سعودية", "fabricated results claim"),
    ("Testimonials from real clients", "false consent claim"),
    ("شهادات من عملاء حقيقيين", "false consent claim"),
    ("Indicative results from real projects", "false consent claim"),
    ("نتائج استرشادية من مشاريع حقيقية", "false consent claim"),
    # Claimed-but-unmeasured security metrics (Trust Center)
    ("Over the past 90 days", "claimed-but-unmeasured uptime metric"),
    ("على مدار 90 يوماً الماضية", "claimed-but-unmeasured uptime metric"),
    ("Last Security Audit", "claimed-but-unperformed audit metric"),
    ("آخر مراجعة أمنية", "claimed-but-unperformed audit metric"),
)


def test_public_components_have_no_fabricated_proof() -> None:
    violations: list[str] = []
    for path in SCANNED:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat, reason in _FORBIDDEN:
            if pat in text:
                violations.append(f"{path.name}: {pat!r} — {reason}")
    assert not violations, "fabricated web claim regression:\n  " + "\n  ".join(violations)


@pytest.mark.skipif(not HOME.exists(), reason="home component not present")
def test_home_keeps_honesty_signal() -> None:
    """The honest 'verified results only / no invented metrics' stance must stay."""
    text = HOME.read_text(encoding="utf-8", errors="ignore")
    assert ("نتائج موثّقة" in text) or ("Verified results only" in text), (
        "home page lost its honesty signal — re-add the 'verified results only' trust badge"
    )
