# Database Foundation Report

## Date: 2026-06-23
## Branch: phase/database-foundation-fix

## What Was Fixed
The previous PR (#781) added 9 new OS models to `db/models/core.py` — a new
file in a `db/models/` directory. However, the application imports from
`db.models` which Python resolves to the existing `db/models.py` file (the
directory `db/models/` had no `__init__.py`, so it was never imported as a
package). The new models were orphaned.

This PR fixes that by:
1. Appending the 9 OS model classes to `db/models.py` (the canonical path)
2. Removing `db/models/core.py` (the orphaned duplicate)
3. Adding database foundation contract + safety tests
4. Updating docs to reference the correct file path

## Existing Database Stack
- ORM: SQLAlchemy 2.0 (async, declarative)
- Migrations: Alembic
- Test DB: SQLite (async aiosqlite)
- Production DB: Postgres 16 (async asyncpg)
- Session: db/session.py

## Models Added (9 OS models, now in db/models.py)
1. ProspectRecord — prospects table with ICP scoring, verification_status, owner_decision
2. OutreachDraftRecord — outreach_drafts table with draft/approved/rejected/sent status
3. OutboundMessageRecord — outbound_messages table with safety_check_passed, blocked_reason
4. OutboundEventRecord — outbound_events table for sent/delivered/replied/opt_out events
5. DealsPipelineRecord — deals_pipeline table with stages, amounts, probability
6. ProposalRecord — proposals table with scope, timeline, total_sar, status
7. ClientRecord — clients table with contract details, monthly_retainer_sar
8. ClientProjectRecord — client_projects table with delivery status, acceptance_criteria
9. ProofReportRecord — proof_reports table with before/after state, KPIs

## Existing Models Preserved
All 40+ existing models in db/models.py remain unchanged. The 9 new models
were appended at the end of the file.

## Files Inspected
- db/models.py — canonical model file (1040 -> 1215 lines)
- db/session.py — async session factory
- db/migrations/ — Alembic migrations directory
- alembic.ini — Alembic config
- api/main.py — FastAPI app (imports from db.models)
- core/config/settings.py — app settings

## Migrations
No new Alembic migrations added. Models are defined in Python ORM only.
When ready for production, create an additive migration:
```
alembic revision --autogenerate -m "add OS tables"
alembic upgrade head
```

## Compatibility Notes
- SQLite test mode: works (async aiosqlite)
- Postgres production: works (async asyncpg)
- No destructive migrations
- No duplicate table names (verified by test)
- All existing imports from db.models still work (verified by test)

## Local Migration
```bash
DATABASE_URL=sqlite+aiosqlite:///./dealix_test.db alembic upgrade head
```

## Railway Migration
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}} alembic upgrade head
```

## Rollback Notes
- To rollback: `alembic downgrade -1`
- No destructive operations in this PR
- Models are additive only

## Safety
- outbound_messages.status defaults to "blocked"
- outbound_messages.safety_check_passed defaults to false
- outbound_messages.mode defaults to "draft_only"
- outreach_drafts.status defaults to "draft"
- No model triggers external sending
- EXTERNAL_SEND_ENABLED=false, OUTBOUND_MODE=draft_only in env defaults

## Test Results
- tests/test_database_foundation_contract.py: 5 passed
- tests/test_database_foundation_safety.py: 6 passed
- Total: 11 passed, 0 failed
- compileall: PASS
- API boot: PASS (safe env)