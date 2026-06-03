#!/usr/bin/env python3
"""Generate WhatsApp Client OS founder reports from the JSONL stores.

Reads the (gitignored, runtime) ``data/whatsapp/*.jsonl`` stores and renders
bilingual markdown into ``reports/whatsapp/``. Counts reflect only recorded
events — no invented funnel numbers. Run from the repo root:

    python3 scripts/generate_whatsapp_reports.py
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.whatsapp_client_os import metrics  # noqa: E402
from auto_client_acquisition.whatsapp_client_os import session_store as store  # noqa: E402

_OUT_DIR = _REPO_ROOT / "reports" / "whatsapp"
_DISCLAIMER = "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"


def _write(name: str, body: str) -> Path:
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = _OUT_DIR / name
    stamp = datetime.now(UTC).isoformat(timespec="seconds")
    path.write_text(f"{body}\n\n> Generated {stamp}\n\n_{_DISCLAIMER}_\n", encoding="utf-8")
    return path


def _metrics_md() -> str:
    m = metrics.compute_metrics()
    lines = [
        "# WhatsApp Metrics — مؤشرات واتساب",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    for key in (
        "new_sessions",
        "inbound_messages",
        "completed_scans",
        "recommendations_generated",
        "action_cards",
        "proposal_requests",
        "permission_cards",
        "payment_handoffs",
        "support_tickets",
        "human_handoffs",
    ):
        lines.append(f"| {key} | {m.get(key, 0)} |")
    return "\n".join(lines)


def _sessions_md() -> str:
    sessions = store.list_sessions()
    lines = [
        "# WhatsApp Session Review — مراجعة الجلسات",
        "",
        f"Total sessions: {len(sessions)}",
        "",
        "| Session | Flow | Permission | Turns | Handoff |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in sessions:
        lines.append(
            f"| {s.session_id} | {s.current_flow} | {s.permission_level} | "
            f"{s.turn_count} | {'yes' if s.handoff_open else 'no'} |"
        )
    return "\n".join(lines)


def _action_queue_md() -> str:
    cards = store.list_cards()
    lines = [
        "# WhatsApp Action Queue — قائمة البطاقات",
        "",
        f"Total cards: {len(cards)}",
        "",
        "| Card | Kind | Risk | Governance |",
        "| --- | --- | --- | --- |",
    ]
    for c in cards:
        lines.append(
            f"| {c.get('card_id', '')} | {c.get('kind', '')} | "
            f"{c.get('risk', '')} | {c.get('governance_decision', '')} |"
        )
    return "\n".join(lines)


def _handoff_queue_md() -> str:
    sessions = [s for s in store.list_sessions() if s.handoff_open]
    lines = [
        "# WhatsApp Handoff Queue — قائمة التصعيد البشري",
        "",
        f"Open handoffs: {len(sessions)}",
        "",
        "| Session | Flow | Last intent |",
        "| --- | --- | --- |",
    ]
    for s in sessions:
        lines.append(f"| {s.session_id} | {s.current_flow} | {s.last_intent} |")
    return "\n".join(lines)


def _assessments_md() -> str:
    rows = store.list_assessments()
    lines = [
        "# WhatsApp Client Assessments — تقييمات العملاء",
        "",
        f"Total assessments: {len(rows)}",
        "",
        "| Assessment | Readiness | Risk | Recommended offer |",
        "| --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('assessment_id', '')} | {r.get('revenue_readiness', 0)} | "
            f"{r.get('risk', '')} | {r.get('recommended_offer_id', '')} |"
        )
    return "\n".join(lines)


def main() -> int:
    written = [
        _write("WHATSAPP_METRICS.md", _metrics_md()),
        _write("WHATSAPP_SESSION_REVIEW.md", _sessions_md()),
        _write("WHATSAPP_ACTION_QUEUE.md", _action_queue_md()),
        _write("WHATSAPP_HANDOFF_QUEUE.md", _handoff_queue_md()),
        _write("WHATSAPP_CLIENT_ASSESSMENTS.md", _assessments_md()),
    ]
    for p in written:
        print(f"wrote {p.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
