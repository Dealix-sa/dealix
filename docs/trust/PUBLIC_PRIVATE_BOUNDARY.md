# Public-Private Boundary — حدود العام والخاص

## Purpose
Define what lives in the public `docs/` tree and what must live in the private `dealix-ops-private/` repo. The boundary is the contract that lets us share methodology publicly without leaking client data.

## Owner
Founder.

## Inputs
- Every file being written or moved.
- Client consent records.
- Internal financial and operational data.

## Outputs
- Routing decision (public docs/ vs private repo).
- Migration list when a file is misplaced.

## Rules (numbered)
1. Default for any new file is private. Public requires explicit reasoning.
2. Client names appear in public docs only when written consent exists.
3. PII never appears in public docs. Ever.
4. Financial figures of clients never appear in public docs.
5. Internal Dealix financials never appear in public docs.
6. Methodology and policy belong in public docs (this repo).
7. Boundary violations are Sev-1 incidents.

## Metrics
- Boundary violations detected (target 0).
- Time from detection to remediation.
- Files migrated per quarter.

## Cadence
Continuous. Quarterly sweep of `docs/` for boundary violations.

## Evidence (paths)
- `docs/trust/registers/boundary_violations.md`
- `dealix-ops-private/consents/`

## Verifier
Founder.

## Runtime Command
`make trust.boundary.scan` searches public docs for boundary-violation patterns.

## What goes in public docs/

- Methodology (how a sprint runs, what a pack contains).
- Policy (this file, no-overclaim, autonomy).
- Schemas (lead table, pack manifest).
- Templates (intake, narrative, handoff, case study).
- Anonymized case studies with consent.
- Sector methodology notes (not client data).
- Public claims with linked evidence.

## What goes in dealix-ops-private/

- Active client data (intakes, lead tables, packs).
- Client names without consent.
- All PII.
- Internal financials.
- Pricing decisions and discount history.
- Consent records (PDFs, signed forms).
- A3 approval logs that reference clients.
- Internal team data.

## Boundary tests

Before writing a file to public docs/, the author runs three tests:

**1. The newspaper test.** If a journalist published this file tomorrow, would any named party have a legitimate complaint? If yes, route to private.

**2. The buyer test.** If a potential client read this file as a stranger, would they find concrete methodology they can verify, or would they find unprovable claims? If the latter, do not publish.

**3. The auditor test.** If an auditor traced every claim in this file, could they find evidence? If not, add the evidence or do not publish.

## Operating substance
The boundary is the foundation of Dealix's public reputation. The public docs/ tree is the long-form proof of how we work. The private repo is where client trust is honored. The two must never cross.

Methodology is public because methodology is non-rival. Sharing it does not weaken Dealix; the differentiation is execution. Buyers who read our methodology and decide to do it themselves were not going to hire us anyway. Buyers who read our methodology and decide we are credible become clients.

Client data is private because we made a contract, written or implied, when they engaged us. That contract does not contain a clause that lets us repurpose their data for our marketing without explicit consent. Anonymized case studies are the controlled exception, with a consent path.

When a file's home is ambiguous, default to private. Migration from private to public is reversible and cheap; migration from public to private is reputational damage that may not be undoable.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
