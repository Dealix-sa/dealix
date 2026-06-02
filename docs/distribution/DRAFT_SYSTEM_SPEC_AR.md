# Draft System Spec — مواصفة نموذج المسودة (Distribution OS v1)

**الغرض:** تعريف **نموذج بيانات المسودة** (Draft data model) الذي يدور حوله كل النظام. المسودة هي الوحدة الذرية: كل تواصل خارجي محتمل يبدأ مسودةً محكومة بالحالة `pending_approval`، ولا يصبح فعلاً إلا بعد موافقة بشرية ونسخ يدوي.

**القاعدة المعمارية:** **لا توجد قناة أتمتة ولا حالة «أُرسل عبر تكامل».** الإرسال دائماً فعل بشري يدوي بعد الموافقة — هذا مقصود في التصميم، لا نقص.

**الكود (يُبنى في هذا الـ PR):** [`auto_client_acquisition/distribution_os/`](../../auto_client_acquisition/distribution_os/) · المخطط: [`schemas/draft.schema.json`](../../schemas/draft.schema.json).

**مراجع:** [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md) · سياسة الجودة: [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) · مستويات الإثبات: [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md).

---

## 1) الحقول (Fields)

| الحقل | النوع | إلزامي | المعنى |
|-------|------|:------:|--------|
| `id` | string | نعم | معرّف فريد للمسودة (مثل `drf_2026_0001`) — لا يحمل PII. |
| `prospect_id` | string | نعم | معرّف المرشّح المرتبط — مرجع داخلي، ليس بريداً ولا هاتفاً. |
| `company` | string | نعم | اسم الشركة المستهدفة (عام، بلا بيانات تعريف شخصية). |
| `sector` | string | نعم | القطاع (مثل `agency`, `clinic`, `real_estate`, `b2b_saas`). |
| `channel` | enum | نعم | قناة **يدوية** فقط — انظر §2. |
| `draft_type` | enum | نعم | نوع المسودة في القِمع — انظر §3. |
| `language` | enum | نعم | `ar` أو `en` (لغة جسم النص). |
| `subject` | string | لا | عنوان للبريد؛ يُترك فارغاً لقنوات بلا عنوان. |
| `body` | string | نعم | نص المسودة المقترح — يخضع لبوابة الجودة قبل العرض. |
| `offer_angle` | string | نعم | زاوية العرض (مثل «ما بعد الـ lead»، «حوكمة المتابعة»). |
| `evidence_level` | enum | نعم | مستوى الإثبات `L0`–`L5` — انظر [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md). |
| `risk_level` | enum | نعم | `low` / `medium` / `high` — يرفع التدقيق على المسودات الأعلى خطراً. |
| `approval_required` | boolean | نعم | **دائماً `true`** — لا مسودة تتخطى الموافقة بالتصميم. |
| `status` | enum | نعم | حالة دورة الحياة — انظر §4. |
| `created_at` | string (ISO 8601) | نعم | وقت التوليد. |
| `updated_at` | string (ISO 8601) | نعم | وقت آخر تغيير حالة/تعديل. |
| `next_action` | string | نعم | الخطوة التالية الواضحة (SOAEN Next Action) — مثل «انسخ وأرسِل يدوياً» أو «انتظر D+2». |

**قاعدة عابرة:** أي حقل قد يحمل بيانات تعريف شخصية (بريد، هاتف، هوية، اسم فرد) **لا يُخزَّن في المسودة ولا في السجلات**. الهوية تبقى مرجعاً داخلياً عبر `prospect_id`.

---

## 2) التعداد: القنوات (`channel`)

كل القنوات **يدوية**. لا توجد قناة أتمتة في هذا التعداد بالتصميم.

| القيمة | المعنى | كيف يتم الإرسال |
|--------|--------|-----------------|
| `email` | بريد إلكتروني | المؤسس ينسخ النص ويرسله من صندوقه يدوياً |
| `whatsapp_manual` | واتساب **يدوي** | المؤسس يرسل بنفسه لجهة يعرفها — لا واتساب بارد، لا إرسال جماعي |
| `linkedin_manual` | لينكدإن **يدوي** | رسالة/تعليق يكتبه المؤسس بنفسه — لا أتمتة لينكدإن |
| `phone_script` | نص مكالمة | سكربت يقرأه المؤسس في مكالمة |
| `proposal_pdf` | عرض PDF | مستند يُراجَع ويُرسَل يدوياً بعد الموافقة |
| `internal_note` | ملاحظة داخلية | لا تُرسَل خارجياً إطلاقاً — للمؤسس فقط |

> ملاحظة سلامة: الكلمتان «whatsapp_manual» و«linkedin_manual» مقصودتان للتأكيد أن القناة **يدوية**. لا يوجد `whatsapp_auto` ولا `linkedin_auto` في النظام.

---

## 3) التعداد: نوع المسودة (`draft_type`)

| القيمة | الموضع في القِمع |
|--------|------------------|
| `outreach_first` | أول تواصل (Day 0) |
| `outreach_followup_1` | متابعة 1 (D+2) |
| `outreach_followup_2` | متابعة 2 (D+4) |
| `breakup` | رسالة إغلاق مهذّبة / إذن بالإغلاق (D+7) |
| `discovery_invite` | دعوة مكالمة اكتشاف بعد رد |
| `diagnostic_summary` | ملخص تشخيصي للعميل |
| `proposal` | عرض (يخرج من [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md)) |
| `proof_pack_intro` | تقديم حزمة الإثبات |
| `payment_followup` | متابعة رابط دفع (بعد 24h) |
| `onboarding_message` | رسالة بدء التشغيل بعد الدفع |
| `renewal_upsell` | تجديد/توسعة (يوم 21–30) |

التسلسل الزمني الكامل لهذه الأنواع في [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md).

---

## 4) التعداد: الحالة (`status`)

| القيمة | المعنى | مَن يغيّرها |
|--------|--------|-------------|
| `generated` | وُلِّدت للتو، قبل بوابة الجودة | النظام |
| `pending_approval` | مرّت الجودة، تنتظر قرار المؤسس | النظام |
| `approved` | وافق المؤسس — جاهزة للنسخ اليدوي | **المؤسس** |
| `needs_edit` | تحتاج تعديلاً قبل القبول | **المؤسس** |
| `rejected` | مرفوضة — لا تُرسَل | **المؤسس** |
| `copied_manually` | نسخها المؤسس وأرسلها **يدوياً** | **المؤسس** |
| `replied` | وصل رد من المرشّح | **المؤسس** |
| `archived` | أُغلقت دورتها | المؤسس/النظام |

**لا توجد حالة `sent` آلية.** الانتقال الأقرب إلى «أُرسِل» هو `copied_manually` — وهو **توثيق لفعل بشري حدث خارج النظام**، لا أمر إرسال أصدره النظام. هذا هو الفرق الجوهري بين «ماكينة تصريف بالموافقة» و«أداة أتمتة إرسال».

### مسار الحالات (الطبيعي)

```text
generated → pending_approval → approved → copied_manually → replied → archived
                            ↘ needs_edit ↗
                            ↘ rejected → archived
```

---

## 5) مرجع المخطط (JSON Schema)

التحقق البنيوي عبر [`schemas/draft.schema.json`](../../schemas/draft.schema.json). الشكل المرجعي:

```json
{
  "id": "drf_2026_0001",
  "prospect_id": "prs_2026_0042",
  "company": "Example Marketing Agency",
  "sector": "agency",
  "channel": "email",
  "draft_type": "outreach_first",
  "language": "ar",
  "subject": "ما بعد الـ lead — سؤال واحد",
  "body": "...نص محكوم...",
  "offer_angle": "post_lead_followup_governance",
  "evidence_level": "L1",
  "risk_level": "low",
  "approval_required": true,
  "status": "pending_approval",
  "created_at": "2026-06-02T07:00:00Z",
  "updated_at": "2026-06-02T07:00:00Z",
  "next_action": "نسخ يدوي بعد موافقة المؤسس"
}
```

**ثوابت يفرضها المخطط:** `approval_required` ثابت على `true`؛ `channel` ضمن القائمة اليدوية فقط؛ `evidence_level` ضمن `L0`–`L5`؛ لا حقل لقناة آلية. أي مسودة تخالف هذه الثوابت تُرفض قبل أن تصل طابور المراجعة (انظر [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md)).

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
