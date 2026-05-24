"""Tests for the Sovereignty evaluator."""

from __future__ import annotations

import pytest

from dealix.hermes.core.schemas import Money, RiskLevel
from dealix.hermes.sovereignty import (
    Sovereignty,
    SovereigntyLevel,
    SovereigntyVerdict,
    is_blocking,
    requires_evidence_pack,
)


def test_low_risk_internal_returns_s0_autonomous() -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.LOW,
        sensitivity="internal",
        monetary_amount=None,
        external_visibility=False,
        entity_type="internal",
    )
    assert verdict.level == SovereigntyLevel.S0_AUTONOMOUS
    assert verdict.required_approvers == 0
    assert verdict.requires_evidence_pack is False


def test_medium_risk_returns_s1_notify_sami() -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.MEDIUM,
        sensitivity="internal",
        entity_type="internal",
    )
    assert verdict.level == SovereigntyLevel.S1_NOTIFY_SAMI
    assert verdict.required_approvers == 0


def test_high_risk_returns_s2_sami_approval_with_evidence_pack() -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.HIGH,
        sensitivity="confidential",
        external_visibility=True,
        entity_type="customer",
    )
    assert verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
    assert verdict.requires_evidence_pack is True
    assert verdict.required_approvers >= 1


def test_critical_risk_returns_s3_sami_only() -> None:
    verdict = Sovereignty.evaluate(risk_level=RiskLevel.CRITICAL)
    assert verdict.level == SovereigntyLevel.S3_SAMI_ONLY
    assert verdict.requires_evidence_pack is True


def test_blocked_flag_returns_s4_never_and_is_blocking() -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.LOW,
        flags={"forbidden": True},
    )
    assert verdict.level == SovereigntyLevel.S4_NEVER
    assert is_blocking(verdict.level) is True
    assert verdict.required_approvers == 2


@pytest.mark.parametrize(
    "trigger",
    [
        "sensitive_data",
        "legal_commitment",
        "strategic_partnership",
        "public_api",
        "mcp_external",
        "financial_transfer",
    ],
)
def test_each_critical_trigger_lifts_to_s3_or_higher(trigger: str) -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.LOW,
        flags={trigger: True},
    )
    if trigger == "strategic_partnership":
        # strategic_partnership lifts to S2 minimum (not S3)
        assert verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
    else:
        assert verdict.level.numeric >= SovereigntyLevel.S3_SAMI_ONLY.numeric


def test_enterprise_price_triggers_s2() -> None:
    verdict = Sovereignty.evaluate(
        risk_level=RiskLevel.LOW,
        monetary_amount=Money.sar(50_000),
    )
    assert verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric


def test_huge_amount_triggers_s4_never() -> None:
    verdict = Sovereignty.evaluate(monetary_amount=Money.sar(500_000))
    assert verdict.level == SovereigntyLevel.S4_NEVER


def test_regulated_sensitivity_lifts_to_s3() -> None:
    verdict = Sovereignty.evaluate(sensitivity="regulated")
    assert verdict.level.numeric >= SovereigntyLevel.S3_SAMI_ONLY.numeric


def test_regulator_entity_lifts_to_s3() -> None:
    verdict = Sovereignty.evaluate(entity_type="regulator")
    assert verdict.level.numeric >= SovereigntyLevel.S3_SAMI_ONLY.numeric


def test_verdict_to_dict_round_trip() -> None:
    verdict = Sovereignty.evaluate(risk_level=RiskLevel.HIGH)
    data = verdict.to_dict()
    assert data["level"] == verdict.level.value
    assert isinstance(data["reasons"], list)
    assert data["required_approvers"] == verdict.required_approvers


def test_requires_evidence_helper_for_each_level() -> None:
    assert requires_evidence_pack(SovereigntyLevel.S0_AUTONOMOUS) is False
    assert requires_evidence_pack(SovereigntyLevel.S1_NOTIFY_SAMI) is False
    assert requires_evidence_pack(SovereigntyLevel.S2_SAMI_APPROVAL) is True
    assert requires_evidence_pack(SovereigntyLevel.S3_SAMI_ONLY) is True
    assert requires_evidence_pack(SovereigntyLevel.S4_NEVER) is True


def test_sovereignty_verdict_is_frozen() -> None:
    verdict = Sovereignty.evaluate()
    assert isinstance(verdict, SovereigntyVerdict)
    with pytest.raises(Exception):
        verdict.level = SovereigntyLevel.S4_NEVER  # type: ignore[misc]
