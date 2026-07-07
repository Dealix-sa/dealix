"""
Safety Gate — the hard boundary for the Autonomous OS.

Every planned step passes through the gate before it is queued. The gate
answers one question: *may this run automatically, or must a human decide?*

Two layers of protection:

1. Forbidden actions — permanently blocked regardless of environment. These
   map to the Dealix safety doctrine (no cold outreach, no scraping, no
   LinkedIn automation, no mass/auto send). They are never queued anywhere;
   they are refused.

2. External send flags — read from the environment. Even when a channel is
   technically enabled (controlled-live approval), the Autonomous OS still
   routes external actions to the approval queue. The gate never authorises
   an *automatic* external send.

The gate is intentionally conservative: unknown risk defaults to approval.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum

# Steps at or above this risk always require human approval.
AUTO_EXECUTE_RISK_CEILING = 0.4

# Actions that are never permitted — they contradict the safety doctrine.
FORBIDDEN_ACTIONS = frozenset(
    {
        "cold_outreach",
        "auto_send",
        "mass_send",
        "bulk_broadcast",
        "linkedin_automation",
        "linkedin_scrape",
        "scrape_contacts",
        "buy_leads",
        "auto_invoice",
        "auto_charge",
    }
)

# Channels considered external. Drafts for these always go to approval.
EXTERNAL_CHANNELS = frozenset({"whatsapp", "email", "sms", "linkedin", "phone"})


class Route(StrEnum):
    """Where a step should go after the gate."""

    AUTO_DRAFT = "auto_draft"  # internal draft artifact, safe to generate now
    APPROVAL = "approval"  # external / high-risk — founder must decide
    BLOCKED = "blocked"  # forbidden by doctrine — never queued


@dataclass(frozen=True)
class SafetyDecision:
    route: Route
    reason: str

    @property
    def allowed_auto(self) -> bool:
        return self.route == Route.AUTO_DRAFT

    @property
    def blocked(self) -> bool:
        return self.route == Route.BLOCKED


def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


class SafetyGate:
    """Draft-only, approval-first enforcement."""

    def __init__(self, env: dict[str, str] | None = None) -> None:
        # Allow injecting an env for tests; default to real process env.
        self._env = env

    def _flag(self, name: str) -> bool:
        if self._env is not None:
            return self._env.get(name, "").strip().lower() in {"1", "true", "yes", "on"}
        return _truthy(name)

    @property
    def outbound_mode(self) -> str:
        if self._env is not None:
            return self._env.get("OUTBOUND_MODE", "draft_only").strip() or "draft_only"
        return os.getenv("OUTBOUND_MODE", "draft_only").strip() or "draft_only"

    @property
    def external_send_enabled(self) -> bool:
        return self._flag("EXTERNAL_SEND_ENABLED")

    def is_forbidden(self, action: str) -> bool:
        return action.strip().lower() in FORBIDDEN_ACTIONS

    def evaluate(
        self,
        *,
        action: str,
        kind: str = "internal",
        channel: str | None = None,
        risk: float = 0.0,
        requires_approval: bool = False,
    ) -> SafetyDecision:
        """Classify a single step into a route. Never raises on policy — it
        returns BLOCKED so callers can record and continue."""
        act = action.strip().lower()

        if self.is_forbidden(act):
            return SafetyDecision(Route.BLOCKED, f"action '{act}' is forbidden by safety doctrine")

        chan = (channel or "").strip().lower()
        if chan in EXTERNAL_CHANNELS:
            # External drafts are always human-gated, even in controlled-live.
            return SafetyDecision(
                Route.APPROVAL,
                f"external channel '{chan}' requires founder approval (draft prepared only)",
            )

        if kind.strip().lower() in {"external_draft", "external"}:
            return SafetyDecision(Route.APPROVAL, "external-draft step requires founder approval")

        if requires_approval:
            return SafetyDecision(Route.APPROVAL, "step explicitly marked requires_approval")

        if risk >= AUTO_EXECUTE_RISK_CEILING:
            return SafetyDecision(
                Route.APPROVAL, f"risk {risk:.2f} >= ceiling {AUTO_EXECUTE_RISK_CEILING}"
            )

        return SafetyDecision(Route.AUTO_DRAFT, "internal low-risk step — safe to draft")

    def assert_draft_only(self) -> None:
        """Raise if the environment somehow authorises automatic external send.
        Called at OS startup as a defensive tripwire."""
        if self.external_send_enabled and self.outbound_mode != "controlled_live":
            raise RuntimeError(
                "SAFETY: EXTERNAL_SEND_ENABLED=true without OUTBOUND_MODE=controlled_live"
            )

    def summary(self) -> dict[str, object]:
        return {
            "outbound_mode": self.outbound_mode,
            "external_send_enabled": self.external_send_enabled,
            "forbidden_actions": sorted(FORBIDDEN_ACTIONS),
            "external_channels": sorted(EXTERNAL_CHANNELS),
            "auto_execute_risk_ceiling": AUTO_EXECUTE_RISK_CEILING,
        }
