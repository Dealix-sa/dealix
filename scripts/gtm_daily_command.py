#!/usr/bin/env python3
"""Generate the founder's single daily GTM command (the 21:00 report).

Reads the sample (or a real) draft / suppression store, runs the quality gate,
plans a reputation-safe sending batch, and writes one scannable markdown order
to ``reports/gtm/GTM_DAILY_COMMAND.md``.

    python3 scripts/gtm_daily_command.py --domain-age-days 10 --domain-health healthy

This never sends. The "sending batch" is a *plan* for the founder to approve.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from auto_client_acquisition.gtm_os.draft_quality_gate import (
    summarize_gate_results,
    validate_outreach_draft,
)
from auto_client_acquisition.gtm_os.outreach_draft import DAILY_DRAFT_MIX
from auto_client_acquisition.gtm_os.sending_ramp import (
    ApprovedDraftRef,
    plan_sending_batches,
    ramp_stage_for,
)


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the daily GTM command report.")
    ap.add_argument("--input", default="data/gtm/outreach/drafts.sample.jsonl")
    ap.add_argument("--suppression", default="data/gtm/suppression/suppression.sample.jsonl")
    ap.add_argument("--report", default="reports/gtm/GTM_DAILY_COMMAND.md")
    ap.add_argument("--domain-age-days", type=int, default=10)
    ap.add_argument("--domain-health", default="healthy")
    args = ap.parse_args(argv)

    repo = Path(__file__).resolve().parents[1]
    drafts = _load_jsonl(repo / args.input)
    suppression = {r["recipient_ref"] for r in _load_jsonl(repo / args.suppression) if r.get("recipient_ref")}

    results = [validate_outreach_draft(d, suppression_refs=suppression) for d in drafts]
    summary = summarize_gate_results(results)

    # Approval-ready drafts -> treat as "approved" only for *planning* the ramp
    # (the founder still approves each before any real send).
    ready_ids = set(summary["approval_ready_ids"])
    by_id = {d["draft_id"]: d for d in drafts}
    approved_refs = [
        ApprovedDraftRef(
            draft_id=did,
            recipient_ref=by_id[did].get("recipient_ref", ""),
            unsubscribe_included=bool(by_id[did].get("unsubscribe_included", False)),
            approval_status="approved",
        )
        for did in ready_ids
    ]
    plan = plan_sending_batches(
        approved=approved_refs,
        domain_age_days=args.domain_age_days,
        domain_health=args.domain_health,
        suppression_refs=suppression,
    )
    stage = ramp_stage_for(args.domain_age_days)

    target_drafts = sum(DAILY_DRAFT_MIX.values())
    lines = [
        "# GTM Daily Command — أمر اليوم التجاري",
        "",
        f"_Generated: {datetime.now(UTC).isoformat()}_",
        "",
        "## 1) Draft production — إنتاج المسودات",
        f"- Target mix / الهدف: **{target_drafts}/day** "
        + ", ".join(f"{k}={v}" for k, v in DAILY_DRAFT_MIX.items()),
        f"- Loaded today / المحمَّلة: **{summary['total']}**",
        f"- Approval-ready / جاهزة للموافقة: **{summary['passed']}**",
        f"- Blocked / محجوبة: **{summary['failed']}**",
        "",
        "## 2) Top approval queue — أعلى قائمة الموافقة",
    ]
    for did in list(summary["approval_ready_ids"])[:50]:
        d = by_id.get(did, {})
        lines.append(f"- `{did}` — {d.get('sector','?')} · {d.get('offer','?')} · {d.get('recipient_role','?')}")
    if not summary["approval_ready_ids"]:
        lines.append("- (none ready — review blocked drafts) / لا يوجد جاهز")

    lines += [
        "",
        "## 3) Sending batch plan — خطة الإرسال (بعد موافقة المؤسس)",
        f"- Ramp stage / مرحلة التدرّج: **{stage.label_en} / {stage.label_ar}** (max {stage.max_per_day}/day)",
        f"- Domain health / صحة الدومين: **{plan.domain_health}**",
        f"- Effective cap / السقف الفعّال: **{plan.effective_daily_cap}/day**",
        f"- Eligible / مؤهّلة: **{plan.eligible_count}** · Scheduled / مجدولة: **{plan.scheduled_count}**",
    ]
    if plan.blocked:
        lines.append(f"- **BLOCKED**: {plan.blocked_reason_en} / {plan.blocked_reason_ar}")
    for b in plan.batches:
        lines.append(f"  - batch `{b.batch_id}` ({b.send_window}): {b.max_volume} drafts")

    lines += ["", "## 4) Warnings — تنبيهات"]
    if plan.excluded:
        for reason, ids in plan.excluded.items():
            lines.append(f"- `{reason}`: {len(ids)} → {', '.join(ids)}")
    if summary["top_failure_reasons"]:
        for code, count in summary["top_failure_reasons"].items():
            lines.append(f"- gate `{code}`: {count}")
    if not plan.excluded and not summary["top_failure_reasons"]:
        lines.append("- none")

    lines += [
        "",
        "## 5) Tomorrow — توصية الغد",
        "- Double the best-performing sector/offer; pause the worst 20%.",
        "- ضاعِف أفضل قطاع/عرض؛ أوقف أسوأ 20%.",
        "",
        "---",
        "> No external send happens without founder approval. هذا أمر تشغيلي — لا إرسال إلا بموافقة المؤسس.",
        "> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.",
        "",
    ]

    out = repo / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"daily command -> {args.report} (ready={summary['passed']} blocked={summary['failed']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
