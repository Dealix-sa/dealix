# Affiliate Network — شبكة أفلييت محكومة

**الغرض:** الأفلييت **المفتوح مبكراً** خطر. الأفلييت **المغلق والمدقق** قناة نمو.

## البداية

- **5–10** شركاء موثوقون فقط.  
- **Scripts معتمدة** + **مراجعة يدوية** لكل حملة.  
- **إفصاح إلزامي** (disclosure).  
- **عمولة بعد invoice_paid فقط** — لا عمولة قبل تحصيل، ولا مع **refund** مفتوح.

## Workflow

```text
affiliate_submits_copy
  → compliance_review
  → approved | edit_required | blocked
  → tracking link (إن وُجد)
  → lead submitted
  → qualified
  → invoice_paid
  → commission_eligible
```

## بوابة استحقاق العمولة (الكل مطلوب)

العمولة تُصرف فقط عند تحقق **كل** الشروط التالية:

- `invoice_paid` مثبت  
- لا **refund** مفتوح على الفاتورة  
- الـlead **غير مكرر**  
- النسخة المعتمدة **متوافقة** (compliant)  
- **disclosure** ظاهر في الحملة

العمولة موصى بها كنطاق تقديري (مثلاً **15–25%** من أول دفعة أو أول 3 أشهر) —
يُحدَّد لكل شريك، ولا يُعلن كرقم ثابت.

## شروط عدم الأهلية (أمثلة)

- Lead **مكرر**  
- ادعاءات غير معتمدة في النسخة  
- غياب **disclosure**  
- قنوات ممنوعة (انظر أدناه)

## ممنوعات

- ROI مضمون، **compliance مضمون** كوعد بيع  
- «Dealix يرسل تلقائياً» للعميل النهائي في سياق يخالف السياسة  
- spam، **cold WhatsApp**، **fake proof**  
- مكافأة قبل **invoice_paid**

## روابط ذات صلة

- [TRUST_LAYER.md](TRUST_LAYER.md)
- [PARTNER_ECONOMY.md](PARTNER_ECONOMY.md)
- [docs/affiliates/AFFILIATE_PROGRAM.md](../affiliates/AFFILIATE_PROGRAM.md) (إن وُجد)
- [docs/strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md](../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md) — المرجع الاستراتيجي
