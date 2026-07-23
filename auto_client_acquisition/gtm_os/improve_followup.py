"""Bridge: improve diagnostic findings -> founder-approval outreach cards.

This is the "automatic sending" story done the Dealix way: it builds the entire
outbound pipeline up to — and stopping dead at — the human approval gate. It is
**draft-only by construction**:

- The module contains NO send / dispatch / transmit function. There is no code
  path that can put a message on a wire. Auto-send is not disabled by a flag here;
  it is structurally absent.
- Every card is stamped ``governance_decision = "approval_required"``,
  ``send_status = "draft"``, ``outbound_mode = "draft_only"``,
  ``dispatchable = False`` from birth (mirrors ``gtm_os.outreach_draft.OutreachDraft``).
- Recipients are opaque ``recipient_ref`` handles (CRM id / caller hash), never a
  raw email or phone — raw PII is rejected.
- Guaranteed-outcome claims are blocked; only hypothesis language survives.

Turning any of this into an actual send requires the founder to act through
``approval_center`` after review, and enabling live channels requires a merged
controlled-live approval PR — neither of which this module can perform.
"""

from __future__ import annotations

import re
from typing import Any

# Draft channels we may compose for. WhatsApp/email/sms are drafted, never sent.
ALLOWED_CHANNELS: tuple[str, ...] = ("whatsapp", "email", "sms", "linkedin_note")
SEQUENCE_STEPS: tuple[str, ...] = (
    "first_touch",
    "follow_up_1",
    "follow_up_2",
    "proposal_intro",
    "close_loop",
)

# Guaranteed-outcome patterns (AR + EN) — mirrors scripts/verify_dealix_positioning.py.
_GUARANTEE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"guaranteed?\s+(revenue|results?|roi|return|income|savings?)", re.I),
    re.compile(r"we\s+guarantee", re.I),
    re.compile(r"عائد\s+مضمون"),
    re.compile(r"أرباح\s+مضمون"),
    re.compile(r"نتائج\s+مضمون"),
    re.compile(r"ضمان\s+(الأرباح|العائد|النتائج)"),
)

# A recipient_ref must be an opaque handle — reject anything that looks like PII.
_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_PHONE_RE = re.compile(r"(?:\+?\d[\s-]?){7,}")


def has_guaranteed_claim(text: str) -> bool:
    """True if the text makes an affirmative guaranteed-outcome claim."""
    return any(p.search(text or "") for p in _GUARANTEE_PATTERNS)


def _reject_pii(recipient_ref: str) -> None:
    if not recipient_ref or not recipient_ref.strip():
        raise ValueError("recipient_ref is required (opaque CRM id / hash)")
    if _EMAIL_RE.search(recipient_ref) or _PHONE_RE.search(recipient_ref):
        raise ValueError(
            "recipient_ref must be an opaque handle, not raw PII "
            "(no email / phone) — hash it upstream"
        )


def compose_followup_text(finding: dict[str, Any], step: str = "follow_up_1") -> str:
    """Compose a hypothesis-language draft from one vetted improve finding.

    Never asserts a guaranteed outcome. Uses 'we expect' / 'we will measure'.
    """
    title = str(finding.get("title") or finding.get("summary") or "فرصة تحسين").strip()
    evidence = str(finding.get("evidence") or finding.get("file") or "").strip()
    ev = f" (الدليل: {evidence})" if evidence else ""
    return (
        f"لاحظنا في التشخيص: {title}{ev}. "
        f"نتوقّع أن معالجتها تحسّن الأداء، وسنقيس الأثر قبل/بعد. "
        f"هل نحوّلها إلى خطة تنفيذ ضمن السبرينت؟"
    )


def build_followup_card(
    *,
    finding: dict[str, Any],
    recipient_ref: str,
    channel: str = "whatsapp",
    step: str = "follow_up_1",
    language: str = "ar",
) -> dict[str, Any]:
    """Build ONE draft-only, approval-required outreach card. Never sends."""
    if channel not in ALLOWED_CHANNELS:
        raise ValueError(f"channel must be one of {ALLOWED_CHANNELS}, got {channel!r}")
    if step not in SEQUENCE_STEPS:
        raise ValueError(f"step must be one of {SEQUENCE_STEPS}, got {step!r}")
    _reject_pii(recipient_ref)

    draft_text = compose_followup_text(finding, step)
    blocked = has_guaranteed_claim(draft_text) or has_guaranteed_claim(
        str(finding.get("title") or "")
    )
    block_reason = "guaranteed-outcome claim (NO_GUARANTEED_CLAIMS)" if blocked else ""

    # Doctrine stamps — invariant regardless of inputs. Fail-closed.
    return {
        "recipient_ref": recipient_ref,
        "channel": channel,
        "step": step,
        "language": language,
        "draft_text": draft_text,
        "evidence": finding.get("evidence") or finding.get("file"),
        "finding_id": finding.get("id"),
        "governance_decision": "approval_required",
        "send_status": "draft",
        "outbound_mode": "draft_only",
        "requires_approval": True,
        "dispatchable": False,
        "blocked": blocked,
        "block_reason": block_reason,
    }


def build_approval_queue(
    findings: list[dict[str, Any]],
    *,
    recipient_ref: str,
    channel: str = "whatsapp",
    step: str = "follow_up_1",
) -> list[dict[str, Any]]:
    """Build a draft-only approval queue from a set of improve findings.

    The returned cards go to the founder for review; nothing here dispatches.
    """
    return [
        build_followup_card(
            finding=f, recipient_ref=recipient_ref, channel=channel, step=step
        )
        for f in findings
    ]
