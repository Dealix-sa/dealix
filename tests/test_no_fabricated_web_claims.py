"""Doctrine guard — the public home page must not display fabricated proof.

Dealix is pre-revenue / founding-cohort. Non-negotiables #4 (no fake /
un-sourced claims) and #5 (no guaranteed outcomes) apply to the website,
not just to outreach drafts. This perimeter test fails if the previously
removed fabricated client logos, invented customer metrics, or made-up
testimonials ever reappear in the commercial launch home component.

If/when real, consented, sourced customer results exist, publish them via
the Proof Pack / Trust Center surfaces — never as hard-coded marketing
strings in this component.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOME = REPO_ROOT / "frontend" / "src" / "components" / "gtm" / "CommercialLaunchHome.tsx"

# High-signal strings from the old fabricated content. Their absence proves
# we did not regress to fake logos / metrics / testimonials.
_FORBIDDEN: tuple[tuple[str, str], ...] = (
    ("نماء للاستثمار", "fabricated client logo"),
    ("Oasis Tech", "fabricated client / testimonial company"),
    ("واحة التقنية", "fabricated client logo"),
    ("عميل راضٍ", "invented 'happy clients' metric"),
    ("Happy Clients", "invented 'happy clients' metric"),
    ("quoteAr", "fabricated testimonial structure"),
    ("quoteEn", "fabricated testimonial structure"),
    ("Guaranteed SLA", "guaranteed-outcome language (#5)"),
    ("SLA مضمون", "guaranteed-outcome language (#5)"),
)


@pytest.mark.skipif(not HOME.exists(), reason="home component not present")
def test_home_has_no_fabricated_proof() -> None:
    text = HOME.read_text(encoding="utf-8", errors="ignore")
    violations = [f"{pat!r} — {reason}" for pat, reason in _FORBIDDEN if pat in text]
    assert not violations, "fabricated web claim regression:\n  " + "\n  ".join(violations)


@pytest.mark.skipif(not HOME.exists(), reason="home component not present")
def test_home_keeps_honesty_signal() -> None:
    """The honest 'verified results only / no invented metrics' stance must stay."""
    text = HOME.read_text(encoding="utf-8", errors="ignore")
    assert ("نتائج موثّقة" in text) or ("Verified results only" in text), (
        "home page lost its honesty signal — re-add the 'verified results only' trust badge"
    )
