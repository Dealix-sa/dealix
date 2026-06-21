"""Contract: the GTM CLI scripts run over the committed sample data.

These guard the quality-gate workflow: if the gate or sample drift so the known
mix changes, CI catches it here.
"""

from __future__ import annotations

from pathlib import Path

from scripts.gtm_daily_command import main as daily_main
from scripts.gtm_quality_gate import main as gate_main


def test_quality_gate_audit_mode_passes(tmp_path: Path) -> None:
    report = tmp_path / "report.md"
    rc = gate_main(["--report", str(report)])
    assert rc == 0
    text = report.read_text(encoding="utf-8")
    # The committed sample is 3 clean + 7 violating drafts.
    assert "Total drafts" in text
    assert "`d001`" in text and "`d008_guarantee`" in text


def test_quality_gate_require_all_pass_fails_on_sample() -> None:
    # The sample intentionally contains failing drafts.
    assert gate_main(["--require-all-pass"]) == 1


def test_daily_command_generates_report(tmp_path: Path) -> None:
    report = tmp_path / "cmd.md"
    rc = daily_main(["--report", str(report), "--domain-age-days", "10", "--domain-health", "healthy"])
    assert rc == 0
    text = report.read_text(encoding="utf-8")
    assert "GTM Daily Command" in text
    assert "Ramp stage" in text
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in text  # required disclaimer


def test_daily_command_blocks_on_unhealthy_domain(tmp_path: Path) -> None:
    report = tmp_path / "cmd2.md"
    rc = daily_main(["--report", str(report), "--domain-age-days", "40", "--domain-health", "bounce_spike"])
    assert rc == 0
    assert "BLOCKED" in report.read_text(encoding="utf-8")
