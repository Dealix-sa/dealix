# Customer Success Playbook — Dealix Managed Ops — كتاب تشغيل نجاح العميل: العمليات المُدارة من Dealix

> Cross-references: [docs/sales/PROPOSAL_TEMPLATE_AR_EN.md](../sales/PROPOSAL_TEMPLATE_AR_EN.md) · [docs/ops/SPRINT_EXECUTION_SOP.md](./SPRINT_EXECUTION_SOP.md) · [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) · [docs/08_value_os/VALUE_DASHBOARD.md](../08_value_os/VALUE_DASHBOARD.md) · [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

## 1. Customer Journey Map — خريطة رحلة العميل

Six stages from first contact to long-term retained partnership.

| Stage | Arabic Label | Duration | Primary Actions | Success Signal |
|---|---|---|---|---|
| 1. Discovery | الاكتشاف | 1 week | Free diagnostic call, 1-page summary delivered, ICP confirmed | Prospect requests sprint proposal |
| 2. Activation | التفعيل | 7 days | Sprint executed, Source Passport signed, Proof Pack delivered, handoff call completed | Client reads full Proof Pack, asks follow-up questions |
| 3. Onboarding | الإعداد | Weeks 1–4 of retainer | Client room access granted, health score baseline set, first monthly KPI report delivered, ZATCA check completed | Client logs in to dashboard; names internal workflow owner |
| 4. Adoption | التبني | Months 2–4 | Sprint sessions run monthly, action plan items executed by client, bilingual reports reviewed in QBR | Client cites specific Proof Pack findings in internal decisions |
| 5. Expansion | التوسع | Month 3+ | Expansion signals monitored, upgrade conversation initiated with evidence, additional sprint capacity or tier upgrade proposed | Client upgrades tier or adds scope |
| 6. Advocacy | المناصرة | Month 6+ | Case-safe summary drafted (with client consent), referral conversation initiated, client invited to co-present at industry event | Client provides referral or approves case-safe summary publication |

**Stage ownership:** The founder owns all stages in the MVP phase. As the team grows, Stages 1–2 transfer to sales and Stages 3–6 transfer to a dedicated customer success role.

---

## 2. Health Score Interpretation — تفسير درجة الصحة

The health score is computed weekly across four dimensions: data quality, engagement activity, ZATCA compliance status, and retainer utilization. Each dimension is scored 0–25; total is 0–100.

| Score Range | Status Label / التسمية | Color Code | Meaning | Required Action |
|---|---|---|---|---|
| 80–100 | Healthy / صحي | Green | All dimensions on track; client engaged and utilizing service | Routine: monthly KPI report, next sprint scheduling |
| 60–79 | Moderate / متوسط | Amber | One or two dimensions lagging; client partially engaged | Proactive: schedule check-in call within 5 business days; identify specific drop-off |
| 40–59 | At-Risk / في خطر | Orange | Multiple dimensions declining; client disengaged from sessions or reports | Urgent: founder-led intervention call within 2 business days; retention protocol activated |
| 0–39 | Critical / حرج | Red | Significant deterioration across dimensions; churn risk high | Immediate: founder call within 24 hours; escalation protocol activated; retention plan presented |

**Score calculation notes:**
- Data quality dimension: based on DQ score delta from sprint baseline
- Engagement dimension: based on client response rate to reports and session attendance
- ZATCA dimension: based on invoice completeness and phase readiness flags
- Utilization dimension: based on sprint sessions used vs. allocated per tier

A score below 40 for two consecutive weeks triggers the escalation protocol (see Section 4).

---

## 3. Monthly Touchpoint Calendar — جدول نقاط التواصل الشهرية

| Touchpoint | Frequency | Format | Owner | Duration |
|---|---|---|---|---|
| Weekly health score delivery | Weekly (Monday) | Auto-generated report to client room + summary email | Automated + founder review | 15 min review |
| Weekly status note | Weekly (Monday) | Bilingual (AR + EN) 2-paragraph summary | Founder | 10 min to write |
| Monthly KPI report | First week of each month | PDF report + 30-min walkthrough call | Founder | 45 min |
| Monthly sprint session | Scheduled by mutual availability | 90-minute focused session | Founder + client workflow owner | 90 min |
| ZATCA compliance check | Monthly (or weekly for Enterprise) | Structured checklist output | Founder | 30 min |
| Proof Pack update | Quarterly (Essential) / Monthly (Professional + Enterprise) | 4-section updated pack delivered to client | Founder | 2 hours |
| Quarterly Business Review (QBR) | Quarterly (Professional + Enterprise) | 60-minute structured review: wins, gaps, next quarter | Founder + client decision maker | 60 min |

**Communication protocol:** all reports and summaries are delivered via the client room dashboard and a direct email to the named client contact. No bulk CCs. No third-party distribution without explicit client approval.

---

## 4. Escalation Protocol — بروتوكول التصعيد

**When to escalate to founder:**

| Trigger | Response Time | Action |
|---|---|---|
| Health score drops below 40 | 24 hours | Founder-led call scheduled immediately |
| Client has not opened two consecutive monthly reports | 48 hours | Founder calls to diagnose disengagement |
| Client raises a governance concern (questions about data use, asks about activities outside scope) | Same business day | Founder handles directly; governance log updated |
| Client requests activity prohibited by Non-Negotiables (cold outreach, scraping, guaranteed outcomes) | Same business day | Founder declines clearly and professionally; logs refusal; offers compliant alternative |
| Client indicates they are evaluating competitors or considering cancellation | Same business day | Founder initiates retention conversation |
| Sprint produces a Proof Pack score below 70 | Immediately upon scoring | Founder notifies client, offers remediation or partial credit per refund policy |
| Data incident or suspected PDPL breach | Immediately | PDPL breach runbook activated; see [docs/ops/PDPL_BREACH_RUNBOOK.md](./PDPL_BREACH_RUNBOOK.md) |

**Escalation log:** every escalation is recorded in the client engagement record with date, trigger, action taken, and resolution. This log is part of the Proof Pack record.

---

## 5. Retention Interventions — تدخلات الاحتفاظ

Five specific interventions when health score drops or churn signals appear. Apply in order of severity.

**Intervention 1 — Proactive Check-In Call (المكالمة الاستباقية)**

Applicable when: Moderate health score (60–79) for two consecutive weeks.

Action: schedule a 30-minute call with the client workflow owner. Agenda: (1) what has been useful in the last 30 days, (2) what has not been used and why, (3) one specific action item the client wants help with before the next sprint session. Adjust the next sprint focus based on this call.

**Intervention 2 — Value Recap Report (تقرير مراجعة القيمة)**

Applicable when: client has not engaged with reports for more than two weeks.

Action: produce a single-page bilingual "Value Since Day 1" summary showing: data quality improvement from sprint baseline, number of priority accounts identified, ZATCA findings and status, sprint sessions completed. Deliver with a personal note from the founder. This is a proof of continued value, not a sales pitch.

**Intervention 3 — Scope Recalibration (إعادة معايرة النطاق)**

Applicable when: client is in Moderate or At-Risk and consistently not using allocated sprint sessions.

Action: offer to swap unused sprint sessions for a different deliverable within the same tier — for example, replacing a sprint session with a dedicated ZATCA compliance deep-dive or a bilingual reporting workshop. The tier price does not change; the composition of deliverables adjusts to match actual need.

**Intervention 4 — Founder Executive Meeting (اجتماع المؤسس التنفيذي)**

Applicable when: At-Risk health score (40–59) for two weeks, or any single-week Critical score.

Action: founder requests a meeting directly with the client's CEO or CFO (not only the workflow owner). The meeting agenda: (1) review health score and diagnose root cause, (2) present a specific 60-day recovery plan with named milestones, (3) confirm or renegotiate scope. The recovery plan is documented and signed by both parties.

**Intervention 5 — Tier Adjustment (تعديل الباقة)**

Applicable when: client is paying for a tier whose deliverables exceed their current organizational capacity.

Action: offer a temporary downgrade to the Essential tier at 2,999 SAR/mo with a defined 90-day review point. The downgrade is not presented as a failure — it is presented as matching the service level to the client's current operational tempo. The option to upgrade returns at any time.

---

## 6. Expansion Signals — إشارات التوسع

Seven signals that indicate a client is ready to discuss upgrading tier or adding scope.

1. **Session demand exceeds allocation:** client requests additional sprint sessions beyond the monthly allocation two months in a row.
2. **Health score sustained at 80+:** client has maintained a Healthy score for three consecutive months — operational stability is achieved and the client can absorb more capability.
3. **Data quality above 80:** the data quality dimension has improved to a level where advanced scoring and AI models produce reliable outputs — conditions for higher-tier deliverables are met.
4. **New data source identified:** client mentions a new CRM, ERP, or data system they want to integrate — this is an expansion conversation, not a scope-creep risk.
5. **Executive involvement increasing:** the CEO or CFO begins attending monthly reviews or QBRs — they are seeing value and considering deeper investment.
6. **Referral behavior:** client has already referred another company to Dealix — strong satisfaction signal that correlates with willingness to invest more.
7. **ZATCA phase transition approaching:** the client is entering a new ZATCA wave that requires more intensive compliance monitoring — a factual trigger for a tier upgrade conversation.

**Expansion conversation rule:** the founder initiates the expansion conversation only when two or more signals are present and only in the context of a scheduled monthly review or QBR — not as an unsolicited sales call.

---

## 7. Churn Prevention Checklist — قائمة منع الإلغاء

15-item checklist. Review monthly for every active retainer client.

- [ ] Client has logged into the dashboard in the past 7 days
- [ ] Most recent monthly KPI report was opened (tracking confirmation)
- [ ] Client workflow owner is still in post and still the named contact
- [ ] All scheduled sprint sessions in the past 30 days were conducted (no silent no-shows)
- [ ] Last ZATCA compliance check delivered and acknowledged by client
- [ ] Health score is 60 or above
- [ ] No open governance concerns or data questions left unanswered for more than 48 hours
- [ ] Client has not requested out-of-scope services (if yes: escalation logged, compliant alternative offered)
- [ ] Payment is current — no overdue invoice
- [ ] Client is not in an active procurement process with a competitor (monitor via LinkedIn organic, not scraping)
- [ ] Proof Pack update is current for the relevant tier frequency
- [ ] At least one capital asset has been deposited from the most recent sprint session
- [ ] QBR is scheduled (Professional and Enterprise tiers only) for the current quarter
- [ ] Client has received at least one case-safe pattern that is directly relevant to their sector
- [ ] Next sprint session is on the calendar with a confirmed agenda topic

---

## 8. Proof Pack Update Process — عملية تحديث حزمة الإثبات

Monthly process (Professional and Enterprise) or quarterly process (Essential) to refresh and deliver the client's Proof Pack.

**Step 1 — Data Pull (سحب البيانات)**
Pull the current data quality score, account scoring delta from baseline, ZATCA compliance status, and sprint session log for the period. All data is from Dealix internal systems — no new client data upload is required unless a sprint session was conducted.

**Step 2 — Section Updates (تحديث الأقسام)**
Update the four dynamic sections of the Proof Pack:
- **Data Audit:** current DQ score vs. baseline, changes in data completeness, new fields or sources added
- **Revenue Map:** updated account scoring, dormant accounts re-activated, pipeline movement observations
- **Action Plan:** status of prior action plan items (complete / in progress / deferred), new recommendations for the next period
- **ROI Projection:** updated estimated value metrics based on observed activity — clearly labeled as estimated, not verified

**Step 3 — Governance Review (مراجعة الحوكمة)**
Founder reviews all updates before delivery. Any AI-generated content in the pack is checked against the governance policy — no unchecked assertions, no guaranteed outcomes language.

**Step 4 — Bilingual Check (فحص ثنائية اللغة)**
Confirm Arabic and English sections are parallel in structure and equivalent in content. Arabic is primary. No section exists only in one language.

**Step 5 — Delivery (التسليم)**
Upload to client room dashboard. Send a brief bilingual summary note (2 paragraphs maximum) to the named client contact. Offer a 30-minute review call if the client wants to walk through the updates. Log delivery in the engagement record.

---

## 9. NPS Collection Process — عملية جمع درجة صافي الترويج

PDPL-compliant satisfaction survey process.

**Frequency:** once per quarter, not more frequently.

**Format:** a single two-question survey delivered directly to the named client contact:
1. On a scale of 0–10, how likely are you to recommend Dealix to a business colleague? (Numerical only)
2. What is the primary reason for your score? (Optional, open text, maximum 200 characters)

**PDPL compliance:**
- The survey is sent to only the named client contact with whom Dealix has an active service relationship — not to any other staff at the client company
- The purpose of data collection is stated in the survey header: "Your response helps us improve service quality. This response is stored securely and will not be shared with any third party."
- Retention: survey responses are retained for 24 months and then deleted per the data retention policy
- Right to withdraw: the client may request deletion of their survey history at any time

**Delivery channel:** email to the named contact's business address — the same address used for monthly reports. Not via WhatsApp or social media.

**Reporting:** NPS results are aggregated and included in Dealix's internal capital ledger as a service quality metric. Individual client scores are never published or shared externally without explicit written consent.

---

## 10. Offboarding Process — عملية إنهاء الخدمة

Professional handoff when a client cancels the retainer.

**Step 1 — Cancellation Acknowledgment (30-day notice received)**
Acknowledge in writing within 24 hours. Confirm the last billing date, the last service delivery date, and the data return date. No retention pressure in this communication.

**Step 2 — Final Sprint Session (if applicable)**
If a sprint session is remaining in the final billing period, offer to conduct it as a "transition sprint" focused on documenting what has been built and handing over action plan items for the client to execute independently.

**Step 3 — Final Proof Pack (final billing period)**
Produce a final, comprehensive Proof Pack covering the full engagement period. Sections: cumulative data quality improvement, full account scoring history, ZATCA compliance summary, complete action plan log, capital assets deposited during the engagement. Delivered on the last day of service.

**Step 4 — Data Return**
Export and deliver all client data in CSV/JSON format. Confirm receipt in writing. Delete all copies from Dealix systems within 30 days of the last billing date, per the data retention policy. Log deletion in the engagement record.

**Step 5 — Engagement Close**
Mark the engagement as closed in the capital ledger. Log all capital assets deposited during the engagement for future anonymized reference. If the client consents, draft a case-safe summary for the Dealix proof library. No consent = no summary.

**Step 6 — Exit Note**
The founder sends a brief personal note thanking the client for the engagement, summarizing two or three specific accomplishments from the work, and stating that Dealix will be available if they choose to return. No sales language. No follow-up after this note unless the client re-initiates contact.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
