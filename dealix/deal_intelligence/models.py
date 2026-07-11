"""Typed, evidence-aware deal intelligence models.

This package contains no sender, scheduler, payment capture, or production code.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from dealix.client_acquisition.models import CONTACTABLE_SOURCES


class DealStage(StrEnum):
    RESEARCH_HOLD = "research_hold"
    NEW = "new"
    CONTACTED = "contacted"
    ENGAGED = "engaged"
    PROPOSED = "proposed"
    PAID = "paid"
    PROOF_DELIVERED = "proof_delivered"
    REFERRAL = "referral"
    LOST = "lost"


ALLOWED_EVENT_TYPES = frozenset(
    {
        "message_sent_manual",
        "message_sent",
       