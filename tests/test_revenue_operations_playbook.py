"""Tests for the Revenue Ops Playbook v1 surface.

These cover the bits that ship as code:
- the docs verifier exits 0 against the committed docs
- the commercial score thresholds behave as specified
- the CEO action queue degrades gracefully on a fresh private dir
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_revenue_ops_docs_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_revenue_operations_playbook.py"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


@pytest.mark.parametrize(
    "metrics,expected_status,min_score",
    [
        ({}, "Revenue Setup", 0),
        ({"lead_count": 25, "contacted": 25, "replied": 5, "sample_sent": 3}, "Revenue Partial", 55),
        (
            {
                "lead_count": 25,
                "contacted": 25,
                "replied": 5,
                "sample_sent": 3,
                "proposal_sent": 1,
            },
            "Revenue Executing",
            70,
        ),
        (
            {
                "lead_count": 25,
                "contacted": 25,
                "replied": 5,
                "sample_sent": 3,
                "proposal_sent": 1,
                "paid": 1,
            },
            "Revenue Operating",
            100,
        ),
    ],
)
def test_commercial_score_thresholds(metrics, expected_status, min_score) -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from ops_runtime.commercial_score import calculate_commercial_score

    result = calculate_commercial_score(metrics)
    assert result["commercial_status"] == expected_status
    assert result["commercial_score"] >= min_score


def test_ceo_action_queue_runs_on_empty_private_ops(tmp_path: Path) -> None:
    private = tmp_path / "dealix-ops-private"
    private.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_ceo_action_queue.py",
            "--private-ops",
            str(private),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CEO Action Queue" in result.stdout
    assert "[PIPELINE]" in result.stdout
