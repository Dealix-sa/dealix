# Dealix — فهرس غرفة البيانات للمستثمرين
# Dealix — Investor Data Room Index

> **تحذير**: هذا الفهرس للأغراض التنظيمية الداخلية فقط. لا تُشارَك المستندات الفعلية مع أي طرف خارجي دون موافقة المؤسس وتوثيق في سجل الحوكمة.
>
> **Warning**: This index is for internal organizational purposes only. No documents from this data room should be shared with any external party without founder approval and governance log entry.

---

## هيكل غرفة البيانات | Data Room Structure

### المستوى 1: الشركة والرؤية | Level 1: Company & Vision

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 1.1 | ملخص المستثمر (AR) | Investor Brief (AR) | `docs/company/INVESTOR_BRIEF_AR.md` | ✓ Ready |
| 1.2 | سرد عرض المستثمرين | Pitch Deck Narrative | `docs/company/PITCH_DECK_NARRATIVE_AR.md` | ✓ Ready |
| 1.3 | اقتصاديات الوحدة 2026 | Unit Economics 2026 | `docs/company/UNIT_ECONOMICS_2026.md` | ✓ Ready |
| 1.4 | التموضع التنافسي | Competitive Positioning | `docs/strategy/COMPETITIVE_POSITIONING_2026.md` | ✓ Ready |
| 1.5 | خطة التوظيف 2026 | Hiring Plan 2026 | `docs/company/HIRING_PLAN_2026.md` | ⚙ In Progress |
| 1.6 | السجل القانوني | Legal Register | `docs/company/LEGAL_REGISTER.md` | 🔒 Founder Review |

---

### المستوى 2: المنتج والتقنية | Level 2: Product & Technology

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 2.1 | مواصفات منتج Managed Ops | Managed Ops Product Spec | `docs/product/PRODUCT_SPEC_MANAGED_OPS.md` | ✓ Ready |
| 2.2 | هيكل API (OpenAPI) | API Architecture (OpenAPI) | `/docs` (live endpoint) | ✓ Live |
| 2.3 | سلم المنتجات الخمسي | 5-Tier Product Ladder | `CLAUDE.md` (section: Products) | ✓ Ready |
| 2.4 | الدعائم الدستورية | Constitutional Gates | `CLAUDE.md` (section: Non-negotiables) | ✓ Ready |
| 2.5 | بنية قاعدة البيانات | Database Schema | `db/models.py` | ✓ Ready |
| 2.6 | خريطة مسار التقنية | Tech Roadmap | `docs/product/TECH_ROADMAP_2026.md` | ⚙ Planned |

---

### المستوى 3: السوق والمبيعات | Level 3: Market & Sales

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 3.1 | كتيب الذهاب للسوق | GTM Playbook 2026 | `docs/strategy/GO_TO_MARKET_PLAYBOOK_2026.md` | ✓ Ready |
| 3.2 | ملف العميل المثالي | ICP Profile 2026 | `docs/sales/ICP_PROFILE_2026.md` | ✓ Ready |
| 3.3 | نموذج العرض (ثنائي اللغة) | Proposal Template (AR/EN) | `docs/sales/PROPOSAL_TEMPLATE_AR_EN.md` | ✓ Ready |
| 3.4 | بطاقات المنافسين | Competitor Battlecards | `/api/v1/competitor-intel/battlecards` | ✓ Live |
| 3.5 | بيانات حجم السوق | Market Size Data | `docs/strategy/COMPETITIVE_POSITIONING_2026.md` | ✓ Ready |
| 3.6 | مسرحية المبيعات | Sales Playbook | `/api/v1/sales-playbook/discovery-script` | ✓ Live |

---

### المستوى 4: العمليات والتسليم | Level 4: Operations & Delivery

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 4.1 | إجراءات Sprint التشغيلية | Sprint Execution SOP | `docs/ops/SPRINT_EXECUTION_SOP.md` | ✓ Ready |
| 4.2 | كتيب نجاح العملاء | Customer Success Playbook | `docs/ops/CUSTOMER_SUCCESS_PLAYBOOK.md` | ✓ Ready |
| 4.3 | كتيب التجديدات | Renewal Playbook | `docs/ops/RENEWAL_PLAYBOOK.md` | ✓ Ready |
| 4.4 | إطار حوكمة الإجراءات | Action Governance Framework | `docs/ops/GOVERNANCE_FRAMEWORK.md` | ⚙ Planned |
| 4.5 | منهجية Proof Pack | Proof Pack Methodology | `/api/v1/proof-pack/{eid}/generate` | ✓ Live |

---

### المستوى 5: الامتثال القانوني والتنظيمي | Level 5: Legal & Regulatory Compliance

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 5.1 | تقييم ZATCA للمحفظة | Portfolio ZATCA Assessment | `/api/v1/zatca-readiness/assess` | ✓ Live |
| 5.2 | تقييم PDPL للمحفظة | Portfolio PDPL Assessment | `/api/v1/pdpl-readiness/assess` | ✓ Live |
| 5.3 | سياسة حماية البيانات | Data Protection Policy | `docs/legal/DATA_PROTECTION_POLICY.md` | 🔒 Founder Review |
| 5.4 | سياسة الاحتفاظ بالبيانات | Data Retention Policy | `docs/legal/DATA_RETENTION_POLICY.md` | 🔒 Founder Review |
| 5.5 | نموذج DPA | Data Processing Agreement | `docs/legal/DPA_TEMPLATE.md` | 🔒 Founder Review |
| 5.6 | سياسة الإفصاح المسؤول | Responsible Disclosure Policy | `docs/legal/RESPONSIBLE_DISCLOSURE.md` | ⚙ Planned |

---

### المستوى 6: دراسات الحالة والإثبات | Level 6: Case Studies & Proof

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 6.1 | دراسة حالة: قطاع التقنية (AR) | Case Study: Tech Sector (AR) | `docs/case-studies/CASE_STUDY_TECHNOLOGY_COMPANY_AR.md` | ✓ Ready |
| 6.2 | دراسة حالة: قطاع اللوجستيات (AR) | Case Study: Logistics (AR) | `docs/case-studies/CASE_STUDY_LOGISTICS_AR.md` | ✓ Ready |
| 6.3 | دراسة حالة: القطاع الصحي | Case Study: Healthcare | `docs/case-studies/CASE_STUDY_HEALTHCARE_AR.md` | ⚙ Planned |
| 6.4 | دراسة حالة: الخدمات المالية | Case Study: Financial Services | `docs/case-studies/CASE_STUDY_FINANCIAL_AR.md` | ⚙ Planned |
| 6.5 | مكتبة Proof Packs | Proof Pack Library | `/api/v1/proof-pack/{eid}/generate` | ✓ Live |
| 6.6 | معايير Dealix المرجعية | Dealix Benchmark Data | `/api/v1/health-intelligence/benchmarks` | ✓ Live |

---

### المستوى 7: المالية | Level 7: Financials

| # | المستند | Document | المسار | Status |
|---|---------|----------|--------|--------|
| 7.1 | اقتصاديات الوحدة 2026 | Unit Economics 2026 | `docs/company/UNIT_ECONOMICS_2026.md` | ✓ Ready |
| 7.2 | توقعات الإيرادات 3 سنوات | 3-Year Revenue Projections | `docs/company/INVESTOR_BRIEF_AR.md` (Section 7) | ✓ Ready |
| 7.3 | تحليل نقطة التعادل | Break-Even Analysis | `docs/company/UNIT_ECONOMICS_2026.md` (Section 9) | ✓ Ready |
| 7.4 | نموذج MRR الحي | Live MRR Model | `/api/v1/cockpit/revenue-summary` | ✓ Live |
| 7.5 | القوائم المالية | Financial Statements | `docs/finance/FINANCIAL_STATEMENTS.md` | 🔒 Founder Review |
| 7.6 | تفاصيل cap table | Cap Table Details | `docs/finance/CAP_TABLE.md` | 🔒 Founder Review |

---

## قواعد الوصول | Access Rules

```
🔒 Founder Review = يتطلب موافقة المؤسس قبل المشاركة مع أي طرف
✓ Ready         = متاح داخلياً — يتطلب سياق إفصاح مناسب قبل المشاركة الخارجية
⚙ Planned       = مخطط للتطوير — غير متاح بعد
✓ Live          = نقطة API نشطة — للاستخدام الداخلي فقط
```

**قاعدة المشاركة المطلقة | Absolute Sharing Rule:**
> لا يُشارَك أي مستند من مستوى 5، 6، أو 7 مع أي طرف خارجي إلا بعد:
> 1. موافقة المؤسس الصريحة
> 2. توقيع NDA من الطرف المستفيد
> 3. تسجيل في سجل الحوكمة مع: الطرف، التاريخ، نطاق الإفصاح، المدة

---

## سجل الإفصاح | Disclosure Log

| التاريخ | الطرف | المستندات المشاركة | الموافق | ملاحظات |
|---------|-------|-------------------|---------|---------|
| — | — | — | — | لا إفصاحات بعد |

---

## تاريخ آخر مراجعة | Last Review Date

**2026-05-31** — مراجعة أولية لهيكل غرفة البيانات  
*[Founder: يُراجَع ويُحدَّث عند كل جولة تمويل أو مراجعة تدقيقية]*
