# تقرير إثباتي: الذاكرة التشغيلية | Operating Memory Evidence Report

> **AR:** يوثّق هذا التقرير الأدلّة على أن طبقة الذاكرة التشغيلية مبنية ومحكومة وفق قواعد الأمان: الذكاء يُحضّر، المؤسس يعتمد، والفعل الخارجي يدوي فقط. يُستخدم كمرجع تدقيق عند المراجعة.
>
> **EN:** This report documents the evidence that the Operating Memory layer is built and governed under the safety rules: AI prepares, founder approves, external action manual only. It is an audit reference for reviews.

## نطاق الطبقة | Layer Scope

| العنصر Item | المرجع Reference |
|---|---|
| تعريفات المخططات / Schema definitions | `config/operating_memory_schemas.json` |
| أداة التحقق / Validator | `scripts/operating_memory_validate.py` |
| القرار/العميل/السوق/الإيراد / Decision/Client/Market/Revenue | `02`–`05` في هذا المجلد |

## قائمة التحقق من الأدلّة | Evidence Checklist

- [x] كل سجل يحمل `id`, `type`, `status`, `source`, وطوابع زمنية. / Every record carries `id`, `type`, `status`, `source`, timestamps.
- [x] السجلات تبدأ `draft` ولا تُعتمد إلا يدويًا. / Records start as `draft`, approved manually only.
- [x] المُحقِّق يرفض الحقول الناقصة وأي أسرار/مفاتيح. / Validator rejects missing fields and any secrets/keys.
- [x] لا مسار إرسال خارجي في الطبقة. / No external-send path in the layer.
- [x] إشارات السوق تحمل مرجع دليل. / Market signals carry an evidence reference.
- [x] أرقام الإيراد حقيقية وباحتمالية صادقة. / Revenue numbers are real with honest probability.

## مطابقة قواعد الأمان | Safety Rules Compliance

| القاعدة Rule | الحالة Status |
|---|---|
| AI prepares, Founder approves | مطبَّقة / Enforced |
| Manual action only | مطبَّقة / Enforced |
| No external sending (email/WhatsApp/LinkedIn) | مطبَّقة / Enforced |
| No scraping / No auto-submit | مطبَّقة / Enforced |
| No fake traction / No guaranteed ROI | مطبَّقة / Enforced |
| No secrets/API keys | مطبَّقة / Enforced |

## إعادة إنتاج الأدلّة | Reproduce Evidence

```bash
python scripts/operating_memory_validate.py --records data/operating_memory/ --strict
```

## الخلاصة | Conclusion

> **AR:** الطبقة متوافقة مع قواعد الأمان وجاهزة كمرجع داخلي. أي تطوير لاحق يجب أن يحافظ على مبدأ "تحضير آلي، اعتماد بشري، فعل يدوي".
>
> **EN:** The layer complies with the safety rules and is ready as an internal reference. Any future change must preserve "AI prepares, human approves, manual action."
