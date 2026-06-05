<div align="center" dir="rtl">

# 🏢 Dealix — نظام تشغيل الأعمال بالذكاء الاصطناعي

### نظام تشغيل أعمال AI-native للشركات السعودية والخليجية — يبدأ من الإيرادات والقرار والإثبات، ثم يتوسّع عبر الشركة.

[![CI](https://github.com/VoXc2/dealix/actions/workflows/ci.yml/badge.svg)](https://github.com/VoXc2/dealix/actions/workflows/ci.yml)
[![الرخصة: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**العربية** · **[English](README.md)**

</div>

---

<div dir="rtl">

## 🌟 ما هو Dealix؟

**Dealix نظام تشغيل أعمال بالذكاء الاصطناعي للشركات السعودية والخليجية.**

يحوّل الشركة من واتساب، Excel، ملفات، اجتماعات، عروض، وقرارات مشتتة إلى **نظام
تشغيل واحد** يعرف:

- ماذا يحدث؟
- ماذا يجب أن يحدث؟
- من يوافق؟
- ما الدليل؟
- وما القرار القادم؟

الإيرادات **ليست** الهوية — هي أول **wedge تجاري** ندخل به الشركة. المنصة الكاملة
أربعة عشر نظام تشغيل:

```
Dealix Business OS
├─ Command OS    ├─ Revenue OS   ├─ Client OS    ├─ Delivery OS
├─ Support OS    ├─ Finance OS   ├─ Data OS      ├─ Governance OS
├─ Proof OS      ├─ Knowledge OS ├─ Agent OS     ├─ Partner OS
├─ Academy OS    └─ Venture OS
```

## 🚪 الدخول للسوق — Dealix Command Sprint

| العنصر | القيمة |
| --- | --- |
| الاسم | **Dealix Command Sprint** |
| المدة | 7 أيام |
| السعر التأسيسي | 499 – 1,500 ريال |
| الهدف | إثبات أول operating loop داخل شركة العميل |
| التسليم | خدمة بقيادة المؤسس (وليست SaaS ذاتية) |

**المخرج — Dealix Command Pack:** Revenue Map · Next Action Board · Follow-up
Drafts · Offer Upgrade · Objection Intelligence · Proof Register · Approval
Register · Executive Command Brief.

ثم نتوسّع من داخل العميل إلى: Client + Delivery + Support + Finance + Data +
Governance.

## 🧭 القاعدة التشغيلية

> الذكاء الاصطناعي يستكشف ويحلّل ويوصي. الـ workflows الحتمية تنفّذ. والبشر يوافقون
> على الالتزامات الخارجية الحرجة.

لا إرسال تلقائي · لا scraping · لا overclaim · موافقة بشرية لأي إجراء خارجي يواجه
العميل.

## 🛡️ التموضع والثقة

- **PDPL-aware** — أقل بيانات، شفافية الاحتفاظ والحذف والنسخ وآلية الشكاوى.
- **ZATCA-aware** — وعي بالفوترة الإلكترونية (استشاري، ولسنا مزوّد فوترة مؤهّل).
- **NCA-aligned controls** — ضوابط متوائمة، ولا ندّعي "certified" إلا باعتماد فعلي.

لا نقول: "نحن CRM" أو "chatbot" أو "وكالة" أو "أتمتة واتساب". نقول: **نظام تشغيل
أعمال AI-native**.

## 📚 مصدر الحقيقة للمنصة

| الوثيقة | الغرض |
| --- | --- |
| [`docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md`](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md) | ما هو Dealix (مرجعي) |
| [`docs/00_platform_truth/DEALIX_BUSINESS_OS_ARCHITECTURE.md`](docs/00_platform_truth/DEALIX_BUSINESS_OS_ARCHITECTURE.md) | كيف تتكامل الأنظمة |
| [`docs/00_platform_truth/PRODUCT_FAMILY_MAP.md`](docs/00_platform_truth/PRODUCT_FAMILY_MAP.md) | سلم العروض |
| [`docs/00_platform_truth/MODULE_STATUS_MAP.md`](docs/00_platform_truth/MODULE_STATUS_MAP.md) | الحالة الصادقة لكل module |
| [`docs/00_platform_truth/PUBLIC_POSITIONING.md`](docs/00_platform_truth/PUBLIC_POSITIONING.md) | ماذا نقول وماذا لا نقول |
| [`docs/01_go_to_market/COMMAND_SPRINT_OFFER.md`](docs/01_go_to_market/COMMAND_SPRINT_OFFER.md) | أول منتج مدفوع |
| [`docs/03_governance/HUMAN_APPROVAL_POLICY.md`](docs/03_governance/HUMAN_APPROVAL_POLICY.md) | عقيدة الموافقة أولاً |
| [`docs/05_founder/FOUNDER_DAILY_COMMAND.md`](docs/05_founder/FOUNDER_DAILY_COMMAND.md) | الإيقاع اليومي للمؤسس |

## 🚀 البدء السريع

```bash
git clone https://github.com/VoXc2/dealix.git
cd dealix
make setup
cp .env.example .env
# عدّل .env ثم:
make run
# توثيق الـ API: http://localhost:8000/docs
```

التحقق من جاهزية الإنتاج:

```bash
make env-check
python scripts/security_smoke.py
python -c "import api.main; print('api import OK')"
make prod-verify
```

> ⚠️ **لا ترفع `.env` أبداً.** المشروع يحميك بـ `.gitignore` و pre-commit عبر
> gitleaks + detect-secrets.

## 🗺️ خطة 12 شهر (ملخص)

| المرحلة | الهدف |
| --- | --- |
| أول 7 أيام | إعادة التموضع + البوابات الصارمة |
| 30 يوم | أول 3 Command Sprints |
| 60 يوم | أول MRR + أول case study |
| 90 يوم | إطلاق محدود (بشروط صارمة) |
| 180 يوم | توسّع Business OS |
| 365 يوم | شركة منصّة |

التفاصيل: [`docs/05_founder/BUSINESS_METRICS.md`](docs/05_founder/BUSINESS_METRICS.md).

## 📜 الرخصة

MIT — راجع [LICENSE](LICENSE).

</div>

---

<div align="center" dir="rtl">

**[📖 التوثيق](docs/)** · **[🇸🇦 مصدر الحقيقة](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md)** · **[🚪 Command Sprint](docs/01_go_to_market/COMMAND_SPRINT_OFFER.md)**

</div>
