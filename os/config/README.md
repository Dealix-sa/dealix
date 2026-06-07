# Dealix Pricing & Revenue Operating System

> نظام التسعير والدخل — ليس جدول أسعار، بل طبقة تشغيل كاملة.
> A pricing & revenue OS — not a price table, a full operating layer.

**المبدأ:** أي سعر يخرج من النظام، لا من الذاكرة. الملفات اليامل هي المصدر الوحيد للحقيقة.
**Principle:** every price comes from the system, never from memory. The YAML files are the single source of truth.

نموذج الدخل: `Audit → Pilot → Production → Managed OS → Usage/Add-ons → Command Center`
كل عميل ليس صفقة واحدة؛ هو أصل شهري متكرر (MRR).

---

## الملفات / Files

| الملف | الغرض |
|---|---|
| `os/config/pricing.yml` | كتاب الأسعار: entry offers, pilots, production, price ladder, customer tiers, VAT |
| `os/config/packages.yml` | باقات الاشتراك الشهرية (Monitor → Enterprise Sovereign) — الباقة الأساسية `managed_os` |
| `os/config/usage_meters.yml` | التسعير حسب الاستخدام (overages) لكل نظام |
| `os/config/discount_policy.yml` | سياسة الخصومات والممنوعات |
| `os/config/payment_terms.yml` | شروط الدفع للمشاريع والاشتراكات + premium بدون retainer |
| `os/config/margin_guardrails.yml` | حدود الهامش — لا تُكسَر بدون استثناء موثّق |
| `finance/mrr_targets.yml` | أهداف MRR (30k → 1M) + funnel math |
| `finance/unit_economics.yml` | اقتصاديات الوحدة (CAC, LTV, تكاليف مباشرة) |
| `sales/PRICE_BOOK_AR.md` / `_EN.md` | نسخة بشرية للقراءة من كتاب الأسعار |
| `sales/QUOTE_TEMPLATE_AR.md` / `_EN.md` | قوالب عروض الأسعار (تُملأ بواسطة السكربت) |

## السكربتات / Scripts

```bash
# حاسبة الهامش — تتحقق ضد margin_guardrails.yml
python scripts/calculate_margin.py --revenue 60000 --kind pilot --estimate

# مولّد عروض الأسعار (مسودة فقط — لا يُرسل)
python scripts/generate_quote.py --list
python scripts/generate_quote.py --offer pilot_pro_api --client "Acme FM" \
    --lang ar --monthly managed_os --out reports/quote_acme.md

# توقّع الدخل الشهري المتكرر + التحقق من اتساق الأهداف
python scripts/generate_mrr_forecast.py
```

## الحوكمة / Governance

- جميع الأسعار **قبل** ضريبة القيمة المضافة 15% (ZATCA).
- مشاركة أي سعر مع عميل تتطلب موافقة المؤسس — بوابة **G03** (`os/06_APPROVAL_GATES.yml`).
- مخرجات السكربتات **مسودات داخلية**؛ لا إرسال خارجي ولا تحصيل مدفوعات حية.
- أي عرض دون الحد الأدنى للهامش يُحجب إلا باستثناء موثّق في `discount_policy.yml`.
