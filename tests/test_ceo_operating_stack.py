"""CEO operating stack script wiring."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ceo_stack_scripts_exist() -> None:
    assert (ROOT / "scripts/run_ceo_operating_stack.sh").is_file()
    assert (ROOT / "scripts/run_ceo_operating_stack.ps1").is_file()
    assert (ROOT / "scripts/run_founder_agent_fleet_rhythm.sh").is_file()


def test_founder_agent_task_queue_yaml() -> None:
    p = ROOT / "dealix/config/founder_agent_task_queue.yaml"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "dealix-pm" in text
    assert "daily_templates" in text
