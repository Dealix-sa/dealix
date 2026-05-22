"""Founder reality check — ground every claim in real files + real evidence.

This module exists because several prior sessions claimed engines, registries,
and routers that never landed in the repo (sovereign_registry.py,
master_orchestrator.py, M&A radar router, investor room with live ARR, a
"100 engine matrix" sweep, etc.). The founder needs a single, honest
snapshot: what is actually wired, what is correctly gated by the no-build
doctrine, and what was claimed but is missing — so today's decisions are
grounded in evidence, not narrative.

The module composes existing analyzers (`founder_comprehensive_plan`,
`first_paid_tracker`, `evidence_csv`) and adds a deterministic audit of
file existence for both real anchors and previously-claimed-but-absent
artifacts. No new state, no fake green verdicts.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.evidence_csv import (
    load_evidence_rows,
    real_evidence_rows,
)
from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_gtm_codification,
    analyze_pdpl_compliance_pass,
    analyze_phase_0_1_gate,
    analyze_weekly_one_decision,
)
from dealix.commercial_ops.paths import REPO_ROOT

# Wired anchors: files that exist today and back the founder OS.
# Each entry is (relative_path, what_it_proves_ar).
WIRED_ANCHORS: tuple[tuple[str, str], ...] = (
    (
        "dealix/commercial_ops/founder_comprehensive_plan.py",
        "محرك الخطة الشاملة + بوابة المرحلة 0–1 + قرار أسبوعي",
    ),
    (
        "dealix/commercial_ops/founder_strongest_plan.py",
        "أقوى خطة 138 مهمة (تفحص برمجياً)",
    ),
    (
        "dealix/commercial_ops/first_paid_tracker.py",
        "تتبع أول دفعة حقيقية + Proof Pack من evidence_events_tracker.csv",
    ),
    (
        "dealix/payments/moyasar.py",
        "عميل Moyasar حقيقي (HTTP Basic + Webhook secret_token)",
    ),
    (
        "dealix/revenue_ops_autopilot/orchestrator.py",
        "Revenue OS — Source → Owner → Approval → Evidence → Next Action",
    ),
    (
        "api/routers/founder.py",
        "API للمؤسس — متصل بالنواة لا بمولّد ثابت",
    ),
    (
        "api/routers/revenue_ops_autopilot.py",
        "API الـ Autopilot — استهداف وتسويق وأدلة",
    ),
    (
        "frontend/src/app/[locale]/ops/founder/page.tsx",
        "غرفة قيادة المؤسس في الواجهة",
    ),
    (
        "frontend/src/components/gtm/OpsFounderCommandCenter.tsx",
        "مكوّن غرفة القيادة — يستهلك API الحقيقي",
    ),
    (
        "docs/commercial/operations/evidence_events_tracker.csv",
        "سجل الأدلة الحقيقي (CSV) — مصدر الحقيقة للبوابة 0–1",
    ),
    (
        "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
        "الخطة التجارية الرئيسية (5 دقائق يومياً)",
    ),
    (
        "docs/commercial/FOUNDER_STRONGEST_PLAN_AR.md",
        "أقوى خطة (138 مهمة) — وثيقة + Checklist",
    ),
    (
        "scripts/founder_one_command.sh",
        "أمر واحد لتشغيل اليوم المحكوم بالكامل",
    ),
    (
        "scripts/run_founder_commercial_day.sh",
        "اليوم التجاري الصباحي (Canonical)",
    ),
    (
        "scripts/verify_dealix_commercial_go_live.sh",
        "بوابة الإطلاق التجاري الرسمية",
    ),
)

# Artifacts repeatedly claimed by past sessions but absent in the repo.
# Each entry: (path, claim_summary_ar). Verified absent at audit time.
CLAIMED_BUT_ABSENT: tuple[tuple[str, str], ...] = (
    (
        "auto_client_acquisition/sovereign_registry.py",
        "ادّعاء «100 محرك سيادي» — لم يُكتب في المستودع",
    ),
    (
        "auto_client_acquisition/master_orchestrator.py",
        "ادّعاء «العقل المدبر يعمل كـ daemon داخل main.py» — غير موجود",
    ),
    (
        "auto_client_acquisition/meta_os/autonomous_developer_agent.py",
        "ادّعاء «وكيل تطوير ذاتي يكتب الكود» — لا يوجد ملف",
    ),
    (
        "api/routers/m_and_a.py",
        "ادّعاء «رادار استحواذ M&A + LOI تلقائي» — لا راوتر",
    ),
    (
        "api/routers/moyasar_billing.py",
        "ادّعاء «راوتر فواتير Moyasar مستقل» — الدمج عبر dealix/payments/moyasar.py وحقن في raouters قائمة",
    ),
    (
        "frontend/src/app/[locale]/meta-os/page.tsx",
        "ادّعاء «شاشة Meta-OS بـ 100 محرك حي» — صفحة غير موجودة",
    ),
    (
        "frontend/src/app/[locale]/investor-room/page.tsx",
        "ادّعاء «غرفة مستثمرين ARR حي» — صفحة غير موجودة",
    ),
)


def _exists(rel_path: str) -> bool:
    return (REPO_ROOT / rel_path).exists()


def audit_wired_anchors() -> list[dict[str, Any]]:
    """Each anchor's real file existence — not a marketing claim."""
    return [
        {
            "path": rel,
            "exists": _exists(rel),
            "proves_ar": proof,
        }
        for rel, proof in WIRED_ANCHORS
    ]


def audit_claimed_but_absent() -> list[dict[str, Any]]:
    """Verify the absence (or surprise presence) of each claim. Honest both ways."""
    return [
        {
            "path": rel,
            "exists": _exists(rel),
            "claim_ar": claim,
        }
        for rel, claim in CLAIMED_BUT_ABSENT
    ]


def evidence_truth() -> dict[str, Any]:
    """Real (non-placeholder) evidence rows + by-type counts. No invention."""
    rows = load_evidence_rows()
    real = real_evidence_rows(rows)
    by_type: dict[str, int] = {}
    for r in real:
        et = (r.get("event_type") or "").strip()
        if et:
            by_type[et] = by_type.get(et, 0) + 1
    return {
        "total_rows": len(rows),
        "real_rows": len(real),
        "by_type": by_type,
        "csv_path": "docs/commercial/operations/evidence_events_tracker.csv",
    }


def next_three_honest_actions(
    *,
    phase_gate: dict[str, Any],
    weekly: dict[str, Any],
    gtm: dict[str, Any],
    pdpl: dict[str, Any],
) -> list[dict[str, str]]:
    """Three concrete actions, each tied to a gate that is currently blocking."""
    actions: list[dict[str, str]] = []

    if not phase_gate.get("gate_open"):
        blockers = phase_gate.get("blockers_ar") or []
        if blockers:
            actions.append(
                {
                    "title_ar": "افتح بوابة المرحلة 0–1",
                    "title_en": "Open the Phase 0–1 gate",
                    "do_ar": blockers[0],
                    "doc": phase_gate.get("phase_doc") or "",
                }
            )

    if (weekly.get("verdict") or "").upper() == "MISSING":
        week_id = (weekly.get("expected_week_id") or weekly.get("week_id") or "").strip()
        actions.append(
            {
                "title_ar": "أضف قرار الأسبوع",
                "title_en": "Add this week's one decision",
                "do_ar": (
                    f"py -3 scripts/founder_weekly_decision_init.py --week {week_id}"
                    if week_id
                    else "py -3 scripts/founder_weekly_decision_init.py"
                ),
                "doc": "docs/ops/FOUNDER_WEEKLY_ONE_DECISION_AR.md",
            }
        )

    gtm_verdict = (gtm.get("verdict") or "").upper()
    if gtm_verdict in {"OPEN", "IN_PROGRESS"}:
        need = max(
            0,
            int(gtm.get("target_deals") or 0) - int(gtm.get("debriefs_with_notes") or 0),
        )
        if need > 0:
            actions.append(
                {
                    "title_ar": "اكتب debrief بعد كل اجتماع",
                    "title_en": "Write a debrief after each meeting",
                    "do_ar": (
                        f'py -3 scripts/founder_meeting_debrief_init.py --company "..."  '
                        f"(باقي {need} debrief للوصول للهدف)"
                    ),
                    "doc": "docs/commercial/operations/FOUNDER_GTM_CODIFICATION_AR.md",
                }
            )

    pdpl_verdict = (pdpl.get("verdict") or "").upper()
    if pdpl_verdict in {"OPEN", "IN_PROGRESS", "EMPTY", "MISSING_CONFIG"}:
        actions.append(
            {
                "title_ar": "أغلق بنود PDPL pass التشغيلية",
                "title_en": "Close PDPL operational pass items",
                "do_ar": "حدّث docs/commercial/operations/founder_pdpl_compliance_pass.yaml",
                "doc": "docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md",
            }
        )

    return actions[:3]


def build_reality_check() -> dict[str, Any]:
    """Single composite snapshot for the founder."""
    phase_gate = analyze_phase_0_1_gate()
    weekly = analyze_weekly_one_decision()
    gtm = analyze_gtm_codification()
    pdpl = analyze_pdpl_compliance_pass()
    wired = audit_wired_anchors()
    absent = audit_claimed_but_absent()
    evidence = evidence_truth()

    wired_present = sum(1 for w in wired if w["exists"])
    surprise_present = [a for a in absent if a["exists"]]
    truly_absent = [a for a in absent if not a["exists"]]

    paid_real = int(phase_gate.get("first_paid", {}).get("payment_received_real") or 0)
    proof_real = int(phase_gate.get("first_paid", {}).get("proof_pack_delivered_real") or 0)
    crm_pending = bool(phase_gate.get("first_paid", {}).get("crm_kpi_pending"))

    if phase_gate.get("gate_open"):
        verdict = "GATE_OPEN"
    elif paid_real or proof_real:
        verdict = "EVIDENCE_IN_PROGRESS"
    elif evidence["real_rows"] > 0:
        verdict = "PIPELINE_OPEN_NO_REVENUE"
    else:
        verdict = "PRE_PIPELINE"

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": verdict,
        "no_build_until_first_paid": not phase_gate.get("gate_open"),
        "wired_anchors": {
            "total": len(wired),
            "present": wired_present,
            "items": wired,
        },
        "claimed_but_absent": {
            "total_claims": len(absent),
            "still_absent": len(truly_absent),
            "surprise_present": surprise_present,
            "items": absent,
        },
        "evidence": evidence,
        "phase_0_1_gate": phase_gate,
        "weekly_one_decision": weekly,
        "gtm_codification": gtm,
        "pdpl_compliance_pass": pdpl,
        "next_actions": next_three_honest_actions(
            phase_gate=phase_gate, weekly=weekly, gtm=gtm, pdpl=pdpl
        ),
        "honesty_notes": {
            "first_paid_real_events": paid_real,
            "proof_pack_real_events": proof_real,
            "crm_kpi_pending": crm_pending,
            "rule": (
                "لا توليد إيرادات مخترعة. الحالة الخضراء تتطلب payment_received "
                "+ proof_pack_delivered + KPIs من CRM حقيقي."
            ),
        },
    }
