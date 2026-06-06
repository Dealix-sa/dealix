# Dealix — Module Status Map / خريطة حالة الوحدات

**Status:** canonical · **Owner:** Founder · **Updated:** 2026-06-06
**Grounded in:** [`../SERVICE_TRUTH_REPORT.md`](../SERVICE_TRUTH_REPORT.md)
(Wave 7.5 audit) and [`../registry/SERVICE_READINESS_MATRIX.yaml`](../registry/SERVICE_READINESS_MATRIX.yaml)

> **Controlled vocabulary (the only allowed statuses):**
> `LIVE`, `PRODUCTION_READY`, `DEMO_FALLBACK`, `BETA`, `PLANNED`, `ROADMAP`,
> `DEPRECATED`.
>
> **Hard rule:** a `PLANNED` / `ROADMAP` / `DEMO_FALLBACK` module is **never**
> presented as LIVE on a customer-facing surface. الوحدة المستقبلية لا تظهر
> أبداً كأنها LIVE.

`DEMO_FALLBACK` = the code path works end-to-end but degrades to an honest
demo until an external credential is supplied (the customer is told).

---

## Core modules

| Module | Status | Customer value (AR) | Activation requirement |
|---|---|---|---|
| Lead Intake (WhatsApp) | PRODUCTION_READY | يستقبل رسائل واتساب ويصنّفها ويجهّز ردّاً للموافقة | Meta Business creds (`WHATSAPP_ACCESS_TOKEN`); DEMO_FALLBACK without |
| Qualification (BANT / MEDDPICC) | PRODUCTION_READY | يحلّل الـ leads ويعطي درجة + تفسير عربي | already live |
| Routing (sector → offer) | PRODUCTION_READY | يوجّه الفرصة للعرض المناسب | already live |
| Data OS (DQ score + dedupe) | PRODUCTION_READY | ينظّف البيانات ويحسب جودتها على 6 أبعاد | signed Source Passport |
| Governance OS (approval + redaction) | PRODUCTION_READY | يحجب ويعتمد المخرجات قبل أي إرسال | already live |
| Proof OS (Proof Pack assembly) | PRODUCTION_READY | يجمع حزمة إثبات ثنائية اللغة مع توقيع | already live |
| Enrichment (Hunter / Apollo / Clearbit) | DEMO_FALLBACK | يُثري بيانات الشركات من مصادر مرخّصة | `HUNTER_API_KEY` + `DEALIX_ENRICHMENT_LIVE_CALLS=true` |
| Outbound Send (WhatsApp business) | DEMO_FALLBACK | يرسل ردوداً معتمدة (بموافقة) عبر واتساب الأعمال | Meta WhatsApp Business approval |

---

## Platform / OS layers

| Module | Status | Customer value (AR) | Activation requirement |
|---|---|---|---|
| Value OS (tier mapping) | PRODUCTION_READY | يربط الـ Proof بقيمة قابلة للقياس | already live |
| Capital OS (asset registration) | PRODUCTION_READY | يسجّل أصول البيانات كأصول رأسمالية | already live |
| Adoption OS | BETA | يقيس تبنّي العميل للنظام | internal beta |
| Client OS (workspace) | PRODUCTION_READY | مساحة عمل معزولة لكل عميل | per-tenant provisioning |
| Self-Growth OS | PLANNED | حلقة نمو داخلية محكومة (مسودات فقط) | see `../06_growth/SELF_GROWTH_OS.md` |
| Autonomous external send | ROADMAP | — (مرفوض حالياً بالتصميم) | never auto; requires future governance review |

---

## Honesty summary

- **PRODUCTION_READY / LIVE today:** 10 modules above.
- **DEMO_FALLBACK (honest, credential-pending):** Enrichment, Outbound Send.
- **PLANNED / ROADMAP (not sold as live):** Self-Growth OS, Autonomous send.

This map is enforced by `scripts/verify_dealix_module_status.py`.
