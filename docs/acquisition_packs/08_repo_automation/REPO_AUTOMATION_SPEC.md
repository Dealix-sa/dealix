# Repo Automation Spec — مواصفة أتمتة المستودع

<!-- Arabic primary | NO_LIVE_SEND | draft_only | SPECIFICATION (design doc, not code) -->

**عربي:** هذه **مواصفة تصميم** لربط حزم اكتساب العملاء بالمستودع — تصف المسارات والنقاط الطرفية والحقول المقترحة. ليست شيفرة ولا التزاماً نهائياً. كل إرسال خارجي يمرّ عبر `approval_center` بمبدأ **NO_LIVE_SEND**: لا يخرج أي شيء بدون موافقة بشرية مسجّلة.

**EN:** This is a **design specification** for wiring the Client Acquisition Packs into the repo — it describes proposed paths, endpoints, and fields. It is not code and not a final commitment. Every external send routes through `approval_center` under the **NO_LIVE_SEND** principle: nothing leaves without recorded human approval.

روابط / Links: [../04_marketer_enablement/MARKETER_FIELD_MANUAL.md](../04_marketer_enablement/MARKETER_FIELD_MANUAL.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md](../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md) · [../09_dashboards/](../09_dashboards/) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## المسارات المقترحة / Proposed File Paths

**عربي:** يعيش هذا الحزم تحت شجرة واحدة لتسهيل الفهرسة والمراجعة:

**EN:** The bundle lives under a single tree to ease indexing and review:

```
docs/acquisition_packs/
  01_client_understanding/CLIENT_UNDERSTANDING_PACK.md
  02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md
  03_offers/OFFER_PACKAGES.md
  04_marketer_enablement/MARKETER_FIELD_MANUAL.md
  05_outreach/OUTREACH_SCRIPTS.md
  07_operating_cadence/DAILY_OPERATING_CADENCE.md
  08_repo_automation/REPO_AUTOMATION_SPEC.md   (this file)
  09_dashboards/{company_scoring,pipeline,daily_numbers}_template.csv
  10_compliance/COMPLIANCE_PACK.md
```

---

## النقاط الطرفية المقترحة / Proposed API Endpoints

**عربي:** على مستوى التوقيع فقط — لا منطق تنفيذ. كل النقاط للقراءة/الكتابة الداخلية؛ لا توجد نقطة ترسل خارجياً مباشرة. الإرسال الخارجي حصراً عبر `approval_center`.

**EN:** Signature level only — no implementation logic. All endpoints are internal read/write; none sends externally. External sending is exclusively via `approval_center`.

```json
{
  "GET  /api/v1/acquisition/daily-numbers": {
    "query": { "date": "YYYY-MM-DD", "sector": "string?" },
    "returns": "daily_numbers row(s) — aggregated targets, not guarantees"
  },
  "POST /api/v1/acquisition/companies/score": {
    "body": { "company_name": "string", "source_type": "enum(public_registry|announcement|founder_signal)",
              "why_now_signal": "string", "fit_score": "0-10", "intent_score": "0-10",
              "consent_basis": "legitimate_interest_b2b" },
    "returns": { "total_score": "0-20", "status": "new|qualified|watch|disqualified",
                 "recommended_offer": "string" }
  },
  "GET  /api/v1/acquisition/pipeline": {
    "query": { "stage": "enum?", "owner": "string?" },
    "returns": "pipeline rows"
  },
  "POST /api/v1/acquisition/pipeline": {
    "body": "pipeline row (stage transition); approval_status defaults to approval_required",
    "returns": "persisted row — NO external send triggered"
  }
}
```

---

## آلة حالة الفرصة / Lead Status State Machine

**عربي:** المراحل والانتقالات المسموحة. كل انتقال يسجّل `stage_entered_date`. الانتقال إلى `contacted` لا يجوز إلا بعد `draft_approved` في `approval_center`.

**EN:** Stages and allowed transitions. Each transition records `stage_entered_date`. Moving to `contacted` is permitted only after `draft_approved` in `approval_center`.

```json
{
  "new":       ["qualified", "lost"],
  "qualified": ["contacted", "lost"],
  "contacted": ["replied", "lost"],
  "replied":   ["meeting", "lost"],
  "meeting":   ["proposal", "lost"],
  "proposal":  ["won", "lost"],
  "won":       [],
  "lost":      []
}
```

**عربي:** قواعد الانتقال: لا قفز فوق مرحلة؛ `lost` متاحة من أي مرحلة؛ متابعة واحدة فقط في `contacted` قبل التحول إلى `lost` عند عدم الرد؛ احترام «إيقاف» يحوّل الفرصة فوراً إلى `lost` مع `notes=opt_out`.

**EN:** Transition rules: no stage-skipping; `lost` is reachable from any stage; only one follow-up in `contacted` before moving to `lost` on no reply; honoring STOP moves the lead immediately to `lost` with `notes=opt_out`.

---

## حقول قاعدة البيانات / Database Fields

**عربي:** تنعكس مباشرة من أعمدة CSV في [../09_dashboards/](../09_dashboards/). لا حقول جديدة بدون مبرّر امتثال.

**EN:** Mapped directly from the CSV columns in [../09_dashboards/](../09_dashboards/). No new field without a compliance justification.

| الجدول / Table | الحقول / Fields |
|---|---|
| `companies` | company_name, sector, region, size_band, source_type, why_now_signal, pain_hypothesis, fit_score, intent_score, total_score, recommended_offer, gap_identified, consent_basis, owner, status, next_action, next_action_date, notes |
| `pipeline` | company_name, contact_role, offer, stage, stage_entered_date, last_touch_date, next_action, next_action_date, value_estimate_sar, probability, approval_status, proof_pack_ref, consent_basis, notes |
| `daily_numbers` | date, sector, companies_analyzed, companies_qualified, drafts_prepared, messages_sent_approved, replies, meetings_booked, proposals_sent, closes, founder_minutes, notes |

**عربي:** قيود: `total_score = fit_score + intent_score`؛ `value_estimate_sar` تقديري دائماً؛ `consent_basis` إلزامي؛ لا حقول هوية وطنية أو بيانات حساسة.

**EN:** Constraints: `total_score = fit_score + intent_score`; `value_estimate_sar` always estimated; `consent_basis` mandatory; no national-ID or sensitive-data fields.

---

## إجراء GitHub اليومي المقترح / Proposed Daily GitHub Action

**عربي:** مهمّة مجدولة تُصدِر **ملخصاً يومياً (markdown)** فقط — لا إرسال خارجي إطلاقاً.

**EN:** A scheduled job that emits **a daily brief (markdown)** only — no external send whatsoever.

```json
{
  "name": "acquisition-daily-brief",
  "schedule": "cron: 0 5 * * 0-4   (05:00 KSA, Sun-Thu)",
  "steps": ["read 09_dashboards CSVs", "compute daily roll-up",
            "emit docs/acquisition_packs/_briefs/brief_YYYY-MM-DD.md"],
  "guardrail": "NO external messaging; outputs markdown only; no STOP/opt-out contacts re-listed"
}
```

---

## أوامر Makefile / Makefile-style Commands

**عربي:** أوامر محلية للتشغيل والمراجعة. أيٌّ منها لا يرسل خارجياً.

**EN:** Local commands for running and review. None of them sends externally.

```
make acquisition-daily      # build today's brief markdown from the CSVs
make acquisition-score      # validate scoring rows and thresholds
make acquisition-pipeline   # print pipeline by stage
make acquisition-compliance # check consent_basis present + opt-out log intact
```

**عربي:** بوابة الإرسال: أي رسالة معتمدة تنتقل إلى `approval_center` كمسوّدة بحالة `approval_required`، ويرسلها إنسان يدوياً بعد الموافقة. لا تجاوز لهذه البوابة في أي أمر أو نقطة طرفية أو إجراء.

**EN:** Send gate: any approved message moves into `approval_center` as a draft with status `approval_required`, sent manually by a human after approval. No command, endpoint, or action bypasses this gate.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
