# Add database foundation for Dealix operating systems

## What This PR Adds

### Fix: OS Models Wired to Canonical Path
The previous PR (#781) added 9 new OS model classes to `db/models/core.py` —
a file inside a `db/models/` directory. However, the application imports from
`db.models`, which Python resolves to the existing `db/models.py` file. The
new directory had no `__init__.py`, so it was never imported as a package.
The OS models were orphaned and inaccessible to the application.

This PR fixes that by:
1. Appending the 9 OS model classes to `db/models.py` (the canonical import path)
2. Removing `db/models/core.py` (the orphaned duplicate)
3. Adding database foundation contract tests (5 tests)
4. Adding database foundation safety tests (6 tests)
5. Updating docs to reference the correct file path

### Models (9 new, all in db/models.py)
1. ProspectRecord — prospects with ICP scoring, source_url, verification_status, owner_decision
2. OutreachDraftRecord — AI-generated drafts with draft/approved/rejected/sent status
3. OutboundMessageRecord — queued/sent/blocked with safety_check_passed, blocked_reason
4. OutboundEventRecord — event log for sent/delivered/replied/opt_out
5. DealsPipelineRecord — pipeline with stages, amounts, probability
6. ProposalRecord — proposals with scope, timeline, total_sar
7. ClientRecord — signed clients with contract details, monthly_retainer_sar
8. ClientProjectRecord — delivery projects with acceptance_criteria
9. ProofReportRecord — before/after evidence with KPIs

### Existing Database Stack Detected
- ORM: SQLAlchemy 2.0 (async, declarative)
- Migrations: Alembic
- Test DB: SQLite (async aiosqlite)
- Production DB: Postgres 16 (async asyncpg)

### Migrations
No new Alembic migrations added. Models are ORM-only (additive).
When ready: `alembic revision --autogenerate -m "add OS tables"`

### Additive Only
- No DROP TABLE, DROP COLUMN, or TRUNCATE
- No existing models modified
- 9 new model classes appended at end of db/models.py
- No duplicate table names (verified by test)

### How Local Tests Were Run
```bash
DATABASE_URL=sqlite+aiosqlite:///./dealix_db_foundation_test.db \
  .venv/Scripts/python.exe -m pytest -q tests/test_database_foundation_contract.py tests/test_database_foundation_safety.py
```
Result: 11 passed, 0 failed

### How Production/Railway Should Run Migrations
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}} alembic revision --autogenerate -m "add OS tables"
DATABASE_URL=${{Postgres.DATABASE_URL}} alembic upgrade head
```

### Safety: No Live Outbound
- outbound_messages.status defaults to "blocked"
- outbound_messages.safety_check_passed defaults to false
- outbound_messages.mode defaults to "draft_only"
- outreach_drafts.status defaults to "draft"
- EXTERNAL_SEND_ENABLED=false, OUTBOUND_MODE=draft_only in env defaults
- No model triggers external sending

### Validation Results
- API boot: API_BOOT_OK (safe env)
- compileall: PASS (api, app, core, db, dealix, scripts)
- Contract tests: 5 passed (OS models importable, existing models preserved, no duplicates)
- Safety tests: 6 passed (defaults verified, safe env boot works)
- Pre-existing DB tests: 29 passed, 2 pre-existing failures (unrelated: needs live Postgres + payment sandbox)

### Not Included
- Alembic migration files (ORM models only — migration to be generated separately)
- Frontend changes
- API endpoint changes
- Company/Brand OS docs
- Product catalog

### Next Recommended Phase
Phase 5: Company + Brand OS