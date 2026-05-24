"""خادم Hermes — base schemas.

Foundational pydantic models and enums shared across the Hermes Universal
Kernel. Everything below this module is stdlib + pydantic only; no other
dealix package may be imported here so that we keep the dependency graph
acyclic.

The shapes here intentionally mirror the spec (§29 workspace scopes, §40
evidence pack money fields, etc.). They are deliberately small so that
higher-level modules can compose them without having to redefine money
or entity references.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────


class RiskLevel(StrEnum):
    """Coarse risk level used by sovereignty + guardrails."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def numeric(self) -> int:
        return {"low": 0, "medium": 1, "high": 2, "critical": 3}[self.value]

    def at_least(self, other: RiskLevel) -> bool:
        return self.numeric >= other.numeric


class WorkspaceScope(StrEnum):
    """Spec §29 — the seven canonical workspaces."""

    SOVEREIGN = "sovereign"
    INTERNAL = "internal"
    CUSTOMER = "customer"
    PARTNER = "partner"
    TRUST = "trust"
    VENTURE = "venture"
    MARKETPLACE = "marketplace"


# ─────────────────────────────────────────────────────────────
# Money — Decimal-backed, currency-aware
# ─────────────────────────────────────────────────────────────


_CURRENCY_RE = re.compile(r"^[A-Z]{3}$")


class Money(BaseModel):
    """A monetary amount. Default currency is Saudi Riyal."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    amount: Decimal = Field(..., description="Decimal amount; non-negative.")
    currency: str = Field(default="SAR", description="ISO-4217 currency code.")

    @field_validator("amount", mode="before")
    @classmethod
    def _coerce_amount(cls, value: Any) -> Decimal:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, int | float | str):
            try:
                return Decimal(str(value))
            except InvalidOperation as exc:  # pragma: no cover - defensive
                raise ValueError(f"invalid decimal amount: {value!r}") from exc
        raise ValueError(f"unsupported money amount type: {type(value)!r}")

    @field_validator("amount")
    @classmethod
    def _non_negative(cls, value: Decimal) -> Decimal:
        if value < Decimal("0"):
            raise ValueError("Money.amount must be >= 0")
        return value

    @field_validator("currency")
    @classmethod
    def _validate_currency(cls, value: str) -> str:
        value = value.upper().strip()
        if not _CURRENCY_RE.match(value):
            raise ValueError(f"invalid currency code: {value!r} (expected ISO-4217)")
        return value

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"

    def is_above(self, threshold: int | float | Decimal) -> bool:
        return self.amount > Decimal(str(threshold))

    @classmethod
    def sar(cls, amount: int | float | str | Decimal) -> Money:
        return cls(amount=Decimal(str(amount)), currency="SAR")


# ─────────────────────────────────────────────────────────────
# Tagging & entity references
# ─────────────────────────────────────────────────────────────


class Tag(BaseModel):
    """A free-form classification tag (kind/value pair)."""

    model_config = ConfigDict(extra="forbid")

    kind: str = Field(..., min_length=1, max_length=64)
    value: str = Field(..., min_length=1, max_length=128)

    @field_validator("kind", "value")
    @classmethod
    def _strip(cls, v: str) -> str:
        return v.strip()


class EntityRef(BaseModel):
    """A pointer to any business entity by (type, id)."""

    model_config = ConfigDict(extra="forbid")

    entity_type: str = Field(..., min_length=1, max_length=64)
    entity_id: str = Field(..., min_length=1, max_length=128)

    def as_str(self) -> str:
        return f"{self.entity_type}:{self.entity_id}"


# ─────────────────────────────────────────────────────────────
# Timestamps mixin
# ─────────────────────────────────────────────────────────────


def utcnow() -> datetime:
    """Centralised UTC clock — easier to monkeypatch in tests."""
    return datetime.now(UTC)


class Timestamps(BaseModel):
    """Created/updated timestamps. Inherit or embed."""

    model_config = ConfigDict(extra="forbid")

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    def touch(self) -> Timestamps:
        return self.model_copy(update={"updated_at": utcnow()})


# Convenient type aliases for downstream modules.
Score1to5 = Annotated[int, Field(ge=1, le=5)]
Confidence = Annotated[float, Field(ge=0.0, le=1.0)]


__all__ = [
    "Confidence",
    "EntityRef",
    "Money",
    "RiskLevel",
    "Score1to5",
    "Tag",
    "Timestamps",
    "WorkspaceScope",
    "utcnow",
]
