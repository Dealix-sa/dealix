# Dealix — OS Map — خارطة نظام التشغيل

> Section 164 of the positioning brief. The full module tree. Each node links to its doc or code module. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الفكرة
نظام تشغيل Dealix ليس «منتجًا واحدًا»، بل أربع طبقات يتفاعل بعضها مع بعض: **اكتساب، خدمة، ثقة، وتحكّم**. تحتها يقع طبقة سادسة هي **العقيدة**.

### الشجرة

```
Dealix OS
├── Layer 0 — العقيدة (Doctrine)
│   ├── الوعود الأربعة → docs/business/FOUR_PROMISES.md
│   ├── ما لا نبنيه (Refusal) → docs/business/COMPANY_PROFILE.md §12
│   └── الإفصاح («تقديرية ليست متحقَّقة») → docs/business/CATEGORY_AND_ONE_LINERS.md
│
├── Layer 1 — Lead Engine (الاكتساب)
│   ├── محوّلات 5: Google Maps, CSE, Hunter, Firecrawl, Wappalyzer → api/services/leads/*
│   ├── مصادر سعودية: Chambers, SDAIA, MCI, ZATCA → api/services/saudi_sources/*
│   ├── ICP scoring → api/services/icp/*
│   └── Source Passport → docs/trust/DATA_BOUNDARIES_SAMPLE.md
│
├── Layer 2 — Service Engine (الخدمات S1-S7)
│   ├── S1-S7 routers → api/routers/services/*
│   ├── Tenant theming → api/services/theming/*
│   └── Pricing → api/routers/pricing.py + docs/business/PRICING_MODEL_V7.md
│
├── Layer 3 — Trust Engine (الثقة)
│   ├── PDPL (المواد 5/13/14/18/21/32) → api/services/pdpl/*
│   ├── ZATCA Phase 2 → api/services/zatca/*
│   ├── SDAIA alignment → docs/trust/ENTERPRISE_TRUST_PACK.md
│   ├── Source Passport → docs/trust/DATA_BOUNDARIES_SAMPLE.md
│   ├── AI Run Ledger → api/services/run_ledger/*
│   └── DSAR endpoints → api/routers/dsar.py
│
├── Layer 4 — Agentic Control Plane (التحكّم بالوكلاء)
│   ├── Agent Registry → docs/trust/AGENT_REGISTRY_SAMPLE.md
│   ├── Tool Permission Matrix → docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md
│   ├── MCP Review → docs/trust/MCP_REVIEW_CHECKLIST.md
│   ├── Evidence Pack Standard → docs/trust/EVIDENCE_PACK_SAMPLE.md
│   ├── Incident Response → docs/trust/INCIDENT_RESPONSE_SAMPLE.md
│   └── AI Use Policy → docs/trust/AI_USE_POLICY_SAMPLE.md
│
├── Layer 5 — Commercial OS (الطبقة التجارية)
│   ├── Offer Catalog → docs/business/OFFER_CATALOG.json
│   ├── Pricing V7 → docs/business/PRICING_MODEL_V7.md
│   ├── Revenue Streams → docs/business/REVENUE_STREAM_QUALITY_MATRIX.md
│   ├── Sales Narratives → docs/business/SALES_NARRATIVES.md
│   ├── Enterprise Packet → docs/enterprise/ENTERPRISE_PACKET.md
│   └── Agency Operating System → docs/40_partners/PARTNER_OPERATING_SYSTEM.md
│
├── Layer 6 — Governance OS (الحوكمة)
│   ├── Governance Model → docs/enterprise/GOVERNANCE_MODEL.md
│   ├── Implementation Plan 30/60/90 → docs/enterprise/IMPLEMENTATION_PLAN.md
│   ├── Commercial Terms Template → docs/enterprise/COMMERCIAL_TERMS_TEMPLATE.md
│   ├── Security Overview → docs/enterprise/SECURITY_OVERVIEW.md
│   └── Value Measurement → docs/enterprise/VALUE_MEASUREMENT.md
│
└── Layer 7 — Investor & Board (المستثمر والمجلس)
    ├── Investor One-Pager → docs/business/INVESTOR_ONE_PAGER.md
    ├── Investor Narrative → docs/business/INVESTOR_NARRATIVE.md
    ├── Board Metrics → docs/business/BOARD_METRICS.md
    ├── Investor Update Template → docs/business/INVESTOR_UPDATE_TEMPLATE.md
    └── Presentation Outline → docs/business/PRESENTATION_OUTLINE_20_SLIDES.md
```

### قراءة الخارطة
- كل طبقة تستهلك من الطبقة تحتها.
- لا طبقة تتجاوز Layer 0 (العقيدة).
- إضافة وحدة جديدة تستوجب إضافة عقدة هنا.

---

## English

### Idea
The Dealix operating system is not a "single product"; it is four interacting layers — **acquisition, service, trust, control** — beneath which lives a **doctrine** layer.

### Tree

```
Dealix OS
├── Layer 0 — Doctrine
│   ├── Four Promises → docs/business/FOUR_PROMISES.md
│   ├── Refusal Doctrine → docs/business/COMPANY_PROFILE.md §12
│   └── Disclosure ("Estimated is not Verified") → docs/business/CATEGORY_AND_ONE_LINERS.md
│
├── Layer 1 — Lead Engine (acquisition)
│   ├── 5 adapters: Google Maps, CSE, Hunter, Firecrawl, Wappalyzer → api/services/leads/*
│   ├── Saudi sources: Chambers, SDAIA, MCI, ZATCA → api/services/saudi_sources/*
│   ├── ICP scoring → api/services/icp/*
│   └── Source Passport → docs/trust/DATA_BOUNDARIES_SAMPLE.md
│
├── Layer 2 — Service Engine (S1-S7)
│   ├── S1-S7 routers → api/routers/services/*
│   ├── Tenant theming → api/services/theming/*
│   └── Pricing → api/routers/pricing.py + docs/business/PRICING_MODEL_V7.md
│
├── Layer 3 — Trust Engine
│   ├── PDPL (Articles 5/13/14/18/21/32) → api/services/pdpl/*
│   ├── ZATCA Phase 2 → api/services/zatca/*
│   ├── SDAIA alignment → docs/trust/ENTERPRISE_TRUST_PACK.md
│   ├── Source Passport → docs/trust/DATA_BOUNDARIES_SAMPLE.md
│   ├── AI Run Ledger → api/services/run_ledger/*
│   └── DSAR endpoints → api/routers/dsar.py
│
├── Layer 4 — Agentic Control Plane
│   ├── Agent Registry → docs/trust/AGENT_REGISTRY_SAMPLE.md
│   ├── Tool Permission Matrix → docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md
│   ├── MCP Review → docs/trust/MCP_REVIEW_CHECKLIST.md
│   ├── Evidence Pack Standard → docs/trust/EVIDENCE_PACK_SAMPLE.md
│   ├── Incident Response → docs/trust/INCIDENT_RESPONSE_SAMPLE.md
│   └── AI Use Policy → docs/trust/AI_USE_POLICY_SAMPLE.md
│
├── Layer 5 — Commercial OS
│   ├── Offer Catalog → docs/business/OFFER_CATALOG.json
│   ├── Pricing V7 → docs/business/PRICING_MODEL_V7.md
│   ├── Revenue Streams → docs/business/REVENUE_STREAM_QUALITY_MATRIX.md
│   ├── Sales Narratives → docs/business/SALES_NARRATIVES.md
│   ├── Enterprise Packet → docs/enterprise/ENTERPRISE_PACKET.md
│   └── Agency Operating System → docs/40_partners/PARTNER_OPERATING_SYSTEM.md
│
├── Layer 6 — Governance OS
│   ├── Governance Model → docs/enterprise/GOVERNANCE_MODEL.md
│   ├── Implementation Plan 30/60/90 → docs/enterprise/IMPLEMENTATION_PLAN.md
│   ├── Commercial Terms Template → docs/enterprise/COMMERCIAL_TERMS_TEMPLATE.md
│   ├── Security Overview → docs/enterprise/SECURITY_OVERVIEW.md
│   └── Value Measurement → docs/enterprise/VALUE_MEASUREMENT.md
│
└── Layer 7 — Investor & Board
    ├── Investor One-Pager → docs/business/INVESTOR_ONE_PAGER.md
    ├── Investor Narrative → docs/business/INVESTOR_NARRATIVE.md
    ├── Board Metrics → docs/business/BOARD_METRICS.md
    ├── Investor Update Template → docs/business/INVESTOR_UPDATE_TEMPLATE.md
    └── Presentation Outline → docs/business/PRESENTATION_OUTLINE_20_SLIDES.md
```

### Reading the Map
- Each layer consumes from the layer below.
- No layer bypasses Layer 0 (doctrine).
- Adding a new module requires adding a node here.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
