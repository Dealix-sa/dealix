"""Fail-closed adapter from the existing proof ledger into canonical proof truth."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from dealix.company_intelligence.outcome_contracts import (
    CanonicalProofEvent,
    ProofSourceEventType,
    ProofType,
    build_proof_event,
)

_RECOGNITION_EVENT_TYPES: dict[ProofType, frozenset