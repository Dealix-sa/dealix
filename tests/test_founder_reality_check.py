"""Founder reality check — wired anchors, absent claims, evidence truth."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from dealix.commercial_ops.founder_reality_check import (
    CLAIMED_BUT_ABSENT,
    WIRED_ANCHORS,
    audit_claimed_but_absent,
    audit_wired_anchors,
    build_reality_check,
    evidence_truth,
    next_three_honest_actions,
)
from dealix.commercial_ops.paths import REPO_ROOT


def test_wired_anchors_all_present():
    audit = audit_wired_anchors()
    assert len(audit) == len(WIRED_ANCHORS)
    missing = [a["path"] for a in audit if not a["exists"]]
    # The reality check claims these files are wired; if any goes missing,
    # the claim itself is now wrong and the test must fail loudly.
    assert not missing, f"wired anchors disappeared from repo: {missing}"


def test_claimed_but_absent_remain_absent():
    audit = audit_claimed_but_absent()
    assert len(audit) == len(CLAIMED_BUT_ABSENT)
    # The whole point of this list is to document what past sessions claimed
    # without shipping. If any item turns up locally, surface it explicitly
    # so the documentation can be updated rather than silently lying.
    surprise = [a["path"] for a in audit if a["exists"]]
    assert not surprise, (
        "documented-as-absent files were found in the repo; "
        f"update CLAIMED_BUT_ABSENT: {surprise}"
    )


def test_evidence_truth_reads_csv():
    ev = evidence_truth()
    assert "total_rows" in ev
    assert "real_rows" in ev
    assert isinstance(ev["by_type"], dict)
    assert ev["real_rows"] <= ev["total_rows"]
    assert ev["csv_path"] == "docs/commercial/operations/evidence_events_tracker.csv"
    assert (REPO_ROOT / ev["csv_path"]).is_file()


def test_build_reality_check_shape():
    snap = build_reality_check()
    for key in (
        "verdict",
        "no_build_until_first_paid",
        "wired_anchors",
        "claimed_but_absent",
        "evidence",
        "phase_0_1_gate",
        "weekly_one_decision",
        "gtm_codification",
        "pdpl_compliance_pass",
        "next_actions",
        "honesty_notes",
    ):
        assert key in snap, f"missing top-level key: {key}"

    assert snap["verdict"] in {
        "PRE_PIPELINE",
        "PIPELINE_OPEN_NO_REVENUE",
        "EVIDENCE_IN_PROGRESS",
        "GATE_OPEN",
    }
    assert snap["wired_anchors"]["present"] == len(WIRED_ANCHORS)


def test_no_build_until_first_paid_matches_gate():
    snap = build_reality_check()
    expected = not snap["phase_0_1_gate"].get("gate_open")
    assert snap["no_build_until_first_paid"] is expected


def test_next_actions_synthesizes_blocking_gates():
    # Synthetic gates so test never depends on whatever the live repo state
    # looks like. The function must surface a phase-0-1 action first when
    # the gate is closed.
    phase_gate = {
        "gate_open": False,
        "blockers_ar": ["سجّل payment_received حقيقي"],
        "phase_doc": "docs/ops/FOUNDER_PHASE_0_1_GATE_AR.md",
    }
    weekly = {"verdict": "MISSING", "expected_week_id": "2026-W21"}
    gtm = {"verdict": "OPEN", "target_deals": 10, "debriefs_with_notes": 0}
    pdpl = {"verdict": "OPEN", "done": 0, "total": 6}

    actions = next_three_honest_actions(
        phase_gate=phase_gate, weekly=weekly, gtm=gtm, pdpl=pdpl
    )
    assert len(actions) == 3
    assert "بوابة المرحلة 0–1" in actions[0]["title_ar"]
    assert "founder_weekly_decision_init.py" in actions[1]["do_ar"]


def test_next_actions_empty_when_everything_open():
    phase_gate = {"gate_open": True, "blockers_ar": []}
    weekly = {"verdict": "READY"}
    gtm = {"verdict": "READY", "target_deals": 10, "debriefs_with_notes": 10}
    pdpl = {"verdict": "PASS", "done": 6, "total": 6}
    actions = next_three_honest_actions(
        phase_gate=phase_gate, weekly=weekly, gtm=gtm, pdpl=pdpl
    )
    assert actions == []


def test_cli_human_mode_prints_verdict():
    script = REPO_ROOT / "scripts" / "founder_reality_check.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(REPO_ROOT),
    )
    # exit 0 only when GATE_OPEN; tolerate either since the gate may close
    # legitimately once a real payment lands.
    assert result.returncode in (0, 1)
    assert "FOUNDER_REALITY_CHECK_VERDICT=" in result.stdout
    assert "WIRED ANCHORS" in result.stdout
    assert "CLAIMED BUT ABSENT" in result.stdout


def test_cli_json_mode_parses():
    script = REPO_ROOT / "scripts" / "founder_reality_check.py"
    result = subprocess.run(
        [sys.executable, str(script), "--json"],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode in (0, 1)
    payload = json.loads(result.stdout)
    assert payload["verdict"]
    assert isinstance(payload["wired_anchors"]["items"], list)


def test_cli_quiet_mode_prints_only_verdict_line():
    script = REPO_ROOT / "scripts" / "founder_reality_check.py"
    result = subprocess.run(
        [sys.executable, str(script), "--quiet"],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(REPO_ROOT),
    )
    lines = [ln for ln in result.stdout.splitlines() if ln.strip()]
    assert len(lines) == 1
    assert lines[0].startswith("FOUNDER_REALITY_CHECK_VERDICT=")
