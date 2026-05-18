"""Regression tests for the M3 dry-run HIGH/MED gap fixes.

Covers: DQ unit rendering (G1), duplicate surfacing (G2), cold-channel
governance enforcement (G3), and the capital-asset minimum (G4/G8).
"""
from __future__ import annotations

import csv
import io

from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.delivery_factory.delivery_sprint import (
    _capital_minimum_met,
    _detect_duplicate_companies,
    run_sprint,
)
from auto_client_acquisition.governance_os.runtime_decision import decide

_DEMO_CSV = "data/demo/saudi_b2b_demo.csv"


def _load_demo() -> tuple[str, list[dict]]:
    text = open(_DEMO_CSV, encoding="utf-8").read()
    accounts = [dict(r) for r in csv.DictReader(io.StringIO(text))]
    return text, accounts


# --- G3: cold-channel governance gate ---------------------------------------

def test_cold_whatsapp_draft_is_blocked() -> None:
    result = decide(
        action="generate_draft",
        context={"text": "مرحبا", "channel": "whatsapp", "is_cold": True},
    )
    assert result.decision.value == "block"
    assert result.safe_alternative == "warm_intro_only"


def test_cold_linkedin_draft_is_blocked() -> None:
    result = decide(
        action="generate_draft",
        context={"text": "hello", "channel": "linkedin", "is_cold": True},
    )
    assert result.decision.value == "block"


def test_warm_email_draft_still_allowed() -> None:
    result = decide(
        action="generate_draft",
        context={"text": "hello", "channel": "email", "is_cold": False},
    )
    assert result.decision.value == "allow"


# --- G2: duplicate detection -------------------------------------------------

def test_detect_duplicate_companies_groups_repeats() -> None:
    rows = [
        {"company_name": "شركة بوابة الأعمال"},
        {"company_name": "بوابة الأعمال"},
        {"company_name": "Unique Co"},
        {"company_name": ""},
    ]
    dups = _detect_duplicate_companies(rows)
    assert len(dups) == 1
    assert dups[0]["occurrences"] == 2


# --- G4/G8: capital-asset minimum -------------------------------------------

def test_capital_minimum_requires_trust_and_knowledge() -> None:
    assert _capital_minimum_met(["proof_example", "sector_insight"]) is True
    assert _capital_minimum_met(["scoring_rule", "draft_template"]) is False
    assert _capital_minimum_met(["proof_example"]) is False


def test_capital_enum_has_eight_types() -> None:
    assert CapitalAssetType.QA_RUBRIC == "qa_rubric"
    assert CapitalAssetType.ARABIC_STYLE_PATTERN == "arabic_style_pattern"
    assert len(list(CapitalAssetType)) == 8


# --- G1 + end-to-end: proof pack renders DQ on the 0-100 scale --------------

def test_sprint_proof_pack_renders_dq_on_100_scale() -> None:
    text, accounts = _load_demo()
    run = run_sprint(
        engagement_id="test_fixes",
        customer_id="INTERNAL_TEST__pytest",
        raw_csv=text,
        accounts=accounts,
        problem_summary="pytest verification",
    )
    sections = (run.proof_pack or {}).get("sections", {})
    assert "/100" in sections["quality_scores"]
    assert "/1.00" not in sections["inputs"]
    assert "/1.00" not in sections["quality_scores"]


def test_sprint_registers_capital_minimum() -> None:
    text, accounts = _load_demo()
    run = run_sprint(
        engagement_id="test_capital",
        customer_id="INTERNAL_TEST__pytest",
        raw_csv=text,
        accounts=accounts,
    )
    step7 = next(s for s in run.steps if s.name == "capital_assets")
    assert step7.output["minimum_met"] is True
