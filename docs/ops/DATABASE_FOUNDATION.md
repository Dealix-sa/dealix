# Database Foundation

## Overview
Dealix uses SQLAlchemy 2.0 async ORM with Postgres in production and SQLite for local tests.

## Models (db/models/core.py)

### Core Models (existing)
- TenantRecord — multi-tenant isolation
- UserRecord — user auth with hashed password + role
- RoleRecord — RBAC role definitions
- AuditLogRecord — data access audit trail (PDPL Art. 18)
- LeadRecord — inbound leads
- DealRecord — deals
- CompanyRecord — subscriber company profiles
- ContactRecord — contacts with opt-out/consent
- AccountRecord — canonical company entities
- SuppressionRecord — suppression list
- OutreachQueueRecord — outreach message queue
- ConsentRequestRecord — consent management

### Operating System Models (Phase 4 additions)
- ProspectRecord — prospects with ICP scoring fields
- OutreachDraftRecord — AI-generated draft messages pending approval
- OutboundMessageRecord — queued/sent/blocked outbound messages
- OutboundEventRecord — event log for outbound messages
- DealsPipelineRecord — deals pipeline with stages and amounts
- ProposalRecord — proposals with scope, timeline, pricing
- ClientRecord — signed clients with contract details
- ClientProjectRecord — delivery projects per client
- ProofReportRecord — before/after evidence reports

## SQLite Test Mode
All models work with SQLite for local testing:
```
DATABASE_URL=sqlite+aiosqlite:///./dealix_test.db
```

## Postgres Production
```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dealix
```

## Safety Defaults
- outbound_messages.status defaults to "blocked"
- outbound_messages.safety_check_passed defaults to false
- outreach_drafts.status defaults to "draft"
- No model triggers external sending

## Migration Policy
- No destructive migrations without documentation
- Always test with SQLite locally before production
- Alembic migrations should be additive only