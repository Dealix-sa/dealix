"""Follow-up Commander — drafts the next message in a sales conversation.

The commander never sends. It returns a draft + a recommended cadence.
The actual send is routed through the sovereignty gate (the
`send_external_message` tool is S3+).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class FollowUpDraft:
    opportunity_id: str
    sequence_step: int
    subject: str
    body_markdown: str
    send_after: datetime
    channel: str = "email"


_TONE = {
    1: "تذكير ودّي بعد ٤٨ ساعة بدون ضغط، نطلب تأكيداً للاهتمام.",
    2: "إعادة صياغة القيمة المركزية + سؤال واحد عن العائق.",
    3: "خاتمة مهذّبة — إذا لم نسمع، نُغلق المحادثة باحترام.",
}


def draft(
    *,
    opportunity_id: str,
    buyer_name: str,
    sequence_step: int,
    promise: str,
    last_contact_at: datetime,
    cooldown_days: tuple[int, int, int] = (2, 5, 9),
) -> FollowUpDraft:
    if sequence_step not in {1, 2, 3}:
        raise ValueError("sequence_step must be 1, 2, or 3")
    cooldown = cooldown_days[sequence_step - 1]
    send_after = last_contact_at + timedelta(days=cooldown)

    tone = _TONE[sequence_step]
    subject = {
        1: f"متابعة سريعة — {promise}",
        2: f"سؤال واحد بخصوص — {promise}",
        3: "إغلاق المحادثة باحترام",
    }[sequence_step]

    body = (
        f"السلام عليكم {buyer_name}،\n\n"
        f"{tone}\n\n"
        f"الوعد: {promise}\n"
        "لا أرقام مُخترعة، ولا التزامات لم نُثبتها.\n\n"
        "تحياتي،\nDealix"
    )
    return FollowUpDraft(
        opportunity_id=opportunity_id,
        sequence_step=sequence_step,
        subject=subject,
        body_markdown=body,
        send_after=send_after,
    )


__all__ = ["FollowUpDraft", "draft"]
