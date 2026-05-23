# Proof Library — مكتبة الأدلة

## Purpose
The catalog of every proof artifact Dealix has — case studies, sprint logs, sector reports, screenshots, written approvals, signed SOWs. Content posts cite this library; investor pack draws from it; client conversations reference it.

## Owner
Founder. Analyst maintains the catalog.

## Inputs
- Sprint delivery artifacts.
- Case study approvals.
- Sector report sources.
- Client written approvals (separate for each use).
- Public press, awards, certifications.

## Outputs
- A single index file (this one).
- Each entry stored under `evidence/proof/<id>/`.

## Entry Schema
| Field | Description |
|---|---|
| id | PR-YYYY-NNN |
| type | sprint-log / case-study-A / case-study-B / sector-report / approval / certification / press |
| date | YYYY-MM-DD |
| owner | Founder / analyst |
| approval status | none-needed / pending / signed |
| expiry | date or none |
| public | yes / no / partner-only |
| link | relative path |
| disclosure required | yes / no |

## Catalog Sections
1. **Sprint logs** — internal, may produce case-safe public posts.
2. **Case studies — Track A (named)** — public with signed approval.
3. **Case studies — Track B (anonymized)** — public, no approval needed but labelled.
4. **Sector reports** — public.
5. **Written client approvals** — internal, references named usage scope.
6. **Certifications** — PDPL, ISO if obtained, SDAIA registrations.
7. **Press / external citations** — public.

## Rules
1. Nothing in the proof library is used externally without checking approval status and expiry.
2. PII never stored in proof artifacts.
3. Approvals re-checked at expiry; expired approvals trigger redaction.
4. Internal-only artifacts cannot be linked from public content.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" appears in any artifact citing numbers.
6. No scraped data, no purchased lists.

## Metrics
- Total artifacts (count by type).
- Approval expiry list (next 90 days).
- Citation rate (how often each artifact is reused).
- Public-safe artifact ratio.

## Cadence
- Continuous catalog update.
- Monthly approval-expiry sweep.
- Quarterly audit.

## Evidence
- This file plus per-entry folder.

## Verifier
Founder.

## Runtime Command
`make proof-audit` — lists expiring approvals, missing-approval items, mis-tagged entries.

## Arabic Summary — ملخص عربي
هذا الفهرس هو الذاكرة المرئية لشركة Dealix. لا يُستخدم أي دليل خارجيًا دون التحقق من الموافقة والانتهاء. القيم التقديرية ليست مُتحقَّقة.
