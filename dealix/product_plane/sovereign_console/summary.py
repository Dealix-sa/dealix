"""
Sovereign Console summary — يجمع كل ما يحتاجه المؤسس في شاشة واحدة:
    - الأفعال المطلوبة (approvals pending)
    - الفعل التالي الأقوى (recommendation)
    - الأخطار النشطة (kill switches tripped + control failures)
    - الـ verified revenue آخر 30 يوم
    - القرارات المعلَّقة
"""

from __future__ import annotations

import dataclasses
from typing import Any

from ...hermes.control_plane.approval_gate import ApprovalGate
from ...hermes.control_plane.kill_switch import KillSwitch
from ...hermes.intelligence_plane.recommendations import RecommendationEngine
from ...hermes.money.revenue_events import RevenueEventLog
from ...hermes.money.revenue_verification import RevenueVerifier


def build_summary(
    *,
    approval_gate: ApprovalGate,
    kill_switch: KillSwitch,
    recommendations: RecommendationEngine,
    revenue_log: RevenueEventLog,
    verifier: RevenueVerifier,
) -> dict[str, Any]:
    pending = approval_gate.list_pending()
    tripped = kill_switch.all_tripped()
    next_actions = recommendations.best_next_actions(5)
    verified_revenue_sar = 0
    for event in revenue_log.all():
        result = verifier.verify(event)
        if result.accepted:
            verified_revenue_sar += event.amount_sar

    return {
        "actions_required": [
            {
                "ticket_id": t.ticket_id,
                "intent": t.intent,
                "approver_role": t.approver_role,
                "sovereignty_level": t.sovereignty_level.value,
                "summary": t.summary,
            }
            for t in pending
        ],
        "active_risks": [
            dataclasses.asdict(k) for k in tripped
        ],
        "best_next_actions": [
            {
                "title": r.title,
                "rationale": r.rationale,
                "score": r.score,
                "suggested_intent": r.suggested_intent,
                "payload": r.payload,
            }
            for r in next_actions
        ],
        "money": {
            "verified_revenue_sar": verified_revenue_sar,
            "event_count": len(revenue_log.all()),
        },
    }


__all__ = ["build_summary"]
