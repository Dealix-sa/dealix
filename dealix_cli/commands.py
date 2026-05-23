from __future__ import annotations

import csv
from pathlib import Path

from execution_engine.evidence_report_generator import generate_evidence_report
from execution_engine.evidence_scanner import scan_stage_1_evidence
from execution_engine.stage_checklist_updater import update_stage_checklist
from ops_runtime.markdown_writer import write_markdown


def ensure_private_ops(private_ops: str) -> Path:
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Private ops root not found: {path}")
    return path


def read_stage_checklist(private_ops_root: str) -> list[dict]:
    checklist_path = Path(private_ops_root) / "stage/stage_exit_checklist.csv"
    if not checklist_path.exists():
        return []
    with checklist_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def recommend_next_action(checklist: list[dict]) -> dict:
    for row in checklist:
        status = (row.get("status") or "").strip().lower()
        if status != "done":
            return {
                "criterion": row.get("criterion", ""),
                "action": row.get("next_action") or "Define a concrete next action for this criterion.",
                "evidence": row.get("evidence") or "Add evidence to the relevant private-ops ledger.",
            }
    return {
        "criterion": "All criteria complete",
        "action": "Trigger CEO + Trust review and decide: Advance / Stay / Reset.",
        "evidence": "stage/evidence_report.md",
    }


def decide_stage(checklist: list[dict]) -> str:
    if not checklist:
        return "STAY"
    pending = [r for r in checklist if (r.get("status") or "").strip().lower() != "done"]
    return "ADVANCE_READY" if not pending else "STAY"


def daily(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    checklist = read_stage_checklist(str(private_ops_path))
    next_action = recommend_next_action(checklist)
    print("Dealix Daily")
    print("-" * 40)
    print(f"Stage criterion in focus: {next_action['criterion']}")
    print(f"Action: {next_action['action']}")
    print(f"Evidence: {next_action['evidence']}")


def weekly(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    checklist = read_stage_checklist(str(private_ops_path))
    decision = decide_stage(checklist)
    print("Dealix Weekly")
    print("-" * 40)
    print(f"Stage decision: {decision}")
    print(f"Open criteria: {sum(1 for r in checklist if (r.get('status') or '').strip().lower() != 'done')}")


def dashboard(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    checklist = read_stage_checklist(str(private_ops_path))
    print("Dealix Dashboard")
    print("-" * 40)
    for row in checklist:
        print(f"- [{row.get('status', 'Pending')}] {row.get('criterion', '')}")


def verify(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    evidence = scan_stage_1_evidence(str(private_ops_path))
    print("Dealix Verify")
    print("-" * 40)
    for criterion, passed in evidence.items():
        print(f"- [{'PASS' if passed else 'PENDING'}] {criterion}")


def sprint(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    checklist = read_stage_checklist(str(private_ops_path))
    pending = [r for r in checklist if (r.get("status") or "").strip().lower() != "done"]
    print("Dealix Sprint")
    print("-" * 40)
    print(f"Pending criteria: {len(pending)}")
    for row in pending:
        print(f"- {row.get('criterion', '')}: {row.get('next_action', '')}")


def stage(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    checklist = read_stage_checklist(str(private_ops_path))
    decision = decide_stage(checklist)
    print("Dealix Stage")
    print("-" * 40)
    print(f"Decision: {decision}")
    for row in checklist:
        print(f"- [{row.get('status', 'Pending')}] {row.get('criterion', '')}")


def advance(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    updated = update_stage_checklist(str(private_ops_path))
    checklist = read_stage_checklist(str(private_ops_path))
    next_action = recommend_next_action(checklist)
    decision = decide_stage(checklist)

    evidence = scan_stage_1_evidence(str(private_ops_path))
    report = generate_evidence_report(evidence)
    report_path = write_markdown(str(private_ops_path / "stage/evidence_report.md"), report)

    print("\nDealix Stage Advance Check")
    print("=" * 40)
    print(f"Updated checklist: {updated}")
    print(f"Stage decision: {decision}")
    print(f"Evidence report: {report_path}")

    print("\nNext Required Action:")
    print(f"- Criterion: {next_action['criterion']}")
    print(f"- Action: {next_action['action']}")
    print(f"- Evidence: {next_action['evidence']}")

    if decision == "ADVANCE_READY":
        print("\nCEO Decision Required:")
        print("- Review stage/weekly_stage_review.md")
        print("- Confirm no trust blockers")
        print("- Decide: Advance / Stay / Reset")
