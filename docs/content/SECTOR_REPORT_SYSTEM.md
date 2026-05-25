# Sector Report System — منظومة تقارير القطاعات

## Purpose
Define the quarterly sector report — methodology, scope, approval, and distribution. Sector reports build Dealix's category authority without exposing client data.

## Owner
Founder. Drafted by analyst, with sector specialist (contractor) input.

## Inputs
- Aggregated workflow observations (de-identified).
- Public sector data (MCIT, GASTAT, Tadawul, regulator publications).
- Buyer interview notes (anonymized).
- Partner observations (with written permission).

## Outputs
- Quarterly report file under `docs/sector-reports/<sector>_<YYYY-Qn>.md`.
- 1000-2000 words.
- Methodology section mandatory.
- Bilingual summary (AR + EN).

## Report Structure
1. Title (bilingual).
2. Executive summary (≤ 200 words, bilingual).
3. Methodology (sources, sample, limitations).
4. Sector overview (public data).
5. Three observations (each with evidence).
6. What we don't know (explicit uncertainty section).
7. Implications for operators (not for investors).
8. Disclosure line.

## Rules
1. No confidential client metrics. Aggregated patterns only, with minimum 5-client sample to anonymize.
2. No client name without written approval per `docs/content/CASE_STUDY_SYSTEM.md`.
3. Methodology section is mandatory; reports without methodology are not published.
4. "What we don't know" section is mandatory.
5. No conversion-rate or ROI claims as fact.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" at the bottom.
7. PDF and markdown versions; PDF watermarked with "Public" or "Partner-only" classification.

## Distribution
- Public version: LinkedIn post + downloadable PDF on owned page.
- Partner-only version (if any): named partners only, NDA in place.
- No mass email blast. No purchased lists.

## Metrics
- Reports per quarter (target 1).
- Downloads per report.
- Citations (count of inbound references).
- Qualified inbound inquiries linking to the report.

## Cadence
- Quarterly: 1 report per quarter.
- Mid-quarter: draft check.
- End-of-quarter: founder review and publish.

## Evidence
- `evidence/content/sector-reports/<sector>_<YYYY-Qn>/sources.md`.
- Sample list (anonymized).

## Verifier
Founder. Sector contractor signs methodology accuracy.

## Runtime Command
`make sector-report SECTOR=<name> Q=<YYYY-Qn>` — opens template, refuses publish without methodology and "what we don't know" sections.

## Arabic Summary — ملخص عربي
تقرير قطاع ربع سنوي، يبني السلطة دون كشف بيانات العملاء. المنهجية إلزامية، وقسم "ما لا نعرفه" إلزامي. أنماط مُجمَّعة فقط بحد أدنى خمسة عملاء. القيم التقديرية ليست مُتحقَّقة.
