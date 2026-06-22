"""Lightweight tests for P0 launch stabilization.

* Safe outbound defaults are enforced.
* No uncontrolled external send.
* Company-day required files exist.
* Command room can be generated or exact blocker is documented.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _safe_env(monkeypatch):
    monkeypatch.setenv("EXTERNAL_SEND_ENABLED", "false")
    monkeypatch.setenv("EMAIL_SEND_ENABLED", "false")
    monkeypatch.setenv("WHATSAPP_SEND_ENABLED", "false")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "false")
    monkeypatch.setenv("SMS_SEND_ENABLED", "false")
    monkeypatch.setenv("OUTBOUND_MODE", "draft_only")


def _run(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode, result.stdout, result.stderr


def test_company_launch_ready_script_exists():
    assert (REPO_ROOT / "scripts" / "verify_company_launch_ready.py").exists()


def test_no_auto_external_send_script_exists():
    assert (REPO_ROOT / "scripts" / "verify_no_auto_external_send.py").exists()


def test_company_launch_ready_runs():
    code, out, err = _run([sys.executable, "scripts/verify_company_launch_ready.py"])
    combined = out + err
    assert code == 0, f"verify_company_launch_ready failed:\n{combined}"
    assert "READY_FOR_MANUAL_OUTREACH" in combined or "NEEDS_REVIEW" in combined


def test_no_auto_external_send_runs():
    code, out, err = _run([sys.executable, "scripts/verify_no_auto_external_send.py"])
    combined = out + err
    assert code == 0, f"verify_no_auto_external_send failed:\n{combined}"


def test_command_room_builds():
    code, out, err = _run([sys.executable, "scripts/command_room/build_command_room.py"])
    combined = out + err
    assert code == 0, f"command_room build failed:\n{combined}"
    assert (REPO_ROOT / "reports" / "command_room" / "index.html").exists()


def test_safe_outbound_env_defaults():
    """Ensure env example files advertise safe defaults."""
    env_example = REPO_ROOT / ".env.example"
    text = env_example.read_text(encoding="utf-8").lower()
    assert "external_send_enabled=false" in text or "external_send_enabled" not in text
    assert "outbound_mode=draft_only" in text or "outbound_mode" not in text
    assert "whatsapp_allow_live_send=false" in text or "whatsapp_allow_live_send" not in text


def test_company_day_required_files_exist():
    required = [
        "scripts/verify_company_launch_ready.py",
        "scripts/verify_no_auto_external_send.py",
        "scripts/run_company_launch_day.py",
        "scripts/command_room/build_command_room.py",
        "scripts/revenue/run_daily_revenue_machine.py",
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    assert not missing, f"Missing required files: {missing}"
