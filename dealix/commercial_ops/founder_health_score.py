"""Founder Health Score — single 0-100 number from real signals.

نقطة صحة المؤسس — رقم واحد 0-100 من إشارات حقيقية.

Compose-only (Article 11). Reads existing modules:
  - evidence_csv.count_evidence_events
  - founder_strongest_plan.strongest_plan_status
  - founder_comprehensive_plan.analyze_pdpl_compliance_pass
  - first_paid_tracker.analyze_first_paid_diagnostic
  - auto_client_acquisition.lead_inbox (defensive — optional)

Honors hard rules:
  - Article 4: read-only, no auto-sends, no external calls
  - Article 8: counts carry is_estimate=True where they're operational
    snapshots (CSV / JSONL), not authoritative finance
  - Article 11: no new business logic — only weighted aggregation
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_pdpl_compliance_pass,
)
from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status

# Sub-score weights (sum to 100). Tuned so evidence flow and paid traction
# matter most — that's what the doctrine cares about (Article 13).
DEFAULT_WEIGHTS: dict[str, int] = {
    "evidence_flow": 25,
    "paid_traction": 25,
    "compliance": 20,
    "plan_wiring": 15,
    "inbox_freshness": 15,
}

# Evidence types that count as real founder activity for the week.
ACTIVE_EVIDENCE_TYPES: frozenset[str] = frozenset(
    {
        "message_sent_manual",
        "reply_received",
        "demo_booked",
        "scope_requested",
        "invoice_sent",
        "payment_received",
        "proof_pack_delivered",
    }
)


def _evidence_flow_score(rows: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Score based on weekly evidence event count + diversity.

    - 0 events this week → 0
    - 1-2 events → 30 (founder is active but slow)
    - 3-5 events → 60 (consistent)
    - 6-10 events → 85 (strong cadence)
    - 11+ events → 100 (excellent)
    - +5 bonus if 3+ different event types this week (diversity)
    """
    counts = count_evidence_events(rows, exclude_placeholders=True)
    week_total = int(counts.get("week_total") or 0)
    by_type = counts.get("week_by_type") or {}
    active_types = sum(
        1 for k, v in by_type.items() if k in ACTIVE_EVIDENCE_TYPES and int(v) > 0
    )

    if week_total >= 11:
        base = 100
    elif week_total >= 6:
        base = 85
    elif week_total >= 3:
        base = 60
    elif week_total >= 1:
        base = 30
    else:
        base = 0

    diversity_bonus = 5 if active_types >= 3 else 0
    score = min(100, base + diversity_bonus)

    actions: list[dict[str, str]] = []
    if week_total == 0:
        actions.append(
            {
                "ar": "سجّل أول حدث أدلة لهذا الأسبوع (لقاء أو رسالة أو ردّ).",
                "en": "Log this week's first evidence event (meeting/message/reply).",
            }
        )
    elif week_total < 3:
        actions.append(
            {
                "ar": "ارفع الإيقاع: استهدف 3+ أحداث أدلة هذا الأسبوع.",
                "en": "Lift cadence: target 3+ evidence events this week.",
            }
        )

    return {
        "score": score,
        "week_total": week_total,
        "active_types_count": active_types,
        "week_by_type": dict(by_type),
        "is_estimate": True,
        "actions": actions,
    }


def _paid_traction_score() -> dict[str, Any]:
    """Score from first-paid Diagnostic tracker — Article 13 milestone."""
    payload = analyze_first_paid_diagnostic()
    verdict = str(payload.get("verdict") or "OPEN").upper()
    # Map qualitative verdict to numeric.
    score_map = {
        "CLOSED": 100,
        "IN_PROGRESS": 50,
        "OPEN": 0,
    }
    score = score_map.get(verdict, 0)

    actions: list[dict[str, str]] = []
    if verdict != "CLOSED":
        actions.append(
            {
                "ar": "أغلق أول Diagnostic مدفوع (Article 13) — سجّل payment_received + proof_pack_delivered.",
                "en": "Close first paid Diagnostic (Article 13) — record payment_received + proof_pack_delivered.",
            }
        )

    return {
        "score": score,
        "verdict": verdict,
        "is_estimate": True,
        "doc": payload.get("dod_doc") or "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
        "actions": actions,
    }


def _compliance_score() -> dict[str, Any]:
    """Score from PDPL compliance pass (operational items, not legal sign-off)."""
    payload = analyze_pdpl_compliance_pass()
    verdict = str(payload.get("verdict") or "OPEN").upper()
    done = int(payload.get("done") or 0)
    total = int(payload.get("total") or 0)

    if verdict == "PASS":
        score = 100
    elif total > 0:
        # Linear from 0 to 90 (cap at 90 unless full PASS).
        score = min(90, int((done / total) * 90))
    else:
        score = 0

    actions: list[dict[str, str]] = []
    if verdict != "PASS":
        remaining = max(0, total - done)
        actions.append(
            {
                "ar": f"أغلق بنود PDPL المتبقية ({remaining}/{total or '?'}) — مراجعة قانونية مطلوبة.",
                "en": f"Close remaining PDPL items ({remaining}/{total or '?'}) — legal review required.",
            }
        )

    return {
        "score": score,
        "verdict": verdict,
        "done": done,
        "total": total,
        "legal_review_required": True,
        "actions": actions,
    }


def _plan_wiring_score() -> dict[str, Any]:
    """Score from strongest-plan wiring — does the plan still resolve to real paths?"""
    payload = strongest_plan_status()
    ok = bool(payload.get("ok"))
    missing = payload.get("missing_paths") or []
    task_count = int(payload.get("task_count") or 0)
    min_tasks = int(payload.get("min_task_count") or 0)

    if ok:
        score = 100
    elif task_count >= min_tasks and not missing:
        score = 85
    elif missing and len(missing) <= 3:
        score = 60
    elif missing and len(missing) <= 8:
        score = 40
    else:
        score = 10

    actions: list[dict[str, str]] = []
    if missing:
        actions.append(
            {
                "ar": f"أصلح wiring أقوى خطة: {len(missing)} مسار ناقص.",
                "en": f"Fix strongest-plan wiring: {len(missing)} missing path(s).",
            }
        )
    if task_count < min_tasks:
        actions.append(
            {
                "ar": f"أقوى خطة: {task_count}/{min_tasks} مهمة — أكمل بقية المهام.",
                "en": f"Strongest plan: {task_count}/{min_tasks} tasks — finish the remainder.",
            }
        )

    return {
        "score": score,
        "ok": ok,
        "task_count": task_count,
        "min_task_count": min_tasks,
        "missing_paths_count": len(missing),
        "missing_paths_sample": list(missing)[:5],
        "actions": actions,
    }


def _inbox_freshness_score(stale_hours: int = 24) -> dict[str, Any]:
    """Score from lead inbox — leads waiting too long lose points.

    Defensive: lead_inbox is optional; missing module → neutral 80.
    """
    try:
        from auto_client_acquisition import lead_inbox  # type: ignore
    except Exception:  # noqa: BLE001
        return {
            "score": 80,
            "note": "lead_inbox_unavailable",
            "stale_count": 0,
            "is_estimate": True,
            "actions": [],
        }

    leads = lead_inbox.list_leads(limit=500) if hasattr(lead_inbox, "list_leads") else []
    if not leads:
        return {
            "score": 100,
            "total_leads": 0,
            "stale_count": 0,
            "is_estimate": True,
            "actions": [],
        }

    cutoff = datetime.now(UTC) - timedelta(hours=stale_hours)
    stale = 0
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
        if created < cutoff:
            stale += 1

    total = len(leads)
    # No stale → 100. 1 stale → 80. 5+ stale → 0.
    if stale == 0:
        score = 100
    elif stale <= 1:
        score = 80
    elif stale <= 3:
        score = 50
    elif stale <= 5:
        score = 20
    else:
        score = 0

    actions: list[dict[str, str]] = []
    if stale > 0:
        actions.append(
            {
                "ar": f"رد على {stale} lead متروك > {stale_hours}h (مسودة فقط، لا إرسال آلي).",
                "en": f"Respond to {stale} lead(s) waiting > {stale_hours}h (draft only — no auto-send).",
            }
        )

    return {
        "score": score,
        "total_leads": total,
        "stale_count": stale,
        "stale_hours_threshold": stale_hours,
        "is_estimate": True,
        "actions": actions,
    }


def _verdict_from_score(score: int) -> dict[str, str]:
    if score >= 80:
        return {
            "level": "HEALTHY",
            "summary_ar": "صحة عمليات قوية — استمر بالإيقاع الحالي.",
            "summary_en": "Strong operating health — keep the cadence.",
        }
    if score >= 50:
        return {
            "level": "CAUTION",
            "summary_ar": "أداء مقبول — أغلق البوابات المتبقية وارفع الإيقاع.",
            "summary_en": "Acceptable — close remaining gates and lift cadence.",
        }
    return {
        "level": "ACTION_NEEDED",
        "summary_ar": "أوقف التوسع — افتح يوم أدلة وأغلق بوابة 0→1 أولاً.",
        "summary_en": "Pause expansion — run an evidence day and close the 0→1 gate first.",
    }


def compute_founder_health_score(
    *,
    weights: dict[str, int] | None = None,
    evidence_rows: list[dict[str, str]] | None = None,
    stale_hours: int = 24,
) -> dict[str, Any]:
    """Return the consolidated founder health snapshot.

    Args:
      weights: optional override for sub-score weights (must sum to 100).
      evidence_rows: optional pre-loaded evidence rows (testing).
      stale_hours: threshold for inbox staleness.

    Returns:
      Dict with overall_score, verdict, sub_scores, top_actions, generated_at.
    """
    rows = evidence_rows if evidence_rows is not None else load_evidence_rows()
    w = dict(weights) if weights else dict(DEFAULT_WEIGHTS)
    if sum(w.values()) != 100:
        # Normalize defensively.
        total = sum(w.values()) or 1
        w = {k: int(round(v * 100 / total)) for k, v in w.items()}

    sub: dict[str, dict[str, Any]] = {
        "evidence_flow": _evidence_flow_score(rows),
        "paid_traction": _paid_traction_score(),
        "compliance": _compliance_score(),
        "plan_wiring": _plan_wiring_score(),
        "inbox_freshness": _inbox_freshness_score(stale_hours=stale_hours),
    }

    weighted = 0.0
    for key, weight in w.items():
        s = sub.get(key) or {}
        weighted += float(s.get("score") or 0) * (weight / 100.0)
    overall = int(round(weighted))
    overall = max(0, min(100, overall))

    verdict = _verdict_from_score(overall)

    # Collect top actions in priority order: paid > compliance > evidence > plan > inbox.
    action_priority = [
        "paid_traction",
        "compliance",
        "evidence_flow",
        "plan_wiring",
        "inbox_freshness",
    ]
    top_actions: list[dict[str, str]] = []
    for key in action_priority:
        for act in (sub.get(key) or {}).get("actions") or []:
            if act not in top_actions:
                top_actions.append(act)
            if len(top_actions) >= 5:
                break
        if len(top_actions) >= 5:
            break

    return {
        "overall_score": overall,
        "verdict": verdict["level"],
        "summary_ar": verdict["summary_ar"],
        "summary_en": verdict["summary_en"],
        "weights": w,
        "sub_scores": {k: v.get("score") for k, v in sub.items()},
        "details": sub,
        "top_actions": top_actions,
        "generated_at": datetime.now(UTC).isoformat(),
        "schema_version": "1.0",
        "is_estimate": True,
        "doctrine_note_ar": (
            "كل الأعداد تقديرات تشغيلية (Article 8). لا إرسال خارجي (Article 4). "
            "تجميع بدون منطق أعمال جديد (Article 11)."
        ),
    }


def render_health_brief_markdown(payload: dict[str, Any]) -> str:
    """Render a copy-paste-friendly Arabic+English brief."""
    overall = payload.get("overall_score", 0)
    verdict = payload.get("verdict", "?")
    summary_ar = payload.get("summary_ar", "")
    summary_en = payload.get("summary_en", "")
    sub = payload.get("sub_scores") or {}
    actions = payload.get("top_actions") or []
    ts = payload.get("generated_at", "")

    lines: list[str] = []
    lines.append(f"# 🩺 Dealix Founder Health · {overall}/100 · {verdict}")
    lines.append("")
    lines.append(f"**{summary_ar}**")
    lines.append(f"_{summary_en}_")
    lines.append("")
    lines.append("## Sub-scores")
    lines.append("")
    lines.append("| الإشارة / Signal | النقاط / Score |")
    lines.append("|---|---:|")
    label_ar = {
        "evidence_flow": "تدفق الأدلة (Evidence flow)",
        "paid_traction": "أول مدفوع (Paid traction)",
        "compliance": "امتثال PDPL (Compliance)",
        "plan_wiring": "ربط أقوى خطة (Plan wiring)",
        "inbox_freshness": "صندوق الـ Leads (Inbox freshness)",
    }
    for k, v in sub.items():
        lines.append(f"| {label_ar.get(k, k)} | {v}/100 |")
    lines.append("")
    if actions:
        lines.append("## Top actions / أهم الإجراءات")
        lines.append("")
        for i, act in enumerate(actions, start=1):
            ar = act.get("ar", "")
            en = act.get("en", "")
            lines.append(f"{i}. **{ar}**")
            if en:
                lines.append(f"   _{en}_")
        lines.append("")
    lines.append("---")
    lines.append(
        "_Article 4: never auto-send. Article 8: counts are estimates. "
        "Article 11: compose-only — no new business logic._"
    )
    lines.append(f"_Generated: {ts}_")
    return "\n".join(lines)
