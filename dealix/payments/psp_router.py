"""
PSP Router — selects payment processor per region, amount, and customer preference.

Wired Day 1 of the Build-Out Plan to ensure revenue is uncoupled from any
single PSP's KYC timeline. Three processors run in parallel: Moyasar
(primary KSA), Hyperpay (parallel KSA fallback), Tap (added by Day 60).

Routing rules (in order):
  1. Explicit customer override (per-tenant config)
  2. Currency restriction (some PSPs only support SAR)
  3. Amount tier (high-value charges → Hyperpay's enterprise tier)
  4. Health check (skip a PSP if its last health check was failing)
  5. Default chain: Moyasar → Hyperpay → Tap

Every routing decision is logged for audit + cost reconciliation.
"""

from __future__ import annotations

import enum
import logging
import os
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

log = logging.getLogger(__name__)


class PSP(str, enum.Enum):
    """Supported Payment Service Providers."""

    MOYASAR = "moyasar"
    HYPERPAY = "hyperpay"
    TAP = "tap"


@dataclass
class PSPHealth:
    """Snapshot of a PSP's operational health."""

    psp: PSP
    is_healthy: bool = True
    consecutive_failures: int = 0
    last_success_at: str | None = None
    last_failure_at: str | None = None
    last_failure_reason: str | None = None


@dataclass
class RoutingDecision:
    """The decision produced by the router, suitable for audit logging."""

    primary: PSP
    fallback_chain: list[PSP] = field(default_factory=list)
    reason: str = ""
    rule_applied: str = ""
    customer_preference: str | None = None


@dataclass
class CheckoutRequest:
    """Normalized checkout request input shared across PSPs."""

    amount_sar: Decimal
    currency: str = "SAR"
    customer_email: str | None = None
    customer_tenant_id: str | None = None
    description: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
    customer_preference: PSP | None = None
    region: str = "SA"  # ISO 3166-1 alpha-2


class PSPRouter:
    """
    Stateless router that selects a PSP and returns an ordered fallback chain.

    Health state is read from environment / config; live health probes
    happen out-of-band and update a Redis/Postgres health table that this
    router consults via the `health_lookup` callable.
    """

    # Default ordering (overridable via DEALIX_PSP_PRIMARY env)
    DEFAULT_CHAIN: list[PSP] = [PSP.MOYASAR, PSP.HYPERPAY, PSP.TAP]

    # Amount threshold above which we prefer Hyperpay (enterprise-grade)
    HIGH_VALUE_SAR_THRESHOLD: Decimal = Decimal("25000")

    def __init__(
        self,
        health_lookup: dict[PSP, PSPHealth] | None = None,
        primary_override: PSP | None = None,
    ) -> None:
        self.health_lookup = health_lookup or {}
        env_primary = os.getenv("DEALIX_PSP_PRIMARY", "").lower()
        if primary_override:
            self.primary = primary_override
        elif env_primary in {p.value for p in PSP}:
            self.primary = PSP(env_primary)
        else:
            self.primary = PSP.MOYASAR

    def select(self, request: CheckoutRequest) -> RoutingDecision:
        """
        Apply routing rules in order and return the decision.

        The decision is deterministic given the same inputs + health state.
        """
        # Rule 1 — Customer preference (highest priority)
        if request.customer_preference is not None:
            chain = self._chain_starting_with(request.customer_preference)
            return RoutingDecision(
                primary=request.customer_preference,
                fallback_chain=chain[1:],
                reason="customer preference honored",
                rule_applied="rule_1_customer_preference",
                customer_preference=request.customer_preference.value,
            )

        # Rule 2 — Currency restriction
        # All current PSPs support SAR. Non-SAR not yet supported.
        if request.currency != "SAR":
            return RoutingDecision(
                primary=PSP.HYPERPAY,
                fallback_chain=[],
                reason=f"non-SAR currency {request.currency} requires multi-currency PSP",
                rule_applied="rule_2_currency",
            )

        # Rule 3 — Amount tier
        if request.amount_sar >= self.HIGH_VALUE_SAR_THRESHOLD:
            chain = self._chain_starting_with(PSP.HYPERPAY)
            return RoutingDecision(
                primary=PSP.HYPERPAY,
                fallback_chain=chain[1:],
                reason=f"amount {request.amount_sar} >= high-value threshold",
                rule_applied="rule_3_amount_tier",
            )

        # Rule 4 — Health check on primary
        primary_health = self.health_lookup.get(self.primary)
        if primary_health and not primary_health.is_healthy:
            healthy_chain = [
                p
                for p in self.DEFAULT_CHAIN
                if self.health_lookup.get(p, PSPHealth(p)).is_healthy
            ]
            if healthy_chain:
                return RoutingDecision(
                    primary=healthy_chain[0],
                    fallback_chain=healthy_chain[1:],
                    reason=f"{self.primary.value} unhealthy ({primary_health.last_failure_reason})",
                    rule_applied="rule_4_health_check",
                )
            return RoutingDecision(
                primary=self.primary,
                fallback_chain=[],
                reason="all PSPs unhealthy — using primary anyway",
                rule_applied="rule_4_health_check_no_healthy",
            )

        # Default — primary + chain
        chain = self._chain_starting_with(self.primary)
        return RoutingDecision(
            primary=self.primary,
            fallback_chain=chain[1:],
            reason="default chain",
            rule_applied="default",
        )

    def _chain_starting_with(self, first: PSP) -> list[PSP]:
        rest = [p for p in self.DEFAULT_CHAIN if p != first]
        return [first, *rest]


__all__ = ["PSP", "PSPHealth", "RoutingDecision", "CheckoutRequest", "PSPRouter"]
