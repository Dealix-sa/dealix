"""
Public API readiness — §105.

A static 10-item checklist + the 7 future API products. The readiness
gate refuses to "go public" until everything is checked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


PUBLIC_API_PRODUCTS: tuple[str, ...] = (
    "value_engine_api",
    "trust_check_api",
    "money_command_api",
    "agent_orchestration_api",
    "asset_library_api",
    "intelligence_graph_api",
    "compliance_audit_api",
)


@dataclass
class PublicAPIReadiness:
    metering: bool = False
    quotas: bool = False
    api_keys_scoped: bool = False
    observability: bool = False
    sla_documented: bool = False
    pricing_published: bool = False
    legal_terms: bool = False
    incident_runbook: bool = False
    audit_trail: bool = False
    customer_value_reports: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}

    def assess(self) -> tuple[bool, list[str]]:
        missing = [k for k, v in self.to_dict().items() if v is False]
        return (len(missing) == 0), missing
