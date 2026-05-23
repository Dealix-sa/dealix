"""Command implementations for the Dealix founder CLI.

Each command is a small, founder-facing checklist runner. They print
deterministic guidance and run the corresponding private-ops verifier when
present. The CLI never sends external messages; it only prints prompts and
runs local verification scripts.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def ensure_private_ops(private_ops: str) -> Path:
    """Resolve and validate the private operations repo path."""
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(
            f"private ops path does not exist: {path}\n"
            "Expected the Dealix private operations repo to be checked out alongside this one."
        )
    if not path.is_dir():
        raise SystemExit(f"private ops path is not a directory: {path}")
    return path


def run_command(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a subprocess command, printing its banner. Exits on non-zero."""
    pretty = " ".join(cmd)
    where = f" (cwd={cwd})" if cwd else ""
    print(f"\n${where} {pretty}")
    result = subprocess.run(cmd, check=False, cwd=str(cwd) if cwd else None)  # noqa: S603
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def sprint(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Priority Execution Sprint")
    print("Goal: first paid Revenue Sprint or PO / written approval.")
    print("\n7-Day Sprint:")
    print("Day 1: Add 25 leads")
    print("Day 2: Send 25 DMs")
    print("Day 3: Prepare 3 samples")
    print("Day 4: Send 1 proposal")
    print("Day 5: Pursue payment / PO / written approval")
    print("Day 6: Test delivery report + QA")
    print("Day 7: Weekly learning review + one playbook update")

    sprint_file = private_ops_path / "sprint/current_sprint.md"
    scorecard = private_ops_path / "sprint/sprint_scorecard.csv"

    print("\nUpdate:")
    print(f"- {sprint_file}")
    print(f"- {scorecard}")

    if (private_ops_path / "verify_priority_sprint.py").exists():
        run_command(
            [sys.executable, str(private_ops_path / "verify_priority_sprint.py")],
            cwd=private_ops_path,
        )

    print("\nPASS: sprint command completed.")


def daily(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Daily Founder Loop")
    print("1. Read founder/daily_brief.md")
    print("2. Review decision_queue.md")
    print("3. Pick one revenue focus")
    print("4. Pick one trust focus")
    print("5. Pick one delivery focus")
    print("6. Execute first revenue action before noon")

    print("\nOpen:")
    print(f"- {private_ops_path / 'founder/daily_brief.md'}")
    print(f"- {private_ops_path / 'founder/decision_queue.md'}")
    print(f"- {private_ops_path / 'pipeline/pipeline_tracker.csv'}")
    print(f"- {private_ops_path / 'sprint/current_sprint.md'}")

    print("\nPASS: daily command completed.")


def close_day(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Close-Day Gate")
    print("1. Pipeline stages updated?")
    print("2. Every lead has next_action?")
    print("3. Revenue action completed?")
    print("4. Approval queue reviewed?")
    print("5. End-of-day note written?")
    print("6. Tomorrow focus clear?")

    if (private_ops_path / "verify_daily_gate.py").exists():
        run_command(
            [sys.executable, str(private_ops_path / "verify_daily_gate.py")],
            cwd=private_ops_path,
        )

    print("\nUpdate before sleep:")
    print(f"- {private_ops_path / 'sprint/daily_execution_log.md'}")
    print(f"- {private_ops_path / 'founder/daily_brief.md'}")
    print(f"- {private_ops_path / 'pipeline/pipeline_tracker.csv'}")


def weekly(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Weekly Learning Review")
    print("1. What moved revenue this week?")
    print("2. What blocked revenue this week?")
    print("3. What did we learn about ICP / message / offer?")
    print("4. One learning decision")
    print("5. One system update committed")

    review_path = private_ops_path / "learning/weekly_intelligence_review.md"
    scorecard = private_ops_path / "sprint/sprint_scorecard.csv"

    print("\nUpdate:")
    print(f"- {review_path}")
    print(f"- {scorecard}")

    print("\nPASS: weekly command completed.")


def verify(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Verify — public + private")

    public_root = Path(__file__).resolve().parent.parent
    public_priority = public_root / "scripts/verify_priority_execution_sprint.py"
    public_layer = public_root / "scripts/verify_priority_operating_layer.py"

    if public_priority.exists():
        run_command([sys.executable, str(public_priority)])
    if public_layer.exists():
        run_command([sys.executable, str(public_layer)])

    for verifier in [
        private_ops_path / "verify_priority_sprint.py",
        private_ops_path / "verify_daily_gate.py",
        private_ops_path / "verify_revenue_actions.py",
    ]:
        if verifier.exists():
            run_command([sys.executable, str(verifier)], cwd=private_ops_path)

    print("\nPASS: verify command completed.")


def dashboard(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)

    print("\nDealix Dashboard")
    print("Open the local dashboard or review the snapshot manually.")

    print("\nKey files:")
    print(f"- {private_ops_path / 'pipeline/pipeline_tracker.csv'}")
    print(f"- {private_ops_path / 'revenue/revenue_action_log.csv'}")
    print(f"- {private_ops_path / 'sprint/sprint_scorecard.csv'}")
    print(f"- {private_ops_path / 'founder/daily_brief.md'}")

    print("\nPASS: dashboard command completed.")
