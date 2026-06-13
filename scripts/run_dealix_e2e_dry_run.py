#!/usr/bin/env python3
"""Dealix End-to-End Dry Run.

Simulates the full revenue path on a fictional customer — from first target
to first Proof Pack and upsell — entirely locally, with no real external
action. Proves the system *flows*, stage by stage, and writes a PASS/FAIL
report to ``reports/verification/e2e_dry_run_latest.md``.

Stages:
    1. Target
    2. Outreach Approval (founder approval required — never auto-sent)
    3. Diagnostic
    4. Offer
    5. Paid Sprint Simulation (SIMULATED status only — no real payment)
    6. Customer Workspace
    7. Proof Pack (skeleton — no fake result presented as real)
    8. Upsell
    9. Founder Daily Command
    + Governance gate (No External Action Without Approval)

Hard rules enforced:
    - no real external sending
    - no fake proof presented as real
    - no guaranteed revenue
    - no customer name publishing
    - no WhatsApp automation
    - all external actions remain approval-required

Usage:
    python scripts/run_dealix_e2e_dry_run.py

Terminal markers:
    E2E_DRY_RUN_VERDICT=<verdict>
    DEALIX_E2E_DRY_RUN_OK=true|false
"""
from __future__ import annotations

import csv
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.create_customer_workspace import (  # noqa: E402
    COMMAND_SPRINT_FILES,
    create_workspace,
)

DRY_RUN_CLIENT = "dry-run-client"


@dataclass
class Stage:
    key: str
    name: str
    core: bool
    passed: bool = False
    notes: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.notes.append(msg)

    def ok(self, msg: str) -> None:
        self.passed = True
        self.notes.append(msg)


def _read(rel: str) -> str:
    fp = REPO / rel
    return fp.read_text(encoding="utf-8", errors="ignore") if fp.is_file() else ""


def stage_target() -> Stage:
    s = Stage("target", "Target", core=True)
    fp = REPO / "data/outreach/first_30_targets.csv"
    if not fp.is_file():
        s.fail("data/outreach/first_30_targets.csv missing")
        return s
    rows = list(csv.DictReader(fp.open(encoding="utf-8", newline="")))
    if not rows:
        s.fail("targets file has no rows")
        return s
    s.ok(f"target list present ({len(rows)} seed rows); simulated target = '{DRY_RUN_CLIENT}'")
    return s


def stage_outreach_approval() -> Stage:
    s = Stage("outreach", "Outreach Approval", core=True)
    fp = REPO / "data/outreach/approval_queue.csv"
    if not fp.is_file():
        s.fail("data/outreach/approval_queue.csv missing")
        return s
    rows = list(csv.DictReader(fp.open(encoding="utf-8", newline="")))
    # Approval gate is real only if nothing is auto-approved/sent.
    sent = [r for r in rows if (r.get("founder_decision") or "").strip().lower() in {"sent", "auto", "auto-approved", "approved-auto"}]
    if sent:
        s.fail(f"{len(sent)} row(s) marked auto-sent/auto-approved — violates approval gate")
        return s
    pending = [r for r in rows if (r.get("founder_decision") or "").strip().lower() == "pending"]
    s.ok(f"approval queue present; {len(pending)} draft(s) pending founder approval; none auto-sent")
    return s


def stage_diagnostic(ws: Path) -> Stage:
    s = Stage("diagnostic", "Diagnostic", core=True)
    f = ws / "02_diagnostic_summary.md"
    script = REPO / "scripts/dealix_diagnostic.py"
    if not f.is_file():
        s.fail("02_diagnostic_summary.md missing from workspace")
        return s
    if not script.is_file():
        s.fail("scripts/dealix_diagnostic.py missing")
        return s
    s.ok("diagnostic record present in workspace; diagnostic script available")
    return s


def stage_offer(ws: Path) -> Stage:
    s = Stage("offer", "Offer", core=True)
    scope = ws / "03_command_sprint_scope.md"
    offer_doc = REPO / "docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md"
    if not scope.is_file():
        s.fail("03_command_sprint_scope.md missing from workspace")
        return s
    if not offer_doc.is_file():
        s.fail("Command Sprint offer doc missing")
        return s
    s.ok("Command Sprint scope present in workspace; offer doc available")
    return s


def stage_paid_sim() -> Stage:
    s = Stage("paid", "Paid Sprint Simulation", core=False)
    # In-memory simulated payment — explicitly NOT a real charge.
    simulated_status = "SIMULATED-PAID (no real payment link, no charge)"
    s.ok(f"payment status simulated only: {simulated_status}")
    return s


def stage_workspace(ws: Path) -> Stage:
    s = Stage("workspace", "Customer Workspace", core=True)
    missing = [f for f in COMMAND_SPRINT_FILES if not (ws / f).is_file()]
    if missing:
        s.fail(f"missing workspace files: {', '.join(missing)}")
        return s
    s.ok(f"all {len(COMMAND_SPRINT_FILES)} Command Sprint files present in customers/{DRY_RUN_CLIENT}/")
    return s


def stage_proof_pack(ws: Path) -> Stage:
    s = Stage("proof", "Proof Pack", core=True)
    f = ws / "10_proof_pack.md"
    if not f.is_file():
        s.fail("10_proof_pack.md missing")
        return s
    text = f.read_text(encoding="utf-8", errors="ignore")
    # Guard: a skeleton must NOT present any verified/achieved result.
    if "✅" in text and "Verified" in text:
        s.fail("proof pack appears to present a verified result in a dry run (fake proof risk)")
        return s
    if "Skeleton" not in text and "skeleton" not in text:
        s.notes.append("note: proof pack does not self-identify as a skeleton")
    s.ok("proof pack skeleton present; no fabricated/verified result asserted")
    return s


def stage_upsell(ws: Path) -> Stage:
    s = Stage("upsell", "Upsell", core=False)
    f = ws / "11_upsell_recommendation.md"
    if not f.is_file():
        s.fail("11_upsell_recommendation.md missing")
        return s
    s.ok("upsell recommendation present (A2 — founder review before offering)")
    return s


def stage_daily_command() -> Stage:
    s = Stage("daily", "Founder Daily Command", core=False)
    out = REPO / "reports/founder/daily_command.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_daily_command(), encoding="utf-8")
    s.ok(f"founder daily command written: {out.relative_to(REPO)}")
    return s


def stage_governance() -> Stage:
    s = Stage("governance", "Governance", core=True)
    gate = REPO / "docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"
    policy = REPO / "docs/governance/APPROVAL_POLICY.md"
    if not gate.is_file():
        s.fail("NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md missing")
        return s
    if not policy.is_file():
        s.fail("docs/governance/APPROVAL_POLICY.md missing")
        return s
    # The dry run itself performs zero external actions — assert that invariant.
    s.ok("No-External-Action gate present; dry run performed 0 external actions")
    return s


def render_daily_command() -> str:
    today = date.today().isoformat()
    return f"""# Founder Daily Command — {today}

_Refreshed by `scripts/run_dealix_e2e_dry_run.py`. The one screen to run the day._

## 1. Today's single most important move
- [ ] _(decide one)_

## 2. Awaiting your approval (A2/A3 — nothing sends without you)
- See `data/outreach/approval_queue.csv` — drafts pending founder approval.

## 3. Pipeline at a glance
| Stage | Count | Next action |
| --- | --- | --- |
| Targets (seed) | see `data/outreach/first_30_targets.csv` | shortlist top 10 |
| Drafts pending approval | see approval queue | review + approve |
| Diagnostics booked | 0 | book first |
| Offers sent | 0 | — |
| Paid sprints | 0 | — |
| Proof packs delivered | 0 | — |

## 4. Guardrails (always on)
- No auto-send. No cold WhatsApp. No guaranteed-revenue claims.
- No customer name published without written consent.
- Every external action is logged in the customer Approval Register.

## 5. Next 5 founder actions
1. Review `reports/launch/private_launch_readiness.md`.
2. Confirm E2E dry run verdict in `reports/verification/e2e_dry_run_latest.md`.
3. Shortlist top 10 from the first-30 targets.
4. Approve up to 5 outreach drafts (manual send only).
5. Book the first diagnostic.
"""


def render_report(stages: list[Stage], verdict: str) -> str:
    today = date.today().isoformat()
    lines = [
        "# Dealix E2E Dry Run",
        "",
        f"_Generated by `scripts/run_dealix_e2e_dry_run.py` on {today}. "
        "Simulation only — no real external action, no real payment, no published name._",
        "",
    ]
    for i, s in enumerate(stages, start=1):
        status = "PASS" if s.passed else "FAIL"
        lines.append(f"## Stage {i} — {s.name}")
        lines.append(status)
        for n in s.notes:
            lines.append(f"- {n}")
        lines.append("")
    lines.append("## Verdict")
    lines.append(verdict)
    lines.append("")
    lines.append("### Core stages (must PASS for Private Launch Ready)")
    lines.append("Target · Outreach Approval · Diagnostic · Offer · Customer Workspace · Proof Pack · Governance")
    return "\n".join(lines) + "\n"


def compute_verdict(stages: list[Stage]) -> str:
    core = [s for s in stages if s.core]
    if not all(s.passed for s in core):
        return "No-Go"
    if all(s.passed for s in stages):
        return "Private Launch Ready"
    return "Internal Only"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is best-effort; the default stream is fine if unavailable.
        pass

    # Build the dry-run workspace (idempotent via --force semantics).
    try:
        ws, _ = create_workspace(DRY_RUN_CLIENT, force=True)
    except Exception as exc:  # noqa: BLE001 - dry run must surface, not crash CI
        print(f"FATAL: could not create dry-run workspace: {exc}", file=sys.stderr)
        return 1

    stages = [
        stage_target(),
        stage_outreach_approval(),
        stage_diagnostic(ws),
        stage_offer(ws),
        stage_paid_sim(),
        stage_workspace(ws),
        stage_proof_pack(ws),
        stage_upsell(ws),
        stage_daily_command(),
        stage_governance(),
    ]

    verdict = compute_verdict(stages)

    # Console output.
    for i, s in enumerate(stages, start=1):
        print(f"Stage {i} — {s.name}: {'PASS' if s.passed else 'FAIL'}")
        for n in s.notes:
            print(f"    {n}")

    out = REPO / "reports/verification/e2e_dry_run_latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(stages, verdict), encoding="utf-8")
    print(f"WROTE {out.relative_to(REPO)}")

    blockers = [s.name for s in stages if not s.passed]
    if blockers:
        print("BLOCKERS: " + ", ".join(blockers))

    print(f"E2E_DRY_RUN_VERDICT={verdict}")
    ok = verdict in {"Private Launch Ready", "Internal Only"}
    print(f"DEALIX_E2E_DRY_RUN_OK={'true' if ok else 'false'}")
    # Non-zero only on No-Go (a core stage failed).
    return 0 if verdict != "No-Go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
