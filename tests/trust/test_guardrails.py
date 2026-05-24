"""Guardrail tests — positive + negative cases per detector."""

from __future__ import annotations

from dealix.trust.guardrails import (
    GuardrailChain,
    NoFalsePartnershipGuardrail,
    NoOverclaimGuardrail,
    NoSensitiveDataGuardrail,
    NoUnauthorizedPricingGuardrail,
)


def test_no_overclaim_passes_on_clean_copy() -> None:
    g = NoOverclaimGuardrail()
    result = g.check({"text": "We help SMBs in Saudi Arabia."})
    assert result.passed is True


def test_no_overclaim_blocks_guarantee_without_evidence() -> None:
    g = NoOverclaimGuardrail()
    result = g.check({"text": "We GUARANTEE results in 30 days."})
    assert result.passed is False
    assert any("guarantee" in f.lower() for f in result.findings)


def test_no_overclaim_warn_when_evidence_present() -> None:
    g = NoOverclaimGuardrail()
    result = g.check({"text": "We are number one in this region.", "evidence_ref": "epk_42"})
    assert result.passed is True
    assert result.findings  # still flagged but allowed


def test_no_sensitive_data_passes_clean_payload() -> None:
    g = NoSensitiveDataGuardrail()
    assert g.check({"text": "Hello, sending today's report."}).passed is True


def test_no_sensitive_data_blocks_pii_payload() -> None:
    g = NoSensitiveDataGuardrail()
    result = g.check(
        {"text": "Customer national id 1234567890 and IBAN SA0380000000608010167519"}
    )
    assert result.passed is False
    assert any("sa_national_id" in f for f in result.findings)
    assert any("iban" in f for f in result.findings)


def test_no_sensitive_data_allows_whitelisted_email() -> None:
    g = NoSensitiveDataGuardrail(whitelisted_email_domains={"dealix.sa"})
    assert g.check({"text": "Email me at sami@dealix.sa"}).passed is True


def test_no_sensitive_data_blocks_external_email() -> None:
    g = NoSensitiveDataGuardrail(whitelisted_email_domains={"dealix.sa"})
    assert g.check({"text": "Email me at sami@example.com"}).passed is False


def test_no_unauthorized_pricing_passes_under_threshold() -> None:
    g = NoUnauthorizedPricingGuardrail(threshold_sar=25_000)
    assert g.check({"text": "Proposal at SAR 10000."}).passed is True


def test_no_unauthorized_pricing_blocks_high_amount() -> None:
    g = NoUnauthorizedPricingGuardrail(threshold_sar=25_000)
    result = g.check({"text": "Quote: SAR 75000 for the year."})
    assert result.passed is False


def test_no_unauthorized_pricing_allows_when_approval_ref_present() -> None:
    g = NoUnauthorizedPricingGuardrail(threshold_sar=25_000)
    result = g.check(
        {"text": "Quote: SAR 75000 for the year.", "approval_ref": "apr_1"}
    )
    assert result.passed is True


def test_no_false_partnership_passes_for_registered_partner() -> None:
    g = NoFalsePartnershipGuardrail(registered_partners={"AWS"})
    assert g.check({"text": "We partnered with AWS this quarter."}).passed is True


def test_no_false_partnership_blocks_unregistered_partner() -> None:
    g = NoFalsePartnershipGuardrail(registered_partners={"AWS"})
    result = g.check({"text": "We are partnering with Microsoft on this."})
    assert result.passed is False
    assert any("microsoft" in f.lower() for f in result.findings)


def test_chain_runs_all_and_returns_collected_results() -> None:
    chain = GuardrailChain()
    results = chain.run_all(
        {
            "text": "We GUARANTEE 100% — proposal SAR 60000 — partner with Google.",
        }
    )
    assert len(results) == 4
    assert GuardrailChain.passed(results) is False


def test_chain_passes_clean_payload() -> None:
    chain = GuardrailChain(
        guardrails=[
            NoOverclaimGuardrail(),
            NoSensitiveDataGuardrail(whitelisted_email_domains={"dealix.sa"}),
            NoUnauthorizedPricingGuardrail(threshold_sar=25_000),
        ]
    )
    results = chain.run_all({"text": "Hi sami@dealix.sa — proposal at SAR 5000."})
    assert GuardrailChain.passed(results) is True
