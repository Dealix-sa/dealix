<!-- Owner: Founder | Date: 2026-05-17 | Arabic primary -->

# Dealix — قرار مصدر التسعير — Pricing Source Decision

> مذكرة قرار من صفحة واحدة: أي وثيقة هي المرجع الرسمي للأسعار والعروض،
> ولماذا. تُحَل بها كل التعارضات في الأرقام.
>
> One-page decision memo: which document is canonical for pricing and
> offers, and why. It resolves every numeric conflict.

---

## 1. القرار — The Decision

**المرجع الرسمي الوحيد للتسعير والعروض هو
[`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md).**

**The single canonical source for pricing and offers is
[`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md).**

السبب: خريطة الربط التجاري تُولَّد من السجل المُنفَّذ في الكود
(`auto_client_acquisition/service_catalog/registry.py`) وتُحرَسها اختبارات
CI (`tests/test_commercial_map.py`). العروض السبعة تأتي من هذا السجل وحده.
عندما يتغير الكود، تتغير الوثيقة تلقائياً — لا يوجد مصدر ثانٍ ينحرف.

Reason: the Commercial Wiring Map is generated from the code-enforced
registry (`auto_client_acquisition/service_catalog/registry.py`) and is
guarded by CI tests (`tests/test_commercial_map.py`). The 7 offers come
from that registry alone. When the code changes, the document changes
automatically — there is no second source to drift.

---

## 2. التعارض — The Conflict

[`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) يعرض
نطاقات أسعار أقدم ومختلفة (مثل "999/شهر" و"2,999–4,999 SAR/شهر"
و"7,500–15,000 SAR/شهر") لا تطابق السجل المُنفَّذ في الكود. هذه النطاقات
ليست مُحرَّسة باختبار، فهي قابلة للانحراف عن الحقيقة.

[`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) shows
older, conflicting price bands (e.g. "999/month", "2,999–4,999 SAR/month",
"7,500–15,000 SAR/month") that do not match the code-enforced registry.
Those bands are not test-guarded, so they can drift from the truth.

عند أي اختلاف بين الوثيقتين، خريطة الربط التجاري تكسب — دائماً.

On any disagreement between the two documents, the Commercial Wiring Map
wins — always.

---

## 3. التوصية — The Recommendation

يُوصى بأن يقوم المؤسس بـ:
The founder is recommended to:

1. وضع علامة "مُستبدَلة — Superseded" في أعلى
   [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)،
   مع إشارة إلى خريطة الربط التجاري كالمرجع الحالي.
   Mark [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
   as "Superseded" at the top, pointing to the Commercial Wiring Map as the
   current reference.
2. إبقاء `OFFER_LADDER_AND_PRICING.md` للسياق التاريخي فقط — لا يُستشهد به
   في أي أصل موجَّه للعميل.
   Keep `OFFER_LADDER_AND_PRICING.md` for historical context only — it is
   not cited in any customer-facing asset.

> ملاحظة: هذه المذكرة **لا تعدّل** `OFFER_LADDER_AND_PRICING.md` نفسه.
> وضع علامة الاستبد: قرار يخص المؤسس.
>
> Note: this memo does **not** edit `OFFER_LADDER_AND_PRICING.md` itself.
> Applying the superseded marker is a founder decision.

---

## 4. القاعدة العملية — The Operating Rule

- كل أصل بيعي أو موجَّه للعميل يستشهد بـ
  [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) للسعر.
  Every sales or customer-facing asset cites
  [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) for price.
- العرض الأول المدفوع هو `revenue_proof_sprint_499` — لا تُذكر أسعار
  مختلفة لنفس العرض.
  The canonical first-paid offer is `revenue_proof_sprint_499` — no
  divergent prices for the same offer.
- لا تُخترع أسعار. إذا لم يكن السعر في خريطة الربط التجاري، فهو غير موجود.
  Do not invent prices. If a price is not in the Commercial Wiring Map, it
  does not exist.

---

## 5. أصول مرتبطة — Related Assets

- السردية الرسمية — [`docs/sales-kit/NARRATIVE_VCURRENT.md`](./NARRATIVE_VCURRENT.md)
- خريطة الربط التجاري — [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md)
- سلم العروض (مُستبدَل — للسياق) — [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
