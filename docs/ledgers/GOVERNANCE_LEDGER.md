# Governance Ledger

Sensitive, **non-negotiable** record. IDs: `G-###`. Mirror critical rows in client `04_governance_log.md`.

## Outcomes

```text
Allow
Allow with approval
Redact
Research-only
Rewrite
Block
Escalate
```

| ID | Date | Client | Issue | Risk | Decision | Control | Owner |
|----|------|--------|-------|------|----------|---------|-------|
| G-001 | | Client A | Missing data source | Medium | Flag research-only | Source required | |
| G-002 | | Client B | Cold WhatsApp request | High | Block | Offer draft-only | |

Policy stack: [`../governance/GOVERNANCE_DECISION.md`](../governance/GOVERNANCE_DECISION.md), [`RISK_REGISTER.md`](../governance/RISK_REGISTER.md).

---

## G-003 — Doctrine hotfix: product-narrative unification (2026-05-18)

**Date:** 2026-05-18
**Owner:** Workstream A — commercial-activation program
**Risk:** High — doctrine-violating sales narrative across launch and sales-kit content
**Decision:** Rewrite (doctrine hotfix; explicitly permitted under the active
commercial freeze, [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) —
production hotfixes for security/doctrine + ledger recording are "Allowed").
**Control:** All customer-facing and launch content now reflects the current
doctrine — Dealix is **Governed Revenue & AI Operations**: the system analyzes,
scores, and drafts; the founder reviews and approves every external action;
nothing is sent or booked autonomously. Entry offer corrected to **free Mini
Diagnostic (rung 0) → 499 SAR 7-Day Revenue Proof Sprint (rung 1)**. The
"1 SAR" transaction is retained **only** as an internal end-to-end payment
test, never a marketed price. Rung 2–5 marketing was **not** restructured
(freeze scope); only doctrine-violating claims inside it were corrected.

### Violations corrected

- **Autonomous "AI sales rep" framing** — "مندوب مبيعات AI" / "AI sales rep"
  rewritten to "عمليات إيراد و AI مُحوكَمة / Governed Revenue & AI Operations".
- **Auto-reply / auto-book claims** — "يرد خلال 45 ثانية", "يحجز demos
  تلقائياً", "بدون تدخل بشري" replaced with draft-and-approve language
  (the founder/customer reviews and approves every external action).
- **"1 SAR" as the public price** — replaced everywhere with the free Mini
  Diagnostic → 499 SAR Sprint ladder; internal-test references explicitly
  labeled as internal-only.
- **Guaranteed outcomes / ROI / fabricated metrics** — guaranteed savings,
  ROI percentages, and invented case-study numbers replaced with honest
  non-guarantee language and "Hypothetical / case-safe" labels.
- **Fake customer testimonials** — landing-page testimonials relabeled as
  hypothetical, case-safe examples.

### Files changed

**Launch content:**
- `docs/ops/launch_content_queue.md` — DM #5, agency-DM template, POSTs 4–7,
  Day +5 follow-up corrected.
- `docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md` — Lucidya DM templates, follow-ups,
  1-SAR test step labeled internal-only.

**Sales-kit (customer-facing + investor + launch assets):**
- `docs/sales-kit/dealix_onepager.md`, `dealix_onepager.html`,
  `dealix_landing_v2.html`, `dealix_roi_calculator.html`,
  `dealix_marketers_page.html`, `dealix_invoice_template.html`
- `docs/sales-kit/dealix_objection_handler.md`, `dealix_personalized_messages.md`,
  `dealix_demo_script_30min.md`, `dealix_demo_transcript_ar.md`,
  `dealix_followup_cadence.md`, `dealix_pilot_agreement.md`,
  `dealix_enterprise_proposal.md`, `dealix_terms_of_service_ar.md`
- `docs/sales-kit/dealix_video_scripts.md`, `dealix_blog_post_1.md`,
  `dealix_blog_post_2.md`, `dealix_blog_post_3.md`, `linkedin_longform_posts.md`,
  `dealix_content_calendar.md`, `dealix_case_study_template.md`
- `docs/sales-kit/dealix_battlecards.md`, `dealix_competitor_battlecards_v2.md`,
  `dealix_pitch_deck.md`, `dealix_product_roadmap.md`
- `docs/sales-kit/dealix_self_dogfooding.md`, `dealix_customer_onboarding.md`,
  `dealix_leads_20_real.md`, `dealix_leads_50_expanded.md`,
  `dealix_referral_program.md`, `dealix_agency_partnerships.md`,
  `dealix_email_drip_sequences.md`
- `docs/sales-kit/MULTI_CHANNEL_OUTREACH_PACK.md`, `SAUDI_AI_GTM_REPORT_2026.md`
- `docs/sales-kit/README.md`, `START_HERE.md`, `MOYASAR_HOSTED_CHECKOUT.md`,
  `DEALIX_EXECUTIVE_RESPONSE.md`, `dealix_invoicing_guide.md`,
  `LAUNCH_TODAY.md`, `dealix_1_riyal_test.sh`

### Not changed (already doctrine-compliant)

`docs/sales-kit/MARKET_SIGNAL_CLASSIFICATION.md`, `OUTREACH_DRAFTS_QUEUED.md`,
`WARM_LIST_WORKFLOW.md`, `CUSTOMER_1_GO_LIVE_RUNBOOK.md` — these already enforce
draft-only, no-guarantee, no-cold-automation rules. Internal payment-test scripts
and infra runbooks (`RAILWAY_MOYASAR_STEP_BY_STEP.md`, `DEALIX_LAUNCH_GATES.md`,
`DEALIX_HONEST_AUDIT.md`, `DAILY_EXECUTION_SCHEDULE_AR.md`, `v5/*`) retain "1 SAR"
strictly as the internal end-to-end payment test, which the doctrine permits.
