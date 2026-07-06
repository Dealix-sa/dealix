"""Sales qualification scorer — deterministic decision tree."""
from __future__ import annotations

from auto_client_acquisition.sales_os.qualification import Decision, qualify


def _all_yes() -> dict:
    return dict(
        pain_clear=True, owner_present=True, data_available=True,
        accepts_governance=True, has_budget=True, wants_safe_methods=True,
        proof_path_visible=True, retainer_path_visible=True,
    )


def test_full_yes_accepts():
    r = qualify(**_all_yes())
    assert r.decision == Decision.ACCEPT
    assert r.score == 100
    assert "revenue_intelligence_sprint" in r.recommended_offer or "data_to_revenue" in r.recommended_offer


def test_cold_whatsapp_request_rejected():
    args = _all_yes()
    args["raw_request_text"] = "We want cold WhatsApp automation to blast leads"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert any("whatsapp" in v for v in r.doctrine_violations)


def test_arabic_guarantee_rejected():
    args = _all_yes()
    args["raw_request_text"] = "نريد ضمان المبيعات في 30 يوم"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert any("guaranteed_sales" in v for v in r.doctrine_violations)


def test_scraping_rejected():
    args = _all_yes()
    args["raw_request_text"] = "Can you scrape LinkedIn for us?"
    r = qualify(**args)
    assert r.decision == Decision.REJECT


def test_missing_data_diagnostic_only():
    args = _all_yes()
    args["data_available"] = False
    args["owner_present"] = False
    r = qualify(**args)
    # Score around 70 — DIAGNOSTIC_ONLY territory
    assert r.decision in {Decision.DIAGNOSTIC_ONLY, Decision.REFRAME}


def test_low_score_refer_out():
    r = qualify(
        pain_clear=False, owner_present=False, data_available=False,
        accepts_governance=True, has_budget=False, wants_safe_methods=True,
        proof_path_visible=False, retainer_path_visible=False,
    )
    assert r.decision in {Decision.REJECT, Decision.REFER_OUT}


def test_no_safe_methods_adds_doctrine_flag():
    args = _all_yes()
    args["wants_safe_methods"] = False
    r = qualify(**args)
    # When wants_safe_methods=False without explicit doctrine text, we soft-flag
    assert r.decision == Decision.REJECT
    assert "declined_safe_methods" in r.doctrine_violations


# ─────────────────────────────────────────────────────────────────────────
# Doctrine phrase-list coverage — paraphrase recall + negation precision.
#
# The trigger list must catch realistic paraphrases of the same forbidden
# request (recall) WITHOUT rejecting the founder's own no-guarantee /
# no-scraping policy language, which legitimately contains the same
# keywords while refusing them (precision). Both directions are tested
# explicitly so future edits to the trigger list can't silently regress
# either one.
# ─────────────────────────────────────────────────────────────────────────


def test_guarantee_paraphrase_guarantee_us_percentage_rejected():
    """The exact real-world paraphrase found during manual CLI testing that
    slipped past the original narrow trigger list."""
    args = _all_yes()
    args["raw_request_text"] = "please guarantee us 30% revenue increase"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "guaranteed_sales" in r.doctrine_violations


def test_guarantee_paraphrase_guarantee_a_result_rejected():
    args = _all_yes()
    args["raw_request_text"] = "can you guarantee a result within a month"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "guaranteed_sales" in r.doctrine_violations


def test_guarantee_paraphrase_guaranteed_revenue_rejected():
    args = _all_yes()
    args["raw_request_text"] = "we need guaranteed revenue growth from this engagement"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "guaranteed_sales" in r.doctrine_violations


def test_scraping_paraphrase_harvest_contacts_rejected():
    args = _all_yes()
    args["raw_request_text"] = "can you harvest contacts from linkedin profiles for us"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "scraping" in r.doctrine_violations


def test_cold_whatsapp_paraphrase_bulk_whatsapp_rejected():
    args = _all_yes()
    args["raw_request_text"] = "we want to send bulk whatsapp messages to our full list"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "cold_whatsapp" in r.doctrine_violations


def test_linkedin_automation_paraphrase_auto_connect_rejected():
    args = _all_yes()
    args["raw_request_text"] = "can you auto-connect on linkedin for us automatically"
    r = qualify(**args)
    assert r.decision == Decision.REJECT
    assert "linkedin_automation" in r.doctrine_violations


def test_founders_own_no_guarantee_policy_text_not_rejected():
    """Regression test: the founder's own objection-handling script
    (sales/OBJECTION_HANDLING_AR.md) legitimately says 'لا نضمن نسبًا. نضمن
    بناء نظام قابل للقياس' ('we do not guarantee percentages; we guarantee
    building a measurable system') — this REFUSES a guarantee, it does not
    request one. If a founder pastes this into --raw-request-text (e.g.
    while drafting notes from a call), qualification must NOT reject it."""
    args = _all_yes()
    args["raw_request_text"] = "لا نضمن نسبًا. نضمن بناء نظام قابل للقياس."
    r = qualify(**args)
    assert r.decision == Decision.ACCEPT
    assert r.doctrine_violations == []


def test_english_no_guarantee_disclaimer_not_rejected():
    args = _all_yes()
    args["raw_request_text"] = (
        "We discussed that we do not guarantee any specific revenue outcome."
    )
    r = qualify(**args)
    assert r.decision == Decision.ACCEPT
    assert r.doctrine_violations == []


def test_no_scraping_policy_statement_not_rejected():
    args = _all_yes()
    args["raw_request_text"] = "The client confirmed no scraping is needed, they have a CRM export."
    r = qualify(**args)
    assert r.decision == Decision.ACCEPT
    assert r.doctrine_violations == []


def test_legitimate_linkedin_mention_without_automation_not_rejected():
    args = _all_yes()
    args["raw_request_text"] = "Their sales team already uses LinkedIn manually for outreach."
    r = qualify(**args)
    assert r.decision == Decision.ACCEPT
    assert r.doctrine_violations == []


def test_unrelated_guarantee_word_not_rejected():
    """'Guarantee' used as an unrelated general business term (e.g. a
    product warranty) must not be mistaken for a guaranteed-sales ask."""
    args = _all_yes()
    args["raw_request_text"] = "Their product comes with a standard warranty period."
    r = qualify(**args)
    assert r.decision == Decision.ACCEPT
    assert r.doctrine_violations == []
