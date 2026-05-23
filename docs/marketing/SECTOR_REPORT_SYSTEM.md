# Sector Report System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Sector reports at Dealix are gravity assets — they pull
> sector-specific buyers into a Dealix conversation by carrying
> evidence those buyers cannot easily find elsewhere.

A sector report at Dealix is not a downloadable whitepaper. It is a
quarterly research artefact built on anonymised operating evidence,
sector observation, and named methodology. The report is the
heaviest single thing the Marketing OS produces and the most
carefully governed.

## Operating Principles

- A sector report is evidence-bearing. Every claim has a method
  and a source.
- A sector report names what Dealix does not yet know. Honest gaps
  are part of the contract.
- A sector report does not publish customer names, logos, or
  unredacted data. Patterns may be aggregated; identifiable detail
  stays in the trust ledger.
- A sector report does not promise outcomes to the reader. It
  surfaces patterns the reader can use to make their own
  decisions.
- A sector report is bilingual by default (Arabic and English).
- A sector report is gated by founder approval before publication.

## Cadence

- Quarterly per active sector.
- Sectors: founder-set, narrow by intention. A new sector is added
  only when Dealix has at least one engagement and one sector
  research partner in it.
- An off-cycle report is allowed for regulatory shifts (e.g. PDPL
  enforcement updates) and is published only if it adds new
  evidence, not new opinion.

## Sector Selection

Sectors are chosen on three criteria:

- Dealix has at least one R2+ engagement in the sector.
- A sector body, sector partner, or named contributor is available
  to review the report before publication.
- The sector is not on the founder-set refusal list.

Sectors evaluated and active are tracked in
`marketing/sector_reports.csv`. Sectors evaluated and declined are
also tracked with the decline rationale.

## Report Anatomy

Every Dealix sector report uses the same structure.

1. **Cover.** Sector, quarter, version, contributors (with
   approval).
2. **Methodology.** How the data was gathered, how anonymisation
   was applied, what the sample size is, what the limitations are.
3. **Sector posture.** A short narrative of the sector's revenue
   posture at the start of the quarter.
4. **Observed patterns.** Three to seven patterns Dealix has
   observed in the sector, each with:
   - Pattern statement.
   - Evidence (anonymised, with method).
   - Caveat (what we do not yet know).
   - Implication (what a sector operator could do with this
     pattern, framed as decision options not guarantees).
5. **Refusal list.** What this report does not claim. Useful
   counter-positioning against vendors who claim more.
6. **Honest gaps.** Areas where Dealix lacks evidence in this
   sector.
7. **Next quarter.** What Dealix will be looking at next.
8. **About Dealix.** Brand line, refusal posture, link to the
   Diagnostic.

## Evidence Discipline

Every pattern in a sector report must trace to one of:

- An anonymised audit ledger entry.
- A sector partner observation (with the partner named only if
  they have approved publication).
- A public data source (cited with link, date, and the relevant
  excerpt).
- A field interview (with the interviewee anonymised unless they
  have approved attribution).

A pattern without a traceable source is removed from the draft.

## Anonymisation

Anonymisation is applied before any pattern enters the draft.

- No company name unless the company has approved attribution.
- No revenue figures or pricing detail tied to a single
  identifiable buyer.
- No screenshots of identifiable data.
- Numerical aggregates require a minimum sample size; sample size
  is stated.
- Quotes are attributed by role and sector only, not by name,
  unless approved.

The Proof Safety Agent runs an anonymisation check against the
draft before founder review.

## Contributors

Named contributors (sector body, partner, interviewee) appear on
the cover only after approval is recorded in the trust ledger. A
contributor may withdraw before publication; the contributor's
section is then removed or rewritten without attribution.

## Distribution

- Excerpt published on the Dealix landing page (gated by lead
  capture for the full report).
- Full report distributed to a curated list: existing buyers,
  approved partners, contributors, sector body members (where the
  sector body has invited distribution).
- The report is not bought-traffic distributed. Paid amplification
  is allowed only after the readiness conditions in
  `DEALIX_MARKETING_OS.md` are met.

## Lead Capture

The download form follows the rules in
`LANDING_PAGE_CONVERSION_SYSTEM.md`: minimal fields, named CTA,
PDPL footer. Form-fills enter the lead inbox in the private ops
runtime; they are not auto-forwarded to a third-party CRM.

## Approval Flow

1. Content Strategist drafts the report with sector research.
2. Brand Guardian eval (claims-safety, brand-voice).
3. Trust Guardian eval (refusal-list, gap statement).
4. Proof Safety Agent eval (anonymisation, contributor approvals).
5. Performance Analyst review (method and sample size).
6. Founder approval — explicit, recorded in the trust ledger with
   the report version.
7. Bilingual review (Arabic and English peer-quality check).
8. Publication by a human operator.

Each step is required. A skipped step blocks publication.

## Versioning

Each report is versioned (`v1`, `v1.1`, `v2`). Corrections after
publication produce a new minor version with a visible changelog
note. Material errors trigger a retraction with a written note in
the trust ledger.

## Retention

- The PDF and source files are retained in the private ops runtime.
- The downloaded lead list is retained per the PDPL posture.
- Anonymisation transformations are retained for audit so any
  pattern can be traced back to its source under controlled
  conditions.

## Failure Modes

- Report published with an identifiable buyer reference. Failure:
  anonymisation breach. Report retracted; trust ledger records the
  retraction.
- Report published with a claim that lacks method. Failure:
  evidence breach. Report retracted; eval is upgraded.
- Contributor withdraws after publication. Failure: governance.
  Contributor section is removed in a minor version; the original
  version is retained in the audit ledger but marked deprecated.
- Report drifts into opinion. Failure: brand drift. Brand Guardian
  flags the draft; the founder recalibrates with the Content
  Strategist.

## Anti-Patterns

- "Sponsored sector report." Dealix does not accept sector report
  sponsorship that would compromise method or refusal posture.
- "Inflate sample size by aggregating across sectors." A sector
  report is sector-specific; cross-sector aggregation produces a
  different artefact.
- "Recycle last quarter's report." A report is not republished
  with cosmetic changes. Each quarter has new evidence or no
  report.
- "Use the report as a sales deck." The report is gravity, not
  pitch. Sales conversations may reference the report but do not
  read from it.

## Metrics That Matter

The Performance Analyst tracks:

- Downloads.
- Qualified conversations from downloaders.
- Sector partner participation (year over year).
- Number of approved customer references contributed to the report.
- Refusal rate (downloaders who were declined for follow-up because
  they were on a suppression list or out of scope).

Metrics not optimised for: raw download count, social shares,
press mentions.

## Localisation

Bilingual by default. Arabic is peer-quality, not translation.
Sector-specific terms in Arabic follow the Saudi business idiom in
use in the sector.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Content calendar: `docs/marketing/CONTENT_CALENDAR_SYSTEM.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Landing page system: `docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.

## Why Sector Reports

Sector reports do three things at once.

- They produce a gravity asset that a buyer cannot find elsewhere.
- They force Dealix to articulate what it knows and what it does
  not.
- They expose the trust contract to a wider audience without ever
  publishing a customer name.

A quarterly sector report is a long-arc trust signal. The buyer who
reads three of them across a year arrives at the Diagnostic
conversation already understanding how Dealix operates. That is the
conversion that matters.
