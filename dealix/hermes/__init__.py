"""
Hermes — Dealix Sovereign Operating Doctrine.

This package is the **kernel doctrine** for Dealix: it turns any input
(signal, lead, message, market event, agent action) into one or more of the
seven canonical value outputs, under sovereign control by Sami.

The doctrine (non-negotiable):

    Anything that enters Dealix MUST exit as one or more of:
        1. Money       — direct cash or pipeline
        2. Data        — fact / result that increases system intelligence
        3. Asset       — template / playbook / report / case study
        4. Partner     — distribution or delivery channel
        5. Trust       — reduced risk or higher sellability
        6. Access      — reach to a customer / sector / network
        7. Learning    — a lesson that improves the next decision

Anything that produces none of the above is **waste** and must be killed.

The pipeline:

    Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset → Scale

Every layer is enforced by an immutable contract (`hermes.core.schemas`) and
mediated by the sovereignty gate (`hermes.sovereignty`). No agent, tool, or
external action bypasses the gate.

Public boundary
---------------
Only the orchestrator + console + selected API routers form the public
surface. Internal modules (intake, scoring, executors) are not stable
contracts.

Doctrine references (in this repository):
- `dealix/commercial_ops/doctrine.py` — commercial non-negotiables
- `dealix/governance/approvals.py` — runtime approval gate (Redis-backed)
- `dealix/trust/` — approval, audit
- `dealix/classifications/` — A/R/S classes (carry these on every action)
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final


class ValueOutput(StrEnum):
    """The seven canonical outputs Hermes recognises. Any flow must map to
    at least one of these or be classified as `WASTE` and killed.
    """

    MONEY = "money"
    DATA = "data"
    ASSET = "asset"
    PARTNER = "partner"
    TRUST = "trust"
    ACCESS = "access"
    LEARNING = "learning"
    WASTE = "waste"


VALUE_OUTPUTS: Final[frozenset[ValueOutput]] = frozenset(
    v for v in ValueOutput if v is not ValueOutput.WASTE
)


DOCTRINE_RULES_AR: Final[tuple[str, ...]] = (
    "كل ما يدخل Dealix يجب أن يخرج بأحد المخرجات السبعة أو يُصنّف هدراً.",
    "لا Agent يعمل خارج Agent Registry وTool Permissions وSovereignty Gate.",
    "لا execution خارجي بدون Trust Check.",
    "لا قرار حساس بدون مذكّرة (Decision Memo) وموافقة سامي عند المستوى المطلوب.",
    "لا outcome بدون asset review.",
    "لا public API ولا Marketplace ولا White-label بدون موافقة سيادية صريحة (S4).",
    "لا أرقام إيراد قبل invoice_paid، ولا upsell قبل Proof.",
)


__all__ = [
    "ValueOutput",
    "VALUE_OUTPUTS",
    "DOCTRINE_RULES_AR",
]
