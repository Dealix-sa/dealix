# Sector Report System

Sector reports are Dealix's most powerful trust-building artifact. They demonstrate that Dealix understands a specific Saudi B2B sector through methodology, not assertion.

**Source of truth:** `$PRIVATE_OPS/sector_report_state.csv`
**Owner:** Marketing Lead + Founder
**Trust gate:** A2 — sector reports are externally published artifacts; founder approval is required at publish.

## What a sector report is

A 1,000-2,000-word study of one Saudi B2B sector that:

- Maps the revenue mechanics in that sector.
- Presents 3-5 aggregated, anonymised patterns.
- Compares against international or historical benchmarks where available.
- Names the methodology in plain language.
- Does not name any specific client.

## What it isn't

- A pitch.
- A list of Dealix features.
- A forecast of any individual buyer's revenue.
- A re-publication of confidential client metrics.

## Structure

| Section | Length |
|---------|--------|
| One-page executive summary (EN + AR) | 200 words |
| Methodology and sample | 200 words |
| Sector mapping | 300-400 words |
| Pattern 1: signal capture | 200 words |
| Pattern 2: qualification | 200 words |
| Pattern 3: proposal cycle | 200 words |
| Pattern 4: cash cycle | 200 words |
| Pattern 5: retention | 200 words |
| Implications for operators | 200 words |
| Limitations | 100 words |
| Disclaimer | 50 words |

## Anonymisation

A sector with fewer than 20 plausible Saudi candidates is aggregated to a wider sector. Specific metric ranges that could reverse-identify a client are widened. Methodology is published; raw data is not.

## Production process

1. Sector chosen from `docs/02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md`.
2. Data pull from `$PRIVATE_OPS/sector_data/<sector>/` with provenance.
3. Patterns drafted by analyst; reviewed by Brand Guardian and Performance Analyst (`docs/ai/PERFORMANCE_ANALYST_AGENT.md`).
4. Bilingual draft prepared.
5. Founder approves at A2.
6. Published on owned surfaces; partners notified.
7. Quarterly: the report is reviewed for currency. Stale reports are archived with a notice.

## Cadence

One report per month, sector rotating. A sector is revisited no more often than every 12 months.

## Failure modes

- **Re-identifiable metric:** a metric range narrows the candidate set to fewer than 20. Detection: anonymisation review. Recovery: widen range; re-approve.
- **Methodology omission:** a pattern is asserted without method. Detection: review checklist. Recovery: add method or remove pattern.
- **Stale data:** the report uses data older than 12 months. Detection: publish-time check. Recovery: refresh or do not publish.

## Recovery path

If a report is published and a client identifies themselves in it without intent, the founder withdraws the report within 24 hours, issues a written apology, and re-issues with broader aggregation.

## Metrics

- Reports published per quarter (target: 3).
- Downloads per report (estimated).
- Reports leading to qualified conversation (estimated).
- Sector coverage breadth (sectors covered in trailing 12 months).

## Disclaimer

Sector reports describe patterns from aggregated data. They are not advice and do not constitute a forecast for any individual organisation. Estimated value is not Verified value.
