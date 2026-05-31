# خارطة طريق التقنية 2026 — Dealix
# Technology Roadmap 2026 — Dealix

> **ملاحظة**: هذه الخارطة تشغيلية وتقديرية. الأولويات والمواعيد قابلة للتغيير بناءً على متطلبات العملاء والموارد المتاحة.
> **Note**: This roadmap is operational and aspirational. Priorities and timelines may shift based on customer requirements and available resources.

---

## المبادئ التوجيهية للهندسة | Engineering Principles

1. **حوكمة أولاً | Governance First** — كل ميزة تعبر من بوابة APPROVAL_FIRST قبل الإطلاق
2. **ZATCA/PDPL أصلي | ZATCA/PDPL Native** — الامتثال مُدمَج في البنية، ليس إضافة لاحقة
3. **عربي أولاً | Arabic First** — واجهة المستخدم والاستجابات بالعربية أساسياً
4. **قابلية التدقيق | Auditability** — كل قرار نظام يُسجَّل في سجل الحوكمة مع timestamp
5. **لا خادم واحد يملك البيانات | No Single Point of Data** — كل قرار يعود للمؤسس

---

## الوضع الحالي | Current State (May 2026)

### Backend — FastAPI (Python 3.11)
- 170+ API routers موثقة ومختبرة
- SQLAlchemy 2.0 async ORM مع Alembic migrations
- Moyasar payment webhook integration
- 400+ pytest tests covering core doctrine gates
- Governance logging على كل إجراء خارجي

### Frontend — Next.js 14 (App Router)
- Bilingual routing: `/ar/*` و `/en/*` عبر next-intl
- Tailwind CSS + shadcn/ui component library
- صفحات جاهزة: Dashboard, Sprint, Onboarding, Pricing, Team, Why Dealix
- أدوات عامة: ZATCA Checker, PDPL Checker, Health Dashboard, ROI Calculator

### Infrastructure
- PostgreSQL (async)
- Pydantic v2 validation
- OpenAPI auto-documentation at `/docs`
- Environment: Railway-ready (Dockerfile + railway.toml)

---

## Q3 2026 (يوليو – سبتمبر) | Q3 2026

### P0 — أعمال جوهرية | Core Work (must ship)

| المهمة | Task | القيمة | الجهد المقدر |
|--------|------|--------|--------------|
| نظام Proof Pack PDF الآلي | Automated PDF Proof Pack generator | تحسين تسليم العملاء | 3 أسابيع |
| بوابة عميل MVP | Customer Portal MVP (login, view sprint status, approve actions) | إنتاج العملاء | 4 أسابيع |
| Moyasar checkout pages | Moyasar checkout pages (499/1500 SAR flows) | تفعيل الإيراد | 2 أسبوع |
| ZATCA XML UBL 2.1 validator | ZATCA invoice format validator (server-side) | امتثال العملاء | 2 أسبوع |
| تشفير PII في قاعدة البيانات | PII field-level encryption (PostgreSQL, SQLAlchemy) | PDPL Article 19 | 2 أسبوع |

### P1 — تحسينات مهمة | Important Improvements

| المهمة | Task | القيمة |
|--------|------|--------|
| إشعارات WhatsApp (بموافقة) | WhatsApp notifications (consent-gated) | سرعة الاستجابة |
| تقرير DQ Score آلي | Automated DQ Score report (weekly PDF) | قيمة الخدمة |
| نظام إدارة المهام للـ Sprint | Sprint task management (founder + client view) | تجربة التسليم |
| مزامنة Notion/Airtable | Notion/Airtable data sync (read-only, with approval) | سهولة الإعداد |

---

## Q4 2026 (أكتوبر – ديسمبر) | Q4 2026

### P0 — أعمال جوهرية | Core Work

| المهمة | Task | القيمة |
|--------|------|--------|
| Managed Ops Dashboard كامل | Full Managed Ops client dashboard (health, ZATCA, PDPL) | قيمة الاحتفاظ |
| نظام التجديد الآلي | Automated renewal workflow (90-day calendar) | NRR |
| PDPL DSAR portal | Self-serve PDPL Data Subject Access Request portal | امتثال PDPL |
| نظام التنبيهات الذكية | Smart alert system (health score drops, ZATCA changes) | تجربة المؤسس |
| API Rate limiting + auth audit | API security hardening (rate limiting, key rotation) | أمن المنصة |

### P1 — تحسينات

| المهمة | Task | القيمة |
|--------|------|--------|
| تكامل ZATCA Fatoora API | ZATCA Fatoora API integration (real Phase 2 submission) | مباشرة للعملاء |
| نظام Referral | Referral program (track + reward) | نمو |
| Mobile-responsive portal | Full mobile optimization for customer portal | تجربة مستخدم |
| نموذج التقرير المخصص | Customizable report templates per sector | تخصيص |

---

## 2027 — رؤية بعيدة المدى | 2027 Long-Term Vision

### الأنظمة القادمة | Upcoming Systems

| النظام | System | الوصف |
|--------|--------|-------|
| Custom AI Engine | محرك AI مخصص | نماذج LLM مضبوطة على بيانات كل عميل (مع PDPL) |
| Multi-tenant SaaS | SaaS متعدد المستأجرين | عزل بيانات كامل لكل شركة |
| Partner API | API للشركاء | شركاء محاسبة وقانون يربطون خدماتهم بـ Dealix |
| AI Compliance Engine | محرك امتثال AI | فحص ZATCA/PDPL آلي لكل مخرجات AI |
| Predictive Health Scoring | درجة صحة تنبؤية | نماذج ML لتوقع الإلغاء قبل 30 يوم |

---

## الديون التقنية المعروفة | Known Technical Debt

| العنصر | Priority | الخطة |
|--------|----------|-------|
| jose/pyo3 conflict (local dev) | P2 | ترقية cryptography library أو تبديل jose |
| Pipeline store (in-memory) | P1 | نقل إلى PostgreSQL مع JSONL fallback |
| Frontend: recharts import (بعض المكونات) | P2 | توحيد على lightweight charting library |
| Growth simulation: static data | P2 | ربط بـ PostgreSQL KPI store |
| Test isolation: module-level mocks | P1 | تحويل لـ pytest fixtures |

---

## قرارات الهندسة الثابتة | Fixed Engineering Decisions

هذه القرارات نهائية — لا تُناقَش دون موافقة صريحة من المؤسس:

1. **APPROVAL_FIRST** — أي إجراء خارجي يتطلب موافقة مُسجَّلة. لا يُبرمَج تجاوز هذه القاعدة أبداً.
2. **لا scraping** — المنصة لا تحتوي ولا تدعم أي أداة جمع بيانات غير مصرح بها.
3. **لا cold WhatsApp** — WhatsApp للمستخدمين الذين أعطوا موافقة صريحة فقط.
4. **governance_decision على كل استجابة** — كل endpoint يعيد هذا الحقل، لا استثناء.
5. **PDPL Article 19** — البيانات الشخصية مشفرة في قاعدة البيانات بمجرد تنفيذ التشفير في Q3 2026.

---

*آخر مراجعة: 2026-05-31 | Last reviewed: 2026-05-31*
