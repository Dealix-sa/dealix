"""Doctrine guard: the Market Production OS never auto-sends.

Reinforces non-negotiable #8 ("no external action without approval") for
the 250/day factory. The factory may produce unlimited *drafts* but must
never mark one ``sent`` or release a send without the human-approved,
ramp-capped path.
"""

from __future__ import annotations

import re
from pathlib import Path

from auto_client_acquisition.market_production_os import (
    MAX_AUTO_SENDS,
    Prospect,
    allowed_sends_today,
    produce_drafts,
    summarize_batch,
)
from auto_client_acquisition.market_production_os.schemas import SendStatus

_FACTORY = (
    Path(__file__).resolve().parents[1]
    / "auto_client_acquisition"
    / "market_production_os"
    / "draft_factory.py"
)

# Any assignment of send_status to a non-draft state inside the factory.
_FORBIDDEN_ASSIGN = re.compile(
    r"send_status\s*=\s*(SendStatus\.(SENT|QUEUED|BOUNCED)|[\"'](sent|queued|bounced)[\"'])"
)


def test_max_auto_sends_is_zero() -> None:
    assert MAX_AUTO_SENDS == 0


def test_factory_only_produces_drafts() -> None:
    drafts = produce_drafts(
        [Prospect(prospect_id="p1", company="شركة", sector="clinics")],
        offers=["Free AI Ops Diagnostic"],
        target=25,
    )
    assert drafts
    assert all(d.send_status == SendStatus.DRAFT.value for d in drafts)
    assert summarize_batch(drafts)["auto_sent"] == 0


def test_factory_source_never_assigns_sent_status() -> None:
    src = _FACTORY.read_text(encoding="utf-8")
    hits = _FORBIDDEN_ASSIGN.findall(src)
    assert not hits, f"draft_factory must never assign a non-draft send_status: {hits}"


def test_ramp_refuses_send_without_approval_or_health() -> None:
    # No approval -> 0 sends regardless of volume.
    no_approval = allowed_sends_today(
        week=4,
        approved_count=1000,
        has_approval=False,
        domain_health_ok=True,
        suppression_ok=True,
        personalization_ok=True,
    )
    assert no_approval.allowed_sends == 0
    # Bad domain health -> 0 sends.
    bad_health = allowed_sends_today(
        week=4,
        approved_count=1000,
        has_approval=True,
        domain_health_ok=False,
        suppression_ok=True,
        personalization_ok=True,
    )
    assert bad_health.allowed_sends == 0
