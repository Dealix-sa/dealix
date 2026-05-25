"""
Red Team — مجمَّع فحوصات أمنية ليلية.

يجمع:
    - prompt_injection_tests.run_injection_suite
    - claim_verifier.ClaimVerifier
    - data_loss_prevention.DLP

في واجهة واحدة `RedTeam.run_all(...)` ليستهلكها nightly CI أو فحص يدوي.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .claim_verifier import ClaimResult, ClaimVerifier
from .data_loss_prevention import DLP, DLPVerdict
from .prompt_injection_tests import InjectionResult, run_injection_suite


@dataclass
class RedTeamReport:
    injection_results: list[InjectionResult] = field(default_factory=list)
    claim_results: list[ClaimResult] = field(default_factory=list)
    dlp_verdict: DLPVerdict | None = None

    @property
    def injection_leaked_count(self) -> int:
        return sum(1 for r in self.injection_results if r.leaked)

    @property
    def unverified_claims_count(self) -> int:
        return sum(1 for r in self.claim_results if not r.verified)

    @property
    def passed(self) -> bool:
        if self.injection_leaked_count > 0:
            return False
        if self.unverified_claims_count > 0:
            return False
        if self.dlp_verdict is not None and not self.dlp_verdict.allow:
            return False
        return True


class RedTeam:
    """واجهة واحدة لتشغيل كل الفحوصات."""

    def __init__(
        self,
        *,
        claim_verifier: ClaimVerifier | None = None,
        dlp: DLP | None = None,
    ) -> None:
        self._claim_verifier = claim_verifier or ClaimVerifier()
        self._dlp = dlp or DLP()

    def run_all(
        self,
        probe_fn: Callable[[str], str],
        draft_text: str,
        urls: list[str],  # noqa: ARG002 — مدمج للتجانس مع باقي الواجهة المستقبلية
        claims: list[str],
        evidence: dict[str, str],
        *,
        workspace_id: str | None = None,
    ) -> RedTeamReport:
        report = RedTeamReport()
        report.injection_results = run_injection_suite(probe_fn)
        report.claim_results = self._claim_verifier.verify(claims, evidence)
        report.dlp_verdict = self._dlp.scan(draft_text, workspace_id)
        return report


__all__ = ["RedTeam", "RedTeamReport"]
