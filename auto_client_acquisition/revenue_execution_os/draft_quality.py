"""Draft quality gate — deterministic scoring before a founder approves copy.

Pure functions: a draft scores 0-100 across claim safety, channel safety,
governance presence, approval-first posture, evidence level, personalization,
and a clear call-to-action. Claim or channel violations fail the draft
regardless of score.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from auto_client_acquisition.revenue_execution_os.models import (
    Draft,
    DraftType,
    Prospect,
)

PASS_THRESHOLD = 70

# Draft types that reference value/results and therefore need evidence >= L1.
VALUE_CLAIM_TYPES: frozenset[str] = frozenset(
    {
        DraftType.DIAGNOSTIC_SUMMARY,
        DraftType.PROOF_PACK_INTRO,
        DraftType.RENEWAL_UPSELL,
    }
)

_WEIGHTS: dict[str, int] = {
    "claim_safe": 30,
    "channel_safe": 20,
    "governed": 10,
    "approval_first": 10,
    "evidence_ok": 10,
    "personalized": 10,
    "has_cta": 10,
}


@dataclass(frozen=True, slots=True)
class DraftQuality:
    draft_id: str
    score: int
    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "draft_id": self.draft_id,
            "score": self.score,
            "passed": self.passed,
            "checks": self.checks,
            "reasons": self.reasons,
        }


def _has_cta(text: str) -> bool:
    return "?" in text or "؟" in text


def score_draft(draft: Draft, prospect: Prospect | None = None) -> DraftQuality:
    """Score a single draft. Claim/channel failures hard-fail the draft."""
    issues = draft.issues or []
    blob = f"{draft.subject}\n{draft.body_ar}\n{draft.body_en}"

    claim_safe = (
        not any(i.startswith("forbidden_claim:") for i in issues)
        and draft.governance_decision != "BLOCK"
    )
    channel_safe = "forbidden_channel_language" not in issues and not any(
        i.startswith("forbidden_term:") for i in issues
    )
    governed = bool(draft.governance_decision)
    approval_first = bool(draft.approval_required)
    evidence_ok = (draft.draft_type not in VALUE_CLAIM_TYPES) or (draft.evidence_level >= 1)
    personalized = True
    if prospect is not None:
        company = (prospect.company or "").strip()
        personalized = bool(company) and (company in blob)
    else:
        personalized = "—" not in blob
    has_cta = _has_cta(blob)

    checks = {
        "claim_safe": claim_safe,
        "channel_safe": channel_safe,
        "governed": governed,
        "approval_first": approval_first,
        "evidence_ok": evidence_ok,
        "personalized": personalized,
        "has_cta": has_cta,
    }
    score = sum(_WEIGHTS[k] for k, ok in checks.items() if ok)

    reasons: list[str] = []
    if not claim_safe:
        reasons.append("forbidden or guaranteed claim present")
    if not channel_safe:
        reasons.append("forbidden channel / operational language present")
    if not evidence_ok:
        reasons.append("value-claim draft missing evidence level >= L1")
    if not personalized:
        reasons.append("not personalized to the prospect")
    if not has_cta:
        reasons.append("no clear call-to-action")

    # Hard gate: a claim or channel violation fails regardless of score.
    passed = claim_safe and channel_safe and score >= PASS_THRESHOLD
    return DraftQuality(
        draft_id=draft.draft_id, score=score, passed=passed, checks=checks, reasons=reasons
    )


@dataclass(frozen=True, slots=True)
class DraftQualityReport:
    total: int
    passed: int
    failed: int
    pass_rate: float
    results: list[DraftQuality] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": round(self.pass_rate, 3),
            "results": [r.to_dict() for r in self.results],
        }


def review_drafts(
    drafts: Iterable[Draft],
    prospects_by_id: Mapping[str, Prospect] | None = None,
) -> DraftQualityReport:
    """Score a batch of drafts and summarize pass/fail."""
    lookup = prospects_by_id or {}
    results = [score_draft(d, lookup.get(d.prospect_id)) for d in drafts]
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    pass_rate = (passed / total) if total else 0.0
    return DraftQualityReport(
        total=total, passed=passed, failed=failed, pass_rate=pass_rate, results=results
    )


__all__ = [
    "PASS_THRESHOLD",
    "VALUE_CLAIM_TYPES",
    "DraftQuality",
    "DraftQualityReport",
    "review_drafts",
    "score_draft",
]
