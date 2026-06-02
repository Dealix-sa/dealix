# Dealix Market Production OS — نظام إنتاج السوق

> ماكينة go-to-market سعودية متعددة القنوات: تُنتج بكثافة، تراجع بصرامة، ترسل بحذر، تتعلّم، وتتوسّع — بدون أن تحرق الدومين أو الهوية أو الثقة.

**الحالة:** أساس قابل للتشغيل (schemas + data + verifier + tests + SOPs).
**المالك:** المؤسس (founder-governed).
**القاعدة الذهبية:** ارفع **الإنتاج** إلى 250 draft/day، ولا ترفع **الإرسال** إلى 250/day إلا بعد اجتياز صحة الدومين، opt-out، suppression، وقواعد الـ ramp.

---

## 1. لماذا هذا النظام؟

الشيء الصحيح ليس "كولد إيميل فقط"، بل نظام إنتاج سوق كامل:

```
Brand → Product Catalog → Sector Intelligence → Prospect Research → Job Signals
→ Cold Email Draft Factory → Compliance + Deliverability Gate → Founder Approval Queue
→ Sending Ramp → Reply Handling → WhatsApp Post-Reply → Proposal + Proof Pack
→ Content → Press → Partnerships → Founder GTM Control Room → Metrics
```

كل جهة تُنتج مخرجًا وتُقاس بمقياس واضح. لا قناة تعمل خارج الحوكمة.

---

## 2. الخريطة الكاملة — من الوثيقة إلى المخطط إلى المحرّك

كل نظام فرعي له: وثيقة تشغيل (`docs/`)، مخطط بيانات (`schemas/`)، بيانات/قوالب (`data/`)، تقرير (`reports/`)،
ومحرّك قائم في الريبو يتكامل معه (`auto_client_acquisition/` و`dealix/`). هذه الطبقة **لا تستبدل** المحرّكات؛ تنظّمها في نظام واحد.

| النظام الفرعي | الوثيقة | المخطط | المحرّك القائم |
|---|---|---|---|
| Brand OS | [docs/brand/](../brand/) · [BRAND_IDENTITY_SYSTEM_AR](../brand/BRAND_IDENTITY_SYSTEM_AR.md) | — | docs/BRAND_PRESS_KIT.md |
| Product Catalog OS | [docs/commercial/PRODUCT_CATALOG_AR](../commercial/PRODUCT_CATALOG_AR.md) · [OFFER_LADDER_AR](../commercial/OFFER_LADDER_AR.md) | — | `sales_os` · docs/commercial/offers/ |
| Sector Intelligence OS | [docs/sectors/](../sectors/) | `data/sectors/sectors.yaml` | `market_intelligence` · `vertical_playbooks` |
| Prospect Research OS | [docs/outreach/PROSPECT_RESEARCH_OS_AR](../outreach/PROSPECT_RESEARCH_OS_AR.md) | `prospect.schema.json` | `data_os` (SourcePassport) |
| Cold Email Draft Factory | [docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR](../outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md) | `outreach_draft.schema.json` | `dealix/marketing_factory` |
| Compliance + Deliverability Gate | [docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR](../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md) · [COLD_EMAIL_COMPLIANCE_AR](../outreach/COLD_EMAIL_COMPLIANCE_AR.md) | `email_account.schema.json` · `suppression.schema.json` | `governance_os` · `channel_policy_gateway` |
| Founder Approval Queue | [docs/outreach/FOUNDER_APPROVAL_QUEUE_AR](../outreach/FOUNDER_APPROVAL_QUEUE_AR.md) | `approval_action.schema.json` | `approval_center` |
| Sending Ramp OS | [docs/outreach/SENDING_RAMP_OS_AR](../outreach/SENDING_RAMP_OS_AR.md) · [SENDING_RAMP_PLAN_AR](../outreach/SENDING_RAMP_PLAN_AR.md) | `sending_batch.schema.json` | `safe_send_gateway` |
| Reply Handling OS | [docs/outreach/REPLY_HANDLING_OS_AR](../outreach/REPLY_HANDLING_OS_AR.md) | `reply.schema.json` | `support_inbox` · `customer_inbox_v10` |
| Job Signal OS | [docs/signals/JOB_SIGNAL_PLAYBOOK_AR](../signals/JOB_SIGNAL_PLAYBOOK_AR.md) | `job_signal.schema.json` | `market_intelligence` |
| Content Production OS | [docs/content/CONTENT_ENGINE_AR](../content/CONTENT_ENGINE_AR.md) | — | `dealix/marketing_factory` · docs/content/ |
| Press OS | [docs/press/PRESS_OUTREACH_OS_AR](../press/PRESS_OUTREACH_OS_AR.md) | — | docs/BRAND_PRESS_KIT.md |
| Partnerships OS | [docs/partnerships/PARTNER_CHANNEL_OS_AR](../partnerships/PARTNER_CHANNEL_OS_AR.md) | — | `partnership_os` · docs/partners/ |
| WhatsApp Post-Reply OS | [docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR](../whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md) | — | `whatsapp_decision_bot` · `channel_policy_gateway` |
| Founder GTM Control Room | [docs/gtm/GTM_CONTROL_ROOM_AR](../gtm/GTM_CONTROL_ROOM_AR.md) | — | `executive_command_center` · `/ops/founder` |
| Metrics + E2E | [docs/gtm/GTM_METRICS_AR](../gtm/GTM_METRICS_AR.md) | — | `business_metrics_board` · `scorecards` |

Proof + Value + Capital تُغذّى من كل engagement مدفوع: `proof_os` · `value_os` · `capital_os`.

---

## 3. المسار من Prospect إلى Cash (مع البوابات)

1. **Research** — `prospect.schema.json` (مصدر من المؤسس أو بيانات عامة مُراجعة يدويًا — لا scraping).
2. **Match** — القطاع → العرض الأول من `data/sectors/sectors.yaml`.
3. **Draft** — 250 draft/day بصيغة `outreach_draft.schema.json` (كل draft فيه `unsubscribe_included` و`personalization_note` حقيقي).
4. **Gate** — Compliance + Deliverability: SPF/DKIM/DMARC، suppression، تخصيص، subject غير مضلّل، risk.
5. **Approve** — Founder Approval Queue (`approval_action.schema.json`): approve / rewrite / shorten / change_offer / nurture / do_not_contact.
6. **Send (ramp)** — `sending_batch.schema.json`: دفعات صغيرة تتدرّج حسب صحة الدومين — **ليس 250/day دفعة واحدة**.
7. **Reply** — تصنيف `reply.schema.json` → الإجراء التالي. unsubscribe/angry/bounce → suppression فورًا.
8. **WhatsApp بعد الرد** — فقط بعد رد إيجابي/موافقة، 1:1، بموافقة المؤسس — لا قناة باردة.
9. **Proposal + Proof Pack** — `proof_os.assemble(...)` بسكور ≥ 70 + Capital Asset.
10. **Learn** — تقرير يومي/أسبوعي يوقف الأسوأ ويضاعف الأفضل.

---

## 4. الحوكمة — الـ 11 non-negotiables (مفروضة باختبارات)

1. لا scraping. 2. لا cold WhatsApp automation. 3. لا LinkedIn automation. 4. لا claims بلا مصدر.
5. لا ضمان نتائج بيع. 6. لا PII في الـ logs. 7. لا إجابة معرفية بلا مصدر. 8. لا إجراء خارجي بلا موافقة.
9. لا agent بلا هوية. 10. لا مشروع بلا Proof Pack. 11. لا مشروع بلا Capital Asset.

البوابات في الكود التي تحرس هذه الطبقة:
- `governance_os.policy_check_draft(text)` — يحجب لغة cold whatsapp / LinkedIn automation / الضمانات (`tests/test_no_cold_whatsapp.py`, `test_no_linkedin_automation.py`, `test_no_guaranteed_claims.py`).
- `revenue_os.anti_waste.validate_pipeline_step(lead_source="scraping" ...)` → `blocked_source` (`tests/test_no_scraping_engine.py`).
- `data_os.pii_flags_for_row(...)` — يرصد PII (`tests/test_no_pii_in_logs.py`).
- منع السلسلة المحظورة عبر كامل الريبو (اختبار القفل على مستوى الريبو في `tests/`).
- اختبارات هذه الطبقة: `tests/test_market_production_os.py` + المحقّق `scripts/verify_market_production_os.py`.

### ممنوعات مطلقة
purchased email lists · fake personalization · misleading subject · Re:/Fwd: كاذبة · إرسال بلا unsubscribe ·
تجاهل opt-out · cold WhatsApp automation · LinkedIn automation · scraping مخالف · claims مضمونة · PII في logs · secrets في prompts.

### مسموح
إنتاج drafts بكثافة · تخصيص واقعي · approval queue · إرسال تدريجي · reply handling · واتساب بعد consent ·
press/partner outreach شخصي · job-signal outreach مدروس وبموافقة.

---

## 5. الامتثال والتسليمية (لماذا لا 250 إرسال/يوم فورًا)

متطلبات مرسلي Gmail تستلزم SPF/DKIM (أو DKIM) لكل المرسلين، وSPF + DKIM + DMARC للمرسلين بكثافة، وone-click
unsubscribe للرسائل التسويقية، وإبقاء معدّل الـ spam تحت 0.3%؛ وتحذّر Google من شراء القوائم أو الإرسال لمن لم يشترك
لأنه يضرّ سمعة الدومين. ونظام CAN-SPAM يشترط عدم تضليل الـ headers/subject، ووجود opt-out واضح يُحترم، وعنوان
بريدي صحيح. لذلك:

- الإنتاج = 250 draft/day منذ اليوم 0.
- الإرسال = 0–20/day في الأسبوع 0، يتدرّج إلى 250/day فقط إذا بقيت المؤشرات صحية.
- العتبات: bounce < 3% · spam complaint < 0.1–0.3% · لا تحذيرات من المزوّد · positive reply rate يتحسّن.

التفاصيل: [EMAIL_DELIVERABILITY_POLICY_AR](../outreach/EMAIL_DELIVERABILITY_POLICY_AR.md) ·
[SENDING_RAMP_PLAN_AR](../outreach/SENDING_RAMP_PLAN_AR.md) · [COLD_EMAIL_COMPLIANCE_AR](../outreach/COLD_EMAIL_COMPLIANCE_AR.md) ·
[UNSUBSCRIBE_POLICY_AR](../outreach/UNSUBSCRIBE_POLICY_AR.md).

---

## 6. التسعير — مصدر الحقيقة

في الريبو سلّم تجاري **موصول بالكود/الاختبارات** (Free / 499 / 1,500 / 2,999–4,999 شهريًا / 5,000–25,000 / Enterprise 25,000–50,000).
أرقام الكتالوج الأكبر (حتى 90,000+) تُعامَل كطبقة **custom/enterprise** فوق السلّم: **quote-based وبموافقة المؤسس فقط**، لا تسعير تلقائي.
لا تتعارض هذه الطبقة مع التسعير الموصول؛ تنظّمه. التفاصيل: [PRICING_GUARDRAILS_AR](../commercial/PRICING_GUARDRAILS_AR.md).

---

## 7. الإيقاع اليومي (Operating Rhythm)

| الوقت | النشاط |
|---|---|
| 07:30 | Research — prospects + job signals + sector triggers |
| 08:30 | Draft Factory — إنتاج 250 drafts |
| 09:00 | Gates — brand voice · personalization · compliance · deliverability · risk |
| 10:00 | Founder Approval — اعتماد أفضل 30–50 |
| 11:00 | Sending Batch — إرسال تدريجي حسب السمعة |
| 13:00 | Reply Queue — تصنيف الردود + الإجراء التالي |
| 15:00 | Partner / Press / Job Signals |
| 18:00 | Content — LinkedIn + proof + founder insight |
| 21:00 | Daily Report — ماذا تعلّمنا؟ ماذا نرسل غدًا؟ أي قطاع نوقفه؟ |

التقارير: [reports/gtm/DAILY_GTM_REPORT.md](../../reports/gtm/DAILY_GTM_REPORT.md) ·
[reports/gtm/WEEKLY_GTM_REVIEW.md](../../reports/gtm/WEEKLY_GTM_REVIEW.md).

---

## 8. المراجعة الأسبوعية

أوقف أسوأ 20% من الرسائل · ضاعف أفضل 20% · حدّث sector playbooks · حدّث objection bank ·
حدّث product catalog · حدّث pricing guardrails · اكتب proof content · اختر 3 press/partner targets فقط.

---

## 9. تعريف النجاح

كل يوم يستطيع النظام: يبحث عن شركات · يطابق الشركة بقطاع وعرض · يُنتج 250 draft مخصص · يفحص جودة كل draft ·
يرتّب الأفضل · يجهّز دفعات إرسال معتمدة · يعالج الردود · يكتشف job signals · يُنتج محتوى/press/partner drafts ·
يوجّه الردود الإيجابية إلى WhatsApp/portal · يُخرج تقرير GTM للمؤسس — **بدون الإضرار بسمعة الدومين أو خرق سياسة الثقة.**

---

## 10. التحقق

```bash
python3 scripts/verify_market_production_os.py   # يطبع DEALIX_MARKET_PRODUCTION_OS_VERDICT=PASS|FAIL
APP_ENV=test pytest tests/test_market_production_os.py -q --no-cov
```

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
