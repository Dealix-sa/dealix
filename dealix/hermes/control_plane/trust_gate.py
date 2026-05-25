"""
TrustGate — refuses any request whose payload makes unverifiable claims
or violates trust constraints (overclaim, missing evidence, sensitive
data leakage in external output, pricing without authorization).

This gate runs *before* the action executes; it inspects the payload
summary attached to the RequestContext. A separate post-execution check
inspects the produced artifact (see ``outcome_gate``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.control_plane.request_context import RequestContext


@dataclass(frozen=True)
class TrustFinding:
    code: str
    severity: str  # "info" | "warn" | "block"
    message: str


@dataclass(frozen=True)
class TrustDecision:
    passed: bool
    findings: tuple[TrustFinding, ...] = field(default_factory=tuple)

    @property
    def blocked(self) -> bool:
        return any(f.severity == "block" for f in self.findings)


_OVERCLAIM_PHRASES = (
    "guaranteed sales",
    "100% conversion",
    "replace your sales team",
    "no risk",
    "always profitable",
)

_BANNED_EXTERNAL_FIELDS = (
    "sovereign_memory",
    "internal_strategy",
    "raw_customer_export",
)


def evaluate(context: RequestContext) -> TrustDecision:
    findings: list[TrustFinding] = []

    summary = (context.payload_summary or "").lower()
    for phrase in _OVERCLAIM_PHRASES:
        if phrase in summary:
            findings.append(
                TrustFinding(
                    code="overclaim",
                    severity="block",
                    message=f"Overclaim phrase detected: {phrase!r}",
                )
            )

    if context.external_action:
        for banned in _BANNED_EXTERNAL_FIELDS:
            if banned in summary:
                findings.append(
                    TrustFinding(
                        code="sovereign_leak",
                        severity="block",
                        message=f"External payload references sovereign field: {banned!r}",
                    )
                )

    if context.capability == "send_external_email" and "price" in summary and "approved" not in summary:
        findings.append(
            TrustFinding(
                code="unapproved_price",
                severity="block",
                message="External email contains pricing without approval marker.",
            )
        )

    passed = not any(f.severity == "block" for f in findings)
    return TrustDecision(passed=passed, findings=tuple(findings))
