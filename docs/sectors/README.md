# Sector Intelligence OS — Index — فهرس ذكاء القطاعات

**Parent / المرجع الأعلى:** [Market Production OS](../market_production_os/README.md)

هذه مجموعة بريفات **داخلية** للذهاب-إلى-السوق (GTM). كل ملف يجيب على سؤالين فقط:
**أي عرض Dealix يناسب هذا القطاع؟** و**كيف نخاطبه؟** — لا تُعرض هذه الوثائق على العميل كما هي.

These are **internal** go-to-market briefs. Each file answers two questions only:
**which Dealix offer fits this sector?** and **how do we talk to it?** — not customer-facing as-is.

## المرجع الثابت / Source of truth

الأسعار والنطاق مصدرها الوحيد: [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md).
أي رقم هنا هو إحالة لذلك الملف، وكل الأسعار **نطاقات حواجز معتمدة من المؤسس — لا تُفعَّل تلقائياً**.

Pricing and scope come only from [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md).
All prices are **founder-approved guardrail ranges — never auto-charged**.

## القطاعات العشرة / The ten sectors

| # | القطاع / Sector | أول عرض مناسب / First-fit offer | السعر المعتمد / Price | الملف / File |
|---|-----------------|---------------------------------|-----------------------|--------------|
| 1 | وكالات التسويق / Marketing agencies | Lead Intelligence Sprint | 9,500 | [MARKETING_AGENCIES_AR.md](MARKETING_AGENCIES_AR.md) |
| 2 | شركات التدريب / Training companies | Lead Intelligence Sprint | 9,500 | [TRAINING_COMPANIES_AR.md](TRAINING_COMPANIES_AR.md) |
| 3 | العيادات / Clinics | Revenue Diagnostic | 3,500 | [CLINICS_AR.md](CLINICS_AR.md) |
| 4 | فرق العقار / Real estate teams | Lead Intelligence Sprint | 9,500 | [REAL_ESTATE_TEAMS_AR.md](REAL_ESTATE_TEAMS_AR.md) |
| 5 | وكالات التوظيف / Recruitment agencies | Lead Intelligence Sprint | 9,500 | [RECRUITMENT_AGENCIES_AR.md](RECRUITMENT_AGENCIES_AR.md) |
| 6 | الخدمات المهنية / Professional services | Revenue Diagnostic | 3,500 | [PROFESSIONAL_SERVICES_AR.md](PROFESSIONAL_SERVICES_AR.md) |
| 7 | مجموعات المطاعم / Restaurant groups | Revenue Diagnostic | 3,500 | [RESTAURANT_GROUPS_AR.md](RESTAURANT_GROUPS_AR.md) |
| 8 | مزوّدو التعليم / Education providers | Lead Intelligence Sprint | 9,500 | [EDUCATION_PROVIDERS_AR.md](EDUCATION_PROVIDERS_AR.md) |
| 9 | شركات اللوجستيات / Logistics companies | Pilot Conversion Sprint | 22,000 | [LOGISTICS_COMPANIES_AR.md](LOGISTICS_COMPANIES_AR.md) |
| 10 | SaaS محلي / Local SaaS | Lead Intelligence Sprint | 9,500 | [LOCAL_SAAS_AR.md](LOCAL_SAAS_AR.md) |

## ملاحظة التسجيل / Scoring note

استخدم هذه القاعدة لترتيب أي قطاع أو حساب قبل اللمسة الأولى (0–100):

Use this rule to score any sector or account before first touch (0–100):

```
score = pain_fit*0.35 + budget_fit*0.25 + data_readiness*0.20 + channel_ok*0.10 + warm_signal*0.10
```

- **pain_fit** — هل الألم التشغيلي (متابعة ضائعة، تقارير مبعثرة، تسرّب فرص) واضح ومتكرر؟
- **budget_fit** — هل القطاع يحتمل العرض الافتراضي (Sprint 9,500) أو يبدأ بـ Diagnostic (3,500)؟
- **data_readiness** — هل لديهم CSV/CRM export قابل للرفع؟ بلا بيانات لا يوجد Sprint.
- **channel_ok** — يقبل **موافقة بشرية على الرسائل** (لا cold blast، لا واتساب بارد، لا أتمتة LinkedIn).
- **warm_signal** — مقدمة شخصية أو inbound أو إشارة شراء حديثة.

**القراءة:** ≥ 70 لمسة هذا الأسبوع · 50–69 مسودة فقط · < 50 لا تُلامس الآن.
القناة الأساسية للاكتساب = **البريد البارد**؛ واتساب **بعد الرد/الموافقة فقط**؛ LinkedIn **يدوي فقط**.
تفاصيل حدود القناة: [WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).

**Reading:** ≥ 70 touch this week · 50–69 draft only · < 50 do not touch yet.
Primary acquisition channel = **cold email**; WhatsApp is **post-reply/opt-in only**; LinkedIn is **manual only**.

## روابط مرجعية / Related docs

- [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) — الأسعار والنطاق
- [OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md](../commercial/OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md) — العرض الافتراضي
- [GTM_OBJECTION_MATRIX_AR.md](../commercial/operations/GTM_OBJECTION_MATRIX_AR.md) — مصفوفة الاعتراضات الحية
- [SAUDI_SECTOR_TAXONOMY.md](../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md) — تصنيف القطاعات
- [WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md) — حدود القناة

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
