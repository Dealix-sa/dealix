#!/usr/bin/env python3
"""Render DEALIX_STAGE_STATUS.md from repo evidence.

Single source of truth for Gate 0–10 PASS / FIX / BLOCKED. Runs with stdlib
plus PyYAML so it does NOT need the full app environment. Use it in CI and
locally before any sales action.

Decision rules per gate are pulled from docs/company/DEALIX_STAGE_GATES_AR.md
and scripts/verify_dealix_ready.py — this script reproduces the *file-presence*
and *score-threshold* checks without importing the application packages.

Usage:
    python scripts/render_stage_status.py            # write DEALIX_STAGE_STATUS.md
    python scripts/render_stage_status.py --check    # exit 1 if any gate != PASS
    python scripts/render_stage_status.py --print    # print to stdout only
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
STATUS_FILE = REPO / "DEALIX_STAGE_STATUS.md"

GATE_OWNER = {
    0: "Sami (Founder)",
    1: "Sami + Delivery",
    2: "Delivery",
    3: "Engineering",
    4: "Governance",
    5: "Sami + Sales",
    6: "Sami (Sales)",
    7: "Delivery",
    8: "Sami + Delivery",
    9: "Sami (Ops)",
    10: "Sami (Strategy)",
}

GATE0_FILES = (
    "docs/company/POSITIONING.md",
    "docs/company/MISSION_VISION.md",
    "docs/company/OPERATING_PRINCIPLES.md",
    "docs/company/ICP.md",
    "docs/company/NORTH_STAR_METRICS.md",
    "docs/company/DO_NOT_SELL_YET.md",
)

GATE2_FILES = (
    "docs/delivery/DELIVERY_STANDARD.md",
    "docs/delivery/DELIVERY_LIFECYCLE.md",
    "docs/delivery/CLIENT_ONBOARDING.md",
    "docs/delivery/SCOPE_CONTROL.md",
    "docs/delivery/HANDOFF_PROCESS.md",
    "docs/delivery/RENEWAL_PROCESS.md",
)

GATE4_FILES = (
    "dealix/registers/no_overclaim.yaml",
    "dealix/registers/compliance_saudi.yaml",
)

GATE5_META_FILES = (
    "docs/delivery/DEMO_READINESS.md",
    "docs/sales/DEMO_SCRIPT.md",
)

LEAD_INTELLIGENCE_DEMO_FILES = (
    "demos/lead_intelligence_demo/demo.csv",
    "demos/lead_intelligence_demo/import_preview.md",
    "demos/lead_intelligence_demo/data_quality_report.md",
    "demos/lead_intelligence_demo/scoring_output.md",
    "demos/lead_intelligence_demo/top_50_accounts.md",
    "demos/lead_intelligence_demo/top_10_actions.md",
    "demos/lead_intelligence_demo/outreach_drafts.md",
    "demos/lead_intelligence_demo/mini_crm_board.md",
    "demos/lead_intelligence_demo/executive_report.md",
    "demos/lead_intelligence_demo/proof_pack.md",
)

AI_QUICK_WIN_DEMO_FILES = (
    "demos/ai_quick_win_demo/process_map.md",
    "demos/ai_quick_win_demo/before_after.md",
    "demos/ai_quick_win_demo/workflow.md",
    "demos/ai_quick_win_demo/approval_step.md",
    "demos/ai_quick_win_demo/time_saved_estimate.md",
    "demos/ai_quick_win_demo/sop.md",
    "demos/ai_quick_win_demo/proof_pack.md",
)

COMPANY_BRAIN_DEMO_FILES = (
    "demos/company_brain_demo/sample_docs/README.md",
    "demos/company_brain_demo/document_inventory.md",
    "demos/company_brain_demo/qa_examples.md",
    "demos/company_brain_demo/answers_with_citations.md",
    "demos/company_brain_demo/no_source_no_answer.md",
    "demos/company_brain_demo/eval_report.md",
    "demos/company_brain_demo/proof_pack.md",
)

GATE5_DEMO_FILES = (
    LEAD_INTELLIGENCE_DEMO_FILES
    + AI_QUICK_WIN_DEMO_FILES
    + COMPANY_BRAIN_DEMO_FILES
    + ("demos/README.md",)
)

GATE6_FILES = (
    "docs/sales/SALES_PLAYBOOK.md",
    "docs/sales/DISCOVERY_SCRIPT.md",
    "docs/sales/OFFER_PAGES.md",
    "docs/sales/OBJECTION_HANDLING.md",
    "docs/sales/PROPOSAL_TEMPLATE.md",
    "docs/sales/FOLLOW_UP_SEQUENCES.md",
    "docs/ops/pipeline_tracker.csv",
)

GATE7_FILES = (
    "docs/delivery/client_onboarding/welcome_message.md",
    "docs/delivery/client_onboarding/data_request.md",
    "docs/delivery/client_onboarding/project_timeline.md",
    "docs/delivery/client_onboarding/roles_and_responsibilities.md",
    "docs/delivery/client_onboarding/review_call_agenda.md",
    "docs/delivery/client_onboarding/approval_process.md",
)

GATE8_FILES = ("docs/delivery/RETAINER_READINESS.md",)

GATE9_FILES = (
    "docs/ops/DAILY_OPERATING_LOOP.md",
    "docs/company/WEEKLY_OPERATING_REVIEW.md",
)

PRODUCT_PACKAGES = (
    "auto_client_acquisition/data_os",
    "auto_client_acquisition/revenue_os",
    "auto_client_acquisition/knowledge_os",
    "auto_client_acquisition/governance_os",
    "auto_client_acquisition/reporting_os",
    "auto_client_acquisition/delivery_os",
)

STARTER_SERVICES = (
    ("Lead Intelligence Sprint", "lead_intelligence_sprint", "docs/services/lead_intelligence_sprint/"),
    ("AI Quick Win Sprint", "quick_win_ops", "docs/services/ai_quick_win_sprint/"),
    ("Company Brain Sprint", "company_brain_sprint", "docs/services/company_brain_sprint/"),
)

OFFER_READINESS_MIN = 85
PRODUCT_READINESS_MIN = 80

SERVICE_WEIGHTS = {
    "has_offer_page": 10,
    "has_intake": 10,
    "has_scope_template": 10,
    "has_module_support": 15,
    "has_report_template": 10,
    "has_qa_checklist": 15,
    "has_demo": 10,
    "has_compliance_checks": 10,
    "has_upsell_path": 10,
}


@dataclass
class GateResult:
    number: int
    name: str
    status: str
    score: int
    max_score: int
    threshold: int
    missing: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    next_action: str = ""
    owner: str = ""
    blocked_external: bool = False


def _missing(paths: tuple[str, ...]) -> list[str]:
    return [p for p in paths if not (REPO / p).is_file()]


def _has_code(rel: str) -> bool:
    root = REPO / rel
    return root.is_dir() and any(root.rglob("*.py"))


def _score_from_missing(paths: tuple[str, ...], threshold: int = 85) -> int:
    """Linear score: full marks if no files missing, scaled otherwise."""
    if not paths:
        return 100
    present = len(paths) - len(_missing(paths))
    return round(present / len(paths) * 100)


def _service_score(service_id: str) -> int:
    """Replicate compute_service_readiness_score without app imports."""
    yaml_path = (
        REPO
        / "auto_client_acquisition"
        / "governance_os"
        / "policies"
        / "service_readiness_defaults.yaml"
    )
    if not yaml_path.is_file():
        return 0
    blob = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    raw = (blob.get("services") or {}).get(service_id, {})
    total = 0
    for key, weight in SERVICE_WEIGHTS.items():
        if raw.get(key):
            total += weight
    return total


def _decision(score: int, threshold: int, *, blocked: bool = False) -> str:
    if blocked:
        return "BLOCKED"
    if score >= threshold:
        return "PASS"
    return "FIX"


def evaluate_gate_0() -> GateResult:
    paths = GATE0_FILES
    missing = _missing(paths)
    score = _score_from_missing(paths)
    status = _decision(score, 85)
    notes = []
    if missing:
        notes.append(f"Missing files: {', '.join(missing)}")
    return GateResult(
        number=0,
        name="Founder Clarity",
        status=status,
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=notes,
        evidence=list(paths),
        next_action="Close any missing positioning/ICP/north-star files." if missing else "Re-read POSITIONING.md monthly; lock if unchanged.",
        owner=GATE_OWNER[0],
    )


def evaluate_gate_1() -> GateResult:
    scores: list[tuple[str, str, int]] = []
    for label, sid, _ in STARTER_SERVICES:
        scores.append((label, sid, _service_score(sid)))
    passing = [s for s in scores if s[2] >= OFFER_READINESS_MIN]
    score = round(sum(s[2] for s in scores) / max(len(scores), 1))
    notes = [f"{label} ({sid}) = {sc}/100" for label, sid, sc in scores]
    status = "PASS" if len(passing) == len(scores) else "FIX"
    return GateResult(
        number=1,
        name="Offer Readiness",
        status=status,
        score=score,
        max_score=100,
        threshold=OFFER_READINESS_MIN,
        notes=notes,
        evidence=[
            "docs/services/lead_intelligence_sprint/offer.md",
            "docs/services/ai_quick_win_sprint/offer.md",
            "docs/services/company_brain_sprint/offer.md",
            "docs/company/OFFER_LADDER.md",
        ],
        next_action=(
            "All three starter offers PASS — keep offer.md scope + pricing locked."
            if status == "PASS"
            else "Bring each starter service to ≥85 (add demo, upsell, qa)."
        ),
        owner=GATE_OWNER[1],
    )


def evaluate_gate_2() -> GateResult:
    missing = _missing(GATE2_FILES)
    score = _score_from_missing(GATE2_FILES)
    notes = []
    if missing:
        notes.append(f"Missing playbook files: {', '.join(missing)}")
    return GateResult(
        number=2,
        name="Delivery Readiness",
        status=_decision(score, 85),
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=notes,
        evidence=list(GATE2_FILES),
        next_action=(
            "Close missing delivery docs before next paid client."
            if missing
            else "Dry-run handoff on a fake client every 2 weeks."
        ),
        owner=GATE_OWNER[2],
    )


def evaluate_gate_3() -> GateResult:
    present = [p for p in PRODUCT_PACKAGES if _has_code(p)]
    missing = [p for p in PRODUCT_PACKAGES if not _has_code(p)]
    score = round(len(present) / len(PRODUCT_PACKAGES) * 100)
    # Pull live API truth from operational state file (best-effort).
    op_state = REPO / "DEALIX_COMPANY_OPERATIONAL_STATE.md"
    checkout_blocked = False
    if op_state.is_file():
        text = op_state.read_text(encoding="utf-8")
        if "Moyasar" in text and "account_inactive_error" in text:
            checkout_blocked = True
    notes = []
    if missing:
        notes.append(f"Missing OS packages: {', '.join(missing)}")
    if checkout_blocked:
        notes.append("Checkout BLOCKED on Moyasar account activation (external).")
    status = _decision(score, PRODUCT_READINESS_MIN, blocked=checkout_blocked and score >= PRODUCT_READINESS_MIN)
    if checkout_blocked and status != "BLOCKED" and score < PRODUCT_READINESS_MIN:
        status = "FIX"
    return GateResult(
        number=3,
        name="Product Readiness (MVP)",
        status=status,
        score=score,
        max_score=100,
        threshold=PRODUCT_READINESS_MIN,
        missing=missing,
        notes=notes,
        evidence=[
            "DEALIX_COMPANY_OPERATIONAL_STATE.md",
            "api/",
        ] + list(PRODUCT_PACKAGES),
        next_action=(
            "Unblock Moyasar (Sami sends activated sk_live_/sk_test_ key)."
            if checkout_blocked
            else "Backend + landing live; checkout verified."
        ),
        owner=GATE_OWNER[3],
        blocked_external=checkout_blocked,
    )


def evaluate_gate_4() -> GateResult:
    missing = _missing(GATE4_FILES)
    score = _score_from_missing(GATE4_FILES)
    # Governance bar is higher.
    status = _decision(score, 90)
    notes = []
    if missing:
        notes.append(f"Missing governance registers: {', '.join(missing)}")
    return GateResult(
        number=4,
        name="Governance Readiness",
        status=status,
        score=score,
        max_score=100,
        threshold=90,
        missing=missing,
        notes=notes,
        evidence=list(GATE4_FILES) + [
            "docs/company/DECISION_RULES.md",
            "docs/trust/HUMAN_OVERSIGHT_MODEL.md",
        ],
        next_action=(
            "Add missing governance registers before any external claim."
            if missing
            else "Review claims register monthly; PII spot-check weekly."
        ),
        owner=GATE_OWNER[4],
    )


def evaluate_gate_5() -> GateResult:
    missing_meta = _missing(GATE5_META_FILES)
    missing_demo = _missing(GATE5_DEMO_FILES)
    paths = GATE5_META_FILES + GATE5_DEMO_FILES
    score = _score_from_missing(paths)
    notes = []
    if missing_meta:
        notes.append(f"Missing demo meta: {', '.join(missing_meta)}")
    if missing_demo:
        notes.append(f"Missing demo files: {len(missing_demo)} (e.g. {missing_demo[0]})")
    return GateResult(
        number=5,
        name="Demo Readiness",
        status=_decision(score, 85),
        score=score,
        max_score=100,
        threshold=85,
        missing=missing_meta + missing_demo,
        notes=notes,
        evidence=[
            "demos/lead_intelligence_demo/",
            "demos/ai_quick_win_demo/",
            "demos/company_brain_demo/",
            "docs/sales/DEMO_SCRIPT.md",
        ],
        next_action=(
            "Record 5-minute walkthrough per demo pack."
            if score >= 85
            else "Complete missing demo files."
        ),
        owner=GATE_OWNER[5],
    )


def evaluate_gate_6() -> GateResult:
    missing = _missing(GATE6_FILES)
    score = _score_from_missing(GATE6_FILES)
    # Cross-check: have we sent first outbound?
    op_state = REPO / "DEALIX_COMPANY_OPERATIONAL_STATE.md"
    first_dm_sent = False
    if op_state.is_file():
        text = op_state.read_text(encoding="utf-8")
        if "First DM sent" in text and "❌ NOT READY" not in text.split("First DM sent")[1][:100]:
            first_dm_sent = True
    notes = []
    if missing:
        notes.append(f"Missing sales files: {', '.join(missing)}")
    if not first_dm_sent:
        notes.append("First outbound DM not yet logged in pipeline_tracker.csv.")
    status = _decision(score, 85)
    if status == "PASS" and not first_dm_sent:
        status = "FIX"
    return GateResult(
        number=6,
        name="Sales Readiness",
        status=status,
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=notes,
        evidence=list(GATE6_FILES) + ["docs/ops/launch_content_queue.md"],
        next_action=(
            "Sami sends DM #1 from launch_content_queue.md and logs sent_at."
            if not first_dm_sent
            else "Maintain 25-50 daily touches with logged outcomes."
        ),
        owner=GATE_OWNER[6],
    )


def evaluate_gate_7() -> GateResult:
    missing = _missing(GATE7_FILES)
    score = _score_from_missing(GATE7_FILES)
    return GateResult(
        number=7,
        name="Client Delivery Readiness",
        status=_decision(score, 85),
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=[],
        evidence=list(GATE7_FILES) + ["clients/_TEMPLATE/"],
        next_action=(
            "First paid client triggers full onboarding walk-through."
            if not missing
            else "Close missing onboarding docs."
        ),
        owner=GATE_OWNER[7],
    )


def evaluate_gate_8() -> GateResult:
    missing = _missing(GATE8_FILES)
    score = _score_from_missing(GATE8_FILES)
    return GateResult(
        number=8,
        name="Retainer Readiness",
        status=_decision(score, 85),
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=["Pending: first sprint completion + proof pack before activation."],
        evidence=list(GATE8_FILES),
        next_action="Activate when first sprint closes successfully.",
        owner=GATE_OWNER[8],
    )


def evaluate_gate_9() -> GateResult:
    missing = _missing(GATE9_FILES)
    score = _score_from_missing(GATE9_FILES)
    return GateResult(
        number=9,
        name="Scale Readiness",
        status=_decision(score, 85),
        score=score,
        max_score=100,
        threshold=85,
        missing=missing,
        notes=["Hire / partner trigger only after 3 paid clients delivered."],
        evidence=list(GATE9_FILES),
        next_action="Defer until first 3 paid clients delivered with NPS ≥ 8.",
        owner=GATE_OWNER[9],
    )


def evaluate_gate_10() -> GateResult:
    return GateResult(
        number=10,
        name="World-Class Readiness",
        status="FIX",
        score=0,
        max_score=100,
        threshold=85,
        notes=[
            "Aspirational. Activate only after 10+ paid projects, 3+ retainers, case studies live.",
        ],
        evidence=["docs/company/WORLD_CLASS_READINESS_AR.md"],
        next_action="Do not measure until MRR is stable.",
        owner=GATE_OWNER[10],
    )


def evaluate_all() -> list[GateResult]:
    return [
        evaluate_gate_0(),
        evaluate_gate_1(),
        evaluate_gate_2(),
        evaluate_gate_3(),
        evaluate_gate_4(),
        evaluate_gate_5(),
        evaluate_gate_6(),
        evaluate_gate_7(),
        evaluate_gate_8(),
        evaluate_gate_9(),
        evaluate_gate_10(),
    ]


def status_emoji(status: str) -> str:
    return {"PASS": "✅", "FIX": "🟡", "BLOCKED": "🔴"}.get(status, "⚪")


def sell_decision(gates: list[GateResult]) -> tuple[str, list[str]]:
    """Replicates DEALIX_READY_FOR_SALES rule: Gates 0,1,2,3,4,5,6 must PASS."""
    required = {0, 1, 2, 3, 4, 5, 6}
    failures: list[str] = []
    for g in gates:
        if g.number not in required:
            continue
        if g.status != "PASS":
            failures.append(f"Gate {g.number} {g.name} = {g.status}")
    if not failures:
        return "SELL_READY_STACK", []
    # Are any individual starter services still sellable?
    g1 = next((g for g in gates if g.number == 1), None)
    if g1:
        for note in g1.notes:
            if "=" not in note:
                continue
            try:
                raw = note.rsplit("=", 1)[-1].split("/", 1)[0].strip()
                if int(raw) >= OFFER_READINESS_MIN:
                    return "SELL_ONLY_READY_SERVICES", failures
            except (ValueError, IndexError):
                continue
    return "DO_NOT_SELL_FULL_CATALOG", failures


def render_markdown(gates: list[GateResult]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    decision, failures = sell_decision(gates)
    lines: list[str] = []
    lines.append("# Dealix Stage Status")
    lines.append("")
    lines.append(
        "**القاعدة:** المرحلة لا تعتبر منتهية إلا إذا صار عندها `PASS` في هذا الملف + "
        "دليل داخل الريبو + اختبار/تحقق خارجي."
    )
    lines.append("")
    lines.append(f"_Last rendered: {now} by `scripts/render_stage_status.py`_")
    lines.append("")
    lines.append(
        "> هذا الملف يُولَّد آلياً. لا تعدّله يدويًا — عدّل الأدلة في الريبو ثم نفّذ `make stage-status`."
    )
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    lines.append(f"**{decision}**")
    lines.append("")
    if failures:
        lines.append("Sales-blocking gates:")
        for f in failures:
            lines.append(f"- {f}")
        lines.append("")
    lines.append("Sale rule: must PASS Gates 0, 1, 2, 4, 5, 6 + Gate 3 as MVP.")
    lines.append("")
    lines.append("## Master Table")
    lines.append("")
    lines.append("<!-- AUTO:STAGE_STATUS_START -->")
    lines.append(
        "| Gate | Name | Status | Score | Threshold | Owner | Evidence | Next Action |"
    )
    lines.append("|---:|---|:---:|---:|---:|---|---|---|")
    for g in gates:
        evidence_link = g.evidence[0] if g.evidence else "—"
        next_action = g.next_action.replace("|", "/")
        lines.append(
            f"| {g.number} | {g.name} | {status_emoji(g.status)} {g.status} | "
            f"{g.score} | {g.threshold} | {g.owner} | "
            f"`{evidence_link}` | {next_action} |"
        )
    lines.append("<!-- AUTO:STAGE_STATUS_END -->")
    lines.append("")
    lines.append("## Per-Gate Detail")
    lines.append("")
    for g in gates:
        lines.append(f"### Gate {g.number} — {g.name}")
        lines.append("")
        lines.append(f"- **Status:** {status_emoji(g.status)} {g.status}")
        lines.append(f"- **Score:** {g.score}/{g.max_score} (Pass ≥ {g.threshold})")
        lines.append(f"- **Owner:** {g.owner}")
        if g.blocked_external:
            lines.append("- **Blocked on:** external dependency (see notes).")
        if g.notes:
            lines.append("- **Notes:**")
            for n in g.notes:
                lines.append(f"  - {n}")
        if g.missing:
            lines.append("- **Missing evidence:**")
            for m in g.missing[:8]:
                lines.append(f"  - `{m}`")
            if len(g.missing) > 8:
                lines.append(f"  - … and {len(g.missing) - 8} more")
        lines.append("- **Evidence anchors:**")
        for e in g.evidence:
            lines.append(f"  - `{e}`")
        lines.append(f"- **Next action:** {g.next_action}")
        lines.append("")
    lines.append("## Verification commands")
    lines.append("")
    lines.append("```bash")
    lines.append("# Lightweight (no app deps):")
    lines.append("python scripts/render_stage_status.py --check")
    lines.append("")
    lines.append("# Full (needs app environment):")
    lines.append("python scripts/verify_dealix_ready.py --skip-tests")
    lines.append("```")
    lines.append("")
    lines.append("## References")
    lines.append("")
    lines.append("- Doctrine: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md)")
    lines.append("- Live state: [`DEALIX_COMPANY_OPERATIONAL_STATE.md`](DEALIX_COMPANY_OPERATIONAL_STATE.md)")
    lines.append("- Readiness center: [`DEALIX_READINESS.md`](DEALIX_READINESS.md)")
    lines.append("- Render script: [`scripts/render_stage_status.py`](scripts/render_stage_status.py)")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Exit non-zero if any required gate is not PASS.")
    ap.add_argument("--print", action="store_true", help="Print to stdout instead of writing the file.")
    ap.add_argument("--json", action="store_true", help="Emit JSON summary on stdout.")
    args = ap.parse_args()

    gates = evaluate_all()
    markdown = render_markdown(gates)

    if args.print:
        sys.stdout.write(markdown)
    else:
        STATUS_FILE.write_text(markdown, encoding="utf-8")
        sys.stderr.write(f"Wrote {STATUS_FILE.relative_to(REPO)}\n")

    if args.json:
        summary = {
            "decision": sell_decision(gates)[0],
            "gates": [
                {
                    "number": g.number,
                    "name": g.name,
                    "status": g.status,
                    "score": g.score,
                    "threshold": g.threshold,
                    "owner": g.owner,
                    "missing": g.missing,
                }
                for g in gates
            ],
        }
        sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    if args.check:
        decision, failures = sell_decision(gates)
        if decision != "SELL_READY_STACK":
            sys.stderr.write(f"NOT_READY_FOR_SALES decision={decision}\n")
            for f in failures:
                sys.stderr.write(f"- {f}\n")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
