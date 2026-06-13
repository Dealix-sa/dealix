"""
Unit tests — PDPL erasure builders (Art. 13 / Art. 14).
اختبارات الوحدة — أدوات مسح البيانات وفق نظام حماية البيانات الشخصية.

Pure unit tests (no DB) against integrations/pdpl.py:
- anonymize_contact_fields() nulls PII and sets the erased marker
- build_erasure_audit_entry() shapes a PDPL Art. 13 audit entry
- ERASURE_CASCADE_ENTITIES lists the contact-graph entities
- build_data_export() produces a PDPL_DATA_EXPORT_V1 with bilingual rights
"""

from __future__ import annotations

import uuid

from integrations.pdpl import (
    CONTACT_PII_FIELDS,
    ERASURE_CASCADE_ENTITIES,
    anonymize_contact_fields,
    build_data_export,
    build_erasure_audit_entry,
)

# ── Anonymization ──────────────────────────────────────────────────


class TestAnonymizeContactFields:
    """anonymize_contact_fields nulls PII and marks the name as erased."""

    def test_email_phone_linkedin_nulled(self):
        result = anonymize_contact_fields()
        assert result["email"] is None
        assert result["phone"] is None
        assert result["linkedin_url"] is None

    def test_name_set_to_erased_marker(self):
        result = anonymize_contact_fields()
        assert result["name"] == "[ERASED]"

    def test_covers_exactly_contact_pii_fields(self):
        # The returned keys must match CONTACT_PII_FIELDS exactly — no more, no less.
        result = anonymize_contact_fields()
        assert set(result.keys()) == set(CONTACT_PII_FIELDS)
        assert set(CONTACT_PII_FIELDS) == {"name", "email", "phone", "linkedin_url"}


# ── Erasure audit entry ────────────────────────────────────────────


class TestBuildErasureAuditEntry:
    """build_erasure_audit_entry shapes a PDPL Art. 13 audit log entry."""

    def _entry(self):
        return build_erasure_audit_entry(
            contact_id="c-123",
            tenant_id="t-456",
            requesting_user_id="u-789",
            entities_erased=["contacts", "leads"],
            reason="subject_request",
        )

    def test_action_is_pdpl_erasure(self):
        assert self._entry()["action"] == "pdpl.erasure"

    def test_pdpl_article_is_art_13(self):
        assert self._entry()["diff"]["pdpl_article"] == "Art. 13"

    def test_erasure_method_is_valid(self):
        method = self._entry()["diff"]["erasure_method"]
        assert method == "cascade_soft_delete_plus_pii_null"

    def test_id_is_valid_uuid(self):
        # uuid.UUID raises ValueError on a malformed id — proves it is a valid UUID.
        entry_id = self._entry()["id"]
        assert str(uuid.UUID(entry_id)) == entry_id

    def test_entities_erased_echoes_input(self):
        assert self._entry()["diff"]["entities_erased"] == ["contacts", "leads"]

    def test_entity_and_tenant_echoed(self):
        entry = self._entry()
        assert entry["entity_type"] == "contact"
        assert entry["entity_id"] == "c-123"
        assert entry["tenant_id"] == "t-456"
        assert entry["user_id"] == "u-789"


# ── Cascade entities ───────────────────────────────────────────────


class TestErasureCascadeEntities:
    """ERASURE_CASCADE_ENTITIES must include the contact-graph entities."""

    def test_includes_contact_graph_entities(self):
        for entity in ("contacts", "leads", "conversations", "gmail_drafts", "linkedin_drafts"):
            assert entity in ERASURE_CASCADE_ENTITIES

    def test_includes_audit_relevant_logs(self):
        assert "email_send_log" in ERASURE_CASCADE_ENTITIES
        assert "outreach_queue" in ERASURE_CASCADE_ENTITIES


# ── Data export ────────────────────────────────────────────────────


class TestBuildDataExport:
    """build_data_export produces a PDPL_DATA_EXPORT_V1 with bilingual rights."""

    def _export(self):
        return build_data_export(
            contact_id="c-123",
            contact_data={"name": "Acme"},
            lead_data=[{"id": "l-1"}],
            conversation_data=[{"id": "m-1"}],
            consent_records=[{"kind": "grant"}],
            audit_records=[{"action": "pdpl.erasure"}],
        )

    def test_export_format_versioned(self):
        assert self._export()["export_format"] == "PDPL_DATA_EXPORT_V1"

    def test_your_rights_bilingual(self):
        rights = self._export()["your_rights"]
        assert isinstance(rights["ar"], list) and rights["ar"]
        assert isinstance(rights["en"], list) and rights["en"]

    def test_export_id_is_valid_uuid(self):
        export_id = self._export()["export_id"]
        assert str(uuid.UUID(export_id)) == export_id

    def test_processing_records_echo_inputs(self):
        export = self._export()
        assert export["processing_records"]["leads"] == [{"id": "l-1"}]
        assert export["processing_records"]["conversations"] == [{"id": "m-1"}]
        assert export["data_subject"]["contact_id"] == "c-123"
