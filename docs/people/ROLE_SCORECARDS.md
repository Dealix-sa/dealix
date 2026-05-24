# Role Scorecards — بطاقات أداء الأدوار

**Purpose / الغرض**
One scorecard per role: mission, inputs, outputs, weekly KPIs, quality bar, handoff format, escalation rules. Replaces vague job descriptions with observable scorecards.
بطاقة أداء لكل دور: المهمة، المدخلات، المخرجات، KPIs أسبوعية، حد الجودة، صيغة التسليم، قواعد التصعيد. تستبدل الوصف الوظيفي المبهم بمعايير قابلة للملاحظة.

**Owner placeholder:** `<founder>` (until a People lead exists).
**Cadence:** Per-role review every 30 days; full set reviewed quarterly. / مراجعة كل دور كل 30 يومًا؛ المجموعة الكاملة فصليًا.
**KPIs:** (1) % of roles with current scorecard, (2) % of contractors scoring "on bar" or above for two consecutive 30-day cycles, (3) count of new roles added without a scorecard (target: 0).
**Risk if missing / مخاطر الغياب:** People do their version of "good work" instead of Dealix's. Reviews become opinion. Hires regress to the mean. / يفعل كل شخص نسخته من «العمل الجيد» بدلًا من نسخة Dealix. التقييم يصبح رأيًا. التوظيفات تنحدر إلى المتوسط.

---

## EN summary

Each role has a one-page scorecard with seven sections: mission (one line), inputs, outputs, weekly KPIs, quality bar, handoff format, and escalation rules. This doc holds the canonical scorecards for the eight named Dealix contractor roles, plus a template for any new role. Scorecards live alongside, not instead of, the role SOPs in `docs/team/` and the org-level scorecards in `docs/scorecards/`.

## ملخص بالعربية

كل دور لديه بطاقة في صفحة واحدة من سبعة أقسام: المهمة (سطر)، المدخلات، المخرجات، KPIs أسبوعية، حد الجودة، صيغة التسليم، قواعد التصعيد. هذا المستند يحوي البطاقات القياسية للأدوار الثمانية، مع قالب لأي دور جديد. البطاقات تتعايش مع SOPs الأدوار في `docs/team/` وبطاقات المستوى التنظيمي في `docs/scorecards/`.

---

## القالب الموحد / Unified template

```yaml
role: <role name>
mission: <one line: the single outcome this role exists to produce>
inputs:
  - <bullet>
outputs:
  - <bullet>
weekly_kpis:
  - <bullet — observable, countable>
quality_bar:
  - <bullet — refer to docs/team/<role>_sop.md>
handoff_format:
  - <bullet — exact artifact format and where it is filed>
escalation_rules:
  - <bullet — what to escalate, to whom, and within what time>
```

---

## 1) Growth Operator — مشغّل النمو

```yaml
role: Growth Operator
mission: Ship founder-approved demand-side artifacts that produce qualified conversations — never automated outreach.
inputs:
  - sector hypothesis from docs/strategy/VERTICAL_PLAYBOOKS.md
  - approved messaging language from docs/01_category/CATEGORY_LANGUAGE.md
  - target list curated by Saudi B2B Researcher
outputs:
  - drafted artifacts (posts, case-safe summaries, one-pagers) sent for founder approval
  - per-artifact distribution plan, manually executed and logged
weekly_kpis:
  - artifacts shipped (count, with founder sign-off)
  - qualified conversations produced (count, attributable)
  - net promoter signal from people on receiving end (anecdotal, captured)
quality_bar:
  - no marketing claims that violate docs/00_constitution/NON_NEGOTIABLES.md
  - no outreach automation; no scraping; no cold WhatsApp
handoff_format:
  - markdown draft + tracked source links + a one-paragraph rationale
escalation_rules:
  - any message that names a competitor → founder before send
  - any artifact that quotes a customer → founder + permission verification
```

---

## 2) Saudi B2B Researcher — باحث الأعمال السعودي

```yaml
role: Saudi B2B Researcher
mission: Produce sector-grade, PDPL-compliant target intelligence that is precise enough to guide outreach without ever doing the outreach.
inputs:
  - sector and sub-sector hypothesis
  - ICP definition from docs/company/ICP.md
  - approved sources list from docs/ops/SAUDI_DATA_SOURCE_CATALOG.md
outputs:
  - per-week target intelligence file with entity-level facts (no personal PII unless explicitly permitted)
  - source-passport entries per docs/04_data_os/SOURCE_PASSPORT.md
weekly_kpis:
  - target entities researched (count)
  - source-passport entries created (count)
  - rejected entries due to ICP mismatch (count, with reason)
quality_bar:
  - no scraping in violation of source terms
  - no PII beyond what is permitted by docs/governance/PDPL_DATA_RULES.md
handoff_format:
  - structured table + passport file references + a one-paragraph signal summary
escalation_rules:
  - any source that has changed its terms → freeze and notify founder
  - any entity that crosses into "do not pursue" list → flag and exit
```

---

## 3) Sales Asset Designer — مصمم أصول البيع

```yaml
role: Sales Asset Designer
mission: Turn approved proposal text into a polished, dignified, sector-appropriate artifact within 48 hours of brief.
inputs:
  - approved proposal text from docs/29_sales_os/PROPOSAL_OS.md
  - brand voice doc docs/company/BRAND_VOICE.md
outputs:
  - finished PDF (or web artifact) ready for send
  - reusable template updates when patterns emerge
weekly_kpis:
  - artifacts shipped within SLA (count, with on-time %)
  - rework rounds per artifact (target: ≤ 1)
quality_bar:
  - no claim added beyond what is in the approved text
  - typography, alignment, and bilingual layout meet brand guide
handoff_format:
  - final PDF + editable source + a one-page change log per template
escalation_rules:
  - any content change request from a customer → not designer's call; route to founder
  - any deviation from brand voice → not designer's call; route to founder
```

---

## 4) RevOps Assistant — مساعد عمليات الإيرادات

```yaml
role: RevOps Assistant
mission: Keep the pipeline truthful, fresh, and aligned with the proposal system.
inputs:
  - opportunity records from the canonical CRM
  - proposal records from docs/29_sales_os/PROPOSAL_OS.md
  - founder weekly priorities
outputs:
  - daily pipeline reconciliation
  - weekly pipeline health report
  - meeting scheduling coordination
weekly_kpis:
  - pipeline freshness lag (target < 24 hours)
  - reconciliation discrepancies caught (count)
  - meeting reschedules avoided (count)
quality_bar:
  - no record updated without source reference
  - no PII shared cross-tool without permission
handoff_format:
  - daily standup line + weekly written report
escalation_rules:
  - any stage change > 1 step in a day → founder ping
  - any opportunity > 60 days in same stage → opens a review entry
```

---

## 5) Delivery Coordinator — منسّق التسليم

```yaml
role: Delivery Coordinator
mission: Make sure every paid engagement ships on time, on scope, with proof — and the founder does not redo it.
inputs:
  - signed scopes from docs/29_sales_os/PROPOSAL_OS.md
  - sprint plan from docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md
outputs:
  - sprint schedule with named milestones
  - weekly delivery health report
  - per-engagement proof-pack assembly per docs/07_proof_os/PROOF_PACK_STANDARD.md
weekly_kpis:
  - milestones hit on time (%)
  - delivery rework requests (count, by source)
  - active engagements with health = green (count)
quality_bar:
  - every milestone has a written acceptance criterion
  - every proof event filed per the standard
handoff_format:
  - sprint plan + weekly report + closing proof pack
escalation_rules:
  - any milestone at risk > 48h → founder
  - any governance event → founder + governance owner
```

---

## 6) Trust/QA Reviewer — مراجع الثقة والجودة

```yaml
role: Trust/QA Reviewer
mission: Block any outbound artifact that breaches Dealix's claim-safety, governance, or PDPL line.
inputs:
  - any outbound artifact (proposals, posts, case summaries, decks)
  - the canonical claim-safety standard docs/05_governance_os/CLAIM_SAFETY.md
outputs:
  - written sign-off (or written hold) per artifact
  - red-flag log filed in docs/07_proof_os/PROOF_OS.md
weekly_kpis:
  - artifacts reviewed (count)
  - artifacts held with reason (count)
  - red flags raised per outbound class
quality_bar:
  - every sign-off references at least one canonical doc
  - holds are always specific and remediable
handoff_format:
  - one-paragraph written verdict + edit suggestions
escalation_rules:
  - any breach of docs/governance/FORBIDDEN_ACTIONS.md → founder + governance owner
  - any pattern observed across 3+ artifacts → opens a recurring-pattern entry
```

---

## 7) Frontend Polish Engineer — مهندس صقل الواجهة

```yaml
role: Frontend Polish Engineer
mission: Make the customer-facing surface look as careful as the back-end is. Polish, accessibility, performance.
inputs:
  - shipping web routes
  - brand voice docs/company/BRAND_VOICE.md
  - accessibility baseline
outputs:
  - per-week visible polish improvements
  - performance baseline maintained or improved
  - bilingual RTL/LTR consistency verified
weekly_kpis:
  - polish PRs merged (count)
  - performance regressions caught (count)
  - accessibility issues resolved (count)
quality_bar:
  - no shipping a page that fails the bilingual baseline
  - no shipping a page that regresses the performance baseline
handoff_format:
  - PR description with before/after screenshots
escalation_rules:
  - any user-facing claim copy change → route to founder, not designer
```

---

## 8) Data Ops Assistant — مساعد عمليات البيانات

```yaml
role: Data Ops Assistant
mission: Classify, clean, and prepare data inside Dealix's data lake without ever touching PII outside the allowed scope.
inputs:
  - raw inbound data files
  - the data lake spec docs/ops/DATA_LAKE_PLAYBOOK.md
  - PII classification rules docs/04_data_os/PII_CLASSIFICATION.md
outputs:
  - cleaned, classified, source-passported datasets
  - per-week data quality score per docs/04_data_os/DATA_QUALITY_SCORE.md
weekly_kpis:
  - datasets processed (count)
  - DQ score average per dataset
  - PII handling exceptions (target: 0)
quality_bar:
  - no dataset enters the lake without a passport
  - no PII processed outside the allowed scope
handoff_format:
  - dataset + passport + one-paragraph data note
escalation_rules:
  - any PII exception → founder + governance owner within 24h
  - any DQ score < threshold → freeze the dataset, open a review entry
```

---

## القالب للأدوار المستقبلية / Template for future roles

```yaml
role: <future role>
mission: <one line>
inputs:
  - <bullet>
outputs:
  - <bullet>
weekly_kpis:
  - <bullet>
quality_bar:
  - <bullet>
handoff_format:
  - <bullet>
escalation_rules:
  - <bullet>
notes_for_first_30_days:
  - <bullet>
```

> Every new role added to the team must have a scorecard merged before the first paid hour. / كل دور جديد يُضاف للفريق يجب أن تُدمَج بطاقته قبل أول ساعة مدفوعة.

---

## القواعد التي لا تُكسر / Hard rules

- Never replace a role SOP with a scorecard; both exist.
- Never let a role escalate by chat. Always written, in the engagement record.
- Never widen a role's mission silently. Mission changes go through the founder and the role SOP.
- Never use a scorecard as a basis for personal evaluation without two consecutive 30-day cycles of observation.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
A scorecard records expectations; it does not promise outcomes. Outcomes are observed across at least two 30-day cycles.

## Related canonical docs

- `docs/team/founder_sop.md`
- `docs/team/sales_sop.md`
- `docs/team/delivery_lead_sop.md`
- `docs/team/qa_reviewer_sop.md`
- `docs/team/ai_engineer_sop.md`
- `docs/team/client_success_sop.md`
- `docs/scorecards/BUSINESS_UNIT_SCORECARD.md`
- `docs/scorecards/PROJECT_SCORECARD.md`
- `docs/people/CONTRACTOR_PLAYBOOK.md`
- `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`
