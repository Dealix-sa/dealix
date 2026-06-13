# Dealix Human Approval Policy

**Owner:** Founder (CEO). **Last updated:** 2026-06-06.
**Principle:** Dealix drafts; a human decides. No external action and no charge
happens without an explicit, recorded human approval.

## 1. What always requires human approval (before execution)
- Any message sent to a person outside Dealix (email, WhatsApp, LinkedIn, SMS).
- Any payment link issued, any charge confirmed, any refund.
- Any commitment made to a customer (scope, price, timeline).
- Any number or claim that will appear in a customer-facing document.

## 2. How approval is recorded
- For an engagement: in the customer's `06_approval_register.md`.
- For outreach: in `data/revenue/outreach_queue.jsonl` (`approval_status`) and
  `reports/revenue/outreach_approval_queue.md`.
- A draft is never marked `sent` unless it was first `approved`.

## 3. Hard prohibitions (never approvable)
- Cold outreach automation / mass blasting.
- Scraping, or taking data from behind any login.
- Guaranteed revenue / ranking / outcome claims.
- Fabricated proof, testimonials, or metrics.
- Automatic ("silent") sending or charging.

## 4. The automation boundary
Agents and scripts in this repo may **draft, score, rank, and queue**. They may
**not send, charge, or commit**. The "send" step is always a human action taken
after reviewing the draft.

## 5. Audit
Anyone reviewing an engagement should be able to answer, for every external
action: *who approved it, when, and where is that recorded?* If the answer is
"no one / nowhere", the action was a policy violation.
