# Sprint Execution SOP — Complete Operating Procedure
# إجراء التشغيل القياسي الكامل لـ Sprint ذكاء الإيراد

**Service:** Revenue Intelligence Sprint — 499 SAR  
**Duration:** 7 working days  
**Owner:** Founder  
**Version:** Wave 17  
**Date:** 2026-05-31

---

## Pre-Sprint — Day 0: قبل البدء

### Payment Confirmed Checklist / قائمة تأكيد الدفع

- [ ] Payment of 499 SAR received and confirmed in Moyasar dashboard.
- [ ] Receipt issued to client (ZATCA-compliant).
- [ ] Onboarding record created in CRM (`account_id` assigned).
- [ ] Sprint ID generated: format `sprint_{account_id}_{YYYY-MM-DD}`.
- [ ] Engagement ID generated: format `eng_{account_id}_{sequential_number}`.
- [ ] Client folder created in data store (isolated per tenant).

### Welcome Message / رسالة الترحيب

- [ ] Welcome message drafted (bilingual AR + EN).
- [ ] Governance check performed on welcome message text.
- [ ] Message approved by founder before sending.
- [ ] Message sent via approved channel only (no cold WhatsApp).
- [ ] Delivery timestamp logged.

**Message template (AR):**
```
مرحباً [اسم العميل]،

شكراً لاختياركم Dealix. تم تأكيد دفعة Sprint ذكاء الإيراد (499 ريال).
سنبدأ العمل غداً وسنُرسل لكم ملخصاً يومياً.

المدة: 7 أيام عمل
المخرج النهائي: Proof Pack كامل + تقرير ثنائي اللغة
```

### Intake Call / مكالمة الاستقبال

- [ ] Intake call scheduled within 24 hours of payment.
- [ ] Call agenda shared with client (max 30 minutes).
- [ ] Key topics: data sources, main pain point, top 3 accounts to analyse.
- [ ] Call notes recorded and linked to engagement record.

---

## Day 1 — Source Passport Audit / تدقيق جواز المصدر

### What to Collect / ما يجب جمعه

Gather the following from the client:

1. **List of all lead sources** (CRM exports, WhatsApp threads, referral logs, inbound forms).
2. **Source metadata** for each source:
   - Source type: `crm | whatsapp | referral | cold | inbound`
   - Total lead count
   - Qualified lead count
   - Average deal value (SAR) if available
   - Any known data quality issues
3. **Data consent confirmation**: client signs or confirms data use is limited to this engagement.

### Step-by-Step DQ Scoring Process / خطوات تسجيل الدرجة

1. Call `SourcePassportBuilder.build(sources)` with raw source dicts.
2. Review `SourcePassport.overall_dq_score`.
3. Review `SourcePassport.red_flags` — each flag requires a note.
4. Document `recommendations_ar` and `recommendations_en` for client handoff.

### Pass / Fail Criteria / معايير النجاح والفشل

| DQ Score | Status | Action |
|----------|--------|--------|
| >= 70 | PASS | Proceed to Day 2 |
| 50-69 | PARTIAL | Founder reviews; proceed with caveats documented |
| < 50 | FAIL | BLOCK Day 2; request client data remediation |

**IMPORTANT:** If DQ < 70, the founder must review and approve before proceeding.

### Sample Output Format / نموذج المخرج

```json
{
  "sources_audited": 3,
  "all_passports_valid": true,
  "overall_dq_score": 78.5,
  "red_flags": ["low_conversion:cold_outreach (12%)"],
  "recommendations_ar": ["قناة 'cold_outreach' لديها معدل تحويل منخفض..."],
  "recommendations_en": ["Source 'cold_outreach' has a low conversion rate..."]
}
```

---

## Day 2 — Account Scoring / تصنيف الحسابات

### Data Needed from Day 1 / البيانات المطلوبة من اليوم الأول

- Validated source passport (`source_id`, `allowed_use` confirmed).
- Raw account rows from client CRM or provided CSV.
- Minimum required columns per row: `company_name`, `sector`, `city`.

### Scoring Matrix Application / تطبيق مصفوفة التصنيف

1. Parse account rows into `ICPDimensions` objects.
2. Call `icp_score(dims)` for each account.
3. Sort by score descending — select top 10.
4. For each top account, generate bilingual recommended action.

**Scoring weights (ICP):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| b2b_service_fit | 25% | Alignment with B2B service model |
| data_maturity | 20% | Client's data infrastructure quality |
| governance_posture | 15% | Compliance and risk awareness |
| budget_signal | 25% | Budget indicators and capacity |
| decision_velocity | 15% | Speed of decision-making |

### What a Score Means / ما تعنيه الدرجة

| Score Range | Priority | Recommended Action |
|-------------|----------|--------------------|
| 80-100 | Top Priority | Propose Sprint within 48 hours |
| 60-79 | High | Schedule call this week |
| 40-59 | Nurture | Send value-education content |
| < 40 | Low | Long-term watch list |

---

## Day 3 — Draft Pack + Client Check-in / حزمة المسوّدات + تواصل العميل

### Draft Deliverables Checklist / قائمة مسوّدات التسليم

- [ ] 3 WhatsApp drafts (AR + EN variants)
- [ ] 1 email sequence (minimum 1 step)
- [ ] 1 proposal (Markdown format, 499 SAR positioning)
- [ ] Governance check on ALL draft content (no unsafe claims)

**RULE: Every draft MUST pass `policy_check_draft()` before advancing.**

### Governance Check — Unsafe Claims / فحص الحوكمة — الادعاءات غير الآمنة

The following are **always BLOCKED**:
- Any affirmative revenue guarantee (e.g., "we guarantee revenue", "نضمن مبيعات")
- Specific percentage revenue claims without source reference
- Fabricated testimonials or fake metrics

The following are **ALLOWED**:
- Refund/service guarantees ("نضمن استرجاع كامل")
- Negated guarantee disclaimers ("لا نضمن", "we do not guarantee")
- Time-based ROI framing ("equivalent to 15 hours of analyst work")

### Client Check-in Message Template / نموذج رسالة التواصل مع العميل

**Requires approval before sending.**

```
AR: مرحباً [اسم العميل]، اليوم الثالث من Sprint. هل لديك أي توضيحات حول الحسابات التي تريد التركيز عليها؟

EN: Hi [Client Name], we're on Day 3 of the sprint. Do you have any clarifications on the accounts you'd like us to focus on?
```

### How to Handle Client Feedback / كيفية التعامل مع ملاحظات العميل

1. Log all client feedback in the engagement record.
2. If scope change requested: founder must approve any scope extension.
3. If data correction provided: re-run DQ scoring on corrected data.
4. Never commit to deliverables outside the agreed 499 SAR scope without a separate agreement.

---

## Day 4 — Deep Analysis / التحليل المعمّق

### Analysis Framework / إطار التحليل

1. **Revenue Gap Analysis**: Compare actual conversion rates to sector benchmarks.
2. **Data Quality Impact**: Estimate lost opportunities due to poor data hygiene.
3. **Account Prioritisation**: Validate ICP scores against client qualitative knowledge.
4. **Process Bottleneck Identification**: Map where leads are lost in the funnel.

### Tools Used / الأدوات المستخدمة

| Tool | Purpose |
|------|---------|
| `SourcePassportBuilder` | DQ scoring |
| `AccountScoringMatrix` | Account prioritisation |
| `policy_check_draft` | Governance on all outputs |
| `ProofPackBuilder` | Evidence extraction |

### Output Format / صيغة المخرج

Each analysis finding must be:
- **Specific**: tied to an observed data point, not a general claim.
- **Bilingual**: AR and EN variants for all client-facing content.
- **Evidenced**: reference the data source (e.g., "based on 48 CRM records").
- **Non-promotional**: describe what was found, not what was promised.

---

## Day 5 — Proof Pack Assembly / تجميع حزمة الإثبات

### L0 to L2 Evidence Building / بناء الأدلة من L0 إلى L2

| Level | Definition | Source in Sprint |
|-------|-----------|-----------------|
| L0 | Stated claim — not verified | Draft copy, stated pain points |
| L1 | Screenshot / document | Source passport, DQ report, account list |
| L2 | System-generated report | Proof Pack completeness report, sprint output logs |
| L3 | Third-party verified | Accountant/auditor sign-off (post-sprint, optional) |
| L4 | Published case study | Founder-approved + customer-consented (never during sprint) |

### Screenshot Standards / معايير لقطات الشاشة

- All screenshots must include a timestamp.
- Screenshots of client data require explicit consent before inclusion.
- No PII in any proof item or screenshot (redact before logging).
- Screenshots tagged with `evidence_type: screenshot` in the ledger.

### Report Generation / إنشاء التقارير

1. Call `ProofPackBuilder.from_sprint_output(sprint_results, account_id)`.
2. Review each `ProofItem` for accuracy.
3. Verify `completeness_score` — target >= 60 for delivery.
4. If < 60: document gaps and note in delivery handoff.

---

## Day 6 — Capital Asset Registration / تسجيل الأصل الرأسمالي

### What Counts as a Capital Asset / ما الذي يُحتسب أصلاً رأسمالياً

Assets that are **reusable across multiple clients**:

| Asset Type | Example |
|-----------|---------|
| `scoring_rule` | Custom ICP scoring rule for a specific sector |
| `draft_template` | Bilingual message template that passed governance |
| `governance_rule` | Policy rule extracted from this engagement |
| `proof_example` | Anonymised proof pack excerpt |
| `sector_insight` | Documented sector-specific finding |
| `productization_signal` | Feature/service gap identified by client |
| `qa_rubric` | Quality assurance checklist created for this work |
| `arabic_style_pattern` | Validated Arabic copy pattern for reuse |

**Minimum: 1 capital asset per engagement.**

### Registration Procedure / إجراء التسجيل

1. Identify the reusable artifact.
2. Determine asset type from taxonomy above.
3. Call `CapitalAssetRegistry.register(asset)`.
4. Confirm `asset_id` returned and logged.

### Naming Convention / اصطلاح التسمية

```
{asset_type}_{sector}_{YYYY-MM}_{sequential}

Examples:
  draft_template_logistics_2026-06_001
  sector_insight_b2b_services_2026-06_001
  proof_example_retail_2026-06_001
```

---

## Day 7 — Delivery + Retainer Pitch / التسليم + عرض الـRetainer

### Final Report Review Checklist / قائمة مراجعة التقرير النهائي

Before sharing with client, founder must confirm:

- [ ] `SprintProofReport.requires_founder_review = True` (always set).
- [ ] All proof items reviewed — no fabricated metrics.
- [ ] DQ score and account scores are from actual data.
- [ ] All draft content passed governance check.
- [ ] No PII in any client-facing section.
- [ ] `approved_at` field set only after founder sign-off.
- [ ] Capital asset registered (minimum 1).

### Delivery Message Template / نموذج رسالة التسليم

**Requires approval before sending.**

```
AR:
مرحباً [اسم العميل]،

أنهينا Sprint ذكاء الإيراد. في المرفق:
- تقرير Proof Pack الكامل (ثنائي اللغة)
- قائمة أعلى 10 حسابات بمعيار ICP
- توصيات عملية فورية

يسعدنا مناقشة النتائج في مكالمة. هل تناسبكم هذا الأسبوع؟

EN:
Hi [Client Name],

We've completed the Revenue Intelligence Sprint. Attached:
- Full Proof Pack (bilingual)
- Top 10 accounts by ICP score
- Immediate actionable recommendations

We'd love to walk you through the findings. Does a call this week work for you?
```

### Retainer Pitch Timing and Framing / توقيت وإطار عرض الـRetainer

**When to present:**
- ONLY after proof pack delivery and initial client acknowledgement.
- ONLY when `RetainerEligibilityCheck.is_eligible = True`.
- ONLY after founder approves the pitch text.

**How to frame:**
- Lead with proven sprint outcomes (what was actually found and documented).
- Use time/effort ROI framing: "this is equivalent to N hours of analyst work."
- NEVER use revenue guarantees or income projections.
- Present the pitch as an offer, not a commitment.

**Tier selection:**

| Tier | SAR/month | When to Recommend |
|------|-----------|-----------------|
| `starter_2999` | 2,999 | L1 proof + satisfaction 7-7.9 |
| `growth_3999` | 3,999 | L2 proof + satisfaction >= 8 |
| `scale_4999` | 4,999 | L3 proof + satisfaction >= 9 |

---

## Post-Sprint — Week 2: ما بعد Sprint

### NPS Collection Process / عملية جمع تقييم NPS

1. Send NPS request 3-5 days after delivery (not immediately).
2. Single question: "On a scale of 0-10, how likely are you to recommend Dealix?"
3. If score >= 9: ask for written testimonial (with consent for publication).
4. If score 7-8: schedule a brief feedback call.
5. If score < 7: escalate to founder immediately — initiate improvement protocol.

Log NPS score in `RetainerEligibilityCheck.satisfaction_score` for retainer gate.

### Health Score Calculation / حساب درجة الصحة

After NPS collected, compute customer health:

| Dimension | Weight | Signals |
|-----------|--------|---------|
| Engagement | 25% | Response time, call attendance |
| Outcome Achievement | 30% | Proof Pack score, measurable results |
| Data Quality | 20% | DQ score from Day 2 |
| Satisfaction | 25% | NPS score |

Target health score for retainer recommendation: >= 70.

### 30-Day Follow-Up Plan / خطة المتابعة لـ 30 يوماً

| Day | Action | Owner |
|-----|--------|-------|
| D+3 | NPS survey sent | System |
| D+7 | Follow-up call scheduled (if retainer eligible) | Founder |
| D+14 | Retainer pitch presented (if approved) | Founder |
| D+21 | Retainer decision expected | Client |
| D+30 | Health score recalculated | System |

---

## Doctrine Guards — الضوابط الجوهرية

All of the following apply throughout the sprint and must never be bypassed:

1. **APPROVAL_FIRST**: No document is sent to a client without founder review. `requires_founder_review = True` is enforced on all generated outputs.

2. **NO_FAKE_METRICS**: Every number in every report traces back to an actual data source. If a metric cannot be sourced, it is marked L0 (claim) not L1+.

3. **NO_REVENUE_GUARANTEES**: The word "guarantee" is never used with revenue outcomes. ROI framing is time-based or effort-based only.

4. **PII_PROTECTION**: No personally identifiable information appears in proof ledger summaries, case study excerpts, or capital assets. Redaction is applied before logging.

5. **CHANNEL_COMPLIANCE**: No outreach via cold WhatsApp, LinkedIn scraping, or unsolicited channels. All outreach drafts pass `policy_check_draft()` before approval.

6. **EVIDENCE_INTEGRITY**: Proof item levels are never auto-promoted. L0 stays L0 until manually verified and upgraded by the founder.

---

*This SOP applies to every Revenue Intelligence Sprint engagement. Deviations require written founder approval and must be logged in the friction log.*
