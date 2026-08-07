# قرار المنتج — إيقاف الإرسال التلقائي منخفض المخاطرة

**الحالة:** مرفوض ومتقاعد — غير قابل للتفعيل بالمتغيرات البيئية  
**تاريخ القرار:** 2026-07-31  
**المالك:** المؤسس + الحوكمة + Product Doctrine  
**المسار السابق:** `api/routers/drafts.py` · `DEALIX_ENABLE_AUTO_SEND_LOW_RISK`

## القرار

لا يملك `Revenue Machine` أو أي Draft أو Opportunity صلاحية إرسال بريد خارجي تلقائياً.
المتغير البيئي القديم `DEALIX_ENABLE_AUTO_SEND_LOW_RISK` لا يمنح أي صلاحية، حتى عندما تكون قيمته `1` أو `true`.

المسار الوحيد المسموح للبريد الخارجي هو:

```text
Draft
→ Compliance Check
→ Explicit Human Approval
→ POST /api/v1/email/send-approved
→ Send Log / Evidence
```

## سبب الإيقاف

المسار الاستكشافي السابق كان يسمح نظرياً بالانتقال من تصنيف داخلي مثل
`warm_outreach_eligible=true` ومتغير بيئي إلى إرسال فعلي. هذا يتعارض مع قواعد
Dealix الحالية:

- draft-only وapproval-first افتراضياً؛
- Opportunity وDraft لا يملكان execution authority؛
- لا إرسال خارجي لمجرد انخفاض درجة المخاطر؛
- الموافقة يجب أن تكون مرتبطة بالفعل المحدد، لا بإعداد بيئي عام؛
- كل إرسال فعلي يحتاج سجل امتثال ودليل تنفيذ.

## سياسة القنوات

| القناة | السياسة الحالية |
|---|---|
| WhatsApp بارد | ممنوع دائماً |
| LinkedIn | بحث يدوي ومسودة شخصية فقط؛ لا scraping أو auto-send |
| Gmail outreach | مسودة ثم موافقة بشرية صريحة عبر `send-approved` |
| Gmail transactional | يظل في مساره المخصص، بقائمة أنواع مسموحة واحترام revoke/opt-out |
| تقويم أو دعوات خارجية | موافقة صريحة قبل الإنشاء أو الإرسال |

## الضوابط البرمجية

عند تسجيل Admin domain:

1. بوابة `_auto_send_low_risk_enabled` مرتبطة بسياسة تعيد `False` دائماً.
2. adapter الإرسال القديم داخل `drafts` يستبدل بـfail-closed adapter.
3. محاولة استدعائه مباشرة تفشل قبل أي اتصال بشبكة Gmail.
4. `/api/v1/email/send-approved` يبقى مسار الإرسال الخارجي المعتمد.

## إعدادات قديمة يجب عدم استخدامها

هذه الأمثلة تاريخية وممنوعة، وليست تعليمات تشغيل:

```bash
export DEALIX_ENABLE_AUTO_SEND_LOW_RISK=1
```

```json
{
  "approval_mode": "auto_send_low_risk"
}
```

وجودها في request أو environment لا يجب أن يؤدي إلى إرسال.

## شروط إعادة النظر مستقبلًا

لا يعاد فتح auto-send إلا عبر RFC جديد وPR مستقل يثبت جميع ما يلي:

- نموذج Approval قابل للتحقق مرتبط بـtenant وaction وdraft؛
- consent/lawful basis موثقان لكل مستلم؛
- idempotency وstop conditions وrate limits؛
- independent security/privacy review؛
- اختبارات production-like دون أسرار حقيقية؛
- موافقة مؤسس صريحة على التغيير وعلى تفعيل الإنتاج.

حتى استيفاء هذه الشروط يبقى الحكم النهائي: **لا auto-send**.
