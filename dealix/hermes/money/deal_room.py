"""Deal Room — single view of a deal across signal, opportunity, outcome."""

from __future__ import annotations

from typing import Any

from dealix.hermes.core.decisions import get_decision_store
from dealix.hermes.core.executions import get_execution_store
from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.signals import get_signal_store


class DealRoom:
    def view(self, opportunity_id: str) -> dict[str, Any]:
        opp = get_opportunity_store().get(opportunity_id)
        if opp is None:
            return {"error": "opportunity_not_found"}
        signal = get_signal_store().get(opp.signal_id)
        decisions = [d for d in get_decision_store().list() if d.opportunity_id == opp.id]
        executions = [
            e for e in get_execution_store().list() if any(d.id == e.decision_id for d in decisions)
        ]
        outcomes = [
            o for o in get_outcome_store().list() if any(e.id == o.execution_id for e in executions)
        ]
        return {
            "opportunity": opp.model_dump(mode="json"),
            "signal": signal.model_dump(mode="json") if signal else None,
            "decisions": [d.model_dump(mode="json") for d in decisions],
            "executions": [e.model_dump(mode="json") for e in executions],
            "outcomes": [o.model_dump(mode="json") for o in outcomes],
        }
