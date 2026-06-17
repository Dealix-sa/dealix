# Dealix — First Revenue Plan

> Goal: close the first **paid Command Sprint**. Manual, founder-led, honest.
> No auto-send, no spam, no guaranteed revenue, no fake proof. Every external
> message requires founder approval.

## 1. Current ICP
Saudi B2B companies, founder/owner-led, 5–50 people, with a recurring or
project revenue motion and a *clear single breakpoint* in how revenue moves.
Primary sectors: B2B marketing agencies, consulting firms, training companies,
IT service providers, business services companies.

## 2. First 30 target structure
- Source: `data/growth/first_30_targets.csv` (structured, founder-owned).
- Mix: ~6 per sector across the 5 sectors.
- Each row starts `research`; promote to `approved` only with `evidence_url`
  or a warm-intro reason. No personal phone numbers. No scraping.

## 3. Top 10 shortlist rules
1. Clear single revenue breakpoint we can name.
2. Decision-maker is reachable (warm intro preferred).
3. Data exists that we can work from (with consent).
4. Realistic 7-day scope.
5. Sector is on the ICP list.
6. Evidence URL or warm-intro reason recorded.
7. No reliance on cold outreach to reach them.
8. Budget plausibility for a paid Sprint.
9. Not a competitor / not a conflict.
10. Founder genuinely wants this as a reference customer.

## 4. First 5 manual outreach drafts
Drafted into `data/revenue/outreach_queue.jsonl` as `draft`, reviewed in
`reports/revenue/outreach_approval_queue.md`. Use the safe first message
(Arabic) — positioning first, 3 seats, 5 deliverables, human approval, a
diagnostic offer. The founder approves and sends each one by hand.

## 5. Diagnostic flow
1. Positive reply → book a 20–30 min diagnostic.
2. Run `sales/COMMAND_SPRINT_DIAGNOSTIC_SCRIPT.md`.
3. Capture into `customers/<slug>/02_diagnostic_summary.md`.
4. Score fit (3–4 yes → propose; else honest redirect).

## 6. Proposal flow
- If fit: send a short proposal — Command Sprint, 7 days, 5 deliverables,
  manual payment, 7-day refund. No revenue guarantees.
- Templates: `templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2` /
  `..._ENGLISH_FULL.md.j2`, adapted to the diagnostic findings.
- Log to `data/revenue/offers.jsonl`; set target status `offer_sent`.

## 7. Payment / manual confirmation path
- Manual payment (link/transfer). **No automatic charge.**
- Founder confirms receipt → record in `customers/<slug>/09_delivery_log.md`
  and `data/revenue/payments.jsonl`; set target status `paid`.
- Refund window: 7 days, honored.

## 8. Customer workspace creation path
- `python scripts/create_customer_workspace.py --name "<Company>"`
- Produces the 12-file Command Sprint workspace under `customers/<slug>/`.

## 9. Proof pack path
- Build `10_proof_pack.md` from `04_revenue_map.md`, `05_proof_register.md`,
  `07_next_action_board.md`, `08_executive_command_brief.md`.
- Every number traces to a source in the Proof Register. No fabricated proof.
- Deliver by day 7 with an executive review.

## 10. Upsell path
- Only after a delivered Proof Pack. Record in `11_upsell_recommendation.md`.
- Managed Revenue Ops is **planned** — offer it only after 3 paid Sprints +
  3 Proof Packs. Draft any upsell message into the approval queue (not sent).

## Guardrails (non-negotiable)
- No auto-send. No spam. No guaranteed revenue. No fake proof.
- Every external message requires founder approval.
- No scraping; no data from behind a login; no cold outreach.

---
_The real test of Wave 7 is not file count — it is the first paid customer reaching a Proof Pack._
