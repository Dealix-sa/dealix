from __future__ import annotations

"""Stage-exit evidence checks.

Each criterion is graded `pass` or `fail` against a piece of evidence on
disk. Stage 1 criteria are hard-coded — they form the "first paying client"
gate from the 90-day plan.
"""

from collections import namedtuple
from pathlib import Path

from .evidence_scanner import (
    count_csv_rows,
    count_files_in_dir,
    latest_commit_in_path,
)

EvidenceCheck = namedtuple(
    "EvidenceCheck",
    ["criterion", "status", "evidence_path", "next_action"],
)

_STATUS_PASS = "pass"
_STATUS_FAIL = "fail"


def _check_threshold(
    criterion: str,
    count: int,
    threshold: int,
    evidence: str,
    next_action: str,
) -> EvidenceCheck:
    if count >= threshold:
        return EvidenceCheck(criterion, _STATUS_PASS, evidence, "")
    return EvidenceCheck(
        criterion,
        _STATUS_FAIL,
        evidence,
        f"{next_action} (have {count} / need {threshold})",
    )


def _stage_1_checks(private_ops: Path) -> list[EvidenceCheck]:
    pipeline_csv = private_ops / "pipeline" / "pipeline_tracker.csv"
    actions_csv = private_ops / "revenue" / "revenue_action_log.csv"
    samples_dir = private_ops / "samples"
    proposals_dir = private_ops / "proposals"
    learning_dir = private_ops / "learning"

    checks: list[EvidenceCheck] = []

    # 1. 25 leads in pipeline
    checks.append(
        _check_threshold(
            "25 qualified leads in pipeline",
            count_csv_rows(pipeline_csv),
            25,
            str(pipeline_csv),
            "Add more leads to pipeline_tracker.csv",
        )
    )

    # 2. 25 DMs sent
    dms = count_csv_rows(
        actions_csv,
        filter_fn=lambda r: (r.get("action_type", "").lower() == "dm_sent"),
    )
    checks.append(
        _check_threshold(
            "25 DMs sent",
            dms,
            25,
            str(actions_csv),
            "Log DMs in revenue_action_log.csv with action_type=dm_sent",
        )
    )

    # 3. 3 samples prepared
    samples = count_files_in_dir(samples_dir)
    checks.append(
        _check_threshold(
            "3 client samples prepared",
            samples,
            3,
            str(samples_dir),
            "Prepare and store sample artefacts in samples/",
        )
    )

    # 4. 1 proposal sent
    proposals = count_files_in_dir(proposals_dir)
    checks.append(
        _check_threshold(
            "1 proposal sent",
            proposals,
            1,
            str(proposals_dir),
            "Send a proposal and store the file in proposals/",
        )
    )

    # 5. Payment / PO pursued
    payments = count_csv_rows(
        actions_csv,
        filter_fn=lambda r: (
            r.get("action_type", "").lower() in {"payment_pursued", "po_pursued"}
        ),
    )
    checks.append(
        _check_threshold(
            "Payment or PO pursued",
            payments,
            1,
            str(actions_csv),
            "Log a payment_pursued or po_pursued row in revenue_action_log.csv",
        )
    )

    # 6. Weekly learning completed
    learning = count_files_in_dir(learning_dir, "*.md")
    checks.append(
        _check_threshold(
            "Weekly learning completed",
            learning,
            1,
            str(learning_dir),
            "Write a learning note into learning/ as YYYY-MM-DD.md",
        )
    )

    # 7. One system update committed
    sha = latest_commit_in_path(private_ops)
    if sha:
        checks.append(
            EvidenceCheck(
                "One system update committed",
                _STATUS_PASS,
                str(private_ops),
                "",
            )
        )
    else:
        checks.append(
            EvidenceCheck(
                "One system update committed",
                _STATUS_FAIL,
                str(private_ops),
                "Commit at least one update inside the private ops repo",
            )
        )

    return checks


def _stage_0_checks(private_ops: Path) -> list[EvidenceCheck]:
    """Stage 0: private ops directory exists with the canonical layout."""
    expected = ["pipeline", "revenue", "stage", "founder"]
    checks: list[EvidenceCheck] = []
    for name in expected:
        sub = private_ops / name
        status = _STATUS_PASS if sub.exists() else _STATUS_FAIL
        next_action = "" if status == _STATUS_PASS else f"Create {sub}"
        checks.append(EvidenceCheck(f"{name}/ directory exists", status, str(sub), next_action))
    return checks


def check_evidence_for_stage(private_ops_path: Path, stage_num: int) -> list[EvidenceCheck]:
    """Return a list of evidence checks for the given stage.

    Unknown stages return a single placeholder check so callers can still
    render output without crashing.
    """
    private_ops_path = Path(private_ops_path)
    if stage_num == 0:
        return _stage_0_checks(private_ops_path)
    if stage_num == 1:
        return _stage_1_checks(private_ops_path)
    return [
        EvidenceCheck(
            f"Stage {stage_num} criteria not yet defined",
            _STATUS_FAIL,
            str(private_ops_path),
            "Define exit criteria for this stage",
        )
    ]
