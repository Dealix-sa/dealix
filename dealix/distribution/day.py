"""Distribution Day — the one daily run that drives the whole machine.

Runs the full pipeline **in-process** (testable, single process, no shelling
out) and renders a founder summary:

    prospects → drafts → quality gate → queue → follow-ups → proposals
             → proof packs → payment handoff → renewals → metrics → win/loss

Verdict is FAIL if prospect validation fails or any draft fails the quality
gate; otherwise PASS. Nothing is sent — the output is a prioritized to-do for
the founder (review + approve + manually send the highest-fit drafts first).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from dealix.distribution import (
    drafts,
    followups,
    metrics,
    payments,
    proof_packs,
    proposals,
    quality,
    renewals,
)
from dealix.distribution.doctrine import OPERATING_MODE, doctrine_snapshot
from dealix.distribution.ledger import now_iso
from dealix.distribution.paths import REPORTS_DIR
from dealix.distribution.prospects import load_prospects, validate_prospects


def run_day(
    prospects_path: Path | None = None,
    *,
    today: date | None = None,
    write_report: bool = True,
    reports_dir: Path | None = None,
) -> dict[str, Any]:
    """Execute the daily distribution pipeline and (optionally) write the report."""
    steps: dict[str, Any] = {}

    prospects = load_prospects(prospects_path)
    validation = validate_prospects(prospects)
    steps["1_prospect_validation"] = validation

    steps["2_drafts"] = drafts.run_generation(prospects_path)
    gate = quality.run_quality_gate(persist=True)
    steps["3_quality_gate"] = {k: gate[k] for k in ("total", "passed", "failed", "ok")}
    steps["3_quality_gate"]["failures"] = gate["failures"]
    steps["4_queue"] = {"pending_drafts": len(drafts.pending_drafts())}
    steps["5_followups"] = followups.run_generation(prospects_path, today=today)
    steps["6_proposals"] = proposals.run_generation(prospects_path)
    steps["7_proof_packs"] = proof_packs.run_generation(prospects_path)
    steps["8_payments"] = payments.run_generation()
    steps["9_renewals"] = renewals.run_generation(prospects_path, today=today)

    snapshot = metrics.compute_metrics()
    steps["10_metrics"] = snapshot["kpis"]
    steps["11_win_loss"] = snapshot["win_loss"]

    failed = (not validation["ok"]) or (not gate["ok"])
    verdict = "FAIL" if failed else "PASS"

    if failed:
        action = "أصلح بوابة الجودة / تحقق المدخلات قبل اعتماد أي مسودة."
    else:
        action = "راجع المسودات المعلقة واعتمد الأنسب أولًا، ثم انسخها وأرسلها يدويًا."

    result = {
        "generated_at": now_iso(),
        "operating_mode": OPERATING_MODE,
        "verdict": verdict,
        "steps": steps,
        "metrics": snapshot,
        "founder_action_ar": action,
        "doctrine": doctrine_snapshot()["clean"],
    }

    if write_report:
        out_dir = reports_dir or REPORTS_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "DISTRIBUTION_DAY.md").write_text(render_report(result), encoding="utf-8")

    return result


def render_report(result: dict[str, Any]) -> str:
    """Bilingual founder-facing markdown for the day's run."""
    s = result["steps"]
    k = result["metrics"]["kpis"]
    f = result["metrics"]["funnel"]
    lines = [
        "# Dealix Distribution Day — تشغيل التصريف اليومي",
        "",
        f"- Generated: {result['generated_at']}",
        f"- Operating mode: `{result['operating_mode']}`",
        f"- **Verdict: {result['verdict']}**",
        "",
        "## KPIs",
        "",
        f"- Pending drafts: {k['pending_drafts']}",
        f"- Approved drafts: {k['approved_drafts']}",
        f"- Due follow-ups: {k['due_followups']}",
        f"- Proposal drafts: {k['proposal_drafts']}",
        f"- Proof packs: {k['proof_packs']}",
        f"- Payment handoffs: {k['payment_handoffs']}",
        f"- Upcoming renewals: {k['upcoming_renewals']}",
        f"- Won / Lost: {k['won_deals']} / {k['lost_deals']}",
        "",
        "## Funnel",
        "",
        f"- Drafts → approved: {f['drafts']} → {f['approved_drafts']} "
        f"({f['draft_approval_rate_pct']}%)",
        f"- Proposals → accepted: {f['proposals']} → {f['accepted_proposals']} "
        f"({f['proposal_accept_rate_pct']}%)",
        f"- Payments → paid: {f['payments']} → {f['paid']} ({f['payment_close_rate_pct']}%)",
        "",
        "## Pipeline steps",
        "",
        f"- Prospects validated: {s['1_prospect_validation']['valid']}/"
        f"{s['1_prospect_validation']['total']} (ok={s['1_prospect_validation']['ok']})",
        f"- New drafts: {s['2_drafts']['new_drafts']}",
        f"- Quality gate: {s['3_quality_gate']['passed']}/{s['3_quality_gate']['total']} "
        f"passed (ok={s['3_quality_gate']['ok']})",
        f"- New follow-ups: {s['5_followups']['new_followups']} "
        f"(high={s['5_followups']['by_priority']['high']})",
        f"- New proposals: {s['6_proposals']['new_proposals']}",
        f"- New proof packs: {s['7_proof_packs']['new_proof_packs']}",
        f"- New payment handoffs: {s['8_payments']['new_handoffs']}",
        f"- New renewals: {s['9_renewals']['new_renewals']}",
        "",
        "## Founder next action",
        "",
        f"- {result['founder_action_ar']}",
        "",
        "> كل المخرجات مسودات — لا إرسال خارجي تلقائي. الموافقة والإرسال يدويان.",
        "",
    ]
    if not result["steps"]["3_quality_gate"]["ok"]:
        lines.append("### ⚠️ Quality gate failures")
        for fail in result["steps"]["3_quality_gate"]["failures"]:
            lines.append(f"- `{fail['id']}`: {', '.join(fail['errors'])}")
        lines.append("")
    return "\n".join(lines)


__all__ = ["render_report", "run_day"]
