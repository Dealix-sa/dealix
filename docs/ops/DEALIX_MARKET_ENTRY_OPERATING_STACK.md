# Dealix Market Entry Operating Stack

This document is the operating-stack overview that binds positioning,
intelligence, offers, revenue, delivery, finance, and customer success
into a single, named stack. It is the single page that an investor, a
partner, or a new operator can read to understand how the system runs
end-to-end.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. The stack (top to bottom)

1. Positioning — `docs/positioning/DEALIX_POSITIONING.md`,
   `docs/positioning/SAUDI_B2B_NARRATIVE.md`.
2. Market intelligence — `docs/intelligence/`.
3. Product (offers and ladder) — `docs/product/DEALIX_PRODUCT_LADDER.md`.
4. Distribution war machine — `docs/growth/`.
5. Revenue factory — `docs/revenue/`.
6. Finance — `docs/finance/`.
7. Delivery — `docs/delivery/`.
8. Customer success — `docs/customer_success/`,
   `docs/client_success/`.
9. Proof — `docs/proof/`.
10. Trust + policy plane — `policies/`, `registries/`, trust ledger.

## 2. The loop

```
Positioning -> Intelligence -> Offers -> Distribution Drafts
   -> Approval Queue -> Operator Send -> Reply Router
   -> Sample / Proposal -> Closed Won
   -> Finance + Delivery + Customer Success
   -> Proof Approval
   -> Back into Demand
```

Every transition is approval-gated. Every artefact is auditable.

## 3. Owners (agent layer)

- ceo_copilot — daily founder brief.
- brand_guardian — brand voice + guarantee scan.
- growth_strategist — sector ranking, ICP, scoring.
- distribution_operator — outreach drafts and reply routing.
- content_strategist — content and community.
- offer_architect — offer ladder.
- performance_analyst — channel and pipeline scorecards.
- trust_guardian — policy-as-code enforcement.
- eval_guardian — agent evals.
- finance_copilot — payment capture and reconciliation.
- delivery_copilot — pipeline + samples + proposals + delivery state.
- security_guardian — security and PDPL posture.
- productization_agent — promote client work into offers.
- partner_revenue_agent — partner referrals.
- proof_safety_agent — proof approval.
- incident_response_agent — incident tracking.

All agents have `external_action_allowed = false` and `kill_switch =
true`.

## 4. Approval classes used

- A1 — observe, read, draft only. Allowed for every layer.
- A2 — assist with explicit approval before external action. Allowed.
- A3 — autonomous external action. Banned at policy level
  (`no_a3_auto`).

## 5. Trust gate (cross-cutting)

- Suppression check.
- Guarantee scan.
- Brand voice check.
- Source attribution.
- Bilingual integrity.
- Audit ledger entry.

Policy file: `policies/dealix_control_policy.yaml`.

## 6. Source of truth files

| Layer | File |
|---|---|
| Sectors | `growth/sector_targets.csv` |
| ICPs | `growth/icp_segments.csv` |
| Personas | `growth/personas.csv` |
| Triggers | `growth/trigger_events.csv` |
| Accounts | `growth/account_scores.csv` |
| Outreach | `outreach/outreach_queue.csv` |
| LinkedIn | `outreach/linkedin_queue.csv` |
| Email | `outreach/email_queue.csv` |
| Contact form | `outreach/contact_form_queue.csv` |
| Follow-up | `outreach/followup_queue.csv` |
| Reply routing | `outreach/reply_routing.csv` |
| Suppression | `outreach/suppression.csv` |
| Pipeline | `sales/pipeline.csv` |
| Samples | `sales/sample_queue.csv` |
| Proposals | `sales/proposal_queue.csv` |
| Payment | `finance/payment_capture_queue.csv` |
| Cash | `finance/cash_collected.csv` |
| Delivery | `delivery/sprint_log.csv` |
| Client health | `customer_success/client_health.csv` |
| Referrals | `customer_success/referral_queue.csv` |
| Proof | `proof/proof_library.csv` |
| Trust | `trust/trust_flags.csv`, `trust/incidents.csv` |
| Evals | `evals/eval_status.csv` |

## 7. Cadence summary

- Daily — brief; queue triage; send approved; pipeline view.
- Weekly — sales meeting (Mon); content review (Wed); close (Fri).
- Monthly — win/loss; channel; objection; sector; finance reconcile;
  client health.
- Quarterly — scoring calibration; channel portfolio reset; offer
  ladder; rhythm self-audit.

## 8. KPI roll-up

- Pipeline coverage (priority-band accounts in motion).
- Reply quality (positive replies / approved sends).
- Sample-to-proposal rate.
- Proposal win rate.
- DSO.
- On-time sprint completion rate.
- Net retention.
- Referral conversion rate.
- Proof library size and freshness.
- A3 attempts (target: 0).

## 9. Risks tracked

- Suppression bleed.
- Brand voice drift.
- Source contamination.
- Channel saturation.
- Confidentiality breach in proof or delivery.
- ZATCA rejection.
- PDPL posture drift.

Each risk has an owner, an alert source, and a documented recovery
path.

## 10. Saudi context

- Bilingual operating reality.
- Relationship density.
- Authority concentration.
- Procurement realism.
- Regulator alignment (PDPL, ZATCA, sector regulators).

## 11. What an operator can do today

- Use the registry-listed agents to draft outbound, schedule content,
  produce samples, and draft proposals.
- Approve those drafts at the Founder Console.
- Send approved drafts manually as a named operator.
- Track pipeline, finance, delivery, and proof in the canonical files.
- Use the trust ledger as the single audit trail.

## 12. What no operator may do

- Bypass approval.
- Use A3 patterns.
- Publish unapproved proof.
- Scrape or buy lists.
- Make guaranteed claims.
- Commit to pricing, terms, or refunds without approval.

## 13. Non-negotiables

These are restated, because they are the spine of the stack:

- No external send by an agent.
- No guaranteed-revenue / sales / meetings language.
- No proof publication without approval.
- No scraping. No purchased lists.
- A3 banned.

The operating stack is the system Dealix would still be proud of after
ten public audits. Every layer is designed around that constraint.
