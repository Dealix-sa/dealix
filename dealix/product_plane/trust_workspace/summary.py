"""
Trust Workspace summary — يخدم الشاشة التي تجاوب: "أي control انتُهك؟ أي
agent/tool/workflow متعطّل؟ أي MCP server يحتاج مراجعة؟"
"""

from __future__ import annotations

import dataclasses
from typing import Any

from ...hermes.control_plane.audit_gate import AuditGate
from ...hermes.control_plane.kill_switch import KillSwitch
from ...hermes.trust.controls import ControlLibrary


def build_summary(
    *,
    control_library: ControlLibrary,
    kill_switch: KillSwitch,
    audit_gate: AuditGate,
    ctx_for_controls: dict[str, Any] | None = None,
    recent_request_ids: list[str] | None = None,
) -> dict[str, Any]:
    verdicts = control_library.evaluate_all(ctx_for_controls or {})
    failures = [v for v in verdicts if not v.passed]

    audit_trail: list[dict[str, Any]] = []
    for req_id in recent_request_ids or []:
        for evt in audit_gate.trace(req_id):
            audit_trail.append(
                {
                    "request_id": evt.request_id,
                    "stage": evt.stage,
                    "actor_id": evt.actor_id,
                    "outcome": evt.outcome,
                    "at": evt.created_at.isoformat(),
                    "summary": evt.payload_summary,
                }
            )

    return {
        "controls": {
            "total": len(verdicts),
            "failing": len(failures),
            "failures": [dataclasses.asdict(v) for v in failures],
        },
        "kill_switches": [dataclasses.asdict(k) for k in kill_switch.all_tripped()],
        "audit_trail": audit_trail,
    }


__all__ = ["build_summary"]
