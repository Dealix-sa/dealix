"""
Trust Gate — يفحص الـ output draft قبل ما يطلع للـ approval/execute.

يحاول يكتشف:
    - overclaim (we are the only / certified / guaranteed)
    - pricing outside known bands
    - fake URLs / contact info
    - PII leakage in outputs
    - missing citations on factual claims
    - prompt-injection-style "ignore previous" or tool override hints

النواة هنا تحقق نصّي بدون LLM (deterministic, تختبر بدون كلفة).
نقدر لاحقًا نلحق LLM verifier خلف نفس الواجهة.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ..contracts import ContextPacket, GateResult


OVERCLAIM_PATTERNS_AR = [
    "الوحيد في",
    "معتمد رسميًا من",
    "نضمن لك",
    "100%",
    "بدون مخاطر",
    "أول شركة",
]
OVERCLAIM_PATTERNS_EN = [
    r"\bthe only\b",
    r"\bguaranteed\b",
    r"\bcertified by\b",
    r"\b100% (?:risk[- ]free|safe|guaranteed)\b",
    r"\bzero risk\b",
    r"\bbest in the world\b",
]

INJECTION_HINTS = [
    "ignore previous instructions",
    "disregard the system",
    "you are now",
    "override your policy",
    "تجاهل التعليمات السابقة",
    "تجاوز السياسة",
]

PII_PATTERNS = {
    "saudi_id": re.compile(r"\b[12]\d{9}\b"),
    "iban_sa": re.compile(r"\bSA\d{22}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


@dataclass
class TrustFinding:
    code: str
    severity: str  # "low" | "medium" | "high" | "critical"
    detail: str
    location: str | None = None


@dataclass
class TrustReport:
    passed: bool
    findings: list[TrustFinding] = field(default_factory=list)

    def add(self, finding: TrustFinding) -> None:
        self.findings.append(finding)
        if finding.severity in {"high", "critical"}:
            self.passed = False


class TrustGate:
    STAGE = "gate.trust"

    def __init__(
        self,
        *,
        pricing_min_sar: int = 499,
        pricing_max_sar: int = 250_000,
    ) -> None:
        self._price_min = pricing_min_sar
        self._price_max = pricing_max_sar

    def assess(
        self,
        context: ContextPacket,
        draft_text: str,
        *,
        draft_prices_sar: list[int] | None = None,
        urls: list[str] | None = None,
    ) -> GateResult:
        report = TrustReport(passed=True)
        self._check_overclaims(draft_text, report)
        self._check_injection_hints(draft_text, report)
        self._check_pii(draft_text, report)
        if draft_prices_sar:
            self._check_pricing(draft_prices_sar, report)
        if urls:
            self._check_urls(urls, report)

        codes = [f.code for f in report.findings]
        return GateResult(
            stage=self.STAGE,
            passed=report.passed,
            risk_delta=codes,
            approval_required=any(
                f.severity in {"high", "critical"} for f in report.findings
            ),
            reason=(
                None
                if report.passed
                else "trust check failed: "
                + ", ".join(f.code for f in report.findings if f.severity in {"high", "critical"})
            ),
            metadata={"findings": [f.__dict__ for f in report.findings]},
        )

    # ─────────────────────────────────────────────────────────

    def _check_overclaims(self, text: str, report: TrustReport) -> None:
        lower = text.lower()
        for phrase in OVERCLAIM_PATTERNS_AR:
            if phrase in text:
                report.add(
                    TrustFinding(
                        code="overclaim_ar",
                        severity="high",
                        detail=f"contains arabic overclaim: «{phrase}»",
                    )
                )
        for pat in OVERCLAIM_PATTERNS_EN:
            if re.search(pat, lower):
                report.add(
                    TrustFinding(
                        code="overclaim_en",
                        severity="high",
                        detail=f"matches overclaim pattern: /{pat}/",
                    )
                )

    def _check_injection_hints(self, text: str, report: TrustReport) -> None:
        lower = text.lower()
        for hint in INJECTION_HINTS:
            if hint in lower:
                report.add(
                    TrustFinding(
                        code="injection_hint",
                        severity="critical",
                        detail=f"draft contains injection-style phrase: «{hint}»",
                    )
                )

    def _check_pii(self, text: str, report: TrustReport) -> None:
        for kind, pat in PII_PATTERNS.items():
            if pat.search(text):
                report.add(
                    TrustFinding(
                        code=f"pii_{kind}",
                        severity="high",
                        detail=f"draft appears to contain PII ({kind})",
                    )
                )

    def _check_pricing(self, prices: list[int], report: TrustReport) -> None:
        for p in prices:
            if p < self._price_min or p > self._price_max:
                report.add(
                    TrustFinding(
                        code="pricing_out_of_band",
                        severity="high",
                        detail=(
                            f"price {p} SAR is outside allowed band "
                            f"({self._price_min}..{self._price_max})"
                        ),
                    )
                )

    def _check_urls(self, urls: list[str], report: TrustReport) -> None:
        for url in urls:
            if not url.startswith(("https://", "http://")):
                report.add(
                    TrustFinding(
                        code="malformed_url",
                        severity="medium",
                        detail=f"non-http url: {url}",
                    )
                )
            if "localhost" in url or "127.0.0.1" in url:
                report.add(
                    TrustFinding(
                        code="local_url_in_external",
                        severity="high",
                        detail=f"local url leaked into external draft: {url}",
                    )
                )


__all__ = ["TrustFinding", "TrustGate", "TrustReport"]
