from __future__ import annotations

"""Implementations for each `dealix <subcommand>`.

Every command takes a `private_ops_path: Path` and returns an int exit code.
All output is plain text suitable for terminals — no colour, no emojis.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

from execution_engine.evidence_checker import check_evidence_for_stage
from execution_engine.evidence_report_generator import generate_evidence_report
from execution_engine.next_action_engine import compute_next_action
from execution_engine.stage_checklist_updater import update_checklist
from execution_engine.stage_decision import advance_if_eligible
from execution_engine.stage_reader import read_current_stage
from ops_runtime.alerts_generator import generate_alerts
from ops_runtime.ceo_brief_generator import generate_daily_brief
from ops_runtime.decision_queue_builder import build_decision_queue
from ops_runtime.learning_decision_engine import decide_learning_actions
from ops_runtime.metrics_calculator import (
    compute_delivery_metrics,
    compute_pipeline_metrics,
    compute_revenue_metrics,
)
from ops_runtime.private_ops_reader import (
    read_clients,
    read_pipeline,
    read_revenue_actions,
)
from ops_runtime.scorecard_updater import update_scorecard
from ops_runtime.weekly_comparison import compare_to_prior_week
from ops_runtime.weekly_metrics_writer import write_weekly_metrics
from ops_runtime.weekly_review_generator import generate_weekly_review
from ops_runtime.weekly_review_v2_generator import generate_weekly_review_v2


def _compute_all_metrics(private_ops_path: Path) -> dict[str, Any]:
    return {
        "pipeline": compute_pipeline_metrics(read_pipeline(private_ops_path)),
        "revenue": compute_revenue_metrics(read_revenue_actions(private_ops_path)),
        "delivery": compute_delivery_metrics(read_clients(private_ops_path)),
    }


def _print(line: str) -> None:
    sys.stdout.write(line + "\n")


def cmd_sprint(private_ops_path: Path) -> int:
    """Print the Revenue Sprint Kit summary."""
    _print("Dealix Revenue Sprint Kit")
    _print("-------------------------")
    _print("Goal: first paying client in 30 days.")
    _print("Required artefacts (see docs/offers/revenue_sprint/):")
    _print("  - Offer one-pager")
    _print("  - Sample / pilot artefact")
    _print("  - Proposal template")
    _print("  - FAQ for objection handling")
    _print(f"Private ops in use: {private_ops_path}")
    return 0


def cmd_kit(private_ops_path: Path) -> int:
    """Print the kit readiness checklist."""
    _print("Sprint Kit Checklist")
    _print("--------------------")
    docs_root = Path(__file__).resolve().parents[1] / "docs" / "offers" / "revenue_sprint"
    items = [
        ("Offer one-pager", docs_root / "offer.md"),
        ("Sample artefact", docs_root / "sample.md"),
        ("Proposal template", docs_root / "proposal.md"),
        ("FAQ", docs_root / "faq.md"),
    ]
    for label, path in items:
        marker = "[x]" if path.exists() else "[ ]"
        _print(f"  {marker} {label} ({path})")
    _print(f"Private ops in use: {private_ops_path}")
    return 0


def cmd_stage(private_ops_path: Path) -> int:
    """Print stage status: done / left / next action."""
    stage = read_current_stage(private_ops_path)
    stage_num = int(stage.get("stage", 0))
    _print(f"Current stage: {stage_num} (status: {stage.get('status', 'unknown')})")
    if stage.get("started_at"):
        _print(f"Started at: {stage['started_at']}")
    if stage.get("target_exit_date"):
        _print(f"Target exit: {stage['target_exit_date']}")

    checks = check_evidence_for_stage(private_ops_path, stage_num)
    update_checklist(private_ops_path, checks)
    generate_evidence_report(private_ops_path, checks)

    done = [c for c in checks if c.status == "pass"]
    left = [c for c in checks if c.status != "pass"]
    _print("")
    _print(f"Done ({len(done)}):")
    for c in done:
        _print(f"  - {c.criterion}")
    _print("")
    _print(f"Left ({len(left)}):")
    for c in left:
        suffix = f" -> {c.next_action}" if c.next_action else ""
        _print(f"  - {c.criterion}{suffix}")
    _print("")
    _print(compute_next_action(checks))
    return 0


def cmd_daily(private_ops_path: Path) -> int:
    """Compute today's brief and write founder/daily_brief.md."""
    metrics = _compute_all_metrics(private_ops_path)
    path = generate_daily_brief(metrics, private_ops_path)
    alerts = generate_alerts(metrics, compare_to_prior_week(private_ops_path))
    build_decision_queue(private_ops_path, alerts)
    _print(f"Daily brief written: {path}")
    _print("Top alerts:")
    if not alerts:
        _print("  (none)")
    else:
        for alert in alerts[:5]:
            _print(
                f"  [{alert.get('severity', 'info').upper()}] {alert.get('message', '')}"
            )
    return 0


def cmd_advance(private_ops_path: Path) -> int:
    """Run the stage advance check."""
    result = advance_if_eligible(private_ops_path)
    if result["advanced"]:
        _print(f"Advanced to stage {result['new_stage']}.")
        return 0
    _print("Not eligible to advance. Blockers:")
    for b in result["blockers"]:
        _print(f"  - {b}")
    return 1


def cmd_close_day(private_ops_path: Path) -> int:
    """Append a close-day entry to founder/founder_time_log.md and write snapshot."""
    private_ops_path = Path(private_ops_path)
    log_path = private_ops_path / "founder" / "founder_time_log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    entry = f"\n## {today}\n- Day closed by dealix close-day\n"
    if not log_path.exists():
        log_path.write_text("# Founder Time Log\n", encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(entry)

    metrics = _compute_all_metrics(private_ops_path)
    brief_path = generate_daily_brief(metrics, private_ops_path)
    _print(f"Close-day entry appended: {log_path}")
    _print(f"Daily snapshot written: {brief_path}")
    return 0


def cmd_weekly(private_ops_path: Path) -> int:
    """Run weekly review + v2 + metrics history + scorecard."""
    metrics = _compute_all_metrics(private_ops_path)
    write_weekly_metrics(metrics, private_ops_path)
    comparisons = compare_to_prior_week(private_ops_path)
    learning = decide_learning_actions(metrics, comparisons)
    review = generate_weekly_review(metrics, private_ops_path)
    review_v2 = generate_weekly_review_v2(
        metrics, comparisons, learning, private_ops_path
    )
    scorecard = update_scorecard(metrics, private_ops_path)
    _print(f"Weekly review: {review}")
    _print(f"Weekly review v2: {review_v2}")
    _print(f"Scorecard: {scorecard}")
    _print(f"Learning actions: {len(learning)}")
    return 0


def cmd_dashboard(private_ops_path: Path) -> int:
    """Regenerate dashboard_data/company_metrics.json."""
    private_ops_path = Path(private_ops_path)
    metrics = _compute_all_metrics(private_ops_path)
    target = private_ops_path / "dashboard_data" / "company_metrics.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    update_scorecard(metrics, private_ops_path)
    _print(f"Dashboard JSON written: {target}")
    return 0


def cmd_verify(private_ops_path: Path) -> int:
    """Run every scripts/verify_*.py via subprocess and report."""
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if not scripts_dir.exists():
        _print(f"No scripts directory at {scripts_dir}")
        return 0
    verify_scripts = sorted(scripts_dir.glob("verify_*.py"))
    if not verify_scripts:
        _print("No verify_*.py scripts found.")
        return 0
    failures = 0
    for script in verify_scripts:
        _print(f"Running {script.name} ...")
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(scripts_dir.parent),
            )
        except (OSError, subprocess.SubprocessError) as exc:
            _print(f"  ERROR running {script.name}: {exc}")
            failures += 1
            continue
        status = "ok" if result.returncode == 0 else f"failed ({result.returncode})"
        _print(f"  {status}")
        if result.returncode != 0:
            failures += 1
    _print("")
    _print(f"Total: {len(verify_scripts)}, failures: {failures}")
    return 0 if failures == 0 else 1
