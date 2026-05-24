# Contractor Playbook — دليل تشغيل المتعاقدين

**Purpose / الغرض**
How Dealix brings on a Saudi B2B contractor — scope, weekly check-ins, success criteria, kill clause, payment terms (placeholders), and trust-page mention rules.
كيف يُضمّ متعاقد سعودي B2B إلى Dealix — النطاق، اللقاء الأسبوعي، معايير النجاح، شرط الإنهاء، شروط الدفع (placeholders)، وقواعد ذكر المتعاقد في صفحات الثقة.

**Owner placeholder:** Hiring lead = `<founder>` initially.
**Cadence:** Per engagement. Quarterly review of active contractors. / لكل ارتباط. مراجعة فصلية للمتعاقدين النشطين.
**KPIs:** (1) median time from intro to first delivered output (target ≤ 14 days), (2) % of contractors with weekly check-in completed on time, (3) % renewed past first 60 days.
**Risk if missing / مخاطر الغياب:** Founder over-hires fast, then redoes everyone's work. Or under-hires, becomes the bottleneck. Both kill momentum. / المؤسس يوظّف بسرعة ثم يعيد عمل الجميع. أو لا يوظّف فيصبح عنق الزجاجة. كلاهما يقتل الزخم.

---

## EN summary

A contractor is brought on for a specific outcome, not for a general "help". The playbook has six parts: scope template, intake checklist, weekly check-in format, written success criteria, an explicit kill clause, and payment terms left as placeholders until the founder writes them. The contractor's mention on any external page follows the trust-page mention rules.

## ملخص بالعربية

يُجلَب المتعاقد لنتيجة محددة، لا لـ«المساعدة العامة». الدليل من ستة أجزاء: قالب النطاق، قائمة الاستقبال، صيغة اللقاء الأسبوعي، معايير نجاح مكتوبة، شرط إنهاء واضح، وشروط دفع تبقى placeholders حتى يكتبها المؤسس. ذكر المتعاقد على أي صفحة خارجية يتبع قواعد ذكر صفحة الثقة.

---

## الأدوار المعتمدة / Approved roles

This playbook applies to the eight Saudi B2B contractor roles already named in the repo. Each has an existing SOP in `docs/team/`:

| Role | Existing SOP |
|---|---|
| Growth Operator | references in `docs/team/sales_sop.md` |
| Saudi B2B Researcher | references in `docs/team/sales_sop.md` |
| Sales Asset Designer | references in `docs/team/sales_sop.md` |
| RevOps Assistant | references in `docs/team/sales_sop.md` |
| Delivery Coordinator | `docs/team/delivery_lead_sop.md` |
| Trust/QA Reviewer | `docs/team/qa_reviewer_sop.md` |
| Frontend Polish Engineer | references in `docs/team/ai_engineer_sop.md` |
| Data Ops Assistant | references in `docs/team/ai_engineer_sop.md` |

> Scorecards for each role live in `docs/people/ROLE_SCORECARDS.md`. The Contractor Playbook governs how they are onboarded, paid, reviewed, and exited.

---

## 1) قالب النطاق / Scope template

كل عقد متعاقد يبدأ بصفحة scope واحدة. لا أكثر.

```yaml
contractor_role: <one of the 8 roles>
engagement_label: ENG-YYYYMMDD-<role-code>
duration: <weeks>
hours_per_week_estimate: <number, capped>
outcome_definition: |
  <one paragraph; observable, time-bound, and tied to one of the strategic goals
   in docs/strategy/DEALIX_GOAL_TREE.md>
in_scope:
  - <bullet>
  - <bullet>
out_of_scope:
  - <bullet>
  - <bullet>
inputs_provided_by_dealix:
  - <bullet>
output_format:
  - <e.g., 1 weekly written summary + final artifact in agreed format>
quality_bar:
  - <reference docs/team/<role>_sop.md>
escalation_owner: <role>
review_cadence: weekly
success_criteria: <see section 4>
kill_clause: <see section 5>
payment_terms: <placeholder until set by founder>
trust_page_mention: not-permitted-until-explicit-approval
data_handling: bound by docs/governance/PDPL_DATA_RULES.md
```

---

## 2) قائمة استقبال أول 7 أيام / Intake checklist — first 7 days

| Day | Task | Owner |
|---|---|---|
| Day 0 | Send signed scope page + the role SOP from `docs/team/`. | Hiring lead |
| Day 0 | Grant access only to the data/tools needed; least-privilege per `docs/governance/PDPL_DATA_RULES.md`. | Hiring lead |
| Day 1 | 45-minute kickoff: read scope together, agree on first deliverable and date. | Hiring lead + contractor |
| Day 2 | Contractor submits a one-page understanding doc echoing the scope back. | Contractor |
| Day 3 | Hiring lead returns one round of corrections in writing. | Hiring lead |
| Day 5 | First deliverable due (small, intentional). | Contractor |
| Day 7 | First weekly check-in. | Both |

> No verbal kickoff without a written scope. No data access before a written understanding doc. / لا انطلاق شفهي بدون scope مكتوب. لا وصول بيانات قبل وثيقة فهم مكتوبة.

---

## 3) اللقاء الأسبوعي / Weekly check-in (30 minutes max)

```yaml
agenda:
  - last_week_delivered: 5 min   # what shipped; not what was attempted
  - quality_review: 10 min       # founder/hiring lead returns specific edits
  - next_week_one_outcome: 10 min  # exactly one concrete deliverable
  - blockers_and_asks: 5 min     # closed by the end of the call
```

Rules:
- The contractor sends the agenda 24 hours before. No agenda → meeting moves a day.
- "Things I tried" is not a deliverable. Only completed artifacts count.
- Any change in scope is captured in writing within 24 hours, never verbally.

---

## 4) معايير النجاح / Success criteria

لكل دور، معايير نجاح تُكتب في scope وتُراجَع كل أسبوعين:

| Role | Headline success criterion |
|---|---|
| Growth Operator | Demand-side artifacts shipped weekly with founder approval. No outreach automation. |
| Saudi B2B Researcher | One sector-specific ICP list per week with verified entity data, no PII handling beyond what is permitted. |
| Sales Asset Designer | One polished proposal/deck per active opportunity within 48 hours of brief. |
| RevOps Assistant | Pipeline freshness < 24 hours; all stages reconciled with `docs/29_sales_os/PROPOSAL_OS.md`. |
| Delivery Coordinator | Active sprints tracked, no missed milestones, weekly delivery health report. |
| Trust/QA Reviewer | Every outbound proof artifact reviewed before send; written sign-off filed. |
| Frontend Polish Engineer | Visible polish improvements shipped weekly; no regression on Lighthouse-style baseline. |
| Data Ops Assistant | All inbound data classified per `docs/04_data_os/PII_CLASSIFICATION.md` before use. |

> A success criterion that cannot be observed within two weeks is not a success criterion — rewrite it. / المعيار الذي لا يمكن ملاحظته خلال أسبوعين ليس معيارًا — أعد صياغته.

---

## 5) شرط الإنهاء / Kill clause

Every contract has an explicit kill clause. It is not punitive; it is a planning tool.

### Default kill conditions

- Two consecutive weeks with no shipped deliverable and no agreed reason.
- One unambiguous breach of `docs/governance/PDPL_DATA_RULES.md` or `docs/governance/FORBIDDEN_ACTIONS.md`.
- One unauthorized external communication on behalf of Dealix.
- A written notice from either party with 14 days' notice for any reason.

### Process

1. Written notice referencing the specific clause.
2. 14-day wind-down with a defined handoff list.
3. Final invoice cleared per the payment terms in the contract.
4. Access revoked at the end of business on the last day.
5. Closing 30-minute call: what worked, what did not. Filed in `docs/memory/delivery_lessons.md`.

> Kill is never communicated by chat alone. Always in writing, in the engagement record. / الإنهاء لا يبلَّغ بالمحادثة وحدها. دائمًا كتابةً، في سجل الارتباط.

---

## 6) شروط الدفع / Payment terms

> All monetary values in this section are **placeholders**. The founder fills them per engagement and per `docs/company/PRICING_DECISION.md`.

| Field | Placeholder | Note |
|---|---|---|
| Rate type | `<hourly | weekly | per-deliverable>` | Choice depends on role. |
| Rate value | `<SAR>` | Set by founder per engagement. |
| Currency | SAR | Default. |
| Invoice frequency | `<weekly | biweekly | per-deliverable>` | Set in scope page. |
| Payment terms | `Net-XX` | Aligned with `docs/revenue/INVOICE_FLOW.md`. |
| Late-payment policy | `<placeholder>` | Set in scope; never opaque. |
| Bonuses / overruns | None unless explicitly written. | No surprise commitments. |

Hard rules:
- No commitment to a rate without the founder's written approval per engagement.
- No equity, no token, no future-payment promises in this playbook. Those require a separate written instrument.
- No payment made before a deliverable is logged in the engagement record.

---

## 7) قواعد ذكر المتعاقد على Trust Page / Trust-page mention rules

| Status | What is allowed |
|---|---|
| Default | The contractor is **not named** on any external page. |
| After 60 days of active engagement | A role-level mention may be made (e.g., "Trust/QA Reviewer") with written permission from the contractor. |
| Naming a person publicly | Requires explicit written consent of the contractor and founder approval. |
| Sharing a contractor's work as a Dealix artifact | Allowed; the contractor is acknowledged internally; external mention follows the rules above. |
| Quoting a contractor publicly | Never without written consent and pre-agreed wording. |

> Reference `docs/14_trust_os/TRUST_PACK.md` for the mention format and `docs/governance/PDPL_DATA_RULES.md` for any PII handling. / يُرجى مراجعة Trust Pack لصيغة الذكر، وقواعد PDPL لأي تعامل مع PII.

---

## قواعد لا تُكسر / Non-negotiables

- Never delegate Founder-only work per `docs/team/founder_sop.md` (positioning, pricing, governance exceptions).
- Never grant a contractor access to a tool or data store beyond what their scope requires.
- Never let an engagement run > 30 days without a weekly check-in record.
- Never let a contractor send external communication "on behalf of Dealix" without explicit founder approval per `docs/05_governance_os/CHANNEL_POLICY.md`.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
No payment number, term, or commitment in this doc is a contract. Placeholders are set by the founder per engagement.

## Related canonical docs

- `docs/team/founder_sop.md`
- `docs/team/sales_sop.md`
- `docs/team/delivery_lead_sop.md`
- `docs/team/qa_reviewer_sop.md`
- `docs/team/ai_engineer_sop.md`
- `docs/team/client_success_sop.md`
- `docs/people/ROLE_SCORECARDS.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/05_governance_os/CHANNEL_POLICY.md`
- `docs/14_trust_os/TRUST_PACK.md`
- `docs/revenue/INVOICE_FLOW.md`
