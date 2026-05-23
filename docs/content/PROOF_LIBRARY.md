# Proof Library

> The single source for sanitized artifacts we can show prospects.
> Lives in `content/proof_library/` (private repo; public-safe exports curated separately).

## What Lives Here

- Sample artifacts (per `SAMPLE_GENERATION_SYSTEM.md`)
- Evidence packs (one per public claim or A3 publication)
- Sanitized case studies (post Trust signoff)
- Approved testimonials
- Sector report PDFs (after publish)
- Methodology notes

## Structure

```
content/proof_library/
├── sector/
│   ├── logistics/
│   │   ├── sample-scorecard-v{N}.pdf
│   │   ├── sample-message-set-v{N}.md
│   │   ├── sample-benchmark-v{N}.pdf
│   │   └── case-study-{pseudonym}-v{N}.md
│   ├── b2b_services/
│   └── manufacturing/
├── format/
│   ├── sample-data-pack-v{N}.pdf
│   ├── sample-evidence-pack-v{N}.pdf
│   └── sample-handoff-doc-v{N}.pdf
├── evidence_packs/
│   └── EP-YYYY-NNN/
│       ├── claim.md
│       ├── sources.md
│       ├── methodology.md
│       └── approval_log.md
├── testimonials/
│   ├── {client_pseudonym}-{date}.md
│   └── INDEX.md
└── INDEX.md
```

## Versioning

- Every artifact has a version number
- Old versions kept (audit trail)
- INDEX.md tracks which version is "current"
- Old artifacts cannot be referenced as "current" once superseded

## Entry Requirements

For an artifact to enter the library:
- claim_guard.py pass
- All client data sanitized or removed
- SAMPLE ARTIFACT header (if sample) or evidence pack manifest (if claim)
- Founder approval (A2 minimum, A3 if making a claim)
- Evidence pack on file (for any quantitative claim)

## Use Discipline

When sending an artifact to a prospect:
- Log which version was sent + when + to whom
- Use only current version
- Confirm artifact is allow-listed for the prospect's segment

## Refresh Cadence

- Per shipped sprint: refresh the matching sector sample
- Monthly: review for stale dates / URLs
- Quarterly: kill artifacts not used in 90+ days

## Cross-Reference With Other Systems

- `SAMPLE_GENERATION_SYSTEM.md` — how samples get made
- `CLAIMS_GUIDE.md` — what claims need evidence
- `CASE_STUDY_SYSTEM.md` — how case studies join the library
- `AUDIT_POLICY.md` — how the library is audited

## What This Library Refuses

- Artifacts without versioning
- Artifacts without trust signoff
- Real client data without explicit sanitization workflow
- "Just one quick edit" without re-approval
- Artifacts that exist in someone's local folder but not in the library

## Public-Safe Export

For public-safe artifacts (anonymized samples, sector reports):
- Curated subset exported to `landing/proof/` (public repo)
- Each export reviewed for safety per `PUBLIC_REPO_SAFETY.md`
- Public versions also versioned + cross-linked to private originals
