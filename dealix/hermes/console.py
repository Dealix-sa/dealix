"""Sovereign Console — the single morning view for Sami.

The console is the read model. It composes the kernel + engines without
mutating anything. The fields below are the only ones the public Sovereign
Console API surfaces — anything new must be added here deliberately.
"""

from __future__ import annotations

from typing import Any

from dealix.hermes import DOCTRINE_RULES_AR
from dealix.hermes.money.dashboard import render as render_money_dashboard
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.products.scale_kill import evaluate_library


def render_console(
    orchestrator: HermesOrchestrator,
    *,
    opportunity_to_offer: dict[str, str] | None = None,
    delivery_capacity: float = 0.8,
    open_proposals: int = 0,
) -> dict[str, Any]:
    """Compose the sovereign console snapshot."""
    money = render_money_dashboard(
        scout=orchestrator.cash_scout,
        outcomes=orchestrator.outcomes,
        open_proposals=open_proposals,
        top_n=5,
    )

    fastest_cash = money.fastest_cash
    top_opp = orchestrator.opportunities.top(1)

    pending = [
        {
            "request_id": r.request_id,
            "action_type": r.action.action_type,
            "level": r.decision.enforced_level.value,
            "reason": r.decision.reason,
        }
        for r in orchestrator.approvals.pending()
    ]

    scale_decisions = evaluate_library(
        library=orchestrator.offers,
        outcomes=orchestrator.outcomes,
        opportunity_to_offer=opportunity_to_offer or {},
        engine=orchestrator.scale,
    )

    scale_items = [d for d in scale_decisions if d.verdict.value == "scale"]
    kill_items = [d for d in scale_decisions if d.verdict.value == "kill"]

    return {
        "command": {
            "fastest_cash_action": (
                {
                    "title": fastest_cash[0].title,
                    "opportunity_id": fastest_cash[0].opportunity_id,
                    "value_estimate_sar": round(fastest_cash[0].expected_value_sar, 2),
                    "next_action": fastest_cash[0].next_action,
                    "approval_required": False,
                }
                if fastest_cash
                else None
            ),
            "top_strategic_opportunity": (
                {
                    "title": top_opp[0].title,
                    "opportunity_id": top_opp[0].opportunity_id,
                    "expected_value_sar": round(top_opp[0].expected_value_sar, 2),
                    "kind": top_opp[0].kind.value,
                }
                if top_opp
                else None
            ),
            "sovereign_approval_required": pending,
            "scale": [
                {"target": d.target, "reason": d.reason, "metrics": d.metrics_snapshot}
                for d in scale_items
            ],
            "kill": [
                {"target": d.target, "reason": d.reason, "metrics": d.metrics_snapshot}
                for d in kill_items
            ],
        },
        "money": {
            "pipeline_value_sar": money.pipeline_value_sar,
            "cash_collected_sar": money.cash_collected_sar,
            "pipeline_to_paid_ratio": money.pipeline_to_paid_ratio,
            "open_proposals": money.open_proposals,
            "fastest_cash": [
                {
                    "opportunity_id": a.opportunity_id,
                    "title": a.title,
                    "kind": a.kind.value,
                    "expected_value_sar": round(a.expected_value_sar, 2),
                    "priority": round(a.priority, 2),
                    "days_to_close": round(a.days_to_close, 1),
                    "next_action": a.next_action,
                }
                for a in money.fastest_cash
            ],
        },
        "trust": {
            "agents_registered": len(orchestrator.agents.all()),
            "tools_registered": len(orchestrator.tools.all()),
            "audit_chain_valid": orchestrator.audit.verify_chain(),
            "approvals_pending": len(pending),
        },
        "doctrine_rules_ar": list(DOCTRINE_RULES_AR),
    }


__all__ = ["render_console"]
