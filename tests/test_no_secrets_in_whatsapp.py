"""Doctrine guard: secrets are never requested or stored in WhatsApp text.

Mirrors the other ``tests/test_no_*`` contract guards. The WhatsApp Client OS
must (a) detect secret material and route integrations to the Secure Portal,
(b) never echo or persist a pasted secret, and (c) never emit a card or reply
that asks for a key in chat.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os import GovernanceDecision
from auto_client_acquisition.whatsapp_client_os import action_cards, brain
from auto_client_acquisition.whatsapp_client_os import session_store as store
from auto_client_acquisition.whatsapp_client_os.permission_os import secret_guard
from auto_client_acquisition.whatsapp_client_os.policy_guard import guard_outbound

# Synthetic credential-shaped value, assembled from fragments so no contiguous
# secret literal exists in source (keeps secret scanners quiet) while still
# exercising the detector at runtime.
_FAKE_KEY = "sk-" + "A1B2C3D4E5F6G7H8I9J0"


@pytest.fixture()
def tmp_stores(tmp_path, monkeypatch):
    for name in ("SESSIONS", "MESSAGES", "CARDS", "ASSESSMENTS", "PERMISSIONS"):
        monkeypatch.setenv(f"DEALIX_WHATSAPP_{name}_PATH", str(tmp_path / f"{name}.jsonl"))
    store.clear_for_test()
    yield
    store.clear_for_test()


def test_pasted_secret_is_flagged() -> None:
    assert secret_guard(f"token {_FAKE_KEY}").contains_secret


def test_outbound_guard_blocks_secret_leak() -> None:
    assert not guard_outbound(f"المفتاح هو {_FAKE_KEY}").allowed


def test_permission_card_never_asks_for_key_in_text() -> None:
    card = action_cards.permission_card("sess", integration="HubSpot")
    # The card routes to the secure portal and explicitly refuses keys in chat.
    assert "البوابة الآمنة" in card.body_ar
    assert "لا ترسل أي مفتاح" in card.body_ar
    assert any(o["id"] == "open_portal" for o in card.options)


def test_brain_does_not_persist_pasted_secret(tmp_stores) -> None:
    resp = brain.handle_message(wa_id="+966512345678", text=f"مفتاحي {_FAKE_KEY}")
    assert resp.governance_decision == GovernanceDecision.REQUIRE_APPROVAL.value
    # The raw secret must not appear in any persisted message.
    for msg in store.list_messages():
        assert _FAKE_KEY not in msg.text_redacted
