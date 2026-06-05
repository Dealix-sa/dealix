<!-- Wave 6 | Owner: Founder | Arabic-first -->

# First 30 Targets Playbook — دليل أول 30 شركة مستهدفة

**Purpose / الغرض:** تحويل الاستهداف من ملف إلى نظام: بحث → تأهيل → تسجيل نقاط → قرار تواصل.

**Data / البيانات:** `data/growth/first_30_targets.csv` (header-only — تُملأ يدويًا).
**Review / المراجعة:** `reports/growth/first_30_targets_review.md` (أسبوعيًا).

---

## Target sectors / القطاعات المستهدفة
- B2B marketing agencies / وكالات تسويق B2B
- Consulting firms / شركات استشارات
- Training companies / شركات تدريب
- IT service providers / مزودو خدمات تقنية
- Business services companies / شركات خدمات أعمال

## Columns / الأعمدة
`company_name, website, city, sector, why_target, pain_hypothesis, evidence_url,
recommended_angle, recommended_offer, outreach_status, next_action, owner, notes`

---

## Rules / القواعد
- **every target needs `evidence_url` or a warm_intro_reason** — لا استهداف بدون دليل.
- no scraping behind login / لا scraping خلف تسجيل دخول.
- no personal phone numbers / لا أرقام شخصية.
- no cold WhatsApp automation / لا أتمتة واتساب باردة.
- no mass email / لا بريد جماعي.
- **manual review before outreach** — مراجعة يدوية قبل أي تواصل.

---

## Scoring (100 points) / التسجيل

| المعيار / Criterion | النقاط |
|---------------------|--------|
| ICP fit | 25 |
| واضح عندهم خدمات B2B / clear B2B services | 15 |
| proof gap محتمل / likely proof gap | 15 |
| follow-up / offer complexity | 15 |
| contact path واضح / clear contact path | 10 |
| founder access / warm path | 10 |
| evidence quality | 10 |

## Decision bands / قرار الاستهداف
- **80–100** → Send manual message this week / أرسل رسالة يدوية هذا الأسبوع.
- **65–79** → Research more / ابحث أكثر.
- **50–64** → Nurture / متابعة.
- **<50** → Reject / استبعاد.

> القرار يُسجّل في عمود `outreach_status` ويُمرّر للموافقة عبر
> `reports/revenue/outreach_approval_queue.md` قبل أي إرسال.
