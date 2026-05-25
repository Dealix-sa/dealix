# Evidence System — نظام الأدلة

## Purpose
Establish the rule that every public claim Dealix makes is linked to a verifiable evidence path. Define where evidence lives, how it is reviewed, and how stale evidence is handled.

## Owner
Founder.

## Inputs
- Public claims in `docs/`, website, sales decks, case studies.
- Source URLs, screenshots, signed consent files, validation logs.

## Outputs
- Claim register: `docs/trust/registers/claim_register.md`.
- Evidence index per claim with path and last-verified date.

## Rules (numbered)
1. Every public claim has a claim ID and an evidence row.
2. Evidence must be reproducible by someone outside Dealix (public URL, signed file, or methodology citation).
3. Evidence with a URL is re-verified every 90 days. Dead links trigger a review.
4. Evidence that cannot be made public stays in `dealix-ops-private/` and the public claim is reframed accordingly.
5. Claims without evidence are removed within 7 days of detection.
6. New claims require evidence before they reach G2 publish.

## Metrics
- Claim coverage: percent of public claims with linked evidence (target 100).
- Stale evidence rate (older than 90 days, not re-verified).
- Removed-without-evidence count per quarter.

## Cadence
Quarterly full sweep. Continuous for new claims.

## Evidence (paths)
- `docs/trust/registers/claim_register.md`
- `docs/trust/registers/evidence_reviews/<quarter>.md`

## Verifier
Founder.

## Runtime Command
`make trust.evidence.audit` scans public docs for claim patterns and reconciles them against the register.

## Claim register row format

```
claim_id: CLM-NNNN
claim_text: <the exact sentence as published>
source_doc: <path/to/the/public/file.md>
evidence_path: <path/to/evidence>
evidence_type: url | screenshot | consent_file | methodology_citation | validation_log
last_verified: YYYY-MM-DD
verifier: <initials>
status: active | retired | under_review
```

## Evidence types

**URL.** Public URL that supports the claim. Re-verified every 90 days. Archived to internal cache on first capture so a dead link does not erase the support.

**Screenshot.** Used when a URL renders dynamic content. Capture includes URL, timestamp, and the visible content. Stored in private repo if it includes any client material.

**Consent file.** Signed PDF stored privately. Public claim references the existence of the consent without exposing it.

**Methodology citation.** When a claim is about how Dealix works (not an external fact), the evidence is a path to the relevant methodology file in this repo.

**Validation log.** When a claim is about a system behavior (schema validation, scanner passes), the evidence is the log file path.

## Operating substance
The Evidence System is what makes Dealix's no-overclaim policy operable. Without an evidence path attached to each claim, the policy is aspirational. With the register, the policy becomes audit-ready in minutes.

The 90-day re-verification cycle exists because the web ages. URLs go dark, organizations restructure, sources move. A claim that was true and supported in March 2026 may be unsupported by July 2026 not because Dealix changed but because the source changed. We catch this on cadence.

When evidence cannot be made public, the claim is reframed. We do not say "client X grew Y percent" with a private consent file; we say "in an engagement under NDA, the methodology produced outputs the client described as material; consent for naming is not granted". The honesty of the reframing is the evidence.

The register is also the input to the public-private boundary sweep. A claim whose only evidence is private but which is published publicly without consent is a Sev-1 violation.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
