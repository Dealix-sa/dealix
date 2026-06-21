"""Contract: the sending ramp protects domain reputation and never sends.

It plans batches from approved drafts only, enforces the ramp curve, blocks an
unhealthy domain entirely, and excludes unapproved / no-unsubscribe / suppressed
/ recently-contacted recipients.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.gtm_os.sending_ramp import (
    ApprovedDraftRef,
    plan_sending_batches,
    ramp_stage_for,
)


@pytest.mark.parametrize(
    "age,expected_cap",
    [(0, 20), (6, 20), (7, 50), (13, 50), (14, 100), (20, 100), (21, 150), (27, 150), (28, 250), (120, 250)],
)
def test_ramp_curve_caps(age: int, expected_cap: int) -> None:
    assert ramp_stage_for(age).max_per_day == expected_cap


def _approved(n: int, *, prefix: str = "d", unsubscribe: bool = True, status: str = "approved") -> list[ApprovedDraftRef]:
    return [
        ApprovedDraftRef(
            draft_id=f"{prefix}{i}",
            recipient_ref=f"rcpt_{prefix}{i}",
            unsubscribe_included=unsubscribe,
            approval_status=status,
        )
        for i in range(n)
    ]


def test_healthy_week4_allows_full_volume() -> None:
    plan = plan_sending_batches(approved=_approved(300), domain_age_days=40, domain_health="healthy")
    assert plan.effective_daily_cap == 250
    assert plan.scheduled_count == 250
    assert plan.blocked is False


def test_degraded_week4_falls_back_to_150() -> None:
    plan = plan_sending_batches(approved=_approved(300), domain_age_days=40, domain_health="warming")
    assert plan.effective_daily_cap == 150
    assert plan.scheduled_count == 150


def test_week0_caps_at_20() -> None:
    plan = plan_sending_batches(approved=_approved(100), domain_age_days=2, domain_health="healthy")
    assert plan.scheduled_count == 20
    assert plan.stage.max_per_day == 20


@pytest.mark.parametrize("bad_health", ["unhealthy", "bounce_spike", "spam_warning"])
def test_unhealthy_domain_blocks_all(bad_health: str) -> None:
    plan = plan_sending_batches(approved=_approved(50), domain_age_days=40, domain_health=bad_health)
    assert plan.blocked is True
    assert plan.scheduled_count == 0
    assert plan.governance_decision == "BLOCK"
    assert plan.batches == []


def test_excludes_unapproved_and_missing_unsubscribe() -> None:
    drafts = _approved(5) + _approved(3, prefix="na", status="approval_required") + _approved(2, prefix="nu", unsubscribe=False)
    plan = plan_sending_batches(approved=drafts, domain_age_days=10, domain_health="healthy")
    assert plan.eligible_count == 5
    assert len(plan.excluded["not_approved"]) == 3
    assert len(plan.excluded["missing_unsubscribe"]) == 2


def test_excludes_suppressed_and_recent() -> None:
    drafts = _approved(6)
    plan = plan_sending_batches(
        approved=drafts,
        domain_age_days=14,
        domain_health="healthy",
        suppression_refs={"rcpt_d0"},
        recently_contacted_refs={"rcpt_d1", "rcpt_d2"},
    )
    scheduled_ids = [ref for batch in plan.batches for ref in batch.draft_refs]
    assert "d0" not in scheduled_ids  # suppressed draft never scheduled
    assert plan.excluded["suppression_hit"] == ["d0"]
    assert set(plan.excluded["frequency_cap"]) == {"d1", "d2"}
    assert plan.eligible_count == 3


def test_batches_chunk_by_size_and_respect_cap() -> None:
    plan = plan_sending_batches(
        approved=_approved(60),
        domain_age_days=14,  # cap 100
        domain_health="healthy",
        batch_size=25,
    )
    assert plan.scheduled_count == 60
    assert [b.max_volume for b in plan.batches] == [25, 25, 10]


def test_daily_cap_override_lowers_volume() -> None:
    plan = plan_sending_batches(
        approved=_approved(100),
        domain_age_days=40,
        domain_health="healthy",
        daily_cap_override=10,
    )
    assert plan.effective_daily_cap == 10
    assert plan.scheduled_count == 10
