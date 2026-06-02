"""Follow-up engine — cadence-driven, draft-only, manual channels.

Cadence (mirrors ``docs/distribution/FOLLOWUP_ENGINE_AR.md``):
  contacted     → D+2 / D+4 / D+7 (the current-due step is surfaced)
  proposal_sent → proposal follow-up at +2 days
  won           → renewal review at +21 days

A follow-up is ``due`` when its due date is on/before the reference date.
Nothing is ever sent — these are reminders the founder actions manually.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from auto_client_acquisition.distribution_os.models import (
    Followup,
    FollowupStatus,
    FollowupType,
    Prospect,
    ProspectStatus,
)

# contacted cadence: ordered (type, day-offset)
_CONTACTED_STEPS: tuple[tuple[FollowupType, int], ...] = (
    (FollowupType.DAY_2, 2),
    (FollowupType.DAY_4, 4),
    (FollowupType.DAY_7, 7),
)
_PROPOSAL_OFFSET_DAYS = 2
_RENEWAL_OFFSET_DAYS = 21


def _as_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def _anchor(p: Prospect) -> date | None:
    return _as_date(p.last_contact_at) or _as_date(p.created_at)


def _make(p: Prospect, ftype: FollowupType, due: date, ref: date, notes: str) -> Followup:
    status = FollowupStatus.DUE.value if due <= ref else FollowupStatus.SCHEDULED.value
    return Followup(
        id=f"fu-{p.id}-{ftype.value}",
        prospect_id=p.id,
        company=p.company,
        due_date=due.isoformat(),
        followup_type=ftype.value,
        status=status,
        channel=p.preferred_channel or "email",
        draft_id=f"drf-{p.id}-outreach_followup_1",
        notes=notes,
    )


def build_followups(prospects: list[Prospect], *, reference: date | None = None) -> list[Followup]:
    """Build the current follow-up for each eligible prospect."""
    ref = reference or datetime.now().date()
    out: list[Followup] = []
    for p in prospects:
        anchor = _anchor(p)
        if anchor is None:
            continue
        days_since = (ref - anchor).days

        if p.status == ProspectStatus.CONTACTED.value:
            # pick the largest cadence step already reached; else the first upcoming
            chosen = _CONTACTED_STEPS[0]
            for step in _CONTACTED_STEPS:
                if days_since >= step[1]:
                    chosen = step
            ftype, offset = chosen
            out.append(
                _make(p, ftype, anchor + timedelta(days=offset), ref, "متابعة محكومة — مسودة فقط")
            )
        elif p.status == ProspectStatus.PROPOSAL_SENT.value:
            out.append(
                _make(
                    p,
                    FollowupType.PROPOSAL_FOLLOWUP,
                    anchor + timedelta(days=_PROPOSAL_OFFSET_DAYS),
                    ref,
                    "متابعة العرض خلال 48 ساعة",
                )
            )
        elif p.status == ProspectStatus.WON.value:
            out.append(
                _make(
                    p,
                    FollowupType.RENEWAL,
                    anchor + timedelta(days=_RENEWAL_OFFSET_DAYS),
                    ref,
                    "مراجعة قيمة وتجديد بعد 21 يوماً",
                )
            )
    return out


def due_followups(prospects: list[Prospect], *, reference: date | None = None) -> list[Followup]:
    """Only the follow-ups that are due on/before the reference date."""
    return [
        f
        for f in build_followups(prospects, reference=reference)
        if f.status == FollowupStatus.DUE.value
    ]


__all__ = ["build_followups", "due_followups"]
