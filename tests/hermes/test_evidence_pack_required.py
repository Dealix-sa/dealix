"""Guard test — evidence-pack requirement by sovereignty level.

Spec §40: sovereignty levels at or above S2 must carry an EvidencePack
before they reach Sami's queue. S0/S1 do not. S4 also requires one (it's
blocked, but the pack documents *why*).
"""

from __future__ import annotations

import pytest

from dealix.hermes.sovereignty import (
    Sovereignty,
    SovereigntyLevel,
    requires_evidence_pack,
)


@pytest.mark.parametrize(
    "level,expected",
    [
        (SovereigntyLevel.S0_AUTONOMOUS, False),
        (SovereigntyLevel.S1_NOTIFY_SAMI, False),
        (SovereigntyLevel.S2_SAMI_APPROVAL, True),
        (SovereigntyLevel.S3_SAMI_ONLY, True),
        (SovereigntyLevel.S4_NEVER, True),
    ],
)
def test_requires_evidence_pack_table(
    level: SovereigntyLevel, expected: bool
) -> None:
    assert requires_evidence_pack(level) is expected


def test_low_risk_evaluator_does_not_require_evidence() -> None:
    verdict = Sovereignty.evaluate(
        risk_level="low",
        sensitivity="internal",
        monetary_amount=None,
        external_visibility=False,
        entity_type="internal",
    )
    assert verdict.level == SovereigntyLevel.S0_AUTONOMOUS
    assert verdict.requires_evidence_pack is False


def test_high_value_action_requires_evidence() -> None:
    # Enterprise-price monetary trigger → S2_SAMI_APPROVAL → evidence required.
    verdict = Sovereignty.evaluate(
        risk_level="medium",
        sensitivity="commercial",
        monetary_amount=30_000,
        external_visibility=True,
        entity_type="customer",
    )
    assert verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
    assert verdict.requires_evidence_pack is True
    assert verdict.required_approvers >= 1


def test_regulated_data_routes_to_s3_with_evidence() -> None:
    verdict = Sovereignty.evaluate(
        risk_level="high",
        sensitivity="regulated",
        monetary_amount=None,
        external_visibility=True,
        entity_type="regulator",
    )
    assert verdict.level == SovereigntyLevel.S3_SAMI_ONLY
    assert verdict.requires_evidence_pack is True
