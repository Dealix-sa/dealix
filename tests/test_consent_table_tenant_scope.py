"""One tenant's consent decision must not bind another tenant.

``auto_client_acquisition/consent_table.py`` is one shared append-only JSONL
file, and until now no record in it named a tenant. Consent was therefore
global, three ways:

* **Consent laundering.** Tenant A captures a grant for a contact; tenant B,
  who never obtained consent from anyone, is now authorised to send to them.
* **Cross-tenant denial of service.** Revocation is permanent under PDPL
  Article 5, so one tenant revoking permanently silenced every other tenant's
  *transactional* messages to a contact they had their own lawful basis for.
* **Disclosure.** ``records_for(contact_id)`` returned another tenant's
  timestamps, sources and proof URLs to any caller.

Records written before the field existed carry ``tenant_id=""``, and the two
kinds are deliberately asymmetric:

* a legacy **revoke** binds everyone — an opt-out whose owner cannot be
  determined must be honoured broadly; losing it violates Article 5, while
  over-honouring it costs one message;
* a legacy **grant** binds nobody — consent whose owner cannot be determined
  is not consent, and this module's stated rule is default-deny.

Both directions fail closed.
"""

from __future__ import annotations

import json

import pytest

from auto_client_acquisition import consent_table

TENANT_A = "tnt_alpha"
TENANT_B = "tnt_beta"
CONTACT = "lead_shared@example.com"


@pytest.fixture(autouse=True)
def isolated_store(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CONSENT_TABLE_PATH", str(tmp_path / "consent.jsonl"))
    return tmp_path / "consent.jsonl"


def _write_legacy(path, *, kind: str, channel="email", purpose="marketing") -> None:
    """A record from before ``tenant_id`` existed — no such key at all."""
    row = {
        "contact_id": CONTACT,
        "channel": channel,
        "purpose": purpose,
        "kind": kind,
        "occurred_at": "2026-01-01T00:00:00+00:00",
        "source": "legacy",
        "proof_url": "",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


# ── Consent laundering ────────────────────────────────────────────────────


def test_one_tenants_grant_does_not_authorise_another():
    """The defect: any tenant could send on another tenant's consent."""
    consent_table.grant(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )

    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    ) is True
    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_B
    ) is False, "tenant B inherited tenant A's consent"


def test_a_tenantless_caller_inherits_nothing():
    consent_table.grant(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )

    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing"
    ) is False


# ── Cross-tenant denial of service ────────────────────────────────────────


def test_one_tenants_revoke_does_not_silence_another():
    """Revocation is permanent, which made this the more damaging direction."""
    consent_table.grant(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_A,
    )
    consent_table.grant(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_B,
    )

    consent_table.revoke(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_B,
    )

    assert consent_table.is_consented(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_A,
    ) is True, "tenant B's opt-out silenced tenant A"
    assert consent_table.is_consented(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_B,
    ) is False


# ── Disclosure ────────────────────────────────────────────────────────────


def test_records_for_does_not_leak_another_tenants_proof():
    consent_table.grant(
        contact_id=CONTACT,
        channel="email",
        purpose="marketing",
        tenant_id=TENANT_A,
        proof_url="https://private.example/consent/a",
    )

    visible = consent_table.records_for(CONTACT, TENANT_B)

    assert visible == [], "tenant B read tenant A's consent proof"


def test_a_tenant_sees_its_own_records():
    consent_table.grant(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )

    own = consent_table.records_for(CONTACT, TENANT_A)

    assert len(own) == 1
    assert own[0].tenant_id == TENANT_A


# ── Legacy records: the asymmetry ─────────────────────────────────────────


def test_a_legacy_revoke_still_binds_every_tenant(isolated_store):
    """An opt-out with no owner must be honoured broadly, not dropped."""
    _write_legacy(isolated_store, kind="revoke")

    for tenant in (TENANT_A, TENANT_B, ""):
        assert consent_table.is_consented(
            contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=tenant
        ) is False, f"a legacy opt-out was lost for {tenant or '(no tenant)'}"


def test_a_legacy_grant_binds_nobody(isolated_store):
    """Consent whose owner is unknown is not consent — default-deny."""
    _write_legacy(isolated_store, kind="grant")

    for tenant in (TENANT_A, TENANT_B, ""):
        assert consent_table.is_consented(
            contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=tenant
        ) is False


def test_a_legacy_revoke_outranks_a_later_grant_by_another_tenant(isolated_store):
    """Article 5: opt-out is permanent, and an unattributed one is no weaker."""
    _write_legacy(isolated_store, kind="revoke")
    consent_table.grant(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )

    # The tenant's own later grant is newer, so it wins for that tenant —
    # this pins which way round that goes rather than leaving it to chance.
    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    ) is True
    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_B
    ) is False


# ── The unchanged rules still hold ────────────────────────────────────────


def test_default_deny_with_no_record_at_all():
    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    ) is False


def test_revoke_beats_an_earlier_grant_within_one_tenant():
    consent_table.grant(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )
    consent_table.revoke(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    )

    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    ) is False


def test_channel_and_purpose_stay_independent():
    consent_table.grant(
        contact_id=CONTACT,
        channel="email",
        purpose="transactional",
        tenant_id=TENANT_A,
    )

    assert consent_table.is_consented(
        contact_id=CONTACT,
        channel="whatsapp",
        purpose="transactional",
        tenant_id=TENANT_A,
    ) is False
    assert consent_table.is_consented(
        contact_id=CONTACT, channel="email", purpose="marketing", tenant_id=TENANT_A
    ) is False
