"""Pure safety classification for canonical strategy steps.

External actions are never auto-authorized by this module.
"""

from __future__ import annotations

from .models import ActionKind, Route, SafetyDecision, StrategyStep

AUTO_RISK_CEILING = 0.40
EXTERNAL_CHANNELS = frozenset({"email", "whatsapp", "sms", "linkedin", "phone", "social"})
BLOCKED_ACTION_PATTERNS = (
    "cold_whatsapp",
    "cold_outreach",
    "auto_send",
    "mass_send",
    "bulk_broadcast",
    "linkedin_automation",
    "linkedin_scrape",
    "scrape_contacts",
    "buy_leads",
    "bypass_consent",
    "fake_proof",
    "fake_revenue",
    "guaranteed_revenue",
    "guaranteed_win",
    "government_access_claim",
    "auto_charge",
    "auto_invoice",
)
_MINIMUM_LEVEL: dict[ActionKind, int] = {
    ActionKind.OBSERVE: 0,
    ActionKind.ANALYZE: 1,
    ActionKind.INTERNAL_DRAFT: 2,
    ActionKind.INTERNAL_WRITE: 3,
    ActionKind.REPO_WRITE: 4,
    ActionKind.EXTERNAL_DRAFT: 5,
    ActionKind.EXTERNAL_ACTION: 5,
    ActionKind.MERGE: 5,
    ActionKind.PUBLISH: 5,
    ActionKind.PAYMENT: 5,
    ActionKind.PRODUCTION: 5,
}
_ALWAYS_APPROVAL = {
    ActionKind.EXTERNAL_DRAFT,
    ActionKind.EXTERNAL_ACTION,
    ActionKind.MERGE,
    ActionKind.PUBLISH,
    ActionKind.PAYMENT,
    ActionKind.PRODUCTION,
}


def _forbidden(action: str) -> str | None:
    normalized = action.strip().casefold()
    return next((pattern for pattern in BLOCKED_ACTION_PATTERNS if pattern in normalized), None)


def evaluate_step(step: StrategyStep, *, autonomy_level: int) -> SafetyDecision:
    if not 0 <= autonomy_level <= 4:
        raise ValueError("autonomy_level must be between 0 and 4")
    forbidden = _forbidden(step.action)
    minimum = _MINIMUM_LEVEL[step.kind]
    if forbidden:
        return SafetyDecision(
            route=Route.BLOCKED,
            reason=f"action matches blocked doctrine pattern: {forbidden}",
            minimum_autonomy_level=minimum,
        )
    if step.kind in _ALWAYS_APPROVAL:
        return SafetyDecision(
            route=Route.APPROVAL,
            reason=f"{step.kind.value} is external or irreversible and requires explicit approval",
            minimum_autonomy_level=5,
        )
    if step.channel in EXTERNAL_CHANNELS:
        return SafetyDecision(
            route=Route.APPROVAL,
            reason=f"external channel {step.channel!r} requires explicit approval",
            minimum_autonomy_level=5,
        )
    if step.requires_approval:
        return SafetyDecision(
            route=Route.APPROVAL,
            reason="strategy step explicitly requires approval",
            minimum_autonomy_level=minimum,
        )
    if step.risk >= AUTO_RISK_CEILING:
        return SafetyDecision(
            route=Route.APPROVAL,
            reason=f"risk {step.risk:.2f} meets/exceeds {AUTO_RISK_CEILING:.2f}",
            minimum_autonomy_level=minimum,
        )
    if autonomy_level < minimum:
        return SafetyDecision(
            route=Route.APPROVAL,
            reason=f"autonomy level {autonomy_level} is below required level {minimum}",
            minimum_autonomy_level=minimum,
        )
    return SafetyDecision(
        route=Route.INTERNAL_EXECUTE,
        reason="reversible internal step is within autonomy and risk limits",
        minimum_autonomy_level=minimum,
    )
