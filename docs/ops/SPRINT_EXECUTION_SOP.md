# Sprint Execution SOP — Dealix 7-Day Revenue Intelligence Sprint — إجراءات التشغيل الموحَّدة: سبرنت ذكاء الإيرادات من Dealix في 7 أيام

> Cross-references: [docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) · [docs/04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md) · [docs/07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) · [docs/05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) · [docs/00_foundation/NON_NEGOTIABLES.md](../00_foundation/NON_NEGOTIABLES.md) · [docs/ops/CUSTOMER_SUCCESS_PLAYBOOK.md](./CUSTOMER_SUCCESS_PLAYBOOK.md)

**Purpose:** This SOP governs every Revenue Intelligence Sprint delivered by Dealix. It is the operational ground truth for Day 1 through Day 7. The [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) provides the strategic rationale; this document provides the daily execution detail.

**الغرض:** تحكم هذه الإجراءات كل سبرنت لذكاء الإيرادات تُقدِّمه Dealix. هي المرجع التشغيلي من اليوم الأول إلى اليوم السابع.

---

## Pre-Sprint Gate — بوابة ما قبل السبرنت

Before Day 1 begins, all of the following must be confirmed.

**Checklist — قائمة الفحص:**
- [ ] Proposal accepted and payment received (499 SAR via Moyasar, VAT invoice issued)
- [ ] Kickoff call scheduled (45–60 minutes, Day 1)
- [ ] Client has identified their named workflow owner (name + title confirmed in writing)
- [ ] Client has confirmed at least one data source they control and will upload
- [ ] Engagement ID generated: `ENG-[YYYY]-[NNN]`
- [ ] Folder created: `engagements/ENG-[YYYY]-[NNN]/`
- [ ] Client room access provisioned in dashboard

**Escalation trigger:** if any pre-sprint gate item cannot be confirmed within 48 hours of payment, pause the sprint and notify the client. Do not begin Day 1 activities on incomplete intake.

---

## Day 1 — Source Passport + Kickoff — اليوم الأول: جواز المصدر والانطلاق

**Time allocation: 2 hours**
**Founder tasks: 1.5 hours active | 30 min documentation**

### Objectives
Establish the data governance contract (Source Passport), define the sprint's single primary workflow, and align on Day 7 deliverables.

### Activities — الأنشطة

**Kickoff Call (45–60 minutes):**
- Confirm the named workflow owner on the client side — this person is the sole point of contact for data decisions. Non-negotiable: if no named owner can be confirmed, halt the sprint.
- Define one primary workflow for the sprint. Examples: dormant account revival, pipeline scoring, invoice data quality, ZATCA pre-audit. One workflow only — scope creep is the most common cause of low proof scores.
- Walk the client through the Source Passport requirements: what data they will upload, in what format, by when (Day 2 morning is the deadline).
- Confirm the Day 7 handoff call time.

**Source Passport Draft:**
After the call, draft the Source Passport with the following fields. The client must review and sign (digitally) before data is uploaded.

```json
{
  "engagement_id": "ENG-YYYY-NNN",
  "client_label": "[anonymized internal label — not client's real name in system]",
  "source_type": "client_upload | crm_export | manual_entry",
  "declared_owner": "[client workflow owner name + title]",
  "allowed_use": "[specific to this sprint workflow only]",
  "pii_flag": true | false,
  "sensitivity": "internal | confidential | restricted",
  "retention_days": 90,
  "signed_by_client": false,
  "signed_date": null
}
```

Note: `source_type` must be one of `client_upload`, `crm_export`, or `manual_entry`. Value `scraped` is not permitted under any circumstances.

**Kickoff Call Agenda Template:**
1. Introductions and engagement overview (5 min)
2. Confirm workflow owner (5 min)
3. Define primary workflow focus (15 min)
4. Source Passport walkthrough — data requirements, format, upload deadline (15 min)
5. Day 7 deliverables preview — what the Proof Pack contains (10 min)
6. Open questions (10 min)

### Outputs — المخرجات
- Signed Source Passport (or unsigned draft pending client signature by EOD)
- Kickoff notes committed to `engagements/ENG-[YYYY]-[NNN]/kickoff_notes.md`
- Workflow definition documented: one sentence, one workflow

### Quality Gate — بوابة الجودة
- Source Passport signed before any data is uploaded
- Workflow is singular and specific (not "improve our sales" — must be "score dormant accounts by ZATCA revenue signal")

### Checklist — قائمة الفحص
- [ ] Kickoff call completed
- [ ] Named workflow owner confirmed in writing
- [ ] Primary workflow defined in one sentence
- [ ] Source Passport draft sent to client for signature
- [ ] Source Passport signed by client (before Day 2 data upload)
- [ ] Day 7 handoff call scheduled
- [ ] Engagement record status updated to `day_1_complete`

---

## Day 2 — Data Upload + DQ Scoring — اليوم الثاني: رفع البيانات وفحص الجودة

**Time allocation: 1 hour**
**Founder tasks: 30 min active | 30 min review**

### Objectives
Receive client data upload, run a non-destructive preview, compute the Data Quality (DQ) score, and make the go/pause/reroute decision.

### Activities — الأنشطة

**Data Receipt:**
Confirm that the client has uploaded data via the agreed channel (secure upload link — not email attachment, not WhatsApp). If data arrives by 10:00 AM, Day 2 activities proceed. If delayed past 2:00 PM, notify the client that Day 3 will slip by 24 hours.

**Preview Run (Non-Destructive):**
Run a sample preview of the first 100 rows without writing to any persistent store. Purpose: confirm file format, column structure, and PII presence.

```bash
python -m cli data import \
  --passport <passport_id> \
  --file client_upload.csv \
  --preview-only
```

**DQ Score Computation:**
Run the full data quality score across six standard dimensions:

| Dimension | Description |
|---|---|
| Completeness | Required fields populated |
| Validity | Field values match declared format/type |
| Uniqueness | Duplicate record count |
| Consistency | Cross-field logical consistency |
| Timeliness | Data age relative to sprint workflow |
| Conformance | Alignment with ZATCA invoice field requirements |

```bash
python -m cli data compute-dq \
  --passport <passport_id> \
  --out engagements/ENG-[YYYY]-[NNN]/dq_score.json
```

### Founder Decision — قرار المؤسس

| DQ Score | Decision | Action |
|---|---|---|
| < 40 | Pause sprint | Notify client; propose 1,500 SAR Data Pack instead; refund 80% of sprint fee per refund policy |
| 40–69 | Proceed with caveats | Document caveats explicitly in Proof Pack; note which findings are limited by data quality |
| ≥ 70 | Proceed clean | Normal sprint execution |

### Outputs — المخرجات
- `dq_score.json` in engagement folder
- DQ baseline logged in proof ledger: `proof_ledger.dq_baseline = <score>`
- Client receives a brief Day 2 status note: DQ score (as a range band, not exact number if below 70), whether the sprint proceeds, and any caveats

### Quality Gate — بوابة الجودة
- No data is processed past preview if DQ < 40
- Caveats are documented before Day 3 begins, not after Day 5

### Checklist — قائمة الفحص
- [ ] Data received via secure channel (not email/WhatsApp)
- [ ] Preview run completed — no errors
- [ ] DQ score computed and stored
- [ ] Founder decision made: proceed / proceed-with-caveats / pause
- [ ] Client notified of DQ result and sprint status
- [ ] Engagement record status updated to `day_2_complete`

---

## Day 3 — Revenue Analysis + ZATCA Check — اليوم الثالث: تحليل الإيرادات وفحص الامتثال

**Time allocation: 2 hours**
**Founder tasks: 1.5 hours active | 30 min review**

### Objectives
Run account scoring against the defined workflow, identify revenue leakage patterns, and produce the ZATCA compliance check output.

### Activities — الأنشطة

**Account Scoring:**
Run the rubric-based account scoring against the full, DQ-checked, deduplicated dataset. The scoring rubric must be explicit — every ranked account has a human-readable justification in Arabic and English. Opaque or unexplainable rankings are demoted.

Scoring dimensions (weighted by workflow context):
- ICP fit score (firmographic match to defined ICP)
- Revenue signal strength (invoice history, payment pattern, engagement frequency)
- ZATCA compliance risk flag (invoice completeness, phase readiness)
- Recency signal (last activity date relative to sprint date)
- Governance risk flag (any field that triggers a PDPL sensitivity flag)

**Revenue Leakage Identification:**
Identify accounts where revenue opportunity is measurable but unrealized:
- Dormant accounts (no activity in past 60–90 days, based on data)
- Incomplete invoice sequences (gaps in ZATCA-required fields)
- Accounts with high ICP fit but no recent pipeline activity
- Accounts with payment delays exceeding standard terms

Document leakage as estimated value ranges, not precise figures. Label all estimates clearly.

**ZATCA Compliance Check:**
Review invoice data against the Phase 2 (and Phase 3 where applicable) ZATCA field requirements:
- Buyer/seller CR numbers present
- VAT registration numbers present and formatted correctly
- Invoice sequence integrity
- Required line-item fields populated
- XML/UBL schema conformance (if electronic invoice data provided)

Output: a compliance status table with pass/fail per field category, and a prioritized remediation list.

### Outputs — المخرجات
- Account scoring output: top 10–20 accounts with Arabic + English justifications
- Revenue leakage summary: estimated value by category, labeled as estimates
- ZATCA compliance table: field-by-field status + remediation priority list

### Quality Gate — بوابة الجودة
- Every top-10 account has a written Arabic justification — no silent scores
- Revenue leakage estimates include explicit confidence levels (high / medium / low)
- ZATCA findings distinguish between Phase 2 required and Phase 3 preparatory items

### Checklist — قائمة الفحص
- [ ] Account scoring run completed
- [ ] All top-10 accounts have Arabic + English justifications
- [ ] Any opaque rankings demoted and reason logged
- [ ] Revenue leakage identified and quantified as estimates
- [ ] ZATCA compliance check completed
- [ ] Day 3 findings committed to engagement folder
- [ ] Engagement record status updated to `day_3_complete`

---

## Day 4 — Draft Pack Assembly + Bilingual Writeup — اليوم الرابع: تجميع حزمة المسودة والكتابة ثنائية اللغة

**Time allocation: 3 hours**
**Founder tasks: 2.5 hours active | 30 min review**

### Objectives
Produce the bilingual findings document and draft outreach recommendations for governance review on Day 5. Assemble the draft Proof Pack structure.

### Activities — الأنشطة

**Bilingual Findings Writeup:**
Write the core findings document in Arabic (primary) and English (secondary). Structure:

1. Executive Summary / الملخص التنفيذي (200 words AR + 200 words EN)
2. Data Quality Assessment / تقييم جودة البيانات (DQ score, key gaps, improvement roadmap)
3. Account Priority List / قائمة الحسابات ذات الأولوية (top 10 with justifications, bilingual)
4. Revenue Leakage Map / خريطة تسرب الإيرادات (by category, estimated values labeled)
5. ZATCA Compliance Status / حالة الامتثال لهيئة الزكاة (field table, remediation priorities)
6. Recommended Actions / الإجراءات الموصى بها (maximum 10 actions, ranked by priority)

**Outreach Draft Preparation:**
For each top-priority account identified, prepare a bilingual outreach draft (AR primary, EN secondary). These drafts are:
- Labeled `DRAFT_ONLY` — they are not sent by Dealix under any circumstances
- Formatted for the client's review and approval before any send
- Checked by the governance OS before proceeding to Day 5

Apply the governance decision matrix to each draft:

| Decision | Meaning |
|---|---|
| ALLOW | Draft is ready for client review and potential send |
| DRAFT_ONLY | Draft needs revision before client review |
| REQUIRE_APPROVAL | Must receive explicit founder sign-off before client presentation |
| REDACT | Contains sensitive content that must be removed |
| BLOCK | Draft violates governance policy — do not present |
| RATE_LIMIT | Only a limited number of these should be presented |
| REROUTE | Redirect to a different communication channel or format |

**Draft Pack Structure Assembly:**
Create the skeleton of the 14-section Proof Pack with all sections present (placeholder content acceptable for sections completed in Days 5–7).

### Outputs — المخرجات
- Bilingual findings document (6 sections, AR + EN)
- Outreach drafts with governance labels (in engagement folder, not sent externally)
- 14-section Proof Pack skeleton committed to engagement folder

### Quality Gate — بوابة الجودة
- No outreach draft is marked ALLOW without governance review on Day 5
- Arabic and English findings are parallel in structure and equivalent in content — not summaries of each other
- Every estimated value figure is labeled as estimated

### Checklist — قائمة الفحص
- [ ] Bilingual findings document completed (all 6 sections)
- [ ] Outreach drafts produced with governance labels
- [ ] More than 50% of drafts not BLOCKED (if so: escalation trigger activated)
- [ ] 14-section Proof Pack skeleton created
- [ ] All Day 4 outputs committed to engagement folder
- [ ] Engagement record status updated to `day_4_complete`

---

## Day 5 — Governance Review + Founder Approval — اليوم الخامس: مراجعة الحوكمة وموافقة المؤسس

**Time allocation: 1 hour**
**Founder tasks: 1 hour focused review**

### Objectives
Founder reviews every outreach draft and every BLOCK/REDACT governance decision. Confirms that no external action has occurred. Approves the draft pack for client presentation.

### Activities — الأنشطة

**Governance Audit:**
Review the governance decision log for all outreach drafts produced on Day 4:
- Confirm every BLOCK has a documented reason
- Confirm every REDACT has a documented reason and the redaction has been applied
- Confirm every ALLOW draft has no guaranteed-outcome language, no PII, and no prohibited content

**Outreach Draft Final Review:**
Read every draft that is labeled ALLOW or REQUIRE_APPROVAL. Confirm:
- Draft is written in first person from the client's voice, not Dealix's voice
- Draft does not imply Dealix is the sender
- Draft has no guaranteed sales language ("this will result in X sales")
- Draft is appropriate for Saudi B2B professional context
- Arabic is primary, English is secondary

**Approval Log Entry:**
For each draft approved: log `approved_by: founder`, `approved_date`, `draft_id`. This log is part of the Proof Pack and is the audit evidence that APPROVAL_FIRST was observed.

**Critical escalation check:**
If more than 50% of the generated drafts are BLOCKED, this signals that the workflow defined on Day 1 may be misaligned with what the client's data can support. Escalate: pause the draft delivery, schedule a call with the client to re-scope, extend the sprint by up to 48 hours without additional charge.

### Outputs — المخرجات
- Governance decision log: final, with all decisions documented
- Approval log: all approved drafts recorded with date and approver
- Any escalation actions taken and logged

### Quality Gate — بوابة الجودة
- Zero external actions have occurred between Day 1 and Day 5
- Every BLOCK has a written reason
- Every approved draft has been read by the founder — no batch approval

### Checklist — قائمة الفحص
- [ ] All governance decisions reviewed
- [ ] All BLOCKed drafts have documented reasons
- [ ] All approved drafts have founder approval log entries
- [ ] Zero external actions confirmed (ledger check)
- [ ] Escalation trigger checked: < 50% block rate confirmed
- [ ] Engagement record status updated to `day_5_complete`

---

## Day 6 — Proof Pack Build — اليوم السادس: بناء حزمة الإثبات

**Time allocation: 2 hours**
**Founder tasks: 1.5 hours build | 30 min quality check**

### Objectives
Complete all 14 sections of the Proof Pack. Compute the proof score. Confirm the pack is deliverable (score ≥ 70).

### Proof Pack — Four Core Sections

The Proof Pack has 14 sections total (per [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)). The four sections most critical to client value are:

**Section A — Data Audit / تدقيق البيانات**
- Source Passport (signed copy)
- DQ baseline score and breakdown by dimension
- Deduplication results: records before and after
- PII flags identified and redaction actions taken
- Data caveats affecting scoring reliability

**Section B — Revenue Map / خريطة الإيرادات**
- Account scoring output: top 10–20 with bilingual justifications
- Revenue leakage map by category with estimated values (labeled as estimates)
- Dormant account list with last-activity dates
- ZATCA compliance table: field-by-field status

**Section C — Action Plan / خطة العمل**
- Top 10 prioritized actions (ranked by estimated impact and execution feasibility)
- For each action: owner (client or Dealix), timeline (immediate / 30 days / 90 days), dependency
- Outreach drafts: all ALLOW-approved drafts, labeled as drafts for client approval before send
- Compliance remediation roadmap: ZATCA fields requiring attention by phase

**Section D — ROI Projection / توقع العائد على الاستثمار**
- Estimated value calculation methodology (transparent, not a black box)
- Three scenarios: conservative / base / optimistic
- Key assumptions stated explicitly
- Labeled clearly: "These are estimated projections based on the data and methodology described above. They are not guaranteed outcomes."
- Arabic equivalent of the above label present on the same page

**Remaining 10 Proof Pack Sections (see [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)):**
- Intake summary, engagement metadata, governance decision log, redaction log, approval log, value-tier mapping, capital asset registration, limitations statement, methodology summary, signature page.

**Proof Score Computation:**
Compute the proof score using the 8-dimension QA rubric from [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md):

| Dimension | Weight |
|---|---|
| Source integrity | 15% |
| DQ transparency | 15% |
| Scoring explainability | 15% |
| Bilingual parity | 10% |
| Governance auditability | 15% |
| Approval discipline | 15% |
| Proof completeness | 10% |
| Capital deposit | 5% |

Minimum deliverable score: 70. Below 70 = do not deliver; extend or refund.

### Outputs — المخرجات
- Complete 14-section Proof Pack (PDF + source files in engagement folder)
- Proof score computed and logged: `proof_ledger.proof_score = <score>`
- Capital asset candidate identified and flagged for Day 7 registration

### Quality Gate — بوابة الجودة
- All 14 sections present with no placeholder text remaining
- Proof score ≥ 70 before Day 7 handoff proceeds
- ROI projection page carries the disclaimer in both AR and EN
- Every estimated value is labeled as estimated

### Checklist — قائمة الفحص
- [ ] All 14 Proof Pack sections completed
- [ ] No placeholder text remaining in any section
- [ ] Proof score computed: record value ___
- [ ] Proof score ≥ 70 (if below: escalation — do not proceed to Day 7)
- [ ] ROI disclaimer present in Arabic and English
- [ ] Capital asset candidate identified
- [ ] Engagement record status updated to `day_6_complete`

---

## Day 7 — Handoff + Capital Registration + Retainer Pitch — اليوم السابع: التسليم وتسجيل الأصل وعرض الاحتفاظ

**Time allocation: 1 hour**
**Founder tasks: 45 min handoff call | 15 min post-call documentation**

### Objectives
Deliver the Proof Pack to the client in a structured handoff call. Register the capital asset. Make a data-backed retainer pitch if eligibility criteria are met. Mark engagement as delivered.

### Handoff Call (60 minutes)

**Agenda:**
1. Proof Pack overview — structure and how to read it (10 min)
2. Section A walkthrough: Data Audit — DQ score, key data gaps (10 min)
3. Section B walkthrough: Revenue Map — top accounts, leakage categories (15 min)
4. Section C walkthrough: Action Plan — top 5 actions, outreach drafts (10 min)
5. Section D walkthrough: ROI Projection — methodology, scenarios, assumptions (5 min)
6. Next steps: retainer proposal or second sprint (10 min)

**Retainer Eligibility Assessment (before the call):**
The retainer pitch is made only when all of the following criteria are met:
- `proof_score >= 80`
- `adoption_score >= 70` (based on client engagement during the sprint)
- Named workflow owner confirmed as continuing post-sprint
- Source Passport renewable for ongoing use
- At least one capital asset deposited

If criteria are not met, offer either a second sprint or a graceful close-out. Do not pitch the retainer as a default close — it must be earned by the data.

**Retainer Pitch (if criteria met):**
Present the Managed Ops offer using the three-tier pricing from [docs/sales/PROPOSAL_TEMPLATE_AR_EN.md](../sales/PROPOSAL_TEMPLATE_AR_EN.md). Lead with the evidence: "Your proof score is X, your data quality improved from Y to Z, and these three action plan items will require ongoing monitoring. Here is what Managed Ops delivers monthly."

### Capital Asset Registration

Register at least one reusable asset from this sprint in the capital ledger:

```json
{
  "asset_id": "ASSET-[YYYY]-[NNN]",
  "asset_type": "scoring_rule | draft_template | governance_rule | sector_insight | proof_example",
  "description": "[one sentence description of the reusable asset]",
  "source_engagement": "ENG-[YYYY]-[NNN]",
  "sector": "[anonymized sector label]",
  "reuse_case": "[how this asset will benefit future engagements]",
  "pii_free": true
}
```

The asset must be genuinely reusable — a specific scoring weight for a Saudi B2B sector, a ZATCA field mapping pattern, a governance rule for a particular data type. Not a one-off transformation that applies only to this client's data.

### Post-Call Documentation

- Mark engagement `status = delivered` in the engagement registry
- Log `proof_ledger.handoff_completed = true`
- Confirm `capital_ledger.asset_id` registered
- Draft case-safe summary in `docs/case-studies/` (publish optional, requires no identifying details)
- Send client a post-call confirmation note: Proof Pack location, action plan owner assignments, next step agreed (retainer / second sprint / close)

### Outputs — المخرجات
- Proof Pack delivered and acknowledged by client
- Capital asset registered in capital ledger
- Case-safe summary draft committed
- Engagement status: `delivered`
- Next step documented and confirmed with client

### Quality Gate — بوابة الجودة
- Handoff call conducted (not a link drop — a structured conversation)
- Capital asset registered with a genuine reuse case
- Case-safe summary contains no PII and no identifying data combinations

### Checklist — قائمة الفحص
- [ ] Handoff call completed (60 minutes)
- [ ] Client confirmed receipt of Proof Pack
- [ ] Retainer pitch made (if eligible) — outcome logged
- [ ] Capital asset registered in ledger
- [ ] Case-safe summary drafted
- [ ] Engagement status marked `delivered`
- [ ] Post-call confirmation note sent to client
- [ ] Final engagement record committed to repo

---

## Escalation Reference Summary — مرجع التصعيد

| Trigger | Day | Response |
|---|---|---|
| Workflow owner unconfirmed | Pre-sprint | Pause sprint, do not begin Day 1 |
| DQ score < 40 | Day 2 | Pause, propose Data Pack, refund 80% of sprint fee |
| DQ score 40–69 | Day 2 | Proceed with documented caveats |
| Source Passport unsigned | Day 2 | Do not upload or process data |
| > 50% drafts BLOCKED | Day 5 | Pause, re-scope workflow with client, extend 48 hours |
| Client requests cold outreach / scraping / guaranteed outcomes | Any day | Refuse, log refusal, end engagement cleanly, refund unearned portion |
| Proof score < 70 | Day 6 | Do not deliver; extend or refund per refund policy |
| Founder bandwidth unavailable | Day 5 | Extend by 48 hours; cost absorbed by Dealix |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
