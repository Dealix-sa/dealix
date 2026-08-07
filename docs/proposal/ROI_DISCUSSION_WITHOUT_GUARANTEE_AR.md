# ROI Discussion Without Guarantee

> **Status:** Hard policy. No ROI number is published without a proof metric.
> **Companion:** `PROOF_PACK_TEMPLATE_AR.md` + `PROPOSAL_TEMPLATE_AR.md`.

## The principle

> We discuss ROI in 3 ways: cost-of-inaction, proof-metric, and risk-adjusted range. Never as a guaranteed number.

## The 3 ways to discuss ROI

### 1. Cost of inaction

> "If you lose 20 leads/month, and the average deal is SAR 5,000, that's SAR 100k/month you're losing. The audit costs a fraction of that."

This is the most honest framing. It anchors the price in the cost of doing nothing.

### 2. Proof metric

> "We will measure [metric 1, metric 2, metric 3] during the pilot. If we hit them, the engagement continues. If not, we stop."

This is the closest we get to a guarantee. We don't guarantee a number; we guarantee that we will measure and stop if we don't hit it.

### 3. Risk-adjusted range

> "In the cases we have, the recovery ranges from SAR X to SAR Y per month. The lower end is conservative. The higher end assumes faster adoption."

This is the softest framing. It is honest about the range and the assumptions.

## The forbidden ROI claims

| Claim | Why forbidden |
| --- | --- |
| "نضمن 2X في 90 يوم." | We don't guarantee. |
| "100% زيادة في الـ pipeline." | Impossible to guarantee. |
| "ROI مضمون." | Same. |
| "ستسترد التكلفة في 30 يوم." | Time-bound guarantee. |
| "Doubling is the floor." | Implies a guarantee. |

## The safe ROI claims

| Claim | When allowed |
| --- | --- |
| "Cost of inaction = X SAR/month." | Always (with the math). |
| "We will measure Y, Z, W." | With a specific metric. |
| "Past cases range from A to B." | Only with n=3+ and the range stated. |
| "If the proof metric is not hit, we stop." | Always (it is the founder's commitment). |
| "The pilot costs [pricing_status: draft_only]." | Always, with the founder-approved note. |

## How the founder handles a "what's the ROI?" question

In a discovery call:

> "ما أقدر أعطيك رقم. أقدر أقول: نحدد مقياس نجاح في أول أسبوع، نقيسه في الأسبوع 2 والـ 4. لو ما تحققت، نوقف. هذا أقرب شي للـ ROI مضمون — بس بدون ادعاءات."

In a proposal:

> The proof metric is the answer. The pricing is `draft_only` with a range. The risk-adjusted range is in the appendix.

In a case study:

> "In 3 cases, the recovery ranged from SAR X to SAR Y per month. The lower end assumes slower adoption; the higher assumes the team ran the daily digest consistently."

## The trust preflight check

The preflight flags any draft that:

- Has a single ROI number (not a range).
- Has a time-bound guarantee.
- Has "guaranteed" + "ROI" in the same sentence.
- Has a number without a proof metric reference.
- Has a number that is suspiciously round (10x, 5x, 100%).

## The audit trail

Every ROI discussion in a draft references a `proof_id` from the proof pack library. The trust preflight verifies the proof pack exists and is not expired.

## When to update

- After 10 deals: if the cost-of-inaction framing is consistently rejected, try the proof-metric framing.
- After 20 deals: if the proof-metric framing is consistently rejected, try the risk-adjusted range.
- After 50 deals: retire the framings that did not work; double down on the ones that did.
