"""Dealix Market Production OS — the go-to-market production layer.

Stdlib-only by design so the gates and factory run anywhere (no pydantic /
app-stack dependency). Honors the 11 non-negotiables; the compliance gate
mirrors the canonical patterns in
``auto_client_acquisition/governance_os/draft_gate.py`` and integrates the
governance ``policy_check_draft`` when the heavy stack is importable.

Doc of record: ``docs/market_production_os/README.md``.
"""

from __future__ import annotations

from dealix.market_production_os.compliance_gate import ComplianceResult, check_draft
from dealix.market_production_os.deliverability import (
    DeliverabilityResult,
    evaluate_account,
    ready_to_send,
)
from dealix.market_production_os.draft_factory import build_draft, produce_daily
from dealix.market_production_os.models import OFFERS, SECTORS, email_sha256, new_id
from dealix.market_production_os.personalization import (
    level_rank,
    personalization_floor_ok,
)
from dealix.market_production_os.prospect_scoring import qualify, score_prospect
from dealix.market_production_os.reply_classifier import classify
from dealix.market_production_os.sending_ramp import RAMP_PHASES, allowed_sends

__all__ = [
    "OFFERS",
    "SECTORS",
    "RAMP_PHASES",
    "ComplianceResult",
    "DeliverabilityResult",
    "check_draft",
    "evaluate_account",
    "ready_to_send",
    "build_draft",
    "produce_daily",
    "email_sha256",
    "new_id",
    "level_rank",
    "personalization_floor_ok",
    "qualify",
    "score_prospect",
    "classify",
    "allowed_sends",
]
