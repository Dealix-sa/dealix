"""Canonical disclaimer constant — core/constants.py.

This test intentionally asserts the EXACT string content (not just
"is non-empty" or "contains a substring"). The whole point of this
constant is that many independent subsystems agree on it byte-for-byte;
a future contributor silently editing the wording here would otherwise
go unnoticed until it caused a customer-facing inconsistency again.
"""
from __future__ import annotations

from core.constants import (
    CANONICAL_DISCLAIMER_AR,
    CANONICAL_DISCLAIMER_BILINGUAL,
    CANONICAL_DISCLAIMER_EN,
)


def test_canonical_disclaimer_en_exact_wording():
    assert CANONICAL_DISCLAIMER_EN == "Estimated value is not Verified value"


def test_canonical_disclaimer_ar_exact_wording():
    assert CANONICAL_DISCLAIMER_AR == "القيمة التقديرية ليست قيمة مُتحقَّقة"


def test_canonical_disclaimer_bilingual_exact_wording():
    assert CANONICAL_DISCLAIMER_BILINGUAL == (
        "Estimated value is not Verified value / "
        "القيمة التقديرية ليست قيمة مُتحقَّقة"
    )


def test_canonical_disclaimer_bilingual_composes_en_and_ar():
    """The combined string must always be EN + ' / ' + AR — never drift
    independently from the two component constants."""
    assert CANONICAL_DISCLAIMER_BILINGUAL == (
        f"{CANONICAL_DISCLAIMER_EN} / {CANONICAL_DISCLAIMER_AR}"
    )


def test_canonical_disclaimer_matches_launch_master_plan():
    """The constant must match the exact wording that
    docs/LAUNCH_MASTER_PLAN.md — the canonical 90-day plan — uses for its
    own bilingual disclosure line and launch-readiness gate."""
    from pathlib import Path

    plan_path = (
        Path(__file__).resolve().parent.parent / "docs" / "LAUNCH_MASTER_PLAN.md"
    )
    plan_text = plan_path.read_text(encoding="utf-8")
    assert CANONICAL_DISCLAIMER_EN in plan_text
    assert CANONICAL_DISCLAIMER_AR in plan_text


def test_no_guarantee_language_in_the_disclaimer_itself():
    """The disclaimer's own wording must never accidentally contain a
    guarantee claim — it exists specifically to disclaim one."""
    lowered = CANONICAL_DISCLAIMER_EN.lower()
    assert "guarantee" not in lowered
    assert "مضمون" not in CANONICAL_DISCLAIMER_AR
