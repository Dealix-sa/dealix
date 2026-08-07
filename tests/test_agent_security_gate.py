"""Tests for the Agent Security Gate scanner (scripts/agent_security_gate.py)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "agent_security_gate",
    Path(__file__).resolve().parents[1] / "scripts" / "agent_security_gate.py",
)
_GATE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_GATE)


_SAFE = """\
name: Safe
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "safe build"
"""

_INJECTION = """\
name: Risky
on:
  issue_comment:
    types: [created]
permissions:
  contents: read
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ github.event.comment.body }}"
"""

_WRITE_ALL = """\
name: Broad
on: [push]
permissions: write-all
jobs:
  x:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
"""

_PR_TARGET_CHECKOUT = """\
name: Dangerous
on:
  pull_request_target:
    types: [opened]
permissions:
  contents: write
jobs:
  x:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./untrusted-script.sh
"""


def _write(tmp_path: Path, name: str, content: str) -> Path:
    d = tmp_path / "workflows"
    d.mkdir(exist_ok=True)
    p = d / name
    p.write_text(content, encoding="utf-8")
    return p


def test_safe_workflow_has_no_findings(tmp_path) -> None:
    _write(tmp_path, "safe.yml", _SAFE)
    assert _GATE.scan(tmp_path / "workflows") == []


def test_untrusted_body_into_run_is_flagged(tmp_path) -> None:
    p = _write(tmp_path, "risky.yml", _INJECTION)
    findings = _GATE.scan_workflow(p)
    assert any("injection risk" in f for f in findings)


def test_write_all_permissions_flagged(tmp_path) -> None:
    p = _write(tmp_path, "broad.yml", _WRITE_ALL)
    findings = _GATE.scan_workflow(p)
    assert any("write-all" in f for f in findings)


def test_pull_request_target_head_checkout_flagged(tmp_path) -> None:
    p = _write(tmp_path, "dangerous.yml", _PR_TARGET_CHECKOUT)
    findings = _GATE.scan_workflow(p)
    assert any("checks out PR head" in f for f in findings)


def test_repo_workflows_pass_the_gate() -> None:
    """The repository's own workflows must remain clean (no regressions)."""
    root = Path(__file__).resolve().parents[1] / ".github" / "workflows"
    assert _GATE.scan(root) == []
