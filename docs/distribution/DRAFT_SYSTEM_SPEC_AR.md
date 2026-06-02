# Dealix Draft System Specification — مواصفة نظام المسودات

> المرجع الحتمي لطبقة المسودات. أي تنفيذ يجب أن يطابق هذا الملف ومخطط
> `dealix/contracts/schemas/distribution_draft.schema.json`.

## 1. الهدف

نظام مسودات واقعي للتصريف **بدون** spam ولا إرسال خارجي غير مضبوط. المخرجات
كلها داخلية (L1) تنتظر موافقة بشرية.

## 2. أنواع المسودات (`draft_type`)

```
outreach_first        رسالة أولى
outreach_followup_1   متابعة 1
outreach_followup_2   متابعة 2
breakup               رسالة إنهاء مهذّبة
discovery_invite      دعوة مكالمة استكشاف
diagnostic_summary    ملخّص تشخيص
proposal              عرض
proof_pack_intro      تقديم Proof Pack
payment_followup      متابعة دفع
onboarding_message    رسالة Onboarding
renewal_upsell        تجديد / توسعة
```

> v1 يولّد `outreach_first` فقط. البقية مدعومة في المخطط ومخصّصة لـ P1.

## 3. حالات المسودة (`status`)

```
generated            مولّدة (حالة وسيطة)
pending_approval     بانتظار الموافقة  ← المخرَج النظيف من المولّد
needs_edit           يحتاج تعديل (تفعّل عند رصد حارس) ← المخرَج عند مخالفة
approved             معتمدة (قرار بشري)
rejected             مرفوضة (قرار بشري)
copied_manually      نُسخت يدويًا (قرار بشري)
sent_via_integration أُرسلت عبر تكامل — **فقط بعد الموافقة**، ولا يكتبها أي سكربت في هذه الطبقة
replied              ردّ العميل
archived             مؤرشفة
```

**قاعدة المولّد:** لا يُنتج إلا `pending_approval` أو `needs_edit`. بقية الحالات
يضبطها الإنسان أو مسار الموافقة. هذا مقفول باختبار في `tests/test_distribution_drafts.py`.

## 4. الحقول المطلوبة

كل مسودة تحتوي (انظر المخطط للقيود الكاملة):

```
id, prospect_id, company, sector, channel, draft_type, language,
body, evidence_level, risk_level, approval_required, status, created_at
```

حقول اختيارية: `subject`, `offer_angle`, `policy_issues`, `updated_at`, `next_action`.

- `approval_required` = **true دائمًا** (مقيّدة `const: true` في المخطط).
- `evidence_level` = **L1** للمسودات المولّدة.
- `policy_issues` غير فارغة ⇒ `status = needs_edit`.

## 5. القنوات (`channel`) — يدوية فقط

```
email            بريد (نسخ يدوي / مسودة)
whatsapp_manual  واتساب يدوي فقط — لا أتمتة
linkedin_manual  لينكدإن يدوي فقط — لا أتمتة
phone_script     نص مكالمة
proposal_pdf     عرض PDF / مسودة
internal_note    ملاحظة داخلية
```

لا يوجد خلف أي قيمة هنا أي محرّك إرسال آلي.

## 6. القواعد الصارمة (مطابقة لحُرّاس الـ CI)

| القاعدة | الحارس الذي يفرضها |
| --- | --- |
| لا cold WhatsApp | `policy_check_draft` + `test_no_cold_whatsapp` |
| لا LinkedIn automation | `policy_check_draft` + `test_no_linkedin_automation` |
| لا scraping | `anti_waste.validate_pipeline_step` + `test_no_scraping_engine` |
| لا PII في السجلات | `pii_flags_for_row` + `test_no_pii_in_logs` |
| لا ادعاء مصدر بلا دليل | `test_no_source_no_answer` |
| لا إرسال بدون موافقة | `enforce_doctrine_non_negotiables` + `test_doctrine_guardrails` |

## 7. كيف يفرض المولّد ذلك (`scripts/generate_distribution_drafts.py`)

1. `enforce_doctrine_non_negotiables()` عند البدء — يؤكّد نظافة الوضع.
2. لكل مسودة: `draft_guard_issues()` يجمع:
   - مخرجات `policy_check_draft(subject + body)`،
   - أعلام `pii_flags_for_row(draft)`،
   - فحص PII نصّي مباشر في الجسم (email/phone).
3. إن وُجدت أي مشكلة ⇒ `status = needs_edit` + `policy_issues` + `next_action`.
4. وإلا ⇒ `status = pending_approval`.

المسودات تُلحق في `data/drafts/drafts.jsonl` (append-only للتدقيق)، ويُكتب تقرير في
`reports/distribution/DRAFT_GENERATION_REPORT.md`.

## 8. دفتر المسودات (JSONL)

ملف append-only، سطر لكل مسودة، يسهّل التدقيق. مثال (مختصر):

```json
{"id":"draft_ab12cd34ef56","prospect_id":"prospect_001","company":"...","sector":"...","channel":"email","draft_type":"outreach_first","language":"ar","body":"...","evidence_level":"L1","risk_level":"low","approval_required":true,"status":"pending_approval","policy_issues":[],"created_at":"2026-06-02T00:00:00+00:00","next_action":"Founder approval before any manual send"}
```
