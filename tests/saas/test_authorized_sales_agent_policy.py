from app.sales_intelligence.authorized_agent import (
    AuthorizationLevel,
    CompanyVoiceProfile,
    SalesAgentRequest,
    evaluate_authorized_sales_action,
)
from app.sales_intelligence.pain_radar import PainSignal, analyze_company_pain


def test_sales_agent_defaults_to_reviewable_draft():
    voice = CompanyVoiceProfile(company_name="Dealix")
    request = SalesAgentRequest(
        target_company="Demo",
        source_url="https://example.com",
        pain_hypothesis="follow_up_leakage",
        recommended_offer="Revenue Command Room Sprint",
    )
    decision = evaluate_authorized_sales_action(request, voice)
    assert decision.allowed is True
    assert decision.status == "draft_ready"


def test_sales_agent_blocks_unauthorized_identity():
    voice = CompanyVoiceProfile(
        company_name="ClientCo",
        allowed_signatory_names=("Authorized Person",),
        allowed_titles=("Sales Director",),
    )
    request = SalesAgentRequest(
        target_company="Demo",
        source_url="https://example.com",
        pain_hypothesis="follow_up_leakage",
        recommended_offer="Revenue Command Room Sprint",
        authorization_level=AuthorizationLevel.AUTHORIZED_REPRESENTATIVE,
        requested_sender_name="Unknown Person",
        requested_sender_title="CEO",
    )
    decision = evaluate_authorized_sales_action(request, voice)
    assert decision.allowed is False
    assert "not authorized" in decision.reason


def test_external_action_requires_review_and_verified_target():
    voice = CompanyVoiceProfile(company_name="Dealix")
    request = SalesAgentRequest(
        target_company="Demo",
        source_url="https://example.com",
        pain_hypothesis="follow_up_leakage",
        recommended_offer="Revenue Command Room Sprint",
        requires_external_action=True,
    )
    decision = evaluate_authorized_sales_action(request, voice)
    assert decision.allowed is False
    assert decision.status == "review_required"


def test_pain_radar_recommends_offer_from_signals():
    result = analyze_company_pain(
        [
            PainSignal(
                source="demo",
                signal_type="follow-up",
                description="WhatsApp replies are delayed and follow-up is inconsistent.",
                confidence=8,
            )
        ]
    )
    assert result.score == 8
    assert result.recommended_offer == "7-Day Revenue Command Room Sprint"
