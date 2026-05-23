# Handoff and QA System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Closing Deals · Built on Trust.

The Handoff and QA System is the gate between sprint execution and
customer-facing delivery. It is the moment we either ship a clean,
brand-aligned, trust-safe deliverable or we don't ship at all. The
gate is owned by the Delivery Copilot, with the Eval Guardian and
Brand Guardian providing assertions, the Proof Safety Agent
contributing when customer data is involved, and the founder
signing off.

## Why the gate exists

Without a deliberate QA gate, quality variance shows up in two
places: the customer's experience and the proof library. Both
compound: a weak handoff produces a weak proof asset, which produces
weaker outreach, which produces a weaker pipeline. The gate is the
cheapest place to spend time.

## Gate inputs

| Input                                | Source                                                              |
| ------------------------------------ | ------------------------------------------------------------------- |
| The sprint deliverable                | Delivery Copilot.                                                   |
| The acceptance criterion              | From the proposal.                                                  |
| The customer-facing message           | Distribution Operator (draft).                                      |
| The proof candidate (where consent)   | Delivery Copilot draft.                                             |
| The trust posture (suppression, PDPL) | Trust Guardian.                                                     |

## Gate checks

The gate has six checks. All six must pass before handoff.

### 1. Acceptance trace

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| The deliverable maps to the written acceptance criterion.          | One-to-one trace, documented in the QA log.                  |

### 2. Brand check

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| Wordmark, tagline, typography, and tone match the brand guide.    | Brand Guardian sign-off recorded.                            |
| Arabic content meets the business-quality bar.                     | `arabic_business_quality` eval suite green.                  |

### 3. Phrasing check

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| No guaranteed revenue, sales, or meeting claims.                  | `no_guaranteed_claims` eval suite green.                     |
| No overclaim per `NO_OVERCLAIM_POLICY.md`.                        | Brand Guardian sign-off.                                      |
| All numeric claims trace to approved proof assets.                | `evidence_required` eval suite green.                         |

### 4. PII check

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| No unredacted PII in deliverables intended for proof or external view. | Proof Safety Agent lint pass.                            |
| Customer-specific identifiers are masked or removed in reusable artifacts. | Lint and human review.                                   |

### 5. Trust posture check

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| No external action queued without approval.                       | Audit ledger inspection.                                     |
| Suppression list considered for any contact recommendations.       | Trust Guardian sign-off.                                     |
| No pricing, contract, or payment-term commitments in deliverables. | Eval gate `pricing_safety`, `contract_safety`, `payment_terms_safety` green. |

### 6. Customer-facing message check

| Check                                                             | Pass criterion                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| Handoff message is brand-aligned and trust-safe.                  | Brand Guardian sign-off.                                     |
| Next-step recommendation is a method, not a sales pitch.           | Reviewer sign-off.                                           |
| Customer's name and identifiers are accurate.                      | Spot-check.                                                  |

## Gate outcomes

| Outcome      | Effect                                                                     |
| ------------ | -------------------------------------------------------------------------- |
| Pass         | Handoff proceeds. Audit row recorded `action: handoff_pass`, `risk: low`.   |
| Pass with notes | Handoff proceeds; the notes are added to the retrospective.              |
| Fail         | Handoff blocked. Issues logged. The sprint cannot complete.                |

## Failure handling

When the gate fails:

1. The Delivery Copilot logs the failure in the QA log.
2. A trust flag at `severity: medium` is opened.
3. The sprint stays in `qa_open` status.
4. The owner fixes the issues and re-submits.
5. Re-runs are unlimited; the gate is not penalty-driven, it is
   correctness-driven.

## Handoff packet

A passing gate produces the handoff packet:

| Component                              | Notes                                                          |
| -------------------------------------- | -------------------------------------------------------------- |
| The deliverable                        | The primary artifact of the sprint.                            |
| Acceptance document                     | Signed by customer.                                            |
| Runbook                                | How the customer operates the deliverable.                    |
| Next-step recommendation               | Method-based, brand-aligned.                                  |
| Proof candidate (if consent recorded)   | A redacted artifact for the proof library.                     |
| QA log                                 | One-page record of the gate decisions.                         |

The packet is delivered via the application; large attachments use
object storage.

## Retrospective

Within seven days of handoff, the Delivery Copilot writes a one-page
retrospective:

- What worked.
- What was hard.
- What we learned.
- Whether the sprint is a productization candidate.

The retrospective lands in the productization candidates file
(`product/productization_candidates.csv`) if applicable.

## Audit events

| Action                       | Risk     | Notes                                                  |
| ---------------------------- | -------- | ------------------------------------------------------ |
| `handoff_pass`               | low      | Gate passed.                                           |
| `handoff_fail`               | medium   | Gate failed; issues to fix.                            |
| `handoff_packet_delivered`    | low      | Customer received the packet.                          |
| `retrospective_filed`         | low      | One-page retro saved.                                  |

## Anti-patterns

| Anti-pattern                                          | Why                                                                       |
| ----------------------------------------------------- | ------------------------------------------------------------------------- |
| Skipping the gate to meet a date                      | The customer's experience matters more than the date.                     |
| Hand-waving the acceptance trace                       | Without trace, scope drift is invisible.                                  |
| Letting overclaim slip in messaging                    | Erodes trust; expensive to undo.                                          |
| Treating the gate as optional for "small" sprints       | The discipline is the brand.                                              |
| Re-running the gate without fixing the issue            | Pattern of failure surfaces in the retrospective.                         |

## Cadence

| Activity                       | Cadence                              |
| ------------------------------ | ------------------------------------ |
| Gate run                       | Per sprint, before handoff.          |
| Retrospective                  | Within 7 days of handoff.            |
| Gate criteria review            | Quarterly with the founder.          |

## Discipline

1. Six checks, all pass, every time.
2. The gate is owned by Delivery; it draws on Brand, Eval, and Trust.
3. Failure means re-run, not penalty.
4. The retrospective is mandatory.
5. The packet is the customer's lasting artifact.

## Cross-references

- `ULTIMATE_DELIVERY_OS.md` for the broader delivery discipline.
- `EVAL_GATE_V1.md` for the suites used here.
- `NO_OVERCLAIM_POLICY.md` for phrasing.
- `CUSTOMER_SUCCESS_OS.md` for what happens after handoff.
