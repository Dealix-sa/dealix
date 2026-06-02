"""250/day Cold-Email Draft Factory.

Produces personalized outreach *drafts* and runs each through the quality
gate. Hard invariants:

  - ``DAILY_DRAFT_TARGET == 250`` (production capacity, not a send quota).
  - ``MAX_AUTO_SENDS == 0`` — this module never sets ``send_status`` to
    anything other than ``"draft"``. Sending is a separate, human-approved,
    ramp-capped path.

Every produced draft includes an unsubscribe line and is at least P1
personalized; otherwise the gate marks it failed and it cannot be queued.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

from auto_client_acquisition.market_production_os.quality_gate import check_draft
from auto_client_acquisition.market_production_os.schemas import (
    ComplianceStatus,
    DraftKind,
    OutreachDraft,
    PersonalizationLevel,
    Prospect,
    SendStatus,
)

DAILY_DRAFT_TARGET: int = 250
MAX_AUTO_SENDS: int = 0

# first_touch + follow_up_1 + follow_up_2 + proposal_intro + close_loop = 250
DEFAULT_MIX: dict[str, int] = {
    DraftKind.FIRST_TOUCH.value: 100,
    DraftKind.FOLLOW_UP_1.value: 75,
    DraftKind.FOLLOW_UP_2.value: 50,
    DraftKind.PROPOSAL_INTRO.value: 15,
    DraftKind.CLOSE_LOOP.value: 10,
}

_UNSUB_AR = "لإيقاف الرسائل: ردّ بكلمة \"إيقاف\" أو استخدم رابط إلغاء الاشتراك."

_SUBJECTS: dict[str, str] = {
    DraftKind.FIRST_TOUCH.value: "ملاحظة سريعة حول متابعة العملاء في {company}",
    DraftKind.FOLLOW_UP_1.value: "متابعة: فكرة عملية لـ {company}",
    DraftKind.FOLLOW_UP_2.value: "آخر متابعة بخصوص تشغيل الإيرادات لدى {company}",
    DraftKind.PROPOSAL_INTRO.value: "مقترح مختصر لـ {company}",
    DraftKind.CLOSE_LOOP.value: "أغلق الموضوع؟ — {company}",
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def daily_mix(target: int = DAILY_DRAFT_TARGET) -> dict[str, int]:
    """Scale the default kind mix to ``target`` (keeps the relative shape)."""
    if target == DAILY_DRAFT_TARGET:
        return dict(DEFAULT_MIX)
    scale = target / DAILY_DRAFT_TARGET
    scaled = {k: max(1, round(v * scale)) for k, v in DEFAULT_MIX.items()}
    # Reconcile rounding drift onto the largest bucket.
    drift = target - sum(scaled.values())
    if drift:
        biggest = max(scaled, key=lambda k: scaled[k])
        scaled[biggest] = max(1, scaled[biggest] + drift)
    return scaled


def _body(prospect: Prospect, offer: str, kind: str, pain: str) -> str:
    company = prospect.company
    role = prospect.recipient_role or "فريق المبيعات"
    lines = [
        f"مرحبًا {role} في {company}،",
        "",
        f"لاحظنا نمطًا شائعًا في {prospect.sector}: {pain}.",
        f"نقترح البدء بـ \"{offer}\" — خطوة محدودة النطاق تكشف أين تضيع الفرص "
        "وترتّب المتابعة، دون أي إرسال خارجي إلا بموافقتكم.",
        "هذه فرص مُثبتة بأدلة، وليست وعودًا بنتائج مضمونة.",
        "",
        "هل أرسل لكم ملخصًا من صفحة واحدة؟",
        "",
        _UNSUB_AR,
    ]
    return "\n".join(lines)


def build_draft(
    *,
    prospect: Prospect,
    offer: str,
    kind: str = DraftKind.FIRST_TOUCH.value,
    pain: str = "ضعف متابعة العملاء المحتملين",
    personalization_level: int = int(PersonalizationLevel.P1),
    evidence_level: int = 1,
    recipient_email: str = "",
    suppression: Sequence[str] = (),
) -> OutreachDraft:
    """Build a single governed draft (``send_status="draft"`` always)."""
    subject = _SUBJECTS.get(kind, _SUBJECTS[DraftKind.FIRST_TOUCH.value]).format(
        company=prospect.company
    )
    body = _body(prospect, offer, kind, pain)
    gate = check_draft(
        subject=subject,
        body=body,
        personalization_level=personalization_level,
        evidence_level=evidence_level,
        unsubscribe_included=True,
        recipient_email=recipient_email,
        lead_source=prospect.source,
        suppression=suppression,
    )
    compliance = (
        ComplianceStatus.PASSED.value if gate.passed else ComplianceStatus.FAILED.value
    )
    return OutreachDraft(
        draft_id=f"draft_{uuid4().hex[:20]}",
        prospect_id=prospect.prospect_id,
        company=prospect.company,
        sector=prospect.sector,
        recipient_role=prospect.recipient_role,
        source=prospect.source,
        kind=kind,
        pain_hypothesis=pain,
        personalization_note=f"{prospect.sector} / {prospect.recipient_role}".strip(" /"),
        personalization_level=int(personalization_level),
        offer=offer,
        subject=subject,
        body=body,
        cta="طلب ملخص من صفحة واحدة",
        language="ar",
        evidence_level=int(evidence_level),
        unsubscribe_included=True,
        risk_level=gate.risk_level,
        compliance_status=compliance,
        send_status=SendStatus.DRAFT.value,  # invariant: never "sent" here
        governance_decision=gate.governance_decision,
        gate_reasons=gate.reasons,
        created_at=_now_iso(),
    )


def produce_drafts(
    prospects: Sequence[Prospect],
    *,
    offers: Sequence[str],
    target: int = DAILY_DRAFT_TARGET,
    suppression: Sequence[str] = (),
) -> list[OutreachDraft]:
    """Produce up to ``target`` drafts across the kind mix.

    Cycles through ``prospects`` and ``offers`` round-robin to reach the
    daily target. Returns drafts only; sends nothing.
    """
    if not prospects:
        return []
    if not offers:
        offers = ("Free AI Ops Diagnostic",)
    mix = daily_mix(target)
    drafts: list[OutreachDraft] = []
    pi = 0
    oi = 0
    for kind, count in mix.items():
        for _ in range(count):
            prospect = prospects[pi % len(prospects)]
            offer = offers[oi % len(offers)]
            drafts.append(
                build_draft(prospect=prospect, offer=offer, kind=kind, suppression=suppression)
            )
            pi += 1
            oi += 1
    return drafts


def summarize_batch(drafts: Sequence[OutreachDraft]) -> dict[str, object]:
    """Aggregate counts for the daily report."""
    passed = sum(1 for d in drafts if d.compliance_status == ComplianceStatus.PASSED.value)
    sent = sum(1 for d in drafts if d.send_status == SendStatus.SENT.value)
    by_kind: dict[str, int] = {}
    for d in drafts:
        by_kind[d.kind] = by_kind.get(d.kind, 0) + 1
    return {
        "generated": len(drafts),
        "quality_passed": passed,
        "quality_failed": len(drafts) - passed,
        "auto_sent": sent,  # must always be 0
        "by_kind": by_kind,
    }


__all__ = [
    "DAILY_DRAFT_TARGET",
    "DEFAULT_MIX",
    "MAX_AUTO_SENDS",
    "build_draft",
    "daily_mix",
    "produce_drafts",
    "summarize_batch",
]
