"""Database foundation contract tests.

Verifies that the required OS model classes exist and are importable
from db.models, and that no duplicate/conflicting model definitions
exist.
"""

import pytest


def test_os_models_importable():
    """All 9 OS model classes must be importable from db.models."""
    from db.models import (
        ProspectRecord,
        OutreachDraftRecord,
        OutboundMessageRecord,
        OutboundEventRecord,
        DealsPipelineRecord,
        ProposalRecord,
        ClientRecord,
        ClientProjectRecord,
        ProofReportRecord,
    )
    assert ProspectRecord.__tablename__ == "prospects"
    assert OutreachDraftRecord.__tablename__ == "outreach_drafts"
    assert OutboundMessageRecord.__tablename__ == "outbound_messages"
    assert OutboundEventRecord.__tablename__ == "outbound_events"
    assert DealsPipelineRecord.__tablename__ == "deals_pipeline"
    assert ProposalRecord.__tablename__ == "proposals"
    assert ClientRecord.__tablename__ == "clients"
    assert ClientProjectRecord.__tablename__ == "client_projects"
    assert ProofReportRecord.__tablename__ == "proof_reports"


def test_existing_models_still_importable():
    """Existing core models must still be importable (no regression)."""
    from db.models import (
        Base,
        TenantRecord,
        UserRecord,
        LeadRecord,
        DealRecord,
        CompanyRecord,
        ContactRecord,
        AuditLogRecord,
    )
    assert TenantRecord.__tablename__ == "tenants"
    assert UserRecord.__tablename__ == "users"
    assert LeadRecord.__tablename__ == "leads"
    assert DealRecord.__tablename__ == "deals"
    assert CompanyRecord.__tablename__ == "companies"
    assert ContactRecord.__tablename__ == "contacts"
    assert AuditLogRecord.__tablename__ == "audit_logs"


def test_no_duplicate_table_names():
    """No two model classes should share the same __tablename__."""
    from db.models import Base
    table_names = []
    for mapper in Base.registry.mappers:
        table = mapper.local_table
        if table is not None:
            table_names.append(table.name)
    duplicates = [name for name in table_names if table_names.count(name) > 1]
    assert len(duplicates) == 0, f"Duplicate table names found: {set(duplicates)}"


def test_prospect_has_source_url():
    """ProspectRecord must have source_url field."""
    from db.models import ProspectRecord
    assert hasattr(ProspectRecord, "source_url")


def test_outbound_message_has_safety_fields():
    """OutboundMessageRecord must have safety_check_passed and blocked_reason."""
    from db.models import OutboundMessageRecord
    assert hasattr(OutboundMessageRecord, "safety_check_passed")
    assert hasattr(OutboundMessageRecord, "blocked_reason")