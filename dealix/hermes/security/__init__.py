"""
Hermes Security — حزمة الفحوصات الأمنية.

تُجمَّع هنا الأدوات: prompt injection tests، output sanitizer،
DLP، claim verifier، source verifier، sandbox، و Red Team.
"""

from __future__ import annotations

from .claim_verifier import ClaimResult, ClaimVerifier
from .data_loss_prevention import DLP, DLPVerdict, RegulatedHit
from .output_sanitizer import OutputSanitizer, Removal, SanitizedOutput
from .prompt_injection_tests import (
    INJECTION_ATTACKS,
    InjectionAttack,
    InjectionResult,
    evaluate_response,
    run_injection_suite,
)
from .red_team import RedTeam, RedTeamReport
from .sandbox import Sandbox, SandboxResult
from .source_verifier import SourceResult, SourceVerifier


__all__ = [
    "DLP",
    "DLPVerdict",
    "INJECTION_ATTACKS",
    "ClaimResult",
    "ClaimVerifier",
    "InjectionAttack",
    "InjectionResult",
    "OutputSanitizer",
    "RedTeam",
    "RedTeamReport",
    "RegulatedHit",
    "Removal",
    "Sandbox",
    "SandboxResult",
    "SanitizedOutput",
    "SourceResult",
    "SourceVerifier",
    "evaluate_response",
    "run_injection_suite",
]
