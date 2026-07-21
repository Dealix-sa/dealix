# OKComputer / PR 559 archive intake — source-of-truth decision

## Mission

Preserve the uploaded packages as reference evidence without introducing a second Dealix runtime.

## Verified facts

- PR #559 is already merged into `main`.
- Current repository is Dealix v3 using Python/FastAPI/PostgreSQL.
- Uploaded app is a standalone v2 using TypeScript/Hono/tRPC/MySQL plus Python helpers.
- Upload files 03 and 05 are byte-for-byte duplicates with SHA-256 `0607034631d517a1259ac08c976837f1e5d385af0d8a7485c5eb01e8784c172f`.
- The current repository already contains Company OS, Approval Queue, Opportunity Graph, Revenue Intelligence Sprint, and Proof Pack capabilities.
- Uploaded API mutations are exposed through `publicQuery`; they must not enter the current runtime.

## Decision

`HOLD` wholesale merge. Preserve as reference-only and extract only capability gaps through separate tested PRs.

## Reuse candidates

- Fail-closed approval behavior.
- Sector offer-routing ideas.
- Governance checklists.
- JSON contract ideas after mapping to v3 models.
- UX references after comparing current web routes.

## Production blocker discovered during intake

- Issue #914 remains open: Vercel runtime startup is blocked by placeholder/missing production secrets.
- `/health` must return 200 twice after controlled rotation.
- Live root inspection returned the title `Dealix | Game Deals & Price Drops`; verify project/domain binding before launch.

## Safety rules

- No secret values in GitHub, logs, or comments.
- No production mutation without explicit approval.
- No live outbound.
- No merge to `main` from this intake record.

## Definition of done

- Intake decision is durably recorded.
- Original files remain preserved outside runtime code.
- Duplicate archive is identified.
- P0 production trust items remain explicit approval items.
- Any later extraction proves a missing capability, has tests, and uses Dealix v3 architecture.

## Verification addendum — 2026-07-21

A repaired, reference-only standalone artifact was produced from upload 03. Upload 05 was excluded as its byte-for-byte duplicate. This artifact is evidence and recovery material; it is not a candidate for wholesale integration into Dealix v3.

### Remediation completed in the standalone reference

- Replaced the MySQL driver and schema dialect with PostgreSQL.
- Replaced router-wide anonymous procedures with authenticated procedures and admin-only destructive/approval actions.
- Added process liveness, database readiness, Railway configuration, and a clean-database migration.
- Split OAuth and JWT secrets, removed unsafe initialization paths, fixed typed API/UI defects, and added unit tests.
- Upgraded vulnerable runtime dependencies and made CI fail on lint, tests, audit, and build failures.
- Corrected documentation so implemented foundations are not represented as production-active operations.

### Verification evidence

- `make full-verify`: passed.
- Configuration validation: 15 YAML files, 11 JSON files, and 9 JSON schemas passed.
- Python: 9 tests passed.
- Web/API: TypeScript check, ESLint, 2 Vitest tests, and production build passed.
- Production dependency audit: 0 known vulnerabilities.
- Drizzle migration consistency check: passed.
- Built-server smoke: `/health` returned 200; `/ready` returned a sanitized 503 when the database was intentionally unreachable.
- Consolidated artifact SHA-256: `feda3ec8d94a1904ffb0734335d16241407bfdc4de2cdc1c77cb198263068fbe`.

### Limits and decision

- No live PostgreSQL integration test was possible in the isolated verification environment.
- No migration was applied to an existing database.
- No production configuration, deployment, domain binding, external message, or secret was changed.
- The source-of-truth decision remains `HOLD`: do not introduce the standalone runtime into Dealix v3. Extract a capability only after proving it is absent in v3, then implement it natively with focused tests.
