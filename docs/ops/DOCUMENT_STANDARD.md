# Dealix Document Standard

Every operating document inside Dealix Company OS must include the
sections below. If a document is missing any of these sections, it
is considered **not yet operational** and `verify_document_quality.py`
will flag it.

## Purpose
Why this document exists. What operating role it plays inside the
Company OS. One paragraph maximum.

## Owner
Who owns the system this document describes, today. A single named
person — not a team, not "TBD". Ownership rotates only when reassigned
explicitly in this section.

## Review Cadence
One of: `Daily`, `Weekly`, `Monthly`, `Quarterly`. The owner must
re-read and confirm the document on this cadence and update
`## Last Reviewed`.

## Inputs
What this system needs to function. Be concrete: signals, data,
decisions, customer evidence, founder direction. Bullet list.

## Outputs
What this system produces. Be concrete: decisions, drafts, dashboards,
templates, queued actions. Bullet list.

## Rules
The non-negotiables. Things that must always be true, or must never
happen. These are tested by verifiers where possible.

## Metrics
How performance of this system is measured. Each metric should have a
name and a target band (or a direction: should grow / should drop).

## Evidence
What proves this system is working. Link to files, workflows, test
output, customer feedback, payments, deliveries, decision logs.

## Last Reviewed
`YYYY-MM-DD` — date the owner last confirmed this document.

---

## Rules for using this standard

1. **No empty operating documents.** If a file exists in an operating
   folder, it must follow this standard.
2. **No "TBD" owners.** Every document has a named owner today.
3. **Public/private boundary.** Public-repo documents must not contain
   customer PII, internal financials, or private pipeline data — those
   live in the private ops repo.
4. **Evidence over claims.** The Evidence section must point to a real
   artifact, not aspirational text.
5. **Verifiers are the gate.** A document is "ready" only when
   `verify_document_quality.py` and `verify_company_os_deep.py` pass.
