# Dealix — Official Commercial Launch OS
# نظام التشغيل التجاري الرسمي لـ Dealix

> **Golden rule / القاعدة الذهبية:**
> AI recommends and drafts. Deterministic workflows verify. Founder approves. Nothing is sent automatically.
> الذكاء الاصطناعي يقترح ويصيغ. مسارات حتمية تتحقق. المؤسس يعتمد. لا شيء يُرسل تلقائيًا.

This system is **Draft Generation + Founder Review + Safety Gates + Commercial
Readiness only.** It does **not** send external messages — no SMTP, no WhatsApp
sending, no LinkedIn automation, no website auto-submit.

هذا النظام **توليد مسودات + مراجعة المؤسس + بوابات أمان + جاهزية تجارية فقط.**
لا يرسل أي رسائل خارجية — لا بريد عبر مخدم، لا واتساب، لا أتمتة لينكدإن، لا إرسال
تلقائي للنماذج.

---

## What Dealix is / ما هو Dealix

Dealix is a **Saudi/GCC B2B AI Revenue & Operations OS.** It is:

- **NOT** a CRM.
- **NOT** a chatbot.
- **NOT** a generic agency.
- **NOT** a mass outreach tool.

Dealix appears as a **commercial and operational operating system** for companies:

1. Discovers B2B opportunities.
2. Classifies companies by sector, pain, and buyer.
3. Generates high-quality drafts.
4. Passes them through a Quality Gate and a Compliance Gate.
5. Places them in a Founder Review Queue.
6. The founder alone decides and sends manually.
7. Any sensitive external action requires human approval.

Dealix نظام تشغيل تجاري وتشغيلي للشركات: يكتشف الفرص، يصنّف الشركات، يولّد مسودات،
يمرّرها على بوابات الجودة والامتثال، يضعها في طابور مراجعة المؤسس، والمؤسس وحده يقرر
ويرسل يدويًا.

---

## The pipeline / المسار

```
Leads (public, consented)
   │
   ▼
Draft generation (>=400/day, review-only)
   │
   ▼
Quality Gate  ──►  Compliance Gate  ──►  Safety Gate
   │
   ▼
Founder Review Queue  ──►  Founder decision  ──►  Manual copy/send
```

No step in this repository sends anything. The "Manual copy/send" box happens
**outside** this repository, by a human, after founder approval, and only after
the external go-live requirements (`21_EXTERNAL_GO_LIVE_REQUIREMENTS.md`) are met.

---

## First 5 official verticals / أول 5 قطاعات رسمية

1. Facilities Management & Maintenance — إدارة المرافق والصيانة
2. Contracting & Project Controls — المقاولات وضبط المشاريع
3. Real Estate & Property Operations — العقار وإدارة الأملاك
4. Legal & Professional Services — المكاتب القانونية والخدمات المهنية
5. Consulting, Training & B2B Services — الاستشارات والتدريب وخدمات B2B

Each vertical has a full playbook under `verticals/`.

---

## How to run / كيفية التشغيل

```bash
python scripts/commercial_generate_400_drafts.py --target 400
python scripts/commercial_safety_audit.py
python scripts/commercial_launch_readiness.py
python scripts/commercial_metrics_summary.py
```

Outputs land in `outputs/commercial_launch/YYYY-MM-DD/` for founder review.

---

## Document map / خريطة الوثائق

| File | Purpose |
|------|---------|
| `00_OFFICIAL_COMMERCIAL_LAUNCH_OS.md` | This overview |
| `01_FIRST_5_VERTICALS_STRATEGY.md` | First-wave vertical strategy |
| `02_OFFER_LADDER_SAR.md` | Offer ladder in SAR |
| `03_PRICING_AND_PACKAGING.md` | Pricing and packaging |
| `04_COMMERCIAL_POSITIONING_AR_EN.md` | Positioning (AR/EN) |
| `05_SALES_NARRATIVE.md` | Sales narrative |
| `06_CHANNEL_POLICY.md` | Channel policy (draft-only) |
| `07_COMPLIANCE_AND_SAFETY_GATES.md` | Compliance + safety gates |
| `08_FOUNDER_DAILY_REVIEW_PLAYBOOK.md` | Founder daily review |
| `09_DAILY_EXECUTION_RHYTHM.md` | Daily execution rhythm |
| `10_SALES_MESSAGING_AR_EN.md` | Sales messaging (AR/EN) |
| `11_OBJECTION_HANDLING.md` | Objection handling |
| `12_DISCOVERY_CALL_SCRIPT.md` | Discovery call script |
| `13_PROPOSAL_TEMPLATE_AR_EN.md` | Proposal template |
| `14_ONE_PAGE_OFFER_AR_EN.md` | One-page offer |
| `15_DELIVERY_OPERATING_SYSTEM.md` | Delivery OS |
| `16_CLIENT_ONBOARDING.md` | Client onboarding |
| `17_PILOT_DELIVERY_CHECKLIST.md` | Pilot delivery checklist |
| `18_HANDOVER_AND_SUCCESS_REPORT.md` | Handover + success report |
| `19_RETENTION_AND_EXPANSION.md` | Retention + expansion |
| `20_COMMERCIAL_METRICS_DASHBOARD.md` | Metrics dashboard |
| `21_EXTERNAL_GO_LIVE_REQUIREMENTS.md` | External go-live (out of repo) |
| `99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md` | Final readiness + Go/No-Go |
