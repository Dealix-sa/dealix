"""Founder Action Inbox — one prioritized list of "founder-only" items.

صندوق إجراءات المؤسس — قائمة موحّدة لكل ما يحتاج لمسة المؤسس.

Sources (all read-only, defensive — missing modules skip silently):
  - Pending approvals (approval_center.list_pending)
  - Stale lead inbox (auto_client_acquisition.lead_inbox)
  - Evidence gap (no events logged today)
  - PDPL pass open items
  - First-paid Diagnostic open state
  - Strongest plan missing-path wiring

Each item carries:
  - priority: P0 (block all), P1 (today), P2 (this week), P3 (later)
  - title_ar / title_en
  - cta_ar / cta_en (one-line action)
  - source (which subsystem produced it)
  - is_estimate flag where the count is operational, not authoritative

Doctrine:
  - Article 4: read-only, no external sends.
  - Article 8: counts marked is_estimate=True where applicable.
  - Article 11: aggregator only, no new business logic.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    load_evidence_rows,
)
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_pdpl_compliance_pass,
)
from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status

_PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def _approval_items() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.approval_center import list_pending  # type: ignore
    except Exception:  # noqa: BLE001
        return []

    try:
        pending = list_pending()
    except Exception:  # noqa: BLE001
        return []

    items: list[dict[str, Any]] = []
    for req in pending or []:
        risk = (getattr(req, "risk_level", "low") or "low").lower()
        priority = "P0" if risk == "high" else "P1" if risk == "medium" else "P2"
        ar_summary = getattr(req, "summary_ar", "") or "موافقة على إجراء"
        en_summary = getattr(req, "summary_en", "") or "Approve action"
        items.append(
            {
                "priority": priority,
                "source": "approval_center",
                "title_ar": f"موافقة معلّقة: {ar_summary[:80]}",
                "title_en": f"Pending approval: {en_summary[:80]}",
                "cta_ar": "افتح /ops/approvals ووافق أو ارفض.",
                "cta_en": "Open /ops/approvals and approve/reject.",
                "object_type": getattr(req, "object_type", ""),
                "object_id": getattr(req, "object_id", ""),
                "approval_id": getattr(req, "approval_id", ""),
                "risk_level": risk,
                "created_at": str(getattr(req, "created_at", "")),
            }
        )
    return items


def _stale_lead_items(stale_hours: int = 24) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition import lead_inbox  # type: ignore
    except Exception:  # noqa: BLE001
        return []

    if not hasattr(lead_inbox, "list_leads"):
        return []

    try:
        leads = lead_inbox.list_leads(limit=500)
    except Exception:  # noqa: BLE001
        return []

    cutoff = datetime.now(UTC) - timedelta(hours=stale_hours)
    items: list[dict[str, Any]] = []
    for lead in leads:
        status = (lead.get("status") or "new").lower()
        if status not in ("new", "contacted_pending"):
            continue
        ts = (lead.get("created_at") or "").strip()
        if not ts:
            continue
        try:
            created = datetime.fromisoformat(ts)
            if created.tzinfo is None:
                created = created.replace(tzinfo=UTC)
        except ValueError:
            continue
        if created >= cutoff:
            continue
        age_hours = int((datetime.now(UTC) - created).total_seconds() / 3600)
        items.append(
            {
                "priority": "P0" if age_hours >= 48 else "P1",
                "source": "lead_inbox",
                "title_ar": f"Lead متروك {age_hours}h: {lead.get('company', lead.get('name', ''))}",
                "title_en": f"Lead waiting {age_hours}h: {lead.get('company', lead.get('name', ''))}",
                "cta_ar": "ردّ يدوي عبر LinkedIn/Email أو سجّل سبب الإسقاط.",
                "cta_en": "Reply manually via LinkedIn/Email or log a drop reason.",
                "lead_id": lead.get("id", ""),
                "age_hours": age_hours,
                "is_estimate": True,
            }
        )
    return items


def _evidence_gap_item(rows: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
    counts = count_evidence_events(rows, exclude_placeholders=True)
    today_total = int(counts.get("today_total") or 0)
    week_total = int(counts.get("week_total") or 0)
    if today_total == 0:
        return [
            {
                "priority": "P1",
                "source": "evidence_csv",
                "title_ar": "لم تسجّل أي حدث أدلة اليوم.",
                "title_en": "No evidence events logged today.",
                "cta_ar": "نفّذ لمسة واحدة (رسالة/ردّ/لقاء) وسجّلها في evidence_events_tracker.csv.",
                "cta_en": "Take one touch (msg/reply/meeting) and log it in evidence_events_tracker.csv.",
                "today_total": today_total,
                "week_total": week_total,
                "is_estimate": True,
            }
        ]
    if week_total < 3:
        return [
            {
                "priority": "P2",
                "source": "evidence_csv",
                "title_ar": f"إيقاع الأسبوع منخفض: {week_total} حدث فقط.",
                "title_en": f"Weekly cadence low: only {week_total} event(s).",
                "cta_ar": "ارفع الإيقاع: استهدف 3+ أحداث أدلة هذا الأسبوع.",
                "cta_en": "Lift cadence: target 3+ evidence events this week.",
                "week_total": week_total,
                "is_estimate": True,
            }
        ]
    return []


def _pdpl_item() -> list[dict[str, Any]]:
    payload = analyze_pdpl_compliance_pass()
    verdict = str(payload.get("verdict") or "OPEN").upper()
    if verdict == "PASS":
        return []
    done = int(payload.get("done") or 0)
    total = int(payload.get("total") or 0)
    remaining = max(0, total - done)
    return [
        {
            "priority": "P0",
            "source": "pdpl_compliance",
            "title_ar": f"PDPL مفتوح: {remaining}/{total} بند متبقّي.",
            "title_en": f"PDPL open: {remaining}/{total} item(s) remaining.",
            "cta_ar": "افتح founder_pdpl_compliance_pass.yaml وأغلق العناصر مع مراجعة قانونية.",
            "cta_en": "Open founder_pdpl_compliance_pass.yaml and close items with legal review.",
            "done": done,
            "total": total,
            "verdict": verdict,
            "legal_review_required": True,
        }
    ]


def _first_paid_item() -> list[dict[str, Any]]:
    payload = analyze_first_paid_diagnostic()
    verdict = str(payload.get("verdict") or "OPEN").upper()
    if verdict == "CLOSED":
        return []
    return [
        {
            "priority": "P0",
            "source": "first_paid_tracker",
            "title_ar": "Article 13: أول Diagnostic مدفوع غير مغلق.",
            "title_en": "Article 13: first paid Diagnostic not yet closed.",
            "cta_ar": "سجّل payment_received + proof_pack_delivered + حدّث KPI من CRM الحقيقي.",
            "cta_en": "Record payment_received + proof_pack_delivered + sync KPI from real CRM.",
            "verdict": verdict,
            "is_estimate": True,
        }
    ]


def _plan_wiring_item() -> list[dict[str, Any]]:
    payload = strongest_plan_status()
    if payload.get("ok"):
        return []
    missing = list(payload.get("missing_paths") or [])
    if not missing:
        # OK is false but no missing paths — likely task count gap.
        return [
            {
                "priority": "P2",
                "source": "strongest_plan",
                "title_ar": (
                    f"أقوى خطة ناقصة مهام: {payload.get('task_count')}/"
                    f"{payload.get('min_task_count')}"
                ),
                "title_en": (
                    f"Strongest plan task gap: {payload.get('task_count')}/"
                    f"{payload.get('min_task_count')}"
                ),
                "cta_ar": "أكمل المهام المفقودة في founder_strongest_plan_checklist.yaml.",
                "cta_en": "Add missing tasks to founder_strongest_plan_checklist.yaml.",
            }
        ]
    return [
        {
            "priority": "P1",
            "source": "strongest_plan",
            "title_ar": f"أقوى خطة: {len(missing)} مسار ناقص.",
            "title_en": f"Strongest plan: {len(missing)} missing path(s).",
            "cta_ar": "أنشئ المسارات أو حدّث الـ checklist لتطابق الواقع.",
            "cta_en": "Create the paths or update the checklist to match reality.",
            "missing_paths_sample": missing[:5],
        }
    ]


def build_action_inbox(
    *,
    stale_hours: int = 24,
    limit: int = 50,
    evidence_rows: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Return prioritized founder action inbox snapshot.

    Args:
      stale_hours: threshold for stale-lead detection.
      limit: cap on returned items (default 50).
      evidence_rows: optional pre-loaded rows for testing.
    """
    rows = evidence_rows if evidence_rows is not None else load_evidence_rows()

    items: list[dict[str, Any]] = []
    items.extend(_approval_items())
    items.extend(_stale_lead_items(stale_hours=stale_hours))
    items.extend(_evidence_gap_item(rows))
    items.extend(_pdpl_item())
    items.extend(_first_paid_item())
    items.extend(_plan_wiring_item())

    # Sort by priority then by creation/age where present.
    items.sort(
        key=lambda x: (
            _PRIORITY_RANK.get(x.get("priority", "P3"), 9),
            -(int(x.get("age_hours") or 0)),
        )
    )

    truncated = items[: max(1, min(limit, 200))]

    by_priority: dict[str, int] = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    by_source: dict[str, int] = {}
    for it in items:
        by_priority[it.get("priority", "P3")] = by_priority.get(it.get("priority", "P3"), 0) + 1
        src = it.get("source", "?")
        by_source[src] = by_source.get(src, 0) + 1

    p0 = by_priority.get("P0", 0)
    p1 = by_priority.get("P1", 0)
    if p0 > 0:
        verdict = "BLOCKED"
        summary_ar = f"يوجد {p0} عنصر P0 يحجب التوسع — أغلقه أولاً."
        summary_en = f"{p0} P0 item(s) block expansion — close first."
    elif p1 > 0:
        verdict = "ACTIVE_DAY"
        summary_ar = f"{p1} عنصر P1 لليوم — افتح الـ Cockpit وابدأ."
        summary_en = f"{p1} P1 item(s) for today — open the cockpit and start."
    elif items:
        verdict = "MAINTENANCE"
        summary_ar = "لا توجد عناصر عاجلة — حافظ على الإيقاع وراجع الأسبوع."
        summary_en = "No urgent items — keep cadence, review the week."
    else:
        verdict = "CLEAR"
        summary_ar = "صندوق نظيف — يوم تعلّم أو دفع P2."
        summary_en = "Inbox clear — learning day or push a P2."

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "schema_version": "1.0",
        "verdict": verdict,
        "summary_ar": summary_ar,
        "summary_en": summary_en,
        "total_items": len(items),
        "by_priority": by_priority,
        "by_source": by_source,
        "items": truncated,
        "truncated": len(items) > len(truncated),
        "is_estimate": True,
        "doctrine_note_ar": (
            "للقراءة فقط (Article 4). الأعداد تقديرات تشغيلية (Article 8). "
            "تجميع بدون منطق جديد (Article 11)."
        ),
    }


def render_inbox_markdown(payload: dict[str, Any]) -> str:
    """Render Arabic+English action inbox as copy-paste markdown."""
    lines: list[str] = []
    total = payload.get("total_items", 0)
    by_pri = payload.get("by_priority") or {}
    verdict = payload.get("verdict", "?")
    lines.append(f"# 📥 Founder Action Inbox · {total} items · {verdict}")
    lines.append("")
    lines.append(f"**{payload.get('summary_ar', '')}**")
    lines.append(f"_{payload.get('summary_en', '')}_")
    lines.append("")
    lines.append(
        f"P0: {by_pri.get('P0', 0)} · P1: {by_pri.get('P1', 0)} · "
        f"P2: {by_pri.get('P2', 0)} · P3: {by_pri.get('P3', 0)}"
    )
    lines.append("")
    for i, item in enumerate(payload.get("items") or [], start=1):
        pri = item.get("priority", "P3")
        ar = item.get("title_ar", "")
        en = item.get("title_en", "")
        cta_ar = item.get("cta_ar", "")
        cta_en = item.get("cta_en", "")
        src = item.get("source", "?")
        lines.append(f"## {i}. [{pri}] {ar}")
        if en:
            lines.append(f"_{en}_")
        lines.append("")
        if cta_ar:
            lines.append(f"→ **{cta_ar}**")
        if cta_en:
            lines.append(f"  _{cta_en}_")
        lines.append(f"  · source: `{src}`")
        lines.append("")
    lines.append("---")
    lines.append("_Article 4: read-only. Article 8: counts are estimates. Article 11: compose-only._")
    return "\n".join(lines)
