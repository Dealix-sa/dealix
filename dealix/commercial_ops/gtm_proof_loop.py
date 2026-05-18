"""GTM proof loop — evidence + weekly decision + first paid."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import FOUNDER_WEEKLY_ONE_DECISION_YAML, REPO_ROOT


def build_gtm_proof_loop_snapshot() -> dict[str, Any]:
    rows = load_evidence_rows()
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    counts = count_evidence_events(rows, exclude_placeholders=True)
    events_today = int(counts.get("today_total") or 0)

    config: dict[str, Any] = {}
    if FOUNDER_WEEKLY_ONE_DECISION_YAML.is_file():
        config = yaml.safe_load(FOUNDER_WEEKLY_ONE_DECISION_YAML.read_text(encoding="utf-8")) or {}

    first_paid = analyze_first_paid_diagnostic()
    blockers: list[str] = []
    if events_today < 1:
        blockers.append("سجّل حدث أدلة واحد اليوم في evidence_events_tracker.csv")
    if not (config.get("one_decision_ar") or "").strip():
        blockers.append("املأ one_decision_ar في dealix/config/founder_weekly_one_decision.yaml")
    if first_paid.get("verdict") == "PENDING":
        blockers.append("لا payment_received بعد — ركّز على أول Diagnostic مدفوع")

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "date": today,
        "verdict": "PASS" if not blockers else "ACTION_REQUIRED",
        "evidence_today": events_today,
        "first_paid": first_paid,
        "weekly_config": config,
        "blockers_ar": blockers,
        "docs": ["docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md"],
    }
