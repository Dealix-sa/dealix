from pathlib import Path

from dealix.company_os.revenue_execution import (
    CompanyRecord,
    build_revenue_case,
    build_revenue_execution,
    load_company_records,
)


def _record(**overrides: object) -> CompanyRecord:
    row: dict[str, object] = {
        "company_name": "Saudi Test Business",
        "sector": "marketing_agency",
        "city": "Riyadh",
        "website": "https://example.sa",
        "source_url": "https://example.sa/about",
        "verification_status": "verified_public",
        "owner_decision": "research_only_no_outreach",
    }
    row.update(overrides)
    return CompanyRecord.from_row(row)


def test_verified_research_seed_is_research_only_and_never_sends(tmp_path: Path) -> None:
    source = tmp_path / "synthetic_companies.csv"
    source.write_text(
        "company_name,sector,city,website,source_url,verification_status,owner_decision\n"
        + "\n".join(
            f"Synthetic Company {index},marketing_agency,Riyadh,"
            f"https://company-{index}.example,https://company-{index}.example/about,"
            "verified_public,research_only_no_outreach"
            for index in range(1, 6)
        ),
        encoding="utf-8",
    )
    records = load_company_records(source, limit=10)
    payload = build_revenue_execution(records)

    assert len(records) == 5
    assert payload["summary"]["verified_companies"] == 5
    assert payload["summary"]["research_only"] == 5
    assert payload["summary"]["provider_handoffs_eligible"] == 0
    assert payload["summary"]["external_actions_performed"] == 0
    assert all(case["dossier"]["source_url"].startswith("https://") for case in payload["cases"])


def test_research_only_creates_a_preview_but_not_contact_permission() -> None:
    case = build_revenue_case(_record())
    actions = {action["channel"]: action for action in case["channel_plan"]}

    assert actions["email"]["status"] == "research_preview"
    assert actions["email"]["can_provider_handoff"] is False
    assert "target_level_owner_decision" in actions["email"]["required_conditions"]
    assert actions["whatsapp"]["status"] == "blocked"
    assert "verified_whatsapp_opt_in" in actions["whatsapp"]["required_conditions"]


def test_email_handoff_requires_every_target_level_gate() -> None:
    case = build_revenue_case(
        _record(
            owner_decision="approved_to_send",
            contact_present=True,
            contact_channel="email",
            consent_status="opted_in",
            consent_proof_url="https://crm.example/consent/123",
            human_approved=True,
            live_gate=True,
        )
    )
    email = next(action for action in case["channel_plan"] if action["channel"] == "email")

    assert email["status"] == "approved_provider_handoff"
    assert email["action_mode"] == "controlled_handoff"
    assert email["can_provider_handoff"] is True
    assert email["required_conditions"] == ()


def test_opt_out_overrides_email_approval() -> None:
    case = build_revenue_case(
        _record(
            owner_decision="approved_to_send",
            contact_present=True,
            contact_channel="email",
            consent_status="opted_in",
            consent_proof_url="https://crm.example/consent/123",
            human_approved=True,
            live_gate=True,
            opted_out=True,
        )
    )
    email = next(action for action in case["channel_plan"] if action["channel"] == "email")

    assert email["status"] == "blocked"
    assert email["can_provider_handoff"] is False


def test_linkedin_is_manual_even_when_target_is_approved() -> None:
    case = build_revenue_case(
        _record(
            owner_decision="founder_approved",
            contact_present=True,
            contact_channel="linkedin",
            human_approved=True,
            live_gate=True,
        )
    )
    linkedin = next(action for action in case["channel_plan"] if action["channel"] == "linkedin")

    assert linkedin["status"] == "pending_manual_review"
    assert linkedin["can_provider_handoff"] is False
    assert "human_final_send_required" in linkedin["required_conditions"]


def test_whatsapp_can_only_reach_approved_manual_handoff_after_opt_in() -> None:
    case = build_revenue_case(
        _record(
            owner_decision="approved_to_send",
            contact_present=True,
            contact_channel="whatsapp",
            relationship_status="inbound",
            consent_status="opted_in",
            consent_proof_url="https://crm.example/consent/wa-123",
            approved_template_or_24h_window=True,
            human_approved=True,
            live_gate=True,
        )
    )
    whatsapp = next(action for action in case["channel_plan"] if action["channel"] == "whatsapp")

    assert whatsapp["status"] == "approved_manual_handoff"
    assert whatsapp["can_provider_handoff"] is True
    assert whatsapp["required_conditions"] == ()


def test_qualified_positive_reply_unlocks_proposal_and_booking_review() -> None:
    case = build_revenue_case(
        _record(
            owner_decision="founder_approved",
            contact_present=True,
            contact_channel="email",
            reply_intent="meeting_request",
            qualification_status="qualified",
            human_approved=True,
        )
    )

    assert case["qualification"]["status"] == "qualified"
    assert case["proposal"]["status"] == "ready_for_founder_review"
    assert case["proposal"]["final_price_commitment"] is False
    assert case["booking"]["status"] == "ready_for_calendar_handoff"
    assert case["booking"]["provider_write_performed"] is False


def test_price_or_contract_reply_creates_human_decision_alerts() -> None:
    case = build_revenue_case(
        _record(
            reply_text="السعر غالي ونحتاج خصم ومراجعة شروط العقد",
            reply_intent="send_details",
        )
    )
    topics = {alert["topic"] for alert in case["decision_alerts"]}

    assert {"pricing_or_discount", "legal_or_contract"}.issubset(topics)
    assert all(alert["risk_level"] == "high" for alert in case["decision_alerts"])
    assert all("final_price" in alert["restricted_commitments"] for alert in case["decision_alerts"])
