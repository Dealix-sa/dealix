# Revenue Factory OS | نظام مصنع الإيرادات

## Purpose | الغرض
The Revenue Factory OS is Dealix's full revenue flow, end-to-end:
Lead → Score → Approve → Draft → Send/Manual → Reply → Sample → Proposal → Payment
→ Delivery → Retention → Proof → Referral.

Every external-facing action is draft → founder approval → queue → manual send.
Nothing is autopilot.

## End-to-end flow | التدفق الكامل
1. **Lead** — captured by Intelligence layer (sector + ICP + trigger + scoring)
2. **Score** — Account Scoring Model assigns A / B / C / Reject
3. **Approve** — founder approves the account for entry into outreach
4. **Draft** — Outbound / LinkedIn / Email / Form / ABM machine produces draft
5. **Send (manual)** — founder approves and manually sends (or pastes)
6. **Reply** — Reply Router classifies and routes
7. **Sample** — Sample Factory produces a tailored sample artifact for buyer
8. **Proposal** — Proposal Factory drafts a proposal; founder approves & sends
9. **Payment** — Payment Capture OS handles invoice + payment link + reconciliation
10. **Delivery** — Delivery QA OS + Ultimate Delivery OS run the engagement
11. **Retention** — Retention & Referral OS keeps client engaged & expanded
12. **Proof** — Proof Approval OS converts engagement into a publishable artifact
13. **Referral** — Partner & Client referral loops back to the Lead stage

## State machine | آلة الحالة
Each account passes through stages. Backward transitions allowed; forward
transitions require trust-gate clearance.

| Stage | Required gate | Approval class |
|---|---|---|
| Lead → Score | Trust risk check | A1 |
| Score → Approve | Founder review | A2 |
| Approve → Draft | Persona + trigger present | A1 |
| Draft → Send | Per-draft approval | A2 |
| Send → Reply | (system observed) | n/a |
| Reply → Sample | Reply intent classification | A2 |
| Sample → Proposal | Sample delivered + buyer interest | A2 |
| Proposal → Payment | Founder approval of proposal terms | A2 |
| Payment → Delivery | Payment captured + reconciled | A1 |
| Delivery → Retention | Delivery success criteria met | A1 |
| Retention → Proof | Written client consent | A2 |
| Proof → Referral | Proof published | A1 |

## Non-negotiables | المبادئ
- No external sending without per-action approval
- No price/contract/payment terms in early-stage drafts
- No proof publishing without written client consent
- No guaranteed-revenue claims at any stage
- Every stage transition emits a policy snapshot + audit row

## Sub-systems referenced | الأنظمة الفرعية
- Intelligence: market_domination, sector_ranker, icp_segmenter, persona_synth,
  competitive_tracker, trigger_engine, account_scorer
- Growth: distribution_war_machine + 11 sub-machines
- Sample Factory, Proposal Factory
- Delivery QA OS, Ultimate Delivery OS
- Payment Capture OS, Ultimate Finance OS, AI Unit Economics System
- Retention & Referral OS, Proof Approval OS
- Performance Improvement OS

## Approval classes | فئات الموافقة
- A1 (auto): internal scoring, internal routing, dashboards, audit logging
- A2 (founder approval): all external sends, proof publication, proposal sends,
  payment-link creation
- A3 (escalation): regulated/government accounts, financial commitments, anything
  touching contract terms

## Trust gate | بوابة الثقة (system-wide)
- Source citations preserved at every stage
- PII minimization enforced
- No guarantee/commitment language outside approved contracts
- Policy snapshot + audit row at every stage transition

## Owner | المالك
Founder is the single human accountable for the whole factory.

## Worker name
`revenue.factory_os` (orchestrator over downstream workers)

## KPI tree | شجرة المؤشرات
- Top KPI: cash collected (monthly)
- Sub: MRR, pipeline value, weighted pipeline, paid clients count
- Funnel rates: lead → A, A → meeting, meeting → proposal, proposal → paid,
  paid → renewal, paid → referral
- Efficiency: founder hours / paid client, AI cost / paid client

## Failure mode | حالات الفشل
- Bottleneck at any stage (most commonly: founder approval throughput)
- State drift (account stuck mid-stage > 30 days)
- Trust-gate violation at any stage halts the factory

## Recovery path | مسار الاسترداد
- Bottleneck dashboard surfaces top 3 stuck stages weekly
- Auto-archive accounts stuck > 90 days with reason
- Any trust-gate violation halts that account's flow and pages founder
