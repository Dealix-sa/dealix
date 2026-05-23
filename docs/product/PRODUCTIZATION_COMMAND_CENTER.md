# Productization Command Center — مركز قيادة التحويل لمنتج

## Purpose
Single dashboard showing every workflow Dealix has run manually, where it sits on the path from manual service to product, and whether it is earning the right to be templated, automated, or promoted to a SaaS candidate. Prevents premature productization and surfaces overdue candidates.

## Owner
Founder (Bassam). Reviewed weekly. No delegation pre-Series A.

## Inputs
- Delivery ledger entries from `docs/03_commercial_mvp/`.
- Workflow logs from `docs/product/WORKFLOW_REGISTRY.md`.
- Repetition counter from delivery analyst.
- Client feedback evidence (see `docs/client_success/FEEDBACK_LOOP.md`).
- Margin and time-to-deliver data from `docs/finance/`.

## Outputs
- Ranked table of productization candidates with stage, repetition count, evidence link, ROI estimate (manual hours saved × frequency × billable rate).
- Weekly "promote / hold / kill" decision per candidate.
- Quarterly SaaS candidate shortlist fed into `docs/product/SAAS_CANDIDATE_RULES.md`.

## Rules
1. No candidate enters this board without 3 paid manual deliveries documented.
2. No candidate is automated until 5 templated deliveries succeed without rework above 10%.
3. No SaaS bet without 10 automated runs proving margin > 60% and < 1 escalation per 10 runs.
4. Estimated ROI is labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
5. Candidate cannot skip stages. Skipping triggers kill review.

## Metrics
- Candidates in pipeline (count by stage).
- Average stage age (days).
- Promotion rate stage-to-stage.
- Kill rate (target ≥ 30% — discipline signal).
- Realised hours saved vs estimated (quarterly).

## Cadence
- Weekly: 30-minute founder review.
- Monthly: cross-check against `docs/founder/CEO_MASTER_DASHBOARD.md`.
- Quarterly: SaaS candidate promotion decision.

## Evidence
- `evidence/productization/<candidate_id>/manual_runs.md`
- `evidence/productization/<candidate_id>/template_runs.md`
- `evidence/productization/<candidate_id>/automation_runs.md`
- Client written approval before any case study or partner referral.

## Verifier
Founder counter-signs. Delivery analyst validates repetition counts. No automated promotion.

## Runtime Command
`make productization-review` — opens this dashboard, prints the candidate table, blocks if any candidate exceeds 90 days at one stage without explicit hold reason.

## Arabic Summary — ملخص عربي
هذه اللوحة تعرض كل مهمة يدوية تم تنفيذها، ومرحلتها على مسار التحويل لمنتج. لا يُرقَّى عمل ما إلى قالب قبل ثلاث عمليات يدوية ناجحة، ولا إلى أتمتة قبل خمس عمليات قالبية ناجحة، ولا إلى منتج SaaS قبل عشر عمليات آلية مُربحة. القيم التقديرية ليست مُتحقَّقة.
