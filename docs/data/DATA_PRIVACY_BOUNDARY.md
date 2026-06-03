# Data Privacy Boundary

## Purpose
Draw the line between public-safe content and private-only content for Dealix.

## Public-safe (may live in the public repo)
- Doctrine docs.
- Verifier scripts.
- Schemas.
- Templates with placeholders (no real names, emails, prices for a named client).
- Anonymized aggregate metrics if approved by Trust workflow.

## Private-only (must live in `dealix-ops-private/`)
- Real company names in any pipeline state.
- Personal contact data (names, emails, phone numbers).
- Real prices quoted to a real client.
- Real revenue numbers.
- Real client deliverables (lead tables, reports).
- Approval logs.
- Anything bearing a contractor / employee identity.

## Rule
When in doubt, treat data as private. The public boundary scanner enforces this.

## Movement between sides
- Public → private: not applicable (public stays public).
- Private → public: requires Trust workflow approval (recorded in `trust/approval_log.csv`),
  must use anonymized form, and must pass `verify_public_safety_v2.py`.

## Sharing private data with external parties
- Customers: only their own data, only via secure channels.
- Contractors: only on the minimum scope, only via private repo / cloud folder access.
- Partners: only with NDA and Trust workflow approval.

## Retention
See `docs/data/DATA_MINIMIZATION_RETENTION.md`.

## Redaction
See `docs/data/REDACTION_SYSTEM.md`.
