# تقرير الإنتاج اليومي للمسودات — Daily Draft Production

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المصدر:** docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md
**يُولَّد بواسطة:** scripts/verify_market_production_os.py
**التاريخ:** {{ date }}

> قالب — الصفوف أدناه عناصر نائبة تُملأ آلياً. 250 مسودة/يوم هدف إنتاج، لا هدف إرسال.

## العدّ حسب النوع

| النوع | الهدف | المُنتَج | اجتاز الجودة | معتمَد |
|-------|------|---------|--------------|--------|
| first-touch | 100 | {{ ft_produced }} | {{ ft_passed }} | {{ ft_approved }} |
| follow-up-1 | 75 | {{ f1_produced }} | {{ f1_passed }} | {{ f1_approved }} |
| follow-up-2 | 50 | {{ f2_produced }} | {{ f2_passed }} | {{ f2_approved }} |
| proposal-intro | 15 | {{ pi_produced }} | {{ pi_passed }} | {{ pi_approved }} |
| breakup | 10 | {{ bu_produced }} | {{ bu_passed }} | {{ bu_approved }} |
| **الإجمالي** | **250** | {{ total_produced }} | {{ total_passed }} | {{ total_approved }} |

## فحوص الجودة (أسباب الحجب)

| سبب الحجب | العدد |
|-----------|------|
| تخصيص دون P1 | {{ blocked_personalization }} |
| risk_level = high | {{ blocked_risk }} |
| انسحاب مفقود | {{ blocked_unsubscribe }} |
| ادّعاء بلا دليل | {{ blocked_evidence }} |
| في قائمة الكبح | {{ blocked_suppressed }} |
| موضوع مضلِّل | {{ blocked_subject }} |

## أفضل القطاعات اليوم

| القطاع | عدد المسودات | متوسط درجة التخصيص |
|--------|--------------|---------------------|
| {{ sector_1 }} | {{ sector_1_count }} | {{ sector_1_pscore }} |
| {{ sector_2 }} | {{ sector_2_count }} | {{ sector_2_pscore }} |

## الخطوة التالية

- رفع أفضل 50 مسودة إلى صف الموافقة: reports/outreach/APPROVAL_QUEUE.md.
- إعادة المسودات المحجوبة إلى المصنع مع سبب الحجب.

## روابط

- مصنع المسودات: docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md
- صف الموافقة: docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
