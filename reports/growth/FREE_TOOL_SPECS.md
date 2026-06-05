# Free Tool Specs — Dealix Self-Growth OS

Generated: 2026-06-05T17:56:13.362289+00:00
Source: `data/growth/free_tools.json` (6 tools)

> Each tool: self-scoring diagnostic → result → ONE recommended next step.
> No fabricated benchmarks. Results are estimates, not Verified value.

| Tool | Route | Goal | CTA | Recommended offer |
|---|---|---|---|---|
| مؤشر نظام تشغيل الأعمال | `/ar/business-os-score` | broad-acquisition | ابدأ تشخيص Dealix | command-sprint |
| حاسبة تسرب الإيراد | `/ar/revenue-leakage-calculator` | sales-intent | احصل على Revenue Leakage Score | command-sprint |
| تدقيق فجوة الإثبات | `/ar/proof-gap-audit` | proof-positioning | احصل على Proof Register خلال Command Sprint | command-sprint |
| مؤشر خطر متابعة واتساب | `/ar/whatsapp-followup-risk-score` | whatsapp-pain | ابدأ تشخيص Dealix | command-sprint |
| قائمة حوكمة الذكاء الاصطناعي | `/ar/ai-governance-checklist` | trust-differentiation | ابدأ تشخيص Dealix | command-sprint |
| مؤشر وضوح التسليم | `/ar/delivery-visibility-score` | delivery-pain | ابدأ تشخيص Dealix | command-sprint |

## مؤشر نظام تشغيل الأعمال — Business OS Score (`business-os-score`)

- Route: `/ar/business-os-score`
- Inputs: sector, monthly_opportunities, follow_up_method, has_crm, uses_whatsapp, has_case_studies, knows_where_deals_stall, has_delivery_tracking
- Output: score_0_100 — shows score, top_3_leaks, recommended_next_step
- CTA (single): **ابدأ تشخيص Dealix**
- Claims guard: No industry benchmark shown unless sourced. Score is self-reported and labelled as an estimate.

## حاسبة تسرب الإيراد — Revenue Leakage Calculator (`revenue-leakage-calculator`)

- Route: `/ar/revenue-leakage-calculator`
- Inputs: monthly_opportunities, avg_deal_value_sar, estimated_leakage_pct
- Output: currency_estimate — shows monthly_risk_estimate_sar, annual_risk_estimate_sar, next_step
- CTA (single): **احصل على Revenue Leakage Score**
- Claims guard: Labelled as an operational risk estimate requiring verification. Never phrased as guaranteed recoverable revenue.

## تدقيق فجوة الإثبات — Proof Gap Audit (`proof-gap-audit`)

- Route: `/ar/proof-gap-audit`
- Inputs: has_case_studies, has_results, has_testimonials, offers_include_proof, team_handles_objections
- Output: score_0_100 — shows proof_readiness_score, missing_proof_assets, next_step
- CTA (single): **احصل على Proof Register خلال Command Sprint**
- Claims guard: No claim that proof guarantees conversion. Output is a readiness estimate.

## مؤشر خطر متابعة واتساب — WhatsApp Follow-up Risk Score (`whatsapp-followup-risk-score`)

- Route: `/ar/whatsapp-followup-risk-score`
- Inputs: whatsapp_volume_monthly, has_next_action_after_chat, has_owner_per_conversation, response_sla_hours
- Output: score_0_100 — shows risk_score, top_leak, next_step
- CTA (single): **ابدأ تشخيص Dealix**
- Claims guard: Diagnoses operating-rhythm gaps. No cold WhatsApp automation is offered or implied.

## قائمة حوكمة الذكاء الاصطناعي — AI Governance Checklist (`ai-governance-checklist`)

- Route: `/ar/ai-governance-checklist`
- Inputs: ai_sends_without_approval, has_audit_log, has_human_review, has_data_retention_policy, has_pii_controls
- Output: checklist_score — shows governance_score, open_risks, next_step
- CTA (single): **ابدأ تشخيص Dealix**
- Claims guard: Positions Approval-first AI. No claim of certification or compliance guarantee.

## مؤشر وضوح التسليم — Delivery Visibility Score (`delivery-visibility-score`)

- Route: `/ar/delivery-visibility-score`
- Inputs: has_delivery_tracking, has_sla, client_sees_status, has_proof_of_delivery
- Output: score_0_100 — shows visibility_score, top_gap, next_step
- CTA (single): **ابدأ تشخيص Dealix**
- Claims guard: Estimate of delivery-visibility maturity. No SLA guarantee implied.
