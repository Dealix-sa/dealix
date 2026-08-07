"""Operating System health API.

Aggregates status from all Dealix OS modules.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from intelligence.communication_hub import CommunicationHub
from intelligence.customer_success_ops import CustomerSuccessOperatingSystem
from intelligence.deep_research import DeepResearchEngine
from intelligence.growth_ops import GrowthOperatingSystem
from intelligence.knowledge_accumulator import KnowledgeAccumulator
from intelligence.negotiation_engine import NegotiationEngine
from intelligence.ops_adapters import list_packages
from intelligence.sales_ops import SalesOperatingSystem
from intelligence.send_gate import SendGate

router = APIRouter(prefix="/api/v1/ops/health", tags=["Operating System Health"])


@router.get("/status")
async def os_health_status() -> dict[str, Any]:
    checks = {
        "send_gate_blocked": SendGate.OUTBOUND_SEND_DISABLED,
        "price_catalog": list_packages(),
        "negotiation_engine": _module_ok(NegotiationEngine),
        "deep_research_engine": _module_ok(DeepResearchEngine),
        "knowledge_accumulator": _module_ok(KnowledgeAccumulator),
        "communication_hub": _module_ok(CommunicationHub),
        "sales_os": _module_ok(SalesOperatingSystem),
        "growth_os": _module_ok(GrowthOperatingSystem),
        "customer_success_os": _module_ok(CustomerSuccessOperatingSystem),
    }
    all_ok = all(isinstance(v, list) or v is True for v in checks.values())
    return {
        "status": "healthy" if all_ok else "degraded",
        "checks": checks,
        "note": "Send gate is hard-coded to blocked. External dispatch requires manual human action.",
    }


def _module_ok(cls: type) -> bool:
    try:
        cls()
        return True
    except Exception:
        return False
