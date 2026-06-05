# Dealix — Commercial Source of Truth — مصدر الحقيقة التجاري
<!-- Owner: Founder | Effective: 2026-06-05 | العربية أولاً -->

> **القاعدة الأولى:** هذا الملف يعلن المستندَين القانونيين (canonical) للتجارة في Dealix.
> أي ملف آخر يخالفهما يُعتبر **مهجوراً (DEPRECATED)** حتى تتم مطابقته — لا يُوثَق به.

---

## 1. المستندات القانونية — Canonical Sources (AR)

| المجال | المستند القانوني | لا تُصدّق غيره |
|--------|------------------|----------------|
| الأسعار وسلم الخدمات | [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) | نعم |
| الموقع التنافسي وICP | [`POSITIONING_AND_ICP.md`](POSITIONING_AND_ICP.md) | نعم |
| فاصل تعارض الأسعار | [`PRICE_AUTHORITY.md`](PRICE_AUTHORITY.md) | نعم |
| ما يُسمح/يُمنع قوله | [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) | نعم |

أي سلسلة سعر أو ادعاء في ملف آخر **يخالف** ما سبق = مهجور حتى المطابقة، لا يُبنى عليه قرار.

## 1. Canonical Sources (EN)

| Domain | Canonical document | Trust no other |
|--------|--------------------|----------------|
| Pricing & offer ladder | [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) | Yes |
| Positioning & ICP | [`POSITIONING_AND_ICP.md`](POSITIONING_AND_ICP.md) | Yes |
| Price-conflict tie-breaker | [`PRICE_AUTHORITY.md`](PRICE_AUTHORITY.md) | Yes |
| Allowed/forbidden claims | [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) | Yes |

Any price string or claim elsewhere that contradicts the above is **DEPRECATED until reconciled** — never trusted.

---

## 2. سلم الأسعار القانوني — Canonical Price Ladder (mirror, لا تعديل)

| # | الخدمة | السعر | شرط الفتح |
|---|--------|-------|-----------|
| 0 | Free AI Ops Diagnostic | مجاني | متاح الآن |
| 1 | 7-Day Revenue Proof Sprint | **499 SAR** | Pilot Gate — سعر تأسيسي لاكتساب الإثبات، أول 3–5 عملاء فقط |
| 2 | Data-to-Revenue Pack | **1,500 SAR** | بعد Sprint |
| 3 | Managed Revenue Ops | **2,999–4,999 SAR/شهر** | بعد pilot |
| 4 | Executive Command Center | **7,500–15,000 SAR/شهر** | بعد 3 pilots + 1 case study |
| 5 | Agency Partner OS | مخصص + **rev-share 15–30%** | بعد 3 proof packs |

> **499 SAR هو آلية اكتساب إثبات (proof-acquisition)، وليس نموذج عمل طويل الأمد.**
> بعد الإثبات قد ترتفع درجة الدخول إلى **3,000–5,000 SAR**.

---

## 3. أولوية ICP — ICP Priority

| الأولوية | الفئة | EN |
|----------|------|----|
| **#1** | وكالات B2B / استشارات / تدريب | B2B agencies / consulting / training |
| **#2** | شركات الخدمات المهنية B2B | B2B professional-services firms |
| **مؤجَّل** | العقار — لا يُجعل أساسياً (يجرّ نحو B2C / cold WhatsApp) | Real estate — DEFERRED, not core |

---

## 4. جملة الموقع — Positioning Sentence (الوحيدة المعتمدة)

> **Dealix = Revenue Operating System for Saudi B2B teams.**
> لا يُباع كـ CRM، ولا chatbot، ولا أداة أتمتة، ولا وكالة تسويق، ولا dashboard،
> ولا "AI يضمن المبيعات".

---

## 5. ضبط التغيير — Change Control (how to change pricing)

أي تغيير سعر يتطلّب تعديل **ملفين معاً** في نفس commit:
1. [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) — المصدر القانوني.
2. هذا الملف + [`PRICE_AUTHORITY.md`](PRICE_AUTHORITY.md) — لتطابق الفاصل.

لا يُعتمد تغيير سعر إن لم تُحدَّث الملفات الثلاثة بنفس الرقم وتاريخ السريان. المالك: المؤسس.

Any price change requires editing **both** the canonical ladder and this file (plus `PRICE_AUTHORITY.md`) in the **same commit**, with matching numbers and effective date. Owner: Founder.

---

روابط: [`PRICE_AUTHORITY.md`](PRICE_AUTHORITY.md) · [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) · [`LAUNCH_GO_NO_GO.md`](LAUNCH_GO_NO_GO.md) · [`MASTER_LAUNCH_ROOM.md`](MASTER_LAUNCH_ROOM.md)

*No guaranteed claims · Missing data = insufficient_data · القيمة التقديرية ليست قيمة مُتحقَّقة.*
