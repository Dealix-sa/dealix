"""Wave 17 — Exit Readiness OS HTTP surface.

Endpoints:
  POST /api/v1/exit-readiness/venture-gate          — check all 9 venture gate conditions
  GET  /api/v1/exit-readiness/operating-chain       — return the canonical operating chain
  POST /api/v1/exit-readiness/chain-progress        — evaluate completion % through chain
  GET  /api/v1/exit-readiness/governance-score      — governance runtime maturity (0-100)
  POST /api/v1/exit-readiness/market-power-score    — market power activation score (0-100)
  GET  /api/v1/exit-readiness/exit-readiness-summary — structured exit pathway summary

Hard rules:
- is_estimate_always_true: scored outputs carry is_estimate per field semantics
- no_fake_revenue: gate evaluation reflects only what has been explicitly confirmed
- approval_required_for_external_actions: gate data must not be shared externally without approval
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.endgame_os.venture_factory import (
    VentureGateChecklist,
    venture_gate_passes,
)
from auto_client_acquisition.endgame_os.operating_chain import (
    CORE_OPERATING_CHAIN,
    chain_complete_through,
)
from auto_client_acquisition.endgame_os.governance_product import (
    GOVERNANCE_RUNTIME_COMPONENTS,
    governance_runtime_maturity_score,
)
from auto_client_acquisition.endgame_os.market_power import (
    MARKET_POWER_SIGNALS,
    market_power_activation_score,
)

router = APIRouter(
    prefix="/api/v1/exit-readiness",
    tags=["Wave 17 — Exit Readiness OS"],
)

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
    "approval_required_for_external_actions": True,
}


# ── Pydantic models ────────────────────────────────────────────────────────────


class VentureGateRequest(BaseModel):
    paid_clients_5plus: bool = False
    retainers_2plus: bool = False
    repeatable_delivery: bool = False
    product_module_clear: bool = False
    playbook_maturity_80plus: bool = False
    owner_exists: bool = False
    healthy_margin: bool = False
    proof_library_exists: bool = False
    core_os_dependency_clear: bool = False


class ChainProgressRequest(BaseModel):
    completed_steps: list[str] = []


class MarketPowerRequest(BaseModel):
    active_signals: list[str] = Field(
        default=[],
        description="Which MARKET_POWER_SIGNALS are currently active",
    )


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.post("/venture-gate")
async def venture_gate(body: VentureGateRequest) -> dict[str, Any]:
    """Evaluate the 9-condition venture spinout gate.

    is_estimate=False: the gate is a boolean checklist, not a probabilistic
    score.  All 9 conditions must be True for the gate to pass.
    """
    checklist = VentureGateChecklist(**body.model_dump())
    passes = venture_gate_passes(checklist)
    checklist_dict = body.model_dump()
    failed = [k for k, v in checklist_dict.items() if not v]
    return {
        "gate_passes": passes,
        "checklist": checklist_dict,
        "failed_gates": failed,
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }


@router.get("/operating-chain")
async def operating_chain() -> dict[str, Any]:
    """Return the canonical Dealix operating chain (ordered list of steps).

    is_estimate=False: this is a static doctrine constant.
    """
    chain_list = list(CORE_OPERATING_CHAIN)
    return {
        "chain": chain_list,
        "length": len(chain_list),
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }


@router.post("/chain-progress")
async def chain_progress(body: ChainProgressRequest) -> dict[str, Any]:
    """Evaluate completion progress through the operating chain.

    Reports per-step completion status and overall percentage.
    is_estimate=False: completion is based on the explicit completed_steps list.
    """
    chain_list = list(CORE_OPERATING_CHAIN)
    completed_set = frozenset(body.completed_steps)
    total = len(chain_list)
    completed_count = sum(1 for s in chain_list if s in completed_set)
    completion_pct = round(completed_count / total * 100, 1) if total else 0.0

    chain_status = [
        {
            "step": step,
            "completed": step in completed_set,
            "complete_through": chain_complete_through(completed_set, step),
        }
        for step in chain_list
    ]

    return {
        "total_steps": total,
        "completed": completed_count,
        "completion_pct": completion_pct,
        "chain_status": chain_status,
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }


@router.get("/governance-score")
async def governance_score(
    components: list[str] = Query(
        default=[],
        description="Components to evaluate; leave empty to use all GOVERNANCE_RUNTIME_COMPONENTS",
    ),
) -> dict[str, Any]:
    """Compute governance runtime maturity score (0-100).

    If no components are supplied, all known GOVERNANCE_RUNTIME_COMPONENTS
    are used as the evaluation set.  is_estimate=False: the score is an
    exact count-based ratio.
    """
    components_to_check: list[str] = components if components else list(GOVERNANCE_RUNTIME_COMPONENTS)
    score = governance_runtime_maturity_score(frozenset(components_to_check))
    return {
        "score": score,
        "components_evaluated": components_to_check,
        "max_score": 100,
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }


@router.post("/market-power-score")
async def market_power_score(body: MarketPowerRequest) -> dict[str, Any]:
    """Score market power activation based on which signals are active.

    Returns a 0-100 score proportional to the fraction of
    MARKET_POWER_SIGNALS present in active_signals.
    is_estimate=False: the score is a deterministic ratio.
    """
    score = market_power_activation_score(frozenset(body.active_signals))
    return {
        "score": score,
        "active_signals": body.active_signals,
        "all_signals": list(MARKET_POWER_SIGNALS),
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }


@router.get("/exit-readiness-summary")
async def exit_readiness_summary() -> dict[str, Any]:
    """Structured overview of exit readiness dimensions and pathways.

    Provides the map of endpoints to call for a full exit readiness assessment.
    is_estimate=False: this is a static reference document.
    """
    return {
        "module": "exit_readiness_os",
        "version": "17.0",
        "exit_pathways": [
            "Series A",
            "Strategic Acquisition",
            "GCC Expansion → IPO",
        ],
        "readiness_dimensions": [
            {
                "dimension": "Operating Chain",
                "endpoint": "/api/v1/exit-readiness/chain-progress",
            },
            {
                "dimension": "Venture Gate",
                "endpoint": "/api/v1/exit-readiness/venture-gate",
            },
            {
                "dimension": "Governance Score",
                "endpoint": "/api/v1/exit-readiness/governance-score",
            },
            {
                "dimension": "Market Power",
                "endpoint": "/api/v1/exit-readiness/market-power-score",
            },
        ],
        "is_estimate": False,
        "hard_gates": _HARD_GATES,
    }
