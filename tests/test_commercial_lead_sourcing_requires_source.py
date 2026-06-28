"""Lead sourcing must never treat a source-less lead as send-ready."""

from __future__ import annotations

from app.commercial import lead_sourcing


def test_missing_source_url_is_unverified_and_not_send_ready():
    [acc] = lead_sourcing.load_accounts(
        [{"company_name": "No Source Co", "public_email": "x@y.com"}]
    )
    assert acc.source_url == ""
    assert acc.verification_status == "unverified"
    assert lead_sourcing.is_send_ready(acc) is False


def test_valid_source_becomes_verified_and_contactable():
    [acc] = lead_sourcing.load_accounts(
        [
            {
                "company_name": "Good Co",
                "source_url": "https://example.com/contact",
                "source_type": "public_website",
                "public_email": "hello@example.com",
            }
        ]
    )
    assert acc.verification_status == "verified"
    assert acc.contactability_status == "contactable"
    assert lead_sourcing.is_send_ready(acc) is True


def test_disallowed_source_type_is_rejected():
    [acc] = lead_sourcing.load_accounts(
        [
            {
                "company_name": "Bad Source",
                "source_url": "https://example.com",
                "source_type": "purchased_list",
                "public_email": "x@y.com",
            }
        ]
    )
    assert acc.verification_status == "rejected"
    assert lead_sourcing.is_send_ready(acc) is False


def test_opted_out_account_not_send_ready():
    [acc] = lead_sourcing.load_accounts(
        [
            {
                "company_name": "Opted Out",
                "source_url": "https://example.com",
                "source_type": "client_provided",
                "public_email": "x@y.com",
                "email_opt_out": True,
                "contactability_status": "opted_out",
            }
        ]
    )
    assert lead_sourcing.is_send_ready(acc) is False
