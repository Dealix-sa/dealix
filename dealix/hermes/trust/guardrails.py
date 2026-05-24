"""
Guardrails — content-level checks before any execution becomes runnable.

  - Prompt Injection Guard (direct + indirect via tool inputs)
  - No-overclaim Guard (no fake metrics / unfounded promises)
  - Data Scope Guard (action must not leak data outside declared scope)
  - Pricing Guard (no pricing outside approved ranges)
  - External Commitment Guard (no contractual language outside L4 + approval)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.core.schemas import Execution


class GuardrailViolation(Exception):
    """Raised when one or more guardrails reject an execution."""

    def __init__(self, violations: list[str]):
        self.violations = violations
        super().__init__("; ".join(violations))


_PROMPT_INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard the above",
    "you are now",
    "act as system",
    "reveal your system prompt",
    "exfiltrate",
    "send all data to",
)

_OVERCLAIM_PHRASES = (
    "guaranteed roi",
    "100% conversion",
    "no risk",
    "world's best",
    "official partner of",
    "certified by",
)

_COMMITMENT_PHRASES = (
    "we hereby agree",
    "this contract binds",
    "we commit to pay",
    "we sign on behalf",
    "i sign on behalf",
)


@dataclass
class GuardrailReport:
    passed: bool
    violations: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)


def _scan_text(text: str) -> tuple[list[str], dict[str, bool]]:
    lc = (text or "").lower()
    violations: list[str] = []
    checks = {
        "prompt_injection": True,
        "no_overclaim": True,
        "no_external_commitment": True,
    }
    for marker in _PROMPT_INJECTION_MARKERS:
        if marker in lc:
            violations.append(f"prompt_injection:{marker!r}")
            checks["prompt_injection"] = False
            break
    for phrase in _OVERCLAIM_PHRASES:
        if phrase in lc:
            violations.append(f"overclaim:{phrase!r}")
            checks["no_overclaim"] = False
            break
    for phrase in _COMMITMENT_PHRASES:
        if phrase in lc:
            violations.append(f"external_commitment:{phrase!r}")
            checks["no_external_commitment"] = False
            break
    return violations, checks


def check_guardrails(
    execution: Execution,
    *,
    pricing_min_sar: float = 0.0,
    pricing_max_sar: float = 250_000.0,
    allowed_scopes: tuple[str, ...] = ("tenant_only", "internal"),
) -> GuardrailReport:
    report = GuardrailReport(passed=True)

    text_blob = " ".join(
        str(v) for v in execution.payload.values() if isinstance(v, str)
    ) + " " + (execution.expected_result or "")

    violations, checks = _scan_text(text_blob)
    report.violations.extend(violations)
    report.checks.update(checks)

    # Pricing guard
    price = execution.payload.get("price_sar")
    pricing_ok = True
    if isinstance(price, (int, float)):
        if price < pricing_min_sar or price > pricing_max_sar:
            report.violations.append(f"pricing_out_of_range:{price}")
            pricing_ok = False
    report.checks["pricing_in_range"] = pricing_ok

    # Data scope guard
    scope = execution.payload.get("data_scope", "tenant_only")
    scope_ok = scope in allowed_scopes
    if not scope_ok:
        report.violations.append(f"data_scope_violation:{scope}")
    report.checks["data_scope_ok"] = scope_ok

    report.passed = not report.violations
    return report
