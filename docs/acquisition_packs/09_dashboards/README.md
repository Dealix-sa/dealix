# Dashboards — لوحات الأرقام

ثلاثة قوالب CSV تشكّل سجل أرقام حزم اكتساب العملاء. هذا الملف يشرح كل قالب، وكل عمود فيه باختصار، وكيف تتصل القوالب ببعضها. لا تُخزَّن أي بيانات شخصية تتجاوز جهة اتصال الأعمال، وعمود `consent_basis` موجود في القالبين ذوي الصلة لتتبّع الامتثال (PDPL).

روابط: [../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md](../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md) · [../07_operating_cadence/DAILY_OPERATING_CADENCE.md](../07_operating_cadence/DAILY_OPERATING_CADENCE.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

## التدفّق

تقييم ← (مؤهَّل) ← خط الأنابيب ← تجميع الأرقام اليومية. كل شركة تبدأ صفاً في ملف التقييم؛ ومتى أصبحت `qualified` تنتقل إلى خط الأنابيب كفرصة نشطة؛ وتُجمَّع نشاطات اليوم كله في صف واحد بملف الأرقام اليومية. المصادر يدوية وعامة فقط — لا كشط ولا قوائم مشتراة.

### company_scoring_template.csv

صف واحد لكل شركة — مدخل القمع. الأعمدة: `company_name, sector, region, size_band, source_type, why_now_signal, pain_hypothesis, fit_score, intent_score, total_score, recommended_offer, gap_identified, consent_basis, owner, status, next_action, next_action_date, notes`.
`company_name` نائب مثل «Example Trading Co». `sector/region/size_band` تصنيف الشركة. `source_type` المصدر العام المسموح (لا كشط/لا شراء). `why_now_signal` الحدث العام الحديث. `pain_hypothesis` فرضية الألم تُختبَر لا تُؤكَّد. `fit_score`+`intent_score`=`total_score`. `recommended_offer` العرض المناسب. `gap_identified` فجوة الإيراد. `consent_basis`=`legitimate_interest_b2b`. `owner` المسؤول. `status`: `new → qualified → contacted → replied → meeting → proposal → won/lost`. `next_action`/`next_action_date` الخطوة التالية. `notes` التعليل.

### pipeline_template.csv

صف واحد لكل فرصة نشطة. الأعمدة: `company_name, contact_role, offer, stage, stage_entered_date, last_touch_date, next_action, next_action_date, value_estimate_sar, probability, approval_status, proof_pack_ref, consent_basis, notes`.
`contact_role` دور وظيفي لا اسم شخص. `offer` العرض المعتمَد. `stage`/`stage_entered_date` المرحلة وتاريخ دخولها. `last_touch_date` آخر تواصل. `value_estimate_sar` قيمة تقديرية لا متحقَّقة. `probability` احتمال تقديري. `approval_status` يؤكد أن أي إرسال تم بعد موافقة بشرية. `proof_pack_ref` مرجع حزمة الإثبات. `consent_basis`=`legitimate_interest_b2b`.

### daily_numbers_template.csv

صف واحد لكل يوم — التجميع. الأعمدة: `date, sector, companies_analyzed, companies_qualified, drafts_prepared, messages_sent_approved, replies, meetings_booked, proposals_sent, closes, founder_minutes, notes`. أرقام أهداف لا ضمانات. `messages_sent_approved` ما أُرسِل يدوياً بعد موافقة فقط. `founder_minutes` لقياس الكفاءة.

---

# Dashboards

Three CSV templates form the numbers ledger for the Client Acquisition Packs. This file explains each template, each of its columns briefly, and how the templates connect. No personal data beyond a business contact is stored, and the `consent_basis` column exists in the two relevant templates for PDPL traceability.

Links: [../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md](../02_daily_engine/DAILY_COMPANY_NUMBERS_ENGINE.md) · [../07_operating_cadence/DAILY_OPERATING_CADENCE.md](../07_operating_cadence/DAILY_OPERATING_CADENCE.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

## The flow

Scoring → (qualified) → pipeline → daily numbers roll-up. Each company starts as a row in the scoring file; once it becomes `qualified` it moves to the pipeline as an active opportunity; the whole day's activity is aggregated into one row in the daily numbers file. Sources are manual and public only — no scraping, no purchased lists.

### company_scoring_template.csv

One row per company — the funnel input. Columns: `company_name, sector, region, size_band, source_type, why_now_signal, pain_hypothesis, fit_score, intent_score, total_score, recommended_offer, gap_identified, consent_basis, owner, status, next_action, next_action_date, notes`.
`company_name` a placeholder like "Example Trading Co". `sector/region/size_band` classify the company. `source_type` the allowed public source (no scraping / no purchase). `why_now_signal` the recent public event. `pain_hypothesis` a hypothesis to be tested, not asserted. `fit_score`+`intent_score`=`total_score`. `recommended_offer` the fitting offer. `gap_identified` the revenue gap. `consent_basis`=`legitimate_interest_b2b`. `owner` the responsible person. `status`: `new → qualified → contacted → replied → meeting → proposal → won/lost`. `next_action`/`next_action_date` the next step. `notes` the rationale.

### pipeline_template.csv

One row per active opportunity. Columns: `company_name, contact_role, offer, stage, stage_entered_date, last_touch_date, next_action, next_action_date, value_estimate_sar, probability, approval_status, proof_pack_ref, consent_basis, notes`.
`contact_role` a job role, not a person's name. `offer` the approved offer. `stage`/`stage_entered_date` the stage and entry date. `last_touch_date` the last contact. `value_estimate_sar` an estimated, not verified, value. `probability` an estimated likelihood. `approval_status` confirms any send happened after human approval. `proof_pack_ref` a reference to the proof pack. `consent_basis`=`legitimate_interest_b2b`.

### daily_numbers_template.csv

One row per day — the roll-up. Columns: `date, sector, companies_analyzed, companies_qualified, drafts_prepared, messages_sent_approved, replies, meetings_booked, proposals_sent, closes, founder_minutes, notes`. Target numbers, not guarantees. `messages_sent_approved` is only what was sent manually after approval. `founder_minutes` measures efficiency.

Examples use placeholders only (e.g. "Example Trading Co"), business contact with `consent_basis = legitimate_interest_b2b`.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
