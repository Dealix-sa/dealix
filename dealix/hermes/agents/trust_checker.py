"""
Trust checker agent — applies guardrails to a draft and returns the result.
"""

from __future__ import annotations

from dealix.hermes.trust.guardrails import TrustCheckRequest, TrustCheckResult, trust_check


def check(request: TrustCheckRequest) -> TrustCheckResult:
    return trust_check(request)
