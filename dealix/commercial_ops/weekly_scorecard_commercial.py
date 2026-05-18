"""Auto-fill commercial weekly scorecard from evidence CSV (no invented CRM numbers)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    is_placeholder_evidence_row,
    load_evidence_rows,
)
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic


KPI_TYPES = [
    "message_sent_manual",
    "reply_received",
    "demo_booked",
    "scope_requested",
    "invoice_sent",
    "payment_received",
    "proof_pack_delivered",
    "partner_intro_created",
]


def build_weekly_scorecard(*, week_end: datetime | None = None) -> dict[str, Any]:
    end = (week_end or datetime.now(UTC)).date()
    start = end - timedelta(days=6)
    rows = load_evidence_rows()

    week_counts: dict[str, int] = {k: 0 for k in KPI_TYPES}
    pilots_proof = 0
    for row in rows:
        if is_placeholder_evidence_row(row):
            continue
        raw = (row.get("event_date") or "").strip()[:10]
        try:
            ed = datetime.fromisoformat(raw).date() if raw else None
        except ValueError:
            ed = None
        if ed is None or not (start <= ed <= end):
            continue
        et = (row.get("event_type") or "").strip()
        if et in week_counts:
            week_counts[et] += 1
        if et == "proof_pack_delivered":
            pilots_proof += 1

    paid = analyze_first_paid_diagnostic()
    evidence = count_evidence_events(rows, on_date=end, exclude_placeholders=True)

    demo = week_counts.get("demo_booked", 0)
    invoice = week_counts.get("invoice_sent", 0)
    conversion = f"{(invoice / demo * 100):.0f}%" if demo else "n/a"

    return {
        "week_end": end.isoformat(),
        "week_start": start.isoformat(),
        "generated_at": datetime.now(UTC).isoformat(),
        "kpi_week": week_counts,
        "north_star": {
            "pilots_active_note": "املأ يدوياً من التسليم الجاري",
            "proof_packs_delivered_week": pilots_proof,
        },
        "conversion_demo_to_invoice": conversion,
        "first_paid_verdict": paid["verdict"],
        "evidence_today_total": evidence["today_total"],
        "template_doc": "docs/commercial/operations/COMMERCIAL_WEEKLY_SCORECARD_AR.md",
    }
