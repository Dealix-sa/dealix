# Delivery QA OS

The Delivery QA OS is the inspection layer that confirms a deliverable is correct, compliant, and complete before it leaves Dealix.

**Source of truth:** `$PRIVATE_OPS/delivery_qa_log.csv`
**Owner:** Delivery Lead
**Trust gate:** A1 — every deliverable passes QA before client send; founder may require A2 for first-of-kind work.

## What QA checks

| Layer | Question |
|-------|----------|
| Scope | Does it satisfy the proposal's definition of done? |
| Accuracy | Are the facts, figures, and citations correct? |
| Provenance | Does every claim trace to a source in `docs/04_data_os/DATA_PROVENANCE.md`? |
| Claim safety | Does any sentence breach the no-guarantee rule? |
| PII | Does the deliverable contain any disallowed PII? |
| Tone | Does the language match `docs/marketing/BRAND_VOICE_EXAMPLES.md`? |
| Bilingual parity | Are EN and AR sections balanced? |
| Disclosure | Is the estimated-value disclaimer present? |

A deliverable that fails any layer returns to the producer with the failure code and remediation note.

## Process

1. Producer (human or agent) submits deliverable to QA queue.
2. Automated lint runs first: PII scan, claim-safety lint, bilingual parity, disclosure check.
3. Brand Guardian agent reviews tone (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
4. Delivery Lead performs scope and accuracy review.
5. Founder signs off if first-of-kind or contractually required.
6. Deliverable is released to the client. Release event logged.

## Lint rules

| Lint | Tool | Pass criteria |
|------|------|---------------|
| PII scan | regex + classifier | Zero matches against PII patterns in `docs/04_data_os/PII_CLASSIFICATION.md` |
| Claim safety | classifier | Zero matches against avoid patterns in `docs/marketing/COPYWRITING_RULES.md` |
| Bilingual parity | length check | EN and AR sections within ±20% length |
| Disclosure | string check | Exact disclosure string present at end |
| Citation density | counter | Every quantitative claim cited |

## Failure modes

- **False negative:** a deliverable passes QA but contains a defect. Detection: client feedback or weekly audit sample. Recovery: written apology, deliverable re-issued, root cause filed.
- **Stuck queue:** deliverables wait more than 2 business days. Detection: nightly job. Recovery: Delivery Lead reassigns or escalates.
- **Tool outage:** classifier or gateway down. Detection: monitor. Recovery: manual QA continues; agent-assisted lint paused; throughput halved with notice.

## Recovery path

If QA produces inconsistent verdicts (lint passes the same item that human review fails), the founder freezes auto-pass logic and requires full human review on every deliverable until the inconsistency is resolved.

## Metrics

- Throughput per week.
- Median time-in-QA.
- Pass rate by layer.
- Defect-escape rate (defects found by client divided by deliverables released).

## Disclaimer

QA confirms compliance with internal standards. It does not guarantee commercial outcome. Estimated value is not Verified value.
