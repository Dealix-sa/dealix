"""Trust posture summary derives from incidents and open escalations."""

from __future__ import annotations

from dealix.hermes.board.trust_summary import summarize


def test_posture_clean_when_no_incidents() -> None:
    s = summarize("2026-Q1", incidents=0, escalations_resolved=2, escalations_open=0, workflows_attested=42)
    assert s.posture == "clean"


def test_posture_elevated_when_incidents_present() -> None:
    s = summarize("2026-Q1", incidents=2, escalations_resolved=1, escalations_open=5, workflows_attested=10)
    assert s.posture == "elevated"
