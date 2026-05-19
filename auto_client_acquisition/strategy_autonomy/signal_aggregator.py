"""Strategic signal aggregator — company signals into one CEO-tier snapshot.

Pulls revenue, proof, adoption, governance-risk and capital signals from
existing ledgers and scorers, then normalizes them into the seven
:class:`StrategySignalInputs` subscores used by the strategy decision
score. Every external call is friction-safe: a failure appends a warning
and never crashes the aggregation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any

from auto_client_acquisition.intelligence_os.strategy_decision import (
    StrategySignalInputs,
)

# Day-90 plan launch anchor. The 90-day execution plan counts day-windows
# from the commercial launch date.
LAUNCH_DATE: str = "2026-03-01"


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, float(value)))


def _resolve_date(on_date: Any) -> str:
    if on_date is None:
        return date.today().isoformat()
    if isinstance(on_date, date):
        return on_date.isoformat()
    return str(on_date)


def _days_between(launch: str, current: str) -> int:
    try:
        d0 = datetime.fromisoformat(launch).date()
        d1 = datetime.fromisoformat(current).date()
        return max(0, (d1 - d0).days)
    except Exception:  # noqa: BLE001
        return 0


@dataclass(frozen=True, slots=True)
class StrategicSignalSnapshot:
    """Normalized CEO-tier signal snapshot for one strategic cycle."""

    customer_id: str
    on_date: str
    days_since_launch: int
    # Raw company metrics.
    total_revenue_sar: int
    mrr_sar: int
    paid_customers: int
    retainer_count: int
    proof_event_count: int
    proof_score: float
    adoption_score: float
    governance_risk_index: float
    capital_asset_count: int
    founder_hours_per_sprint: float
    # Seven normalized subscores (0-100) for the strategy decision score.
    signal_inputs: dict[str, float] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def as_strategy_inputs(self) -> StrategySignalInputs:
        """Project the snapshot into the strategy decision score inputs."""
        s = self.signal_inputs
        return StrategySignalInputs(
            revenue_signal=s.get("revenue", 0.0),
            margin_signal=s.get("margin", 0.0),
            proof_signal=s.get("proof", 0.0),
            repeatability_signal=s.get("repeatability", 0.0),
            governance_safety=s.get("governance", 0.0),
            productization_signal=s.get("productization", 0.0),
            strategic_moat=s.get("moat", 0.0),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def aggregate_strategic_signals(
    *,
    on_date: Any = None,
    customer_id: str = "dealix_strategic",
    pipeline_summary: dict[str, int] | None = None,
    founder_hours_per_sprint: float = 0.0,
) -> StrategicSignalSnapshot:
    """Aggregate company signals into a single strategic snapshot.

    Every external call is friction-safe — a failure appends to
    ``warnings`` and falls back to a conservative default.
    """
    on_date_str = _resolve_date(on_date)
    days_since_launch = _days_between(LAUNCH_DATE, on_date_str)
    warnings: list[str] = []

    summary = dict(pipeline_summary or {})

    # ── revenue truth ───────────────────────────────────────────────
    total_revenue_sar = 0
    paid_customers = 0
    commitments = 0
    proof_event_count = 0
    try:
        from auto_client_acquisition.revenue_pipeline.revenue_truth import (
            snapshot_revenue_truth,
        )

        rev = snapshot_revenue_truth(
            pipeline_summary=summary,
            proof_event_files_count=int(summary.get("proof_event_files_count", 0)),
        )
        total_revenue_sar = int(rev.total_revenue_sar)
        paid_customers = int(rev.paid)
        commitments = int(rev.commitments)
        proof_event_count = int(rev.proof_event_files_count)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"revenue_truth: {exc}")
        total_revenue_sar = int(summary.get("total_revenue_sar", 0))
        paid_customers = int(summary.get("paid", 0))
        commitments = int(summary.get("commitments", 0))

    mrr_sar = int(summary.get("mrr_sar", 0))
    retainer_count = int(summary.get("retainer_count", 0))

    # ── proof score ─────────────────────────────────────────────────
    proof_score = float(summary.get("proof_score", 0.0))

    # ── adoption score ──────────────────────────────────────────────
    adoption_value = float(summary.get("adoption_score", 0.0))
    try:
        from auto_client_acquisition.adoption_os.adoption_score import compute

        adoption = compute(
            customer_id=customer_id,
            channels_enabled=int(summary.get("channels_enabled", 0)),
            integrations_connected=int(summary.get("integrations_connected", 0)),
            sectors_targeted=int(summary.get("sectors_targeted", 0)),
            total_drafts_lifetime=int(summary.get("total_drafts_lifetime", 0)),
            logins_last_30d=int(summary.get("logins_last_30d", 0)),
            drafts_approved_last_30d=int(summary.get("drafts_approved_last_30d", 0)),
            replies_acted_on_last_30d=int(summary.get("replies_acted_on_last_30d", 0)),
        )
        adoption_value = float(adoption.score)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"adoption_score: {exc}")

    # ── governance risk index ───────────────────────────────────────
    governance_risk = float(summary.get("governance_risk_index", 0.0))
    try:
        from auto_client_acquisition.command_os.governance_risk_index import (
            GovernanceRiskInputs,
            compute_governance_risk_index,
        )

        governance_risk = compute_governance_risk_index(
            GovernanceRiskInputs(
                pii_sensitivity=float(summary.get("pii_sensitivity", 20.0)),
                external_action_potential=float(
                    summary.get("external_action_potential", 20.0)
                ),
                source_uncertainty=float(summary.get("source_uncertainty", 20.0)),
                claim_risk=float(summary.get("claim_risk", 10.0)),
                channel_risk=float(summary.get("channel_risk", 10.0)),
                agent_autonomy=float(summary.get("agent_autonomy", 30.0)),
                client_industry_sensitivity=float(
                    summary.get("client_industry_sensitivity", 20.0)
                ),
            )
        )
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"governance_risk_index: {exc}")

    # ── capital assets ──────────────────────────────────────────────
    capital_asset_count = int(summary.get("capital_asset_count", 0))
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets

        capital_asset_count = len(list_assets(limit=500))
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"capital_ledger: {exc}")

    # ── normalize into the seven strategy subscores ─────────────────
    # Revenue: 40K SAR cumulative is the day-90 target → 100.
    revenue_signal = _clamp(total_revenue_sar / 400.0)
    # Margin proxy: MRR vs the 8K SAR plan floor at day 90.
    margin_signal = _clamp(mrr_sar / 80.0)
    proof_signal = _clamp(proof_score)
    # Repeatability: 3 retainers is the day-90 target.
    repeatability_signal = _clamp((retainer_count / 3.0) * 100.0)
    # Governance safety is the inverse of the risk index.
    governance_safety = _clamp(100.0 - governance_risk)
    productization_signal = _clamp((capital_asset_count / 8.0) * 100.0)
    # Strategic moat: adoption breadth proxies durable lock-in.
    moat_signal = _clamp(adoption_value)

    signal_inputs: dict[str, float] = {
        "revenue": round(revenue_signal, 1),
        "margin": round(margin_signal, 1),
        "proof": round(proof_signal, 1),
        "repeatability": round(repeatability_signal, 1),
        "governance": round(governance_safety, 1),
        "productization": round(productization_signal, 1),
        "moat": round(moat_signal, 1),
    }

    return StrategicSignalSnapshot(
        customer_id=customer_id,
        on_date=on_date_str,
        days_since_launch=days_since_launch,
        total_revenue_sar=total_revenue_sar,
        mrr_sar=mrr_sar,
        paid_customers=paid_customers,
        retainer_count=retainer_count,
        proof_event_count=proof_event_count,
        proof_score=round(proof_score, 1),
        adoption_score=round(adoption_value, 1),
        governance_risk_index=round(governance_risk, 1),
        capital_asset_count=capital_asset_count,
        founder_hours_per_sprint=round(float(founder_hours_per_sprint), 1),
        signal_inputs=signal_inputs,
        warnings=warnings,
    )


__all__ = [
    "LAUNCH_DATE",
    "StrategicSignalSnapshot",
    "aggregate_strategic_signals",
]
