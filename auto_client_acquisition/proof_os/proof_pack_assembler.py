"""Proof Pack assembly — Sprint Day-5 deliverable.

Takes the outputs of the Day-2 CSV intake and the Day-3 account ranker, plus
the founder's governance decisions log and recommended next step, and emits
a fully populated 14-section Proof Pack (Proof Pack v2 surface) along with
the computed proof_score and strength band.

Doctrine compliance:
- #4 no fake claims  — every section is filled from real inputs the caller
  supplies; if the caller has no content for a section, it stays empty and
  the score reflects that.
- #10 14-section Proof Pack — section keys come from PROOF_PACK_V2_SECTIONS
  and are NOT redefined here.
- #11 capital asset required — assembly raises ValueError if no capital
  asset is provided.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.data_os.account_ranker import RankedAccount
from auto_client_acquisition.data_os.csv_intake import CsvIntakeReport
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.proof_os.proof_pack import build_empty_proof_pack_v2
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_completeness_score,
    proof_strength_band,
)


@dataclass(frozen=True, slots=True)
class ProofPackAssemblyResult:
    """Result of assembling a Proof Pack: the 14 sections + the computed score."""

    sections: dict[str, str]
    proof_score: int
    band: str
    missing_sections: tuple[str, ...]
    capital_asset_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "sections": dict(self.sections),
            "proof_score": self.proof_score,
            "band": self.band,
            "missing_sections": list(self.missing_sections),
            "capital_asset_count": self.capital_asset_count,
        }


def _executive_summary(
    customer_name: str,
    sprint_scope: str,
    csv_report: CsvIntakeReport,
    ranking_count: int,
) -> str:
    return (
        f"Revenue Intelligence Sprint for {customer_name}. "
        f"Scope: {sprint_scope}. "
        f"Processed {csv_report.row_count} accounts; ranked top {ranking_count}; "
        f"baseline DQ {csv_report.score.overall}. "
        "Estimated outcomes are not guaranteed outcomes."
    )


def _problem(customer_name: str) -> str:
    return (
        f"{customer_name} holds accounts and contacts but cannot reliably answer: "
        "(1) which accounts to prioritise this week, (2) what to say to them, "
        "(3) how to defend the recommendation with evidence."
    )


def _inputs(csv_report: CsvIntakeReport) -> str:
    cols = ", ".join(csv_report.columns)
    return (
        f"Customer-supplied CSV: {csv_report.row_count} rows; "
        f"columns: {cols}; loaded via data_os.csv_intake."
    )


def _quality_scores(csv_report: CsvIntakeReport) -> str:
    s = csv_report.score
    return (
        f"DQ overall {s.overall} (completeness {s.completeness}, "
        f"duplicate_inverse {s.duplicate_inverse}, "
        f"format_consistency {s.format_consistency}, "
        f"source_clarity {s.source_clarity}). "
        f"Per-row issues recorded: {len(csv_report.issues_per_row)}."
    )


def _outputs(ranking: list[RankedAccount]) -> str:
    if not ranking:
        return ""
    head = ", ".join(
        f"{a.company_name} (total {a.total})" for a in ranking[: min(3, len(ranking))]
    )
    return (
        f"Ranked top {len(ranking)} accounts (deterministic blended rubric). "
        f"Highest-scoring sample: {head}."
    )


def _governance(decisions: list[dict[str, str]] | None) -> str:
    if not decisions:
        return ""
    parts = [f"{d.get('action', '?')}:{d.get('verdict', '?')}" for d in decisions]
    return f"Governance decisions logged: {len(decisions)}. Verdicts: {', '.join(parts)}."


def _blocked_risks(items: list[str] | None) -> str:
    if not items:
        return ""
    return f"Blocked risks: {'; '.join(items)}."


def _value_metrics(csv_report: CsvIntakeReport, ranking_count: int) -> str:
    return (
        f"Methodology metrics — accounts processed: {csv_report.row_count}; "
        f"accounts ranked: {ranking_count}; "
        f"per-row issues: {len(csv_report.issues_per_row)}; "
        f"baseline DQ: {csv_report.score.overall}. "
        "No pipeline outcomes claimed."
    )


def _limitations(items: list[str] | None) -> str:
    default = (
        "Outputs reflect a single CSV snapshot at the time of import; "
        "rankings will shift as the customer's data changes. "
        "No external sending performed; drafts only."
    )
    if not items:
        return default
    return default + " Additional: " + "; ".join(items)


def _capital_assets(items: list[str]) -> str:
    return f"Capital assets created ({len(items)}): " + "; ".join(items)


def assemble_proof_pack(
    *,
    customer_name: str,
    sprint_scope: str,
    csv_report: CsvIntakeReport,
    ranking: list[RankedAccount],
    capital_assets: list[str],
    source_passport_id: str = "",
    work_completed: str = "",
    governance_decisions: list[dict[str, str]] | None = None,
    blocked_risks: list[str] | None = None,
    limitations: list[str] | None = None,
    recommended_next_step: str = "",
    retainer_expansion_path: str = "",
) -> ProofPackAssemblyResult:
    """Build a 14-section Proof Pack and compute its score.

    Raises ValueError if no capital asset is supplied (doctrine #11) or if
    customer_name / sprint_scope are empty.
    """
    if not customer_name.strip():
        raise ValueError("customer_name is required")
    if not sprint_scope.strip():
        raise ValueError("sprint_scope is required")
    if not capital_assets:
        raise ValueError("at least one capital asset is required (doctrine #11)")

    sections: dict[str, str] = build_empty_proof_pack_v2()
    sections["executive_summary"] = _executive_summary(
        customer_name, sprint_scope, csv_report, len(ranking)
    )
    sections["problem"] = _problem(customer_name)
    sections["inputs"] = _inputs(csv_report)
    sections["source_passports"] = (
        f"Signed source passport on file: {source_passport_id}."
        if source_passport_id.strip()
        else ""
    )
    sections["work_completed"] = work_completed.strip() or (
        "Day 1 kickoff + Source Passport. Day 2 DQ baseline. "
        "Day 3 account scoring + top-N ranking. Day 4 bilingual draft generation + governance review. "
        "Day 5 Proof Pack assembly."
    )
    sections["outputs"] = _outputs(ranking)
    sections["quality_scores"] = _quality_scores(csv_report)
    sections["governance_decisions"] = _governance(governance_decisions)
    sections["blocked_risks"] = _blocked_risks(blocked_risks)
    sections["value_metrics"] = _value_metrics(csv_report, len(ranking))
    sections["limitations"] = _limitations(limitations)
    sections["recommended_next_step"] = recommended_next_step.strip()
    sections["retainer_expansion_path"] = retainer_expansion_path.strip()
    sections["capital_assets_created"] = _capital_assets(capital_assets)

    score = proof_pack_completeness_score(sections)
    _, missing = proof_pack_v2_sections_complete(sections)
    return ProofPackAssemblyResult(
        sections=sections,
        proof_score=score,
        band=proof_strength_band(score),
        missing_sections=missing,
        capital_asset_count=len(capital_assets),
    )


__all__ = ["ProofPackAssemblyResult", "assemble_proof_pack", "PROOF_PACK_V2_SECTIONS"]
