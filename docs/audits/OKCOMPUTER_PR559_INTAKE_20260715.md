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

