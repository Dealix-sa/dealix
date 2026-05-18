# Dealix — Appendix فني (للتقنية والامتثال)

**يُرفق مع:** Leave-behind أو غرفة المبيعات الرقمية — **ليس للعرض المباشر** إلا عند طلب IT/Legal.

---

## A1 — معمارية عالية المستوى

**عنوان:** البيانات تمر عبر Source Passport قبل أي scoring أو مسودة

- مصادر مسموحة فقط (`source_registry`) — لا scraping إنتاجي
- Postgres + event-sourced Revenue Memory
- وكلاء AI خلف بوابة موافقة (Safe Agent Runtime)

---

## A2 — Decision Passport

**عنوان:** كل إجراء خارجي يحتاج جواز قرار بمالك وموعد وهدف إثبات

| الحقل | الغرض |
|-------|--------|
| owner | مسؤول بشري |
| deadline | موعد القرار |
| proof_target | مستوى دليل L0–L5 |
| evidence | مراجع قابلة للتدقيق |

API مرجع: `GET /api/v1/decision-passport/golden-chain`

---

## A3 — Anti-Waste

**عنوان:** لا upsell بدون proof ولا تسويق عام تحت L4

- `POST /api/v1/revenue-os/anti-waste/check`
- قواعد deterministic قبل أي إرسال

---

## A4 — PDPL والاتصال

**عنوان:** المعالجة تتطلب أساساً نظامياً — البارد غير مدعوم في المنتج

- موافقة مسجّلة للقنوات الحساسة
- مسودات WhatsApp/Email تنتظر موافقة صريحة
- سياسة خصوصية: [`../../sales-kit/dealix_privacy_policy_ar.md`](../../sales-kit/dealix_privacy_policy_ar.md)

---

## A5 — الأمان والتشغيل

**عنوان:** بيئة production معزولة عن التجارب — أسرار خارج المستودع

- تشفير في النقل (TLS)
- تدقيق إجراءات AI
- FAQ أمني: [`../../sales-kit/dealix_security_faq.md`](../../sales-kit/dealix_security_faq.md)

---

## A6 — التكاملات

**عنوان:** التكاملات عبر واجهات — لا credentials في الكود

| التكامل | الحالة الافتراضية |
|---------|-------------------|
| HubSpot CRM | اختياري |
| Gmail | مسودة + موافقة |
| WhatsApp | payload فقط — لا إرسال بارد |
| Moyasar | دفع عند التفعيل |

---

## A7 — SLA ومخرجات Sprint

**عنوان:** Sprint ٧ أيام له معايير قبول مكتوبة في SOW

- ١٠ حسابات مُرتّبة (أو حسب العقد)
- Draft Pack ثنائي اللغة
- Proof Pack ١٤ قسماً
- أصل واحد على الأقل في Capital Ledger

---

## A8 — أسئلة IT الشائعة

1. **أين تُخزَّن البيانات؟** — حسب نشر العميل (SaaS / dedicated — يُحدد في العقد).
2. **هل تدربون على بيانات العميل لنماذج عامة؟** — لا بدون اتفاق كتابي.
3. **من يملك المخرجات؟** — العميل؛ Dealix تحتفظ بمنهجية وأصول مجهّزة.

---

**مرجع API:** [`../../../AGENTS.md`](../../../AGENTS.md) — Revenue OS catalog
