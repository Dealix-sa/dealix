# Dealix — Value Measurement — قياس القيمة

The board-grade metric set Dealix reports against. Each metric has a definition, a formula, a source-of-truth system, a review cadence, and a named owner. Vanity metrics are excluded by design.

مجموعة المؤشرات بمستوى المجلس التي يعتمدها ديلكس. لكل مؤشر تعريف وصيغة ومصدر حقيقة ودورة مراجعة ومالك مُسمّى. لا يُعرض مؤشر شكليّ.

---

## 1. Board Metrics Catalogue — كاتالوج مؤشرات المجلس

### 1.1 Verified Revenue — الإيراد المُتحقَّق
- **Definition.** Revenue recorded in the customer's billing or contract system that is attributable, through the audit chain, to a Dealix-governed workflow.
- **Formula.** Sum of contracts and retainers with an attribution reference in the Evidence Pack.
- **Source of truth.** Customer billing system + CRM.
- **Cadence.** Monthly reconciliation; quarterly board reporting.
- **Owner.** CRO (customer-side) + Dealix Risk & Compliance.

### 1.2 Revenue Quality — جودة الإيراد
- **Definition.** Share of Verified Revenue that is recurring (retainer-class) or expansion of an existing relationship.
- **Formula.** Recurring + Expansion / Verified Revenue.
- **Source of truth.** Billing system.
- **Cadence.** Monthly.
- **Owner.** CFO.

### 1.3 Pipeline Quality — جودة القمع
- **Definition.** Share of opportunities classified as Evidenced (linked to source-of-truth signals) versus Estimated (unverified).
- **Formula.** Evidenced opps / Total opps in the window.
- **Source of truth.** CRM + Evidence Pack.
- **Cadence.** Weekly operational; monthly board.
- **Owner.** Commercial Lead.

### 1.4 Gross Margin — الهامش الإجمالي
- **Definition.** Gross margin on Dealix-attributed revenue, after delivery and tooling costs.
- **Formula.** (Revenue − Direct delivery costs − Tooling costs) / Revenue.
- **Source of truth.** Finance ledger.
- **Cadence.** Monthly.
- **Owner.** CFO.

### 1.5 Retainer Conversion — تحويل الاشتراكات
- **Definition.** Share of pilots that convert into a monthly retainer within 90 days of pilot close.
- **Formula.** Pilots converted / Pilots closed.
- **Source of truth.** Contract system.
- **Cadence.** Monthly trailing 90-day window.
- **Owner.** Commercial Lead.

### 1.6 Agent ROI — عائد الوكيل
- **Definition.** Net contribution per agent — verified revenue or cost-avoidance attributed to the agent, net of its tooling and oversight cost.
- **Formula.** (Attributed revenue + Verified cost-avoidance − Tooling − Oversight) / Period.
- **Source of truth.** Evidence Pack outcome graph + Finance ledger.
- **Cadence.** Quarterly.
- **Owner.** PMO + Finance.

### 1.7 Trust Incidents — حوادث الثقة
- **Definition.** Count of recorded incidents by severity (S0/S1/S2/S3) in the period.
- **Formula.** Sum by severity.
- **Source of truth.** Incident response log.
- **Cadence.** Continuous; monthly board summary.
- **Owner.** Risk & Compliance.
- **Target.** S0 = 0; S1 ≤ 1 per quarter; all classes trend toward zero.

### 1.8 Approvals Pending — الموافقات المعلّقة
- **Definition.** Count and aging of items waiting in the Approval Center by class.
- **Formula.** Count, mean age, p90 age, breach count.
- **Source of truth.** Approval Center.
- **Cadence.** Daily operational; weekly board snapshot.
- **Owner.** PMO.

### 1.9 Assets Created — الأصول المُنتَجة
- **Definition.** Count of reusable governance and revenue artifacts produced in the period (policies, registries, matrices, evidence packs, playbooks).
- **Formula.** Count by class.
- **Source of truth.** Asset library + Evidence Pack archive.
- **Cadence.** Monthly.
- **Owner.** Risk & Compliance + Dealix delivery lead.

### 1.10 Assets Reused — الأصول المُعاد استخدامها
- **Definition.** Count of reuses of an existing asset across engagements or accounts.
- **Formula.** Count of reuse events; ratio of reuse to creation.
- **Source of truth.** Asset library reference graph.
- **Cadence.** Monthly.
- **Owner.** Dealix delivery lead.

### 1.11 Partner Revenue — إيراد الشركاء
- **Definition.** Revenue attributable to agency or partner channels operating on Dealix rails.
- **Formula.** Sum of partner-attributed contracts and retainers.
- **Source of truth.** Billing system + Partner attribution table.
- **Cadence.** Monthly.
- **Owner.** Partner Lead.

### 1.12 Founder Time Leverage — رافعة وقت المؤسس
- **Definition.** The fraction of founder time spent on compounding artifacts (assets, approvals, evidence reviews) versus one-off interventions.
- **Formula.** (Compounding hours) / (Total tracked founder hours).
- **Source of truth.** Founder office time ledger.
- **Cadence.** Monthly.
- **Owner.** Founder office.
- **Target.** Trend upward. Below 50% is a flag.

---

## 2. Founder Time Leverage — التفصيل

**Why we measure it.** The founder is the highest-cost, highest-leverage decision-maker in the system. Time spent on one-off interventions is time not spent on compounding decisions. We measure leverage to make founder time a board-visible asset.

**What counts as compounding.**
- Drafting or signing off on policy, registry, or matrix updates that apply to multiple engagements.
- Approving Evidence Packs that document a reusable pattern.
- Decisions on enterprise discounts (because they set a precedent).
- Mentoring sessions that produce a recorded artifact.

**What counts as one-off (not compounding).**
- Single-customer firefighting without a documented learning.
- Repeat administrative approvals that should be standing rules.
- Ad-hoc external communication that does not change the system.

**Operational rule.** When one-off interventions exceed half of tracked founder time, the next planning cycle prioritizes converting them into compounding artifacts.

**AR.**
**لماذا نقيسه.** المؤسس صانع القرار الأعلى تكلفة والأعلى رافعة. الوقت في تدخلات لمرة واحدة ليس وقتًا على قرارات تتراكم. نقيس الرافعة لجعل وقت المؤسس أصلًا مرئيًا للمجلس.

**ما يُعدّ مُتراكمًا.** صياغة أو اعتماد تحديثات السياسة والسجل والمصفوفة تنطبق على عدة ارتباطات، اعتماد حقائب أدلة تُوثّق نمطًا مُعاد استخدامه، قرارات الخصم المؤسسي (لأنها سابقة)، جلسات إرشاد تنتج أصلًا مُسجَّلًا.

**ما لا يُعدّ مُتراكمًا.** إطفاء حرائق عميل دون تعلّم موثّق، اعتمادات إدارية متكررة يفترض أن تتحوّل قواعد دائمة، اتصالات خارجية مرتجلة لا تغيّر النظام.

**القاعدة.** حين تتجاوز التدخلات لمرة واحدة نصف وقت المؤسس المُتتبَّع، تُولي الدورة التالية تحويلها إلى أصول مُتراكمة.

---

## 3. What This Catalogue Refuses — ما يرفضه الكاتالوج

- Replies, opens, impressions, calls dialed, messages sent, or any activity metric displayed as a board outcome.
- Pipeline counts unattached to source-of-truth signals.
- Closed-deal metrics not reconciled to billing.
- Projections branded as facts.

**AR.** يرفض الكاتالوج: الردود والفتح والظهور وعدد المكالمات والرسائل أو أي مؤشر نشاط كنتيجة للمجلس؛ أعداد القمع غير المرتبطة بإشارات المصدر؛ مؤشرات الإغلاق غير المُسوّاة مع الفوترة؛ التوقعات بلباس الحقائق.

---

## 4. Reporting Cadence Summary — ملخّص دورة التقارير

| Cadence | Recipients | Contents |
|---|---|---|
| Daily | PMO + Risk on-call | Approvals Pending, Trust Incidents (S0/S1 alerts) |
| Weekly | Commercial Lead, Risk, PMO | Pipeline Quality, Approvals breaches, Asset events |
| Monthly | Executive sponsor, CFO, CRO | Verified Revenue, Revenue Quality, Gross Margin, Retainer Conversion, Partner Revenue |
| Quarterly | Board / Risk Committee | Agent ROI, Trust Incidents trend, Assets Created/Reused, Founder Time Leverage |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/enterprise/GOVERNANCE_MODEL.md` · `/home/user/dealix/docs/enterprise/IMPLEMENTATION_PLAN.md` · `/home/user/dealix/docs/business/PRICING_RULES.md`
