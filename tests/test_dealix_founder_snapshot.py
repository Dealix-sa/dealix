"""Smoke tests for scripts/dealix_founder_snapshot.py.

These tests don't rely on the real verifier outcomes (which depend on
many other moving pieces in the repo). They:
  - confirm the snapshot module imports cleanly
  - confirm the verdict computation handles all three states
  - confirm main() emits the FOUNDER_SNAPSHOT_VERDICT line
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))

snap_mod = importlib.import_module("dealix_founder_snapshot")


@pytest.fixture
def fake_check_factory():
    def make(name, pass_, exit_code=0, tail="ok"):
        return snap_mod.CheckResult(
            name=name, cmd=["x"], exit_code=exit_code, pass_=pass_, tail=tail
        )
    return make


def test_verdict_green_when_all_pass(monkeypatch, fake_check_factory, capsys):
    monkeypatch.setattr(
        snap_mod,
        "_run",
        lambda name, cmd, timeout=90: fake_check_factory(name, True),
    )
    monkeypatch.setattr(sys, "argv", ["dealix_founder_snapshot.py"])
    rc = snap_mod.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "FOUNDER_SNAPSHOT_VERDICT=GREEN" in out
    assert "passed=3/3" in out


def test_verdict_red_when_none_pass(monkeypatch, fake_check_factory, capsys):
    monkeypatch.setattr(
        snap_mod,
        "_run",
        lambda name, cmd, timeout=90: fake_check_factory(name, False, exit_code=1, tail="FAIL"),
    )
    monkeypatch.setattr(sys, "argv", ["dealix_founder_snapshot.py"])
    rc = snap_mod.main()
    out = capsys.readouterr().out
    assert rc == 1
    assert "FOUNDER_SNAPSHOT_VERDICT=RED" in out


def test_verdict_amber_when_partial(monkeypatch, fake_check_factory, capsys):
    sequence = iter([True, False, True])

    def fake_run(name, cmd, timeout=90):
        return fake_check_factory(name, next(sequence))

    monkeypatch.setattr(snap_mod, "_run", fake_run)
    monkeypatch.setattr(sys, "argv", ["dealix_founder_snapshot.py"])
    rc = snap_mod.main()
    out = capsys.readouterr().out
    assert rc == 1
    assert "FOUNDER_SNAPSHOT_VERDICT=AMBER" in out
    assert "passed=2/3" in out


def test_json_flag_emits_full_payload(monkeypatch, fake_check_factory, capsys):
    monkeypatch.setattr(
        snap_mod,
        "_run",
        lambda name, cmd, timeout=90: fake_check_factory(name, True),
    )
    monkeypatch.setattr(sys, "argv", ["dealix_founder_snapshot.py", "--json"])
    rc = snap_mod.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert '"verdict": "GREEN"' in out
    assert '"checks":' in out
