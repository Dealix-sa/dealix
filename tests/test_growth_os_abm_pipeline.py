"""ABM pipeline + AccountCard tests."""

from __future__ import annotations

import pytest

from dealix.growth_os.abm.account_card import AccountCard, Stakeholder
from dealix.growth_os.abm.agent_roster import ABM_AGENT_ROSTER, list_agents
from dealix.growth_os.abm.pipeline import ABM_STAGES, ABMPipeline, advance_stage


def _sample() -> AccountCard:
    return AccountCard(
        account_id="acc_001",
        account_label="Agency X",
        icp_key="agencies",
        stage="target",
        stakeholders=[
            Stakeholder(role="founder", influence="champion", notes=""),
        ],
    )


def test_abm_stages_have_all_required_steps() -> None:
    expected = (
        "target",
        "research",
        "pain_hypothesis",
        "stakeholder_map",
        "personalized_offer",
        "message",
        "followup",
        "proposal",
        "deal_room",
        "outcome",
    )
    assert expected == ABM_STAGES


def test_advance_stage_moves_one_step_and_is_idempotent_at_end() -> None:
    card = _sample()
    assert card.stage == "target"
    nxt = advance_stage(card)
    assert nxt.stage == "research"

    final = AccountCard.model_validate({**card.model_dump(), "stage": "outcome"})
    assert advance_stage(final).stage == "outcome"


def test_advance_stage_unknown_raises() -> None:
    bad = AccountCard.model_validate({**_sample().model_dump(), "stage": "nope"})
    with pytest.raises(ValueError):
        advance_stage(bad)


def test_pipeline_count_by_stage() -> None:
    pipeline = ABMPipeline(
        accounts=[
            _sample(),
            AccountCard.model_validate({**_sample().model_dump(), "account_id": "acc_002", "stage": "research"}),
        ]
    )
    counts = pipeline.count_by_stage()
    assert counts["target"] == 1
    assert counts["research"] == 1
    assert counts["outcome"] == 0


def test_agent_roster_contains_required_personas() -> None:
    required = {
        "account_research",
        "stakeholder_mapper",
        "pain_hypothesis",
        "personalized_pitch",
        "followup",
        "deal_room",
    }
    assert required.issubset(set(ABM_AGENT_ROSTER.keys()))
    assert len(list_agents()) >= 6
