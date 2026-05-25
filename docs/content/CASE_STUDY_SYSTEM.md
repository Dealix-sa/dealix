# Case Study System — منظومة دراسات الحالة

## Purpose
Define how case studies are produced, approved, and published. Every case study is either named-with-written-approval or labelled "Hypothetical / case-safe template". No fabrication, no implied customers.

## Owner
Founder. Drafted by analyst.

## Inputs
- Delivery ledger and SOW.
- Written client approval (signed) for named case studies.
- Outcome metrics with verified values.
- `docs/content/PROOF_LIBRARY.md` entry.

## Outputs
- Case study file under `docs/case-studies/case_NNN_anonymized.md` or `case_NNN_named.md`.
- Quote, outcome, methodology, scope, disclosure.

## Two Tracks
### Track A — Named Case Study
- Requires written client approval signed by an authorized signatory.
- Approval covers: client name, logo (if used), outcome numbers, quotes.
- Approval valid for 24 months; renewal required after.
- Stored under `evidence/case-studies/<id>/approval.pdf`.

### Track B — Anonymized / Hypothetical
- Used when no client approval, or when the pattern is composite.
- Header must include the line: "Hypothetical / case-safe template — نمط افتراضي مُؤمَّن".
- No detail that identifies the client (sector size + region only).
- No real revenue numbers; ranges only.

## Case Study Structure
1. Title (bilingual).
2. Context (sector, scale band).
3. Problem (one paragraph).
4. Scope (bullet list).
5. Approach (methodology, references to internal playbooks).
6. Outcome (verified numbers if Track A; ranges if Track B).
7. What did not work (mandatory section).
8. Lessons (bilingual).
9. Disclosure line.

## Rules
1. No named case study without signed approval.
2. No PII (email, phone, national ID) in any case study.
3. "Hypothetical / case-safe template" header is mandatory on Track B.
4. No promises of repeat outcomes.
5. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" appears at the bottom.
6. No outbound automation, scraping, or cold blast described as a service.
7. Length 500-700 words.

## Metrics
- Case studies published per quarter (target 1 Track A, 2 Track B).
- Approval lead time (target ≤ 14 days).
- Renewal rate of named approvals.
- Inbound citations of case studies.

## Cadence
- Drafted within 30 days of sprint close.
- Quarterly review of approval validity.

## Evidence
- Signed approval PDF.
- Source delivery artifacts.

## Verifier
Founder counter-signs.

## Runtime Command
`make case-study CASE=<id>` — opens template, checks for approval evidence, refuses publish on missing approval.

## Arabic Summary — ملخص عربي
دراسات الحالة إما باسم العميل بموافقة مكتوبة، أو افتراضية مُؤمَّنة بوسم صريح. لا بيانات شخصية. لا وعود بنتائج مكررة. القيم التقديرية ليست مُتحقَّقة.
