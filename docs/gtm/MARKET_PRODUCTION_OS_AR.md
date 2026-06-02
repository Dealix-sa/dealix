# نظام إنتاج السوق — Dealix Market Production OS — Master Index

نظام إنتاج السوق هو ماكينة الذهاب إلى السوق (GTM) في Dealix للشركات السعودية B2B.
ليس «مسارًا واحدًا»، بل منظومة متعددة القنوات: تنتج بكثافة، تُراجع بصرامة، تُرسل
بحذر تدريجي، تتعلّم، وتتوسّع — دون أن تحرق سمعة الدومين أو الهوية أو الثقة.

> القاعدة الأساسية: **ارفع الإنتاج إلى 250 مسودة/يوم، لكن لا ترفع الإرسال إلى 250/يوم
> إلا بعد تجهيز الدومين (SPF/DKIM/DMARC)، وإلغاء الاشتراك بنقرة واحدة، وقائمة الكبت
> (suppression)، ومنحنى الإحماء، ومراقبة الردود والـ spam.** كل إرسال خارجي يتطلب
> موافقة المؤسس.

هذا الملف هو الفهرس الرئيسي. كل منظومة لها وثائقها وبياناتها ومخططاتها وتقاريرها.

---

## القاعدة الأساسية — 250 مسودة مقابل 250 إرسال

| البند | مسموح اليوم | غير مسموح حتى تكتمل الشروط |
|---|---|---|
| الإنتاج (drafts) | 250 مسودة/يوم | — |
| الإرسال (sends) | 0–20/يوم في الأسبوع 0 | 250/يوم قبل اكتمال الإحماء والصحة |

الشروط قبل رفع الإرسال (مرجع: [SENDING_RAMP_PLAN_AR](../outreach/SENDING_RAMP_PLAN_AR.md)):
- SPF + DKIM + DMARC مهيأة، ودومين تتبع مخصص، وreply-to صحيح، وعنوان بريدي صالح.
- رابط إلغاء اشتراك بنقرة واحدة (List-Unsubscribe) في كل رسالة تسويقية.
- قائمة كبت فعّالة، ومعالجة ارتداد، ومراقبة معدل الشكاوى.
- مؤشرات صحية ضمن الحدود: ارتداد < 3%، شكاوى spam < 0.3% (يفضّل < 0.1%).

> هذه ملخصات تشغيلية لإرشادات Gmail للمرسلين وقانون CAN-SPAM وحساسية PDPL — وليست
> استشارة قانونية. راجع [COLD_EMAIL_COMPLIANCE_AR](../outreach/COLD_EMAIL_COMPLIANCE_AR.md).

---

## خريطة النظام — System Map

```txt
Brand OS
→ Product Catalog OS
→ Sector Intelligence OS
→ Prospect Research OS
→ Job Signal OS
→ Cold Email Draft Factory
→ Compliance + Deliverability Gate
→ Founder Approval Queue
→ Sending Ramp OS
→ Reply Handling OS
→ WhatsApp Post-Reply OS
→ Proposal + Proof Pack OS
→ Content OS
→ Press OS
→ Partnership OS
→ Founder GTM Control Room
```

---

## المنظومات — Subsystems

### 1. Brand OS — الهوية والتواصل
نظام الهوية البصرية واللفظية وسياسة الادعاءات والمحتوى والإخراج.
- [BRAND_IDENTITY_SYSTEM_AR](../brand/BRAND_IDENTITY_SYSTEM_AR.md)
- [BRAND_MESSAGING_HOUSE_AR](../brand/BRAND_MESSAGING_HOUSE_AR.md)
- [BRAND_VISUAL_DIRECTION_AR](../brand/BRAND_VISUAL_DIRECTION_AR.md)
- [BRAND_VOICE_AR](../brand/BRAND_VOICE_AR.md)
- [BRAND_CLAIMS_POLICY_AR](../brand/BRAND_CLAIMS_POLICY_AR.md)
- [BRAND_CONTENT_RULES_AR](../brand/BRAND_CONTENT_RULES_AR.md)
- [BRAND_OUTBOUND_SYSTEM_AR](../brand/BRAND_OUTBOUND_SYSTEM_AR.md)
- [BRAND_ASSET_CHECKLIST_AR](../brand/BRAND_ASSET_CHECKLIST_AR.md)
- مرجع موجود: [DEALIX_VISUAL_IDENTITY_AR](../brand/DEALIX_VISUAL_IDENTITY_AR.md)

### 2. Product Catalog OS — كتالوج المنتجات
لا يخترع الوكيل عروضًا؛ كل عرض من الكتالوج وله دليل.
- [PRODUCT_CATALOG_AR](../commercial/PRODUCT_CATALOG_AR.md)
- [OFFER_LADDER_AR](../commercial/OFFER_LADDER_AR.md)
- [PRICING_GUARDRAILS_AR](../commercial/PRICING_GUARDRAILS_AR.md)
- [ICP_MATRIX_AR](../commercial/ICP_MATRIX_AR.md)
- [BUYER_PERSONAS_AR](../commercial/BUYER_PERSONAS_AR.md)
- [OBJECTION_BANK_AR](../commercial/OBJECTION_BANK_AR.md)
- [PROOF_LIBRARY_AR](../commercial/PROOF_LIBRARY_AR.md)

### 3. Sector Intelligence OS — ذكاء القطاعات
عشرة قطاعات سعودية بترتيب الأولوية. الفهرس: [data/sectors/sectors.yaml](../../data/sectors/sectors.yaml).
1. [وكالات التسويق](../sectors/MARKETING_AGENCIES_AR.md)
2. [شركات التدريب](../sectors/TRAINING_COMPANIES_AR.md)
3. [العيادات](../sectors/CLINICS_AR.md)
4. [فرق العقار](../sectors/REAL_ESTATE_TEAMS_AR.md)
5. [وكالات التوظيف](../sectors/RECRUITMENT_AGENCIES_AR.md)
6. [الخدمات المهنية](../sectors/PROFESSIONAL_SERVICES_AR.md)
7. [مزوّدو التعليم](../sectors/EDUCATION_PROVIDERS_AR.md)
8. [مجموعات المطاعم](../sectors/RESTAURANT_GROUPS_AR.md)
9. [شركات اللوجستيك](../sectors/LOGISTICS_COMPANIES_AR.md)
10. [SaaS/الخدمات المحلية](../sectors/LOCAL_SAAS_AR.md)
- التقرير: [reports/sectors/SECTOR_PRIORITY_REPORT](../../reports/sectors/SECTOR_PRIORITY_REPORT.md)

### 4. Prospect Research OS — بحث العملاء المحتملين
بدون scraping؛ من قوائم المؤسس والوارد والإحالات والبحث اليدوي العام.
- [PROSPECT_RESEARCH_OS_AR](../outreach/PROSPECT_RESEARCH_OS_AR.md)
- المخطط: [schemas/prospect.schema.json](../../schemas/prospect.schema.json)
- البيانات: [data/prospects/](../../data/prospects/) · [قائمة الكبت](../../data/prospects/suppression_list.jsonl)

### 5. Cold Email Draft Factory — مصنع المسودات
ينتج 250 مسودة/يوم؛ كل مسودة تمر ببوابة الجودة ثم قائمة موافقة المؤسس.
- [COLD_EMAIL_DRAFT_FACTORY_AR](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md)
- [PERSONALIZATION_RULES_AR](../outreach/PERSONALIZATION_RULES_AR.md)
- [COLD_EMAIL_SEQUENCES_AR](../outreach/COLD_EMAIL_SEQUENCES_AR.md) · [EN](../outreach/COLD_EMAIL_SEQUENCES_EN.md)
- المخطط: [schemas/outreach_draft.schema.json](../../schemas/outreach_draft.schema.json)

### 6. Compliance + Deliverability Gate — بوابة الامتثال والتسليم
- [EMAIL_DELIVERABILITY_POLICY_AR](../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md)
- [COLD_EMAIL_COMPLIANCE_AR](../outreach/COLD_EMAIL_COMPLIANCE_AR.md)
- [UNSUBSCRIBE_POLICY_AR](../outreach/UNSUBSCRIBE_POLICY_AR.md)
- [SENDING_RAMP_PLAN_AR](../outreach/SENDING_RAMP_PLAN_AR.md)
- مخططات: [email_account](../../schemas/email_account.schema.json) · [sending_batch](../../schemas/sending_batch.schema.json) · [suppression](../../schemas/suppression.schema.json)
- محرّك البوابة (كود): [dealix/marketing_factory/market_production_os.py](../../dealix/marketing_factory/market_production_os.py)
- وحدات موجودة: `auto_client_acquisition/channel_policy_gateway/` · `auto_client_acquisition/safe_send_gateway/` · `auto_client_acquisition/email/compliance.py`

### 7. Founder Approval Queue — قائمة موافقة المؤسس
- [FOUNDER_APPROVAL_QUEUE_AR](../outreach/FOUNDER_APPROVAL_QUEUE_AR.md)
- المخطط: [schemas/approval_action.schema.json](../../schemas/approval_action.schema.json)
- التقرير: [reports/outreach/APPROVAL_QUEUE](../../reports/outreach/APPROVAL_QUEUE.md)

### 8. Sending Ramp OS — منحنى الإرسال التدريجي
- [SENDING_RAMP_OS_AR](../outreach/SENDING_RAMP_OS_AR.md)
- تقارير: [SENDING_BATCH_PLAN](../../reports/outreach/SENDING_BATCH_PLAN.md) · [DOMAIN_HEALTH_REVIEW](../../reports/outreach/DOMAIN_HEALTH_REVIEW.md)

### 9. Reply Handling OS — معالجة الردود
- [REPLY_HANDLING_OS_AR](../outreach/REPLY_HANDLING_OS_AR.md)
- المخطط: [schemas/reply.schema.json](../../schemas/reply.schema.json) · وحدة: `auto_client_acquisition/email/reply_classifier.py`
- التقرير: [reports/outreach/REPLY_QUEUE](../../reports/outreach/REPLY_QUEUE.md)

### 10. Job Signal OS — إشارات الوظائف كمؤشرات شراء
- [JOB_SIGNAL_PLAYBOOK_AR](../signals/JOB_SIGNAL_PLAYBOOK_AR.md)
- المخطط: [schemas/job_signal.schema.json](../../schemas/job_signal.schema.json) · البيانات: [data/signals/](../../data/signals/)
- التقرير: [reports/signals/JOB_SIGNAL_REPORT](../../reports/signals/JOB_SIGNAL_REPORT.md)

### 11. Content Production OS — إنتاج المحتوى
- [CONTENT_ENGINE_AR](../content/CONTENT_ENGINE_AR.md)
- [LINKEDIN_SYSTEM_AR](../content/LINKEDIN_SYSTEM_AR.md)
- [CASE_STUDY_SYSTEM_AR](../content/CASE_STUDY_SYSTEM_AR.md)
- [PROOF_CONTENT_SYSTEM_AR](../content/PROOF_CONTENT_SYSTEM_AR.md)
- المخطط: [schemas/content_idea.schema.json](../../schemas/content_idea.schema.json) · البيانات: [data/content/](../../data/content/)
- التقرير: [reports/content/CONTENT_CALENDAR](../../reports/content/CONTENT_CALENDAR.md)

### 12. Press OS — العلاقات الإعلامية
- [PRESS_OUTREACH_OS_AR](../press/PRESS_OUTREACH_OS_AR.md)
- [FOUNDER_STORY_AR](../press/FOUNDER_STORY_AR.md)
- [MEDIA_TARGETS_AR](../press/MEDIA_TARGETS_AR.md)
- [PROOF_MILESTONES_AR](../press/PROOF_MILESTONES_AR.md)
- التقرير: [reports/press/PRESS_PIPELINE](../../reports/press/PRESS_PIPELINE.md)

### 13. Partnerships OS — الشراكات
- [PARTNER_CHANNEL_OS_AR](../partnerships/PARTNER_CHANNEL_OS_AR.md)
- [AGENCY_PARTNER_PLAYBOOK_AR](../partnerships/AGENCY_PARTNER_PLAYBOOK_AR.md)
- [CONSULTANT_PARTNER_PLAYBOOK_AR](../partnerships/CONSULTANT_PARTNER_PLAYBOOK_AR.md)
- [REFERRAL_PROGRAM_AR](../partnerships/REFERRAL_PROGRAM_AR.md)
- المخطط: [schemas/partner.schema.json](../../schemas/partner.schema.json) · البيانات: [data/partners/](../../data/partners/)
- التقرير: [reports/partnerships/PARTNER_PIPELINE](../../reports/partnerships/PARTNER_PIPELINE.md)

### 14. WhatsApp Post-Reply OS — واتساب بعد الرد
لا واتساب بارد، لا أتمتة باردة؛ فقط بعد رد/موافقة، ومسودات بموافقة المؤسس.
- [WHATSAPP_POST_REPLY_FLOW_AR](../whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md)
- [WHATSAPP_READINESS_SCAN_AR](../whatsapp/WHATSAPP_READINESS_SCAN_AR.md)
- [WHATSAPP_ACTION_CARDS_AR](../whatsapp/WHATSAPP_ACTION_CARDS_AR.md)
- حدود القناة: [WHATSAPP_BOUNDARY](../02_saudi_positioning/WHATSAPP_BOUNDARY.md) · وحدة: `auto_client_acquisition/whatsapp_decision_bot/`
- التقرير: [reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE](../../reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md)

### 15. Founder GTM Control Room — غرفة قيادة المؤسس
- [FOUNDER_GTM_CONTROL_ROOM_AR](FOUNDER_GTM_CONTROL_ROOM_AR.md)
- واجهات تشغيل موجودة: `/[locale]/ops/founder` · `/ops/marketing` (راجع AGENTS.md).

### 16. Metrics + E2E — المقاييس والاختبارات
- [GTM_METRICS_AR](GTM_METRICS_AR.md)
- تقارير: [DAILY_GTM_REPORT](../../reports/gtm/DAILY_GTM_REPORT.md) · [WEEKLY_GTM_REVIEW](../../reports/gtm/WEEKLY_GTM_REVIEW.md)
- التحقق: `python3 scripts/verify_market_production_os.py` (يطبع `DEALIX_MARKET_PRODUCTION_OS_VERDICT`).
- الاختبارات: [tests/test_market_production_os.py](../../tests/test_market_production_os.py).

---

## الإيقاع اليومي — Daily Operating Rhythm

| الوقت | الخطوة | الناتج |
|---|---|---|
| 07:30 | Research | prospects + job signals + sector triggers |
| 08:30 | Draft Factory | 250 مسودة |
| 09:00 | Gates | brand voice · personalization · compliance · deliverability · risk |
| 10:00 | Founder Approval | اعتماد أفضل 30–50 |
| 11:00 | Sending Batch | إرسال تدريجي حسب السمعة |
| 13:00 | Reply Queue | تصنيف الردود وتوليد الإجراءات |
| 15:00 | Partners/Press/Job Signals | تواصل شخصي مدروس |
| 18:00 | Content | LinkedIn + proof + founder insight |
| 21:00 | Daily Report | ماذا تعلّمنا؟ ماذا نرسل غدًا؟ |

## المراجعة الأسبوعية — Weekly Review
أوقف أسوأ 20% من الرسائل، وضاعف أفضل 20%؛ حدّث playbooks القطاعات وبنك الاعتراضات
وكتالوج المنتجات وحدود التسعير؛ اكتب محتوى دليل؛ اختر 3 جهات press/partner فقط.

---

## الحوكمة — الغير قابل للتفاوض (11)
راجع [NON_NEGOTIABLES](../00_constitution/NON_NEGOTIABLES.md) و[طبقة الدستور](../00_foundation/).

ممنوع: قوائم بريد مشتراة · scraping · عناوين مضللة · Re:/Fwd: كاذبة · إرسال بلا إلغاء
اشتراك · تجاهل opt-out · واتساب بارد آلي · أتمتة LinkedIn · ادعاءات مضمونة · PII في
السجلات · أسرار في prompts.

مسموح: إنتاج مسودات بكثافة · تخصيص واقعي · قائمة موافقة · إرسال تدريجي · معالجة ردود ·
واتساب بعد الموافقة · تواصل press/partner/job-signal شخصي ومدروس.

---

## التشغيل والتحقق — Run + Verify

```bash
# تحقق من المخططات + البيانات + بوابات النظام
python3 scripts/verify_market_production_os.py

# الاختبارات
APP_ENV=test pytest tests/test_market_production_os.py -q
```

---

## EN Mirror (condensed)

The Market Production OS is Dealix's multi-channel GTM machine for Saudi B2B. It
produces up to **250 drafts/day**, but **sends are capped by the warm-up ramp and
domain health — 250 sends/day is only reachable after SPF/DKIM/DMARC, one-click
unsubscribe, an active suppression list, and healthy metrics (bounce < 3%, spam
< 0.3%)**. Every external send requires founder approval. The 16 subsystems above
cover brand, catalog, sectors, prospects, the draft factory, the compliance and
deliverability gate, the approval queue, the sending ramp, reply handling, job
signals, content, press, partnerships, WhatsApp post-reply, the founder control
room, and metrics/E2E. Schemas live in `schemas/`, seed data in `data/`, the
governed core in `dealix/marketing_factory/market_production_os.py`, reports in
`reports/`, and the verifier in `scripts/verify_market_production_os.py`.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
