"""
delivery — playbook per product. Every product is shippable without
Sami in the room because the playbook is explicit: inputs, steps,
templates, quality gates, approval gates, outputs, outcome metrics,
upsell.
"""

from dealix.hermes.delivery.ai_trust_kit_delivery import AI_TRUST_KIT_PLAYBOOK
from dealix.hermes.delivery.executive_pmo_delivery import EXECUTIVE_PMO_PLAYBOOK
from dealix.hermes.delivery.founder_os_delivery import FOUNDER_OS_PLAYBOOK
from dealix.hermes.delivery.market_report_delivery import MARKET_REPORT_PLAYBOOK
from dealix.hermes.delivery.mcp_risk_delivery import MCP_RISK_PLAYBOOK
from dealix.hermes.delivery.revenue_hunter_delivery import REVENUE_HUNTER_PLAYBOOK
from dealix.hermes.delivery.training_delivery import TRAINING_PLAYBOOK
from dealix.hermes.delivery.white_label_delivery import WHITE_LABEL_PLAYBOOK

PLAYBOOK_REGISTRY = {
    "ai_trust_kit_delivery": AI_TRUST_KIT_PLAYBOOK,
    "executive_pmo_delivery": EXECUTIVE_PMO_PLAYBOOK,
    "founder_os_delivery": FOUNDER_OS_PLAYBOOK,
    "market_report_delivery": MARKET_REPORT_PLAYBOOK,
    "mcp_risk_delivery": MCP_RISK_PLAYBOOK,
    "revenue_hunter_delivery": REVENUE_HUNTER_PLAYBOOK,
    "training_delivery": TRAINING_PLAYBOOK,
    "white_label_delivery": WHITE_LABEL_PLAYBOOK,
}

__all__ = ["PLAYBOOK_REGISTRY"]
