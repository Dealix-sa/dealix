"""Command implementations for the Dealix founder CLI.

Every command is intentionally simple and read-mostly. They do not send
external messages. They do not charge customers. They do not modify the
public repo without explicit founder action.
"""

from __future__ import annotations

import csv
import datetime as dt
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def ensure_private_ops(path: str) -> Path:
    """Resolve and validate the private-ops directory."""
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        print(f"ERROR: private ops path does not exist: {resolved}")
        raise SystemExit(2)
    if not resolved.is_dir():
        print(f"ERROR: private ops path is not a directory: {resolved}")
        raise SystemExit(2)
    return resolved


def run_command(args: list[str]) -> int:
    """Run a subprocess and stream output. Exits the CLI on non-zero return."""
    print(f"\n$ {' '.join(args)}")
    result = subprocess.run(args)
    if result.returncode != 0:
        print(f"ERROR: command exited with code {result.returncode}")
        raise SystemExit(result.returncode)
    return result.returncode


def _read_lines(path: Path, limit: int | None = None) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        return lines[:limit]
    return lines


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def daily(private_ops: str) -> None:
    """Print the daily founder brief: today's 3, approvals, yesterday's actions."""
    ops = ensure_private_ops(private_ops)
    today = dt.date.today()

    print(f"\n== Dealix daily brief — {today.isoformat()} ==\n")

    print("-- Today's 3 (founder/decision_queue.md) --")
    queue_lines = _read_lines(ops / "founder" / "decision_queue.md", limit=40)
    if not queue_lines:
        print("(empty — write 3 lines in founder/decision_queue.md before doing anything else)")
    else:
        for line in queue_lines:
            print(line)

    print("\n-- Approvals waiting (founder/approvals_waiting.md) --")
    approvals = _read_lines(ops / "founder" / "approvals_waiting.md", limit=40)
    if not approvals:
        print("(none)")
    else:
        for line in approvals:
            print(line)

    print("\n-- Yesterday's revenue actions --")
    yesterday = (today - dt.timedelta(days=1)).isoformat()
    rows = _read_csv(ops / "revenue" / "revenue_action_log.csv")
    recent = [r for r in rows if r.get("date") in (today.isoformat(), yesterday)]
    if not recent:
        print(f"(no actions logged for {yesterday} or {today.isoformat()})")
    else:
        for r in recent:
            print(
                f"- {r.get('date'):10}  {r.get('action_type', '?'):20}  "
                f"lead={r.get('lead_id', '?'):>4}  {r.get('summary', '')[:60]}"
            )

    brief_dir = ops / "founder"
    brief_dir.mkdir(parents=True, exist_ok=True)
    brief_path = brief_dir / "daily_brief.md"
    brief_path.write_text(
        _render_daily_brief(today, queue_lines, approvals, recent),
        encoding="utf-8",
    )
    print(f"\nBrief written to: {brief_path}")


def _render_daily_brief(
    today: dt.date,
    queue_lines: list[str],
    approvals: list[str],
    recent_actions: list[dict[str, str]],
) -> str:
    body = [
        f"# Daily Brief — {today.isoformat()}",
        "",
        "## Today's 3",
        "",
        "\n".join(queue_lines) if queue_lines else "(empty)",
        "",
        "## Approvals waiting",
        "",
        "\n".join(approvals) if approvals else "(none)",
        "",
        "## Recent revenue actions",
        "",
    ]
    if recent_actions:
        for r in recent_actions:
            body.append(
                f"- {r.get('date')} `{r.get('action_type', '?')}` "
                f"lead={r.get('lead_id', '?')} — {r.get('summary', '')}"
            )
    else:
        body.append("(none in last 24h)")
    body.append("")
    return "\n".join(body)


def stage(private_ops: str) -> None:
    """Show current stage, exit criteria, and what is missing."""
    ops = ensure_private_ops(private_ops)
    from execution_engine.evidence_scanner import scan_evidence

    report = scan_evidence(ops)
    stage_dir = ops / "stage"
    stage_dir.mkdir(parents=True, exist_ok=True)
    (stage_dir / "evidence_report.md").write_text(report.to_markdown(), encoding="utf-8")
    print(report.to_markdown())


def advance(private_ops: str) -> None:
    """Advance to the next stage if and only if exit criteria are met."""
    ops = ensure_private_ops(private_ops)
    from execution_engine.evidence_scanner import STAGES, scan_evidence
    from execution_engine.stage_checklist_updater import update_checklist

    report = scan_evidence(ops)
    checklist_path = ops / "stage" / "stage_exit_checklist.csv"
    update_checklist(checklist_path, report)

    if not report.passed:
        print(report.to_markdown())
        print("\nERROR: cannot advance — exit criteria not met.")
        raise SystemExit(1)

    current = report.stage
    idx = STAGES.index(current)
    if idx + 1 >= len(STAGES):
        print(f"Already at final stage: {current}. Nothing to advance.")
        return

    next_stage = STAGES[idx + 1]
    current_stage_file = ops / "stage" / "current_stage.md"
    current_stage_file.parent.mkdir(parents=True, exist_ok=True)
    current_stage_file.write_text(
        f"# Current stage\n\nstage: {next_stage}\nadvanced_at: {report.generated_at}\n",
        encoding="utf-8",
    )
    print(f"\nAdvanced: {current} -> {next_stage}")
    print(f"Wrote: {current_stage_file}")


def kit() -> None:
    """Verify the Revenue Sprint Kit is present and complete."""
    run_command([sys.executable, "scripts/verify_revenue_sprint_kit.py"])


def weekly_close(private_ops: str) -> None:
    """Write this week's weekly review template into the private repo."""
    ops = ensure_private_ops(private_ops)
    today = dt.date.today()
    iso_year, iso_week, _ = today.isocalendar()
    target = ops / "weekly_reviews" / f"{iso_year}-W{iso_week:02d}.md"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        print(f"Weekly review already exists: {target}")
        return

    template = REPO_ROOT / "docs" / "learning" / "LEARNING_LOOP.md"
    if not template.exists():
        print(f"ERROR: missing template {template}")
        raise SystemExit(2)

    # Extract the embedded review template (between triple-backticks).
    body = template.read_text(encoding="utf-8")
    start = body.find("```markdown\n")
    end = body.find("```", start + 1) if start != -1 else -1
    if start == -1 or end == -1:
        print("ERROR: template block not found in LEARNING_LOOP.md")
        raise SystemExit(2)
    embedded = body[start + len("```markdown\n") : end]

    embedded = embedded.replace("<ISO_week>", f"{iso_year}-W{iso_week:02d}")
    target.write_text(embedded, encoding="utf-8")
    print(f"Wrote weekly review template: {target}")
    print("Fill it in, commit one playbook update, then run `make advance`.")


def audit(private_ops: str) -> None:
    """Run the full public + private implementation audit."""
    private_ops_path = ensure_private_ops(private_ops)
    run_command([sys.executable, "scripts/audit_dealix_implementation.py"])

    private_audit = private_ops_path / "audit_private_ops.py"
    if private_audit.exists():
        run_command([sys.executable, str(private_audit)])
    else:
        template = REPO_ROOT / "templates" / "private_ops_audit_template.py"
        print(f"\nMissing private audit script: {private_audit}")
        if template.exists():
            print(f"A template is available at {template}.")
            print(f"Copy it to {private_audit} to enable private-ops checks.")
        raise SystemExit(1)
    print("\nPASS: Full Dealix implementation audit completed.")


def init(private_ops: str) -> None:
    """Bootstrap a private-ops directory with the minimum file layout."""
    ops = ensure_private_ops(private_ops)
    layout = (
        "founder/decision_queue.md",
        "founder/approvals_waiting.md",
        "founder/daily_brief.md",
        "sprint/current_sprint.md",
        "sprint/sprint_scorecard.csv",
        "stage/current_stage.md",
        "stage/stage_exit_checklist.csv",
        "stage/evidence_report.md",
        "pipeline/pipeline_tracker.csv",
        "revenue/revenue_action_log.csv",
        "offers/revenue_sprint/founder_dm_pack.md",
        "offers/revenue_sprint/sample_pack_template.md",
        "offers/revenue_sprint/proposal_fast_template.md",
        "offers/revenue_sprint/client_intake.md",
        "offers/revenue_sprint/delivery_report_template.md",
        "offers/revenue_sprint/qa_checklist.md",
        "offers/revenue_sprint/handoff_template.md",
        "offers/revenue_sprint/feedback_request.md",
        "offers/revenue_sprint/retainer_ask.md",
        "learning/weekly_intelligence_review.md",
        "weekly_reviews/template.md",
        "metrics_history/weekly_metrics.csv",
    )
    headers = {
        "pipeline/pipeline_tracker.csv": (
            "id,lead_name,company,role,segment,linkedin_url,email,phone,"
            "channel,message_version,sent_at,reply_status,next_followup,"
            "demo_booked_at,plan,payment_status,revenue_sar,notes,stage,next_action\n"
        ),
        "revenue/revenue_action_log.csv": (
            "date,action_type,lead_id,channel,summary,amount_sar,next_followup,link\n"
        ),
        "sprint/sprint_scorecard.csv": (
            "iso_week,sprint_name,client,target_metric,target_value,actual_value,status,notes\n"
        ),
        "stage/stage_exit_checklist.csv": (
            "stage,check,status,evidence,updated_at\n"
        ),
        "metrics_history/weekly_metrics.csv": (
            "iso_week,leads_added,dms_sent,replies,samples_sent,proposals_sent,"
            "payment_attempts,cash_sar,sprints_delivered,playbook_updates\n"
        ),
        "stage/current_stage.md": "# Current stage\n\nstage: setup\n",
        "stage/evidence_report.md": "# Evidence Report\n\n_Run `make stage` to populate._\n",
        "founder/daily_brief.md": "# Daily Brief\n\n_Run `make daily` to populate._\n",
    }
    for relative in layout:
        target = ops / relative
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        content = headers.get(relative, f"# {Path(relative).stem.replace('_', ' ')}\n")
        target.write_text(content, encoding="utf-8")
        print(f"created: {target.relative_to(ops)}")

    private_audit = ops / "audit_private_ops.py"
    template = REPO_ROOT / "templates" / "private_ops_audit_template.py"
    if not private_audit.exists() and template.exists():
        shutil.copyfile(template, private_audit)
        print(f"copied audit template -> {private_audit.relative_to(ops)}")

    print("\nPrivate ops initialised.")
