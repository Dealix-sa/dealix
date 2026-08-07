#!/usr/bin/env python3
"""Generate the WhatsApp Client OS founder ops reports from the JSONL ledgers.

Writes three markdown reports under ``reports/whatsapp/``:
- WHATSAPP_SESSION_REVIEW.md     — sessions by stage + recent activity
- WHATSAPP_ACTION_QUEUE.md       — cards + handoffs awaiting human review
- WHATSAPP_CONVERSION_METRICS.md — the funnel/conversion metrics

Reads only the live ledgers (no invented numbers). With empty ledgers the
reports render the structure + zeros + a note. Run from repo root:

    python3 scripts/whatsapp_client_os_report.py
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.whatsapp_client_os import client_profile_store as store
from auto_client_acquisition.whatsapp_client_os.metrics import compute_metrics

_OUT = _REPO_ROOT / "reports" / "whatsapp"
_HEADER = (
    "> مُولّد آليًا بواسطة `scripts/whatsapp_client_os_report.py` — لا تُحرّر يدويًا.\n"
    f"> آخر تحديث: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}\n"
)


def _session_review() -> str:
    sessions = store.list_sessions(limit=500)
    lines = [
        "# مراجعة جلسات WhatsApp Client OS",
        "",
        _HEADER,
        "",
        f"إجمالي الجلسات: **{len(sessions)}**",
        "",
    ]
    if not sessions:
        lines.append("_لا توجد جلسات بعد — تُنشأ عبر `POST /api/v1/whatsapp-client-os/message`._")
        return "\n".join(lines)
    lines += [
        "| الجلسة | الشركة | المرحلة | الصلاحية | الرسائل | تحويل بشري |",
        "|---|---|---|---|---|---|",
    ]
    for s in sessions[:100]:
        lines.append(
            f"| `{s.session_id}` | {s.company_name or '—'} | {s.stage} | {s.permission_level} "
            f"| {s.message_count} | {'نعم' if s.handoff_requested else 'لا'} |"
        )
    return "\n".join(lines)


def _action_queue() -> str:
    cards = store.list_action_cards(limit=500)
    handoffs = store.list_handoffs(limit=500)
    lines = ["# قائمة الإجراءات — WhatsApp Client OS", "", _HEADER, ""]
    lines += [f"كروت بانتظار المراجعة: **{len(cards)}** · تحويلات بشرية: **{len(handoffs)}**", ""]
    lines += ["## الكروت", ""]
    if cards:
        lines += [
            "| النوع | العنوان | المخاطرة | يحتاج موافقة | مرجع العرض |",
            "|---|---|---|---|---|",
        ]
        for c in cards[-50:]:
            lines.append(
                f"| {c.kind} | {c.title_ar[:40]} | {c.risk} | {'نعم' if c.requires_approval else 'لا'} | {c.catalog_ref or '—'} |"
            )
    else:
        lines.append("_لا كروت في القائمة._")
    lines += ["", "## التحويلات البشرية", ""]
    if handoffs:
        lines += ["| السبب | الشركة/المعرّف | الإجراء المقترح | الأهمية |", "|---|---|---|---|"]
        for h in handoffs[-50:]:
            lines.append(
                f"| {h.reason} | `{h.client_handle}` | {h.suggested_action_ar} | {h.urgency} |"
            )
    else:
        lines.append("_لا تحويلات بشرية._")
    return "\n".join(lines)


def _conversion_metrics() -> str:
    m = compute_metrics()
    lines = ["# مقاييس التحويل — WhatsApp Client OS", "", _HEADER, ""]
    rows = [
        ("جلسات جديدة", m["new_sessions"]),
        ("تقييمات بدأت", m["assessments_started"]),
        ("تقييمات اكتملت", m["assessments_completed"]),
        ("معدل إكمال التقييم", m["assessment_completion_rate"]),
        ("طلبات صلاحيات", m["permission_requests"]),
        ("معدل اعتماد الصلاحيات", m["permission_approval_rate"]),
        ("معدل طلب العروض", m["proposal_request_rate"]),
        ("معدل تحويل الدفع", m["payment_handoff_rate"]),
        ("تحويلات بشرية", m["human_handoff_count"]),
        ("معدل التحويل البشري", m["human_handoff_rate"]),
    ]
    lines += ["| المقياس | القيمة |", "|---|---|"]
    lines += [f"| {label} | {val} |" for label, val in rows]
    if m.get("recommended_offers"):
        lines += ["", "## العروض الموصى بها", "", "| العرض | عدد |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in m["recommended_offers"].items()]
    if m.get("stages"):
        lines += ["", "## المراحل", "", "| المرحلة | عدد |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in m["stages"].items()]
    return "\n".join(lines)


def main() -> int:
    _OUT.mkdir(parents=True, exist_ok=True)
    (_OUT / "WHATSAPP_SESSION_REVIEW.md").write_text(_session_review() + "\n", encoding="utf-8")
    (_OUT / "WHATSAPP_ACTION_QUEUE.md").write_text(_action_queue() + "\n", encoding="utf-8")
    (_OUT / "WHATSAPP_CONVERSION_METRICS.md").write_text(
        _conversion_metrics() + "\n", encoding="utf-8"
    )
    for name in (
        "WHATSAPP_SESSION_REVIEW.md",
        "WHATSAPP_ACTION_QUEUE.md",
        "WHATSAPP_CONVERSION_METRICS.md",
    ):
        print(f"wrote reports/whatsapp/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
