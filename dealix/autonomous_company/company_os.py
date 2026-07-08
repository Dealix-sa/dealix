"""Autonomous Company OS orchestrator — runs one self-operating cycle.

Cycle:
    load durable memory -> ingest warm-lead inbox -> derive stages from evidence
    -> score & decide next-best actions -> compute KPIs & forecast
    -> render Command Room (md + html) + machine outputs -> persist memory
    -> self-verify safety.

Fully offline, deterministic, stdlib-only. No send, no charge, no secrets.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from . import command_room, decision_engine, revenue, state
from .decision_engine import DecisionResult
from .schemas import Deal, KPIs

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports" / "autonomous_company"

# Outbound flags that must never be enabled for the cycle to run.
_LIVE_FLAGS = (
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
)


@dataclass
class CycleResult:
    run_date: date
    deals: list[Deal]
    kpis: KPIs
    decision: DecisionResult
    learning: list[str]
    outputs: dict[str, str] = field(default_factory=dict)
    added_leads: int = 0

    def summary(self) -> dict[str, Any]:
        return {
            "date": self.run_date.isoformat(),
            "added_leads": self.added_leads,
            "kpis": self.kpis.to_dict(),
            "top_actions": len(self.decision.recommendations),
            "approvals_pending": len(self.decision.approvals),
            "stalled": len(self.decision.stalled),
            "outputs": self.outputs,
        }


def _safety_violations() -> list[str]:
    v = []
    for flag in _LIVE_FLAGS:
        if str(os.environ.get(flag, "false")).strip().lower() in {"1", "true", "yes", "on"}:
            v.append(f"{flag} must be false")
    mode = str(os.environ.get("OUTBOUND_MODE", "draft_only")).strip().lower()
    if mode and mode != "draft_only":
        v.append(f"OUTBOUND_MODE must be draft_only (found: {mode})")
    return v


def _learning(kpis: KPIs, decision: DecisionResult) -> list[str]:
    notes: list[str] = []
    if kpis.stalled_deals:
        notes.append(
            f"{kpis.stalled_deals} deal(s) stalled — the engine ranked their rescue "
            "actions higher this cycle."
        )
    if decision.approvals:
        notes.append(
            f"{len(decision.approvals)} draft(s) are the current bottleneck; founder "
            "approval here unblocks the most revenue."
        )
    if kpis.recognized_revenue_sar == 0 and kpis.open_pipeline_sar > 0:
        notes.append(
            "No revenue recognized yet but pipeline exists — focus on moving the "
            "highest-score deal one stage forward to the first payment_received."
        )
    if not decision.recommendations:
        notes.append(
            "Empty book — add warm, opted-in leads to the inbox to start the loop."
        )
    notes.append(
        "Next cycle rule: prioritise (closest-to-payment) then (stalled+valuable) "
        "then (highest score)."
    )
    return notes


def run_cycle(
    run_date: date | None = None,
    top_n: int = 10,
    write: bool = True,
    strict_safety: bool = True,
) -> CycleResult:
    run_date = run_date or date.today()

    violations = _safety_violations()
    if violations and strict_safety:
        raise RuntimeError("Refusing to run — unsafe outbound flags: " + "; ".join(violations))

    st = state.load_state()
    deals = state.load_deals(st)
    deals, added = state.ingest_inbox(deals, run_date)

    decision = decision_engine.decide(deals, run_date, top_n=top_n)
    kpis = revenue.compute_kpis(deals, run_date)
    learning = _learning(kpis, decision)

    result = CycleResult(
        run_date=run_date,
        deals=deals,
        kpis=kpis,
        decision=decision,
        learning=learning,
        added_leads=added,
    )

    if write:
        history = st.get("history", [])
        history.append(
            {
                "date": run_date.isoformat(),
                "recognized_revenue_sar": kpis.recognized_revenue_sar,
                "active_deals": kpis.active_deals,
                "approvals_pending": len(decision.approvals),
            }
        )
        state.save_state(deals, history)
        result.outputs = _write_outputs(result)
    return result


def _write_outputs(result: CycleResult) -> dict[str, str]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    d = result.run_date.isoformat()

    md = command_room.render_markdown(result.run_date, result.kpis, result.decision, result.learning)
    html_page = command_room.render_html(result.run_date, result.kpis, result.decision)

    dated_md = REPORTS_DIR / f"{d}_command_room.md"
    latest_md = REPORTS_DIR / "command_room.md"
    latest_html = REPORTS_DIR / "command_room.html"
    actions_json = REPORTS_DIR / f"{d}_actions.json"
    kpis_json = REPORTS_DIR / "kpis.json"

    dated_md.write_text(md, encoding="utf-8")
    latest_md.write_text(md, encoding="utf-8")
    latest_html.write_text(html_page, encoding="utf-8")
    actions_json.write_text(
        json.dumps(
            {
                "date": d,
                "recommendations": [r.to_dict() for r in result.decision.recommendations],
                "approvals": [r.to_dict() for r in result.decision.approvals],
                "stalled": [r.to_dict() for r in result.decision.stalled],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    kpis_json.write_text(json.dumps(result.kpis.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def rel(p: Path) -> str:
        return str(p.relative_to(ROOT))

    return {
        "command_room_html": rel(latest_html),
        "command_room_md": rel(latest_md),
        "dated_md": rel(dated_md),
        "actions_json": rel(actions_json),
        "kpis_json": rel(kpis_json),
    }
