"""
dealix.os_runtime — Executable OS Runtime for Dealix Company OS

Provides:
  - Config loader for os/*.yml and os/growth/*.yml
  - Pydantic models for all OS entities
  - Validator for cross-consistency checks
  - CLI entry point via `python -m dealix.os_runtime`
"""

from dealix.os_runtime.config_loader import OSConfigLoader
from dealix.os_runtime.schemas import (
    AntibanRule,
    ApprovalGate,
    Channel,
    DraftQueueItem,
    Market,
    OfferTier,
    PersuasionDossier,
    ScoringConfig,
)
from dealix.os_runtime.validator import OSValidator, ValidationResult

__all__ = [
    "OSConfigLoader",
    "OSValidator",
    "ValidationResult",
    "OfferTier",
    "Market",
    "ScoringConfig",
    "ApprovalGate",
    "Channel",
    "AntibanRule",
    "PersuasionDossier",
    "DraftQueueItem",
]
