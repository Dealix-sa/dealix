# Sample Factory

The Sample Factory produces the free diagnostic that opens every Dealix engagement. It is rung 1 of the offer ladder (`docs/product/DEALIX_PRODUCT_LADDER.md`).

**Source of truth:** `$PRIVATE_OPS/sample_factory_queue.csv`
**Owner:** Revenue Lead
**Trust gate:** A1 — diagnostic cannot be sent externally without founder sign-off on the case-safe summary.

## Purpose

A sample is the lowest-friction evidence we can hand a prospect. It must be:

- Specific to the prospect's sector.
- Anonymised against any real customer data.
- Reproducible (the same input produces the same output).
- Bounded (a diagnostic is not a paid engagement).

A sample is not a pitch. It is a small, verifiable artifact that demonstrates that Dealix understands the prospect's revenue mechanics.

## What a sample contains

| Section | Source | Length |
|---------|--------|--------|
| Sector context | `docs/02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md` | 1 page |
| Three observed patterns | aggregated case data, no PII | 1 page |
| One diagnostic question | Revenue Lead | 0.5 page |
| Recommended next step | offer ladder rung | 0.5 page |

Total: 3 pages. Bilingual EN + AR. Every page carries the disclaimer "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Production process

1. Inbound or sourced signal lands in `signals.csv`.
2. Revenue Lead checks ICP fit using `docs/00_foundation/DEALIX_POSITIONING.md`.
3. If fit, opportunity is promoted to `sample_factory_queue.csv` with state `drafting`.
4. Sample is drafted from the standard template. No real customer names are used.
5. Brand Guardian agent reviews for tone and claim safety (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
6. Founder approves at gate A1. Approval is logged.
7. Sample is delivered through the agreed channel (email or founder-led DM, never bulk automation).

## Failure modes

- **PII leak:** a draft includes a real customer name. Detection: PII scan before stage 6. Recovery: draft rejected, re-written, audit row written.
- **Guarantee language:** a draft promises a result. Detection: copy lint against `docs/marketing/COPYWRITING_RULES.md`. Recovery: rewrite; founder re-approves.
- **Stale queue:** sample older than 5 business days. Detection: nightly job. Recovery: queue review by Revenue Lead.

## Recovery path

If the sample factory is paused (policy violation, eval failure, runtime fault), the queue freezes. No drafts move to delivery. The founder receives a daily digest of paused items until the issue clears.

## Metrics

- Samples drafted this week.
- Samples approved this week.
- Samples delivered this week.
- Sample-to-paid-engagement conversion (estimated).
- Median time from signal to approved sample.

## Boundary

The Sample Factory does not perform cold outreach, does not scrape, and does not send unsolicited messages to anyone the prospect has not introduced. All delivery channels are pre-agreed and PDPL-aware (`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`).

## Disclaimer

The diagnostic is a reference document. It is not a forecast and does not constitute a commitment of revenue. Estimated value is not Verified value.
