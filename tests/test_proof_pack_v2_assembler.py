"""Tests for Sprint Day-5 Proof Pack assembly (v2 surface)."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.data_os.account_ranker import ICPProfile, rank_accounts
from auto_client_acquisition.data_os.csv_intake import score_csv
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
)
from auto_client_acquisition.proof_os.proof_pack_assembler import (
    ProofPackAssemblyResult,
    assemble_proof_pack,
)

HEADER = "company_name,sector,city,source,email,phone\n"


def _csv(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "accounts.csv"
    p.write_text(HEADER + body, encoding="utf-8")
    return p


def _common(tmp_path: Path):
    p = _csv(
        tmp_path,
        "Acme,fintech,Riyadh,crm_export,ceo@acme.sa,+966500000001\n"
        "Beta,fintech,Riyadh,crm_export,ceo@beta.sa,+966500000002\n"
        "Gamma,health,Jeddah,crm_export,ceo@gamma.sa,+966500000003\n",
    )
    csv_report = score_csv(p, has_valid_passport=True)
    icp = ICPProfile(preferred_sectors=("fintech",), preferred_cities=("riyadh",))
    rows = [
        {"company_name": "Acme", "sector": "fintech", "city": "Riyadh",
         "source": "crm_export", "email": "ceo@acme.sa", "phone": "+966500000001"},
        {"company_name": "Beta", "sector": "fintech", "city": "Riyadh",
         "source": "crm_export", "email": "ceo@beta.sa", "phone": "+966500000002"},
        {"company_name": "Gamma", "sector": "health", "city": "Jeddah",
         "source": "crm_export", "email": "ceo@gamma.sa", "phone": "+966500000003"},
    ]
    ranking = rank_accounts(rows, icp=icp, top_n=3)
    return csv_report, ranking


def test_assemble_returns_all_fourteen_sections_in_order(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot — top 10",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["ICP rubric v1"],
        source_passport_id="SP-001",
        recommended_next_step="Approve top-3 outreach drafts",
        retainer_expansion_path="Managed Ops if proof>=80",
    )
    assert isinstance(result, ProofPackAssemblyResult)
    assert tuple(result.sections.keys()) == PROOF_PACK_V2_SECTIONS


def test_full_inputs_yield_score_100(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Reusable rubric"],
        source_passport_id="SP-001",
        governance_decisions=[{"action": "send", "verdict": "ALLOW"}],
        blocked_risks=["No high-risk targets detected"],
        recommended_next_step="Approve drafts",
        retainer_expansion_path="Managed Ops path",
    )
    assert result.proof_score == 100
    assert result.band == "case_candidate"
    assert result.missing_sections == ()


def test_minimum_inputs_leave_missing_sections(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Rubric"],
    )
    assert result.proof_score < 100
    assert "source_passports" in result.missing_sections
    assert "recommended_next_step" in result.missing_sections


def test_missing_customer_name_raises(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    with pytest.raises(ValueError, match="customer_name"):
        assemble_proof_pack(
            customer_name="",
            sprint_scope="Pilot",
            csv_report=csv_report,
            ranking=ranking,
            capital_assets=["Rubric"],
        )


def test_missing_capital_asset_raises(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    with pytest.raises(ValueError, match="capital asset"):
        assemble_proof_pack(
            customer_name="TestCo",
            sprint_scope="Pilot",
            csv_report=csv_report,
            ranking=ranking,
            capital_assets=[],
        )


def test_executive_summary_contains_non_guarantee_disclaimer(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Rubric"],
    )
    assert "not guaranteed" in result.sections["executive_summary"]


def test_value_metrics_reports_methodology_not_outcomes(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Rubric"],
    )
    vm = result.sections["value_metrics"]
    assert "Methodology metrics" in vm
    assert "No pipeline outcomes claimed" in vm


def test_to_dict_is_serializable(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    payload = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Rubric"],
    ).to_dict()
    assert payload["capital_asset_count"] == 1
    assert isinstance(payload["sections"], dict)
    assert 0 <= payload["proof_score"] <= 100


def test_quality_scores_section_includes_dq_breakdown(tmp_path: Path) -> None:
    csv_report, ranking = _common(tmp_path)
    result = assemble_proof_pack(
        customer_name="TestCo",
        sprint_scope="Pilot",
        csv_report=csv_report,
        ranking=ranking,
        capital_assets=["Rubric"],
    )
    qs = result.sections["quality_scores"]
    assert "completeness" in qs
    assert "duplicate_inverse" in qs
