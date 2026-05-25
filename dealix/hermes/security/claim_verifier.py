"""
Claim Verifier — تحقّق من ادعاءات النصّ مقابل قاعدة شواهد.

كل ادعاء يجب أن يحمل مرجعًا لمفتاح شاهد موجود في قاموس الشواهد، وإلّا
يُعتبر غير موثَّق.

تنسيق الادعاء المتوقَّع:
    "<claim text> [evidence:<key>]"

إذا لم يحتوِ الادعاء على مرجع، أو كان المرجع يشير إلى مفتاح غير موجود،
يُعاد `verified=False` مع تفسير واضح.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ClaimResult:
    claim: str
    verified: bool
    evidence_key: str | None = None
    evidence_value: str | None = None
    reasons: list[str] = field(default_factory=list)


_EVIDENCE_REF_RE = re.compile(r"\[evidence:([A-Za-z0-9_\-\.]+)\]")


def _extract_evidence_keys(claim: str) -> list[str]:
    return _EVIDENCE_REF_RE.findall(claim)


class ClaimVerifier:
    """يفحص كل ادعاء ضدّ قاموس شواهد ويُرجع تقرير تفصيلي."""

    def verify(
        self,
        claims: list[str],
        evidence: dict[str, str],
    ) -> list[ClaimResult]:
        if not isinstance(claims, list):
            raise TypeError("claims must be a list[str]")
        if not isinstance(evidence, dict):
            raise TypeError("evidence must be a dict[str, str]")

        results: list[ClaimResult] = []
        for claim in claims:
            if not isinstance(claim, str) or not claim.strip():
                results.append(
                    ClaimResult(
                        claim=claim if isinstance(claim, str) else "",
                        verified=False,
                        reasons=["empty_or_invalid_claim"],
                    )
                )
                continue

            keys = _extract_evidence_keys(claim)
            if not keys:
                results.append(
                    ClaimResult(
                        claim=claim,
                        verified=False,
                        reasons=["missing_evidence_reference"],
                    )
                )
                continue

            # نأخذ أوّل مرجع لربط الادعاء بشاهده الأساسي.
            primary_key = keys[0]
            if primary_key not in evidence:
                results.append(
                    ClaimResult(
                        claim=claim,
                        verified=False,
                        evidence_key=primary_key,
                        reasons=[f"evidence_key_not_found:{primary_key}"],
                    )
                )
                continue

            value = evidence[primary_key]
            if not value or not value.strip():
                results.append(
                    ClaimResult(
                        claim=claim,
                        verified=False,
                        evidence_key=primary_key,
                        evidence_value=value,
                        reasons=[f"evidence_value_empty:{primary_key}"],
                    )
                )
                continue

            results.append(
                ClaimResult(
                    claim=claim,
                    verified=True,
                    evidence_key=primary_key,
                    evidence_value=value,
                    reasons=["evidence_present"],
                )
            )

        return results


__all__ = ["ClaimResult", "ClaimVerifier"]
