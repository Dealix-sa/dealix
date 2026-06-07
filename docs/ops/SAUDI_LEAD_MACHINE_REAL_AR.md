# مكينة الليدز السعودية — الطبقة الحقيقية / Saudi Lead Machine — Real Layer

_آخر تحديث: 2026-06-07_

هذه الطبقة تحوّل "مكينة الليدز" من قالب فارغ (`REPLACE:` placeholders) إلى **نظام
حقيقي يعمل يومياً**: عالم حسابات مستهدفة سعودي حقيقي ومُصدَّر، مُقيَّم بـ ICP، يُنتج
**مسودات تواصل دافئ يومية تتطلب موافقتك** قبل أي إرسال.

> This turns the lead machine from an empty template into a **real, daily-operating
> system**: a real, sourced Saudi B2B target universe, ICP-scored, producing
> **daily approval-gated warm-outreach drafts**.

---

## ما الذي يحترم الدستور هنا / Why this is doctrine-safe

| القاعدة (Non-negotiable) | كيف نلتزم بها |
|---|---|
| #1 لا scraping | بحث عام يدوي عن **معلومات شركات منشورة** فقط — لا استخراج آلي. |
| #4 لا ادعاءات بلا مصدر | كل حساب يحمل `source_url` عام حقيقي — يرفض المحرّك أي صف بلا مصدر. |
| #6 لا PII في السجلّات | عمود `contact` فارغ دائماً — لا أسماء/هواتف/إيميلات شخصية. الاسم يُعبّأ عند المقدمة الدافئة. |
| #7 لا معرفة بلا مصدر | الـ`why_now` و`pain_hypothesis` فرضيات مُعلّمة، والمصدر مرفق. |
| #8 لا إجراء خارجي بلا موافقة | كل مسودة `approval_required` — لا إرسال آلي إطلاقاً. |

**لماذا لا نضع أرقام جوال جاهزة؟** لأن أكبر أصل لدى Dealix هو الثقة (PDPL أصلاً،
الموافقة أولاً). تلفيق بيانات شخصية أو شرائها يدمّر هذا الأصل ويخالف الدستور. الطريق
الحقيقي = مقدمة دافئة + موافقتك، وهو ما يبنيه هذا النظام.

---

## المكوّنات / Components

| الملف | الدور |
|---|---|
| `docs/commercial/operations/targeting/saudi_b2b_target_universe.csv` | عالم الحسابات الحقيقي المُصدَّر (24+ حساب، قابل للتوسيع). |
| `scripts/dealix_target_universe.py` | تحميل + بوابات دستورية + تقييم ICP + اختيار اليوم. |
| `scripts/dealix_daily_draft_pack.py` | يُنتج مسودات اليوم (واتساب + بريد، عربي/إنجليزي) — كلها بموافقة. |
| `tests/test_target_universe.py` | حُرّاس: يرفضون أي صف بلا مصدر / بـPII / بقناة باردة / مسودة بلا موافقة. |

---

## التشغيل اليومي / Daily run (90 ثانية)

```bash
# 1) شوف حسابات اليوم (الأعلى قيمة أولاً)
python3 scripts/dealix_target_universe.py --top 10

# 2) ولّد حزمة المسودات (تُكتب في data/outreach/drafts/YYYY-MM-DD/)
python3 scripts/dealix_daily_draft_pack.py --top 10

# 3) افتح الخطة
#   data/outreach/drafts/<اليوم>/INDEX.md
```

خيارات: `--rotate` لتدوير الحسابات يومياً على كامل العالم · `--date YYYY-MM-DD` ·
`--founder "اسمك"` (أو `DEALIX_FOUNDER_NAME`).

ثم لكل حساب: **(1)** احصل على مقدمة دافئة/أساس قانوني، **(2)** عبّئ الاسم الحقيقي،
**(3)** راجع وأرسل **يدوياً بنفسك**، **(4)** سجّل النتيجة.

---

## كيف تكبر المكينة / How it grows — most important

1. **أضف شبكتك الدافئة في القمة:** عبّئ صفوفاً جديدة في الـCSV (شركات من شبكتك/CRM).
   اترك `contact` فارغاً، ضع `source_type=warm_intro` و`source_url` (مثلاً ملف CRM أو
   مقدمة). هذه الصفوف ستتصدّر التقييم لأنها الأعلى قابلية للإغلاق.
2. **حدّث `status`** أثناء العمل (`message_drafted` → `sent_manual` → `replied` →
   `meeting_booked`) لتغذية War Room.
3. **الـinbound** من الموقع (`/dealix-diagnostic`, `/risk-score`) يدخل نفس خط
   التقييم عبر `POST /api/v1/leads`.

---

_القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value_
