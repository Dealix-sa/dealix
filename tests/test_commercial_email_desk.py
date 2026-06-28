"""Email desk: ingest a thread, draft a reply, always with unsubscribe."""

from __future__ import annotations

import pytest

from app.commercial import email_desk, safety
from app.commercial.schemas import CommercialAccount


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def _account():
    return CommercialAccount(
        account_id="a1",
        company_name="Acme",
        source_url="https://x.sa/c",
        source_type="client_provided",
        verification_status="verified",
        contactability_status="contactable",
        public_email="a@x.sa",
        icp_score=75.0,
        pain_hypothesis="lead follow-up",
    )


def test_ingest_and_reply_with_unsubscribe():
    thread = email_desk.ingest_thread(
        "a1", "Hello", [
            {"direction": "outbound", "from": "dealix", "body": "Hi, worth a call?"},
            {"direction": "inbound", "from": "client", "body": "Send more details and pricing"},
        ]
    )
    reply = email_desk.draft_reply(thread, _account())
    assert reply.channel == "email"
    assert "List-Unsubscribe" in reply.headers
    assert reply.subject.lower().startswith("re:")
    assert reply.send_status == "draft"
    # The drafted reply is appended to the thread as a draft, not sent.
    assert thread.messages[-1]["is_draft"] is True


def test_price_objection_in_email_is_claim_safe():
    thread = email_desk.ingest_thread(
        "a1", "Hi", [{"direction": "inbound", "from": "c", "body": "too expensive"}]
    )
    reply = email_desk.draft_reply(thread, _account())
    assert safety.contains_blocked_claim(reply.body_en) is None
    assert safety.contains_blocked_claim(reply.body_ar) is None
