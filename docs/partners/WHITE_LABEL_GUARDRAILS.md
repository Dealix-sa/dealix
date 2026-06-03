# White-Label Guardrails

## Purpose
Allow white-label arrangements only when quality and trust survive the relabel.

## Pre-conditions
- The white-label partner has a documented buyer profile aligned with our ICP.
- Pricing alignment: partner cannot sell Dealix-delivered work below cost.
- Quality control: every white-label deliverable must pass Dealix QA ≥ 75 before relabeling.
- Trust: partner agrees to honor Dealix proof rules even under their brand.

## Restrictions
- No white-label of named case studies.
- No white-label of sector reports.
- No white-label of automation tools (engineering output) without a separate engineering license.

## Per-engagement workflow
1. Partner introduces opportunity with scope.
2. Dealix produces deliverable.
3. Dealix passes QA.
4. Partner relabels and delivers to end customer.
5. Dealix invoices partner; partner invoices customer.
6. End customer never sees Dealix branding unless they ask.

## Disclosure
- If asked, Dealix will confirm involvement (we never lie about authorship).
- Partner must disclose that "this deliverable was produced by an external operating system" if directly asked.

## Tracking
- `partners/partner_tracker.csv`: row with `type=White-label`.
- Each engagement logged in the partner's section of `evidence/execution_evidence_ledger.csv`.

## Termination
- Either party can pause new white-label projects with 30 days' notice.
- Active engagements complete under existing terms.

## Anti-patterns
- Vague co-branding ("powered by") without legal clarity.
- White-labeling a deliverable to a downstream buyer at < 70% of Dealix list price (signal of margin death).
- Accepting bad revenue under partner pressure.
