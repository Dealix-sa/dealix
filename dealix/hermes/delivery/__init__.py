"""
Delivery playbooks.

Each productized offer ships with a structured DeliveryPlaybook describing
inputs, steps, outputs, and quality gates. The quality-checklist module
verifies the playbook before delivery is marked complete.
"""

from __future__ import annotations

from dealix.hermes.delivery.agency_white_label_delivery import (
    AGENCY_WHITE_LABEL_PLAYBOOK,
)
from dealix.hermes.delivery.ai_trust_kit_delivery import AI_TRUST_KIT_PLAYBOOK
from dealix.hermes.delivery.delivery_playbook import DeliveryPlaybook
from dealix.hermes.delivery.market_radar_delivery import MARKET_RADAR_PLAYBOOK
from dealix.hermes.delivery.quality_checklists import (
    QualityCheckResult,
    run_quality_checklist,
)
from dealix.hermes.delivery.revenue_hunter_delivery import (
    REVENUE_HUNTER_PLAYBOOK,
)
from dealix.hermes.delivery.value_report_delivery import VALUE_REPORT_PLAYBOOK

ALL_PLAYBOOKS: dict[str, DeliveryPlaybook] = {
    p.offer_id: p
    for p in (
        REVENUE_HUNTER_PLAYBOOK,
        AI_TRUST_KIT_PLAYBOOK,
        AGENCY_WHITE_LABEL_PLAYBOOK,
        MARKET_RADAR_PLAYBOOK,
        VALUE_REPORT_PLAYBOOK,
    )
}

__all__ = [
    "DeliveryPlaybook",
    "REVENUE_HUNTER_PLAYBOOK",
    "AI_TRUST_KIT_PLAYBOOK",
    "AGENCY_WHITE_LABEL_PLAYBOOK",
    "MARKET_RADAR_PLAYBOOK",
    "VALUE_REPORT_PLAYBOOK",
    "ALL_PLAYBOOKS",
    "QualityCheckResult",
    "run_quality_checklist",
]
