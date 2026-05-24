"""Tests for `dealix.training.workshop_builder.WorkshopBuilder`."""

from __future__ import annotations

import pytest

from dealix.training.workshop_builder import WorkshopBuilder, WorkshopDraft


def test_draft_governance_workshop_has_relevant_objectives() -> None:
    builder = WorkshopBuilder()
    draft = builder.draft(
        topic="AI governance for operators",
        audience="Operators",
        duration_hours=2.0,
    )
    assert isinstance(draft, WorkshopDraft)
    assert draft.duration_hours == 2.0
    assert any("evidence pack" in o.lower() for o in draft.learning_objectives)
    assert len(draft.agenda) >= 3
    assert draft.materials


def test_draft_sales_workshop_picks_sales_objectives() -> None:
    builder = WorkshopBuilder()
    draft = builder.draft(
        topic="Revenue Hunter playbook",
        audience="Sales",
        duration_hours=4.0,
    )
    assert any("qualification" in o.lower() for o in draft.learning_objectives)
    # 4 hours = 240 min; should produce at most 8 slots.
    assert 3 <= len(draft.agenda) <= 8


def test_draft_rejects_zero_duration() -> None:
    builder = WorkshopBuilder()
    with pytest.raises(ValueError):
        builder.draft(topic="x", audience="y", duration_hours=0.0)
