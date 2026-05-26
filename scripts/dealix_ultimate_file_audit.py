from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports" / "readiness"

GROUPS = {
    "01_core_runtime": [
        "dealix.py",
        "dealix_local_ai.py",
        "local_ai/local_ai_config.json",
        "scripts/dealix-local-ai-env.ps1",
        "scripts/verify_local_ai.py",
        "scripts/dealix-operator-day.ps1",
        "scripts/dealix-launch-mode.ps1",
    ],
    "02_quality_governance_safety": [
        "scripts/score_local_output.py",
        "scripts/local_generate_score_check.py",
        "scripts/ledger_guard.py",
        "scripts/backup_ledgers.py",
        "scripts/runtime_snapshot.py",
        "scripts/restore_latest_snapshot.py",
        "scripts/pipeline_status_machine.py",
        "docs/trust/HERMES_TRUST_MODEL_AR.md",
    ],
    "03_sales_execution": [
        "data/ledgers/prospects.json",
        "scripts/build_manual_send_queue.py",
        "scripts/build_followup_queue.py",
        "scripts/triage_reply.py",
        "scripts/lead_status_report.py",
        "scripts/ceo_close_report.py",
        "docs/ops/APPROVED_OUTREACH_TEMPLATES_AR.md",
        "docs/sales/APPROVED_REPLY_LIBRARY_AR.md",
        "docs/sales/FOLLOW_UP_LIBRARY_AR.md",
    ],
    "04_revenue_payment": [
        "scripts/proposal_from_lead.py",
        "scripts/payment_request.py",
        "scripts/start_paid_delivery.ps1",
        "scripts/confirm_payment.ps1",
        "scripts/revenue_ledger.py",
        "data/ledgers/revenue_ledger.json",
    ],
    "05_delivery_proof_retainer": [
        "scripts/new_client_intake.py",
        "scripts/delivery_tracker.py",
        "scripts/generate_ai_trust_report.py",
        "scripts/generate_delivery_accuracy_report.py",
        "scripts/proof_from_lead.py",
        "scripts/retainer_offer.py",
        "scripts/complete_delivery.ps1",
        "data/ledgers/delivery_ledger.json",
    ],
    "06_hermes_core": [
        "scripts/hermes_safe_init.py",
        "scripts/hermes_founder_brief.py",
        "scripts/hermes_opportunity_radar.py",
        "scripts/hermes_score.py",
        "scripts/hermes_capture_signal.py",
        "scripts/hermes_decision_memo.py",
        "scripts/hermes_deal_room.py",
        "scripts/hermes_compound_input.py",
        "scripts/hermes_log_outcome.py",
        "scripts/hermes_trust_pack.py",
        "scripts/hermes_weekly_review.py",
        "scripts/hermes-core-run.ps1",
    ],
    "07_hermes_partner_productization": [
        "scripts/hermes_partner_init.py",
        "scripts/hermes_partner_os.py",
        "scripts/hermes_partner_pack.py",
        "scripts/hermes_case_study.py",
        "scripts/hermes_productization_gate.py",
        "scripts/hermes-partner-product-run.ps1",
        "docs/partners/HERMES_PARTNER_OS_AR.md",
        "docs/productization/HERMES_PRODUCTIZATION_RULES_AR.md",
    ],
    "08_key_ledgers": [
        "data/ledgers/hermes_signals.json",
        "data/ledgers/hermes_opportunities.json",
        "data/ledgers/hermes_outcomes.json",
        "data/ledgers/hermes_assets.json",
        "data/ledgers/hermes_deal_rooms.json",
        "data/ledgers/hermes_partners.json",
        "data/ledgers/hermes_productization.json",
    ],
    "09_manuals": [
        "docs/launch/DEALIX_LOCAL_PRODUCTION_OPERATING_MANUAL_AR.md",
        "docs/hermes/HERMES_CORE_V1_OPERATING_MANUAL_AR.md",
        "docs/trust/HERMES_TRUST_MODEL_AR.md",
        "docs/partners/HERMES_PARTNER_OS_AR.md",
        "docs/productization/HERMES_PRODUCTIZATION_RULES_AR.md",
    ],
}

CORE_WEIGHT = {
    "01_core_runtime": 5,
    "02_quality_governance_safety": 5,
    "03_sales_execution": 5,
    "04_revenue_payment": 4,
    "05_delivery_proof_retainer": 4,
    "06_hermes_core": 4,
    "07_hermes_partner_productization": 3,
    "08_key_ledgers": 4,
    "09_manuals": 2,
}


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    total = 0
    present = 0
    weighted_total = 0
    weighted_present = 0
    rows = []
    missing = []

    for group, files in GROUPS.items():
        weight = CORE_WEIGHT.get(group, 1)
        for f in files:
            total += 1
            weighted_total += weight
            path = ROOT / f
            ok = path.exists()
            if ok:
                present += 1
                weighted_present += weight
            else:
                missing.append(f)

            rows.append({
                "group": group,
                "file": f,
                "present": ok,
                "weight": weight,
            })

    score = round((weighted_present / weighted_total) * 100, 2) if weighted_total else 0
    verdict = "PASS" if score >= 90 and not any(m.startswith("dealix.py") for m in missing) else "REVIEW_REQUIRED"

    md = [
        "# Dealix/Hermes Ultimate File Audit",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"- Present: {present}/{total}",
        f"- Weighted readiness score: {score}%",
        f"- Verdict: {verdict}",
        "",
        "## Missing Files",
        "",
    ]

    if missing:
        for m in missing:
            md.append(f"- `{m}`")
    else:
        md.append("- None")

    md += [
        "",
        "## Full Matrix",
        "",
        "| Group | File | Present | Weight |",
        "|---|---|---|---:|",
    ]

    for r in rows:
        md.append(f"| {r['group']} | `{r['file']}` | {r['present']} | {r['weight']} |")

    md += [
        "",
        "## Interpretation",
        "",
        "- 90%+ = system is operationally complete enough to sell and deliver.",
        "- Missing core runtime or safety files must be fixed before launch.",
        "- Missing partner/productization files is acceptable before first partner conversation, but should be completed soon.",
    ]

    out = REPORTS / f"ultimate-file-audit-{time.strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(md), encoding="utf-8")

    json_out = REPORTS / f"ultimate-file-audit-{time.strftime('%Y%m%d-%H%M%S')}.json"
    json_out.write_text(json.dumps({
        "present": present,
        "total": total,
        "score": score,
        "verdict": verdict,
        "missing": missing,
        "rows": rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"ULTIMATE_FILE_AUDIT_REPORT={out}")
    print(f"ULTIMATE_FILE_AUDIT_JSON={json_out}")
    print(f"ULTIMATE_FILE_AUDIT_SCORE={score}")
    print(f"ULTIMATE_FILE_AUDIT_VERDICT={verdict}")

    if verdict != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
