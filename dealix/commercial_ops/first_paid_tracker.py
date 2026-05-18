"""First paid Diagnostic tracker — evidence-based verdict."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.evidence_csv import load_evidence_rows, real_evidence_rows


def analyze_first_paid_diagnostic() -> dict[str, Any]:
    rows = real_evidence_rows(load_evidence_rows())
    paid = any((r.get("event_type") or "").strip() == "payment_received" for r in rows)
    proof = any((r.get("event_type") or "").strip() == "proof_pack_delivered" for r in rows)
    if paid and proof:
        return {"verdict": "PASS", "note_ar": "دفع + Proof Pack مسجّلان في evidence CSV"}
    if paid:
        return {"verdict": "PARTIAL", "note_ar": "دفع مسجّل — أكمل Proof Pack"}
    return {"verdict": "PENDING", "note_ar": "لا payment_received في evidence CSV بعد"}
