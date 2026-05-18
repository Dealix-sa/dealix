"""First paid Diagnostic tracker — evidence-based verdict."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.evidence_csv import load_evidence_rows, real_evidence_rows
from dealix.commercial_ops.paths import REPO_ROOT

EVIDENCE = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
DOD_DOC = REPO_ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"


def analyze_first_paid_diagnostic() -> dict[str, Any]:
    events = load_evidence_rows()
    rows = real_evidence_rows(events)
    paid_n = sum(1 for r in rows if (r.get("event_type") or "").strip() == "payment_received")
    proof_n = sum(
        1 for r in rows if (r.get("event_type") or "").strip() == "proof_pack_delivered"
    )
    if paid_n and proof_n:
        verdict = "CLOSED"
        note_ar = "دفع + Proof Pack مسجّلان في evidence CSV"
    elif paid_n or proof_n:
        verdict = "IN_PROGRESS"
        note_ar = "دفع مسجّل — أكمل Proof Pack" if paid_n else "Proof بدون دفع — راجع SOP"
    else:
        verdict = "PIPELINE_OPEN"
        note_ar = "لا payment_received في evidence CSV بعد"

    return {
        "verdict": verdict,
        "note_ar": note_ar,
        "evidence_path": str(EVIDENCE.relative_to(REPO_ROOT)).replace("\\", "/"),
        "dod_doc": str(DOD_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
        "total_events": len(events),
        "real_company_events": len(rows),
        "payment_received_real": paid_n,
        "proof_pack_delivered_real": proof_n,
        "first_close_ready": bool(paid_n and proof_n),
        "crm_kpi_pending": True,
    }
