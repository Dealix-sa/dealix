# Dealix Module Status Map — خريطة حالة الوحدات

> Status: LIVE (this register) · Audience: Internal source of truth · Owner: Founder
> Related: [PRODUCT_FAMILY_MAP.md](PRODUCT_FAMILY_MAP.md) · [LAUNCH_CONTROL_TOWER.md](LAUNCH_CONTROL_TOWER.md) · [BRAND_IDENTITY_SYSTEM.md](BRAND_IDENTITY_SYSTEM.md)

This is the honest, conservative inventory of what may be sold, demoed, or only documented today. When marketing wants to claim a module is "live," it must appear LIVE or BETA here first. Backend module references point at `auto_client_acquisition/` and `api/routers/` so status reflects code, not ambition.

**Status taxonomy:** LIVE = ready to use · BETA = near-ready · INTERNAL = internal only · DOCS_ONLY = documented only · FUTURE = later · BLOCKED = needs fix · DEPRECATED = do not use.

---

## EN — Module Status

### Sellable wedge (the only paid surface at launch)

| Module / Offer | Status | Backend / Doc reference | Notes |
|---|---|---|---|
| Dealix Command Sprint (engagement) | BETA | `api/routers/sprint_runner.py` | The paid entry point; delivered as a scoped cycle. |
| Diagnostic | BETA | `api/routers/diagnostic.py`, `diagnostic_workflow.py` | Guided read that feeds the Sprint. |
| Business OS Score | BETA | routing target across `docs/06_growth/` | Self-serve signal; routes to Diagnostic / Sprint. |

### Command Sprint included modules

| Module | Status | Backend reference | Notes |
|---|---|---|---|
| Market Intelligence Lite | BETA | `api/routers/market_intelligence.py`, `auto_client_acquisition/enrichment_provider.py` | Permitted sources only; no scraping behind login. |
| Revenue Map | BETA | `api/routers/revenue_os.py`, `commercial_map.py` | Estimated, not guaranteed. |
| Proof Register | BETA | `api/routers/case_study_engine.py` | Verified vs estimated marked; no public case without approval. |
| Executive Command Brief | BETA | `api/routers/executive_os.py`, `founder_command_summary.py` | Leadership read. |
| Approval Register | BETA | `api/routers/approval_center.py` | Approval-first by design. |
| Next Action Board | BETA | `api/routers/business_now.py` | Named owner per action. |
| Delivery Lite | BETA | `api/routers/delivery_os.py` | Handover + deliverable tracking. |
| Upsell Recommendation | BETA | `api/routers/expansion_engine.py`, `value_os.py` | Evidenced; customer decides. |

### Business OS layers (platform backbone)

| Layer | Status | Backend reference | Notes |
|---|---|---|---|
| Revenue OS | BETA | `api/routers/revenue_os.py`, `sales_os.py` | First wedge backbone. |
| Proof OS / Value OS | BETA | `api/routers/value_os.py`, `case_study_engine.py` | Evidence + value framing. |
| Governance OS | BETA | `api/routers/agent_governance.py`, `governance_risk_dashboard.py` | PDPL/ZATCA, audit, policy. |
| Data OS | BETA | `api/routers/data_os.py`, `auto_client_acquisition/consent_table.py` | Memory + lineage; consent-aware. |
| Delivery OS | BETA | `api/routers/delivery_os.py`, `delivery_factory.py` | — |
| Command / Founder OS | BETA | `api/routers/founder_dashboard.py`, `executive_command_center.py` | Founder rhythm. |
| Adoption OS | INTERNAL | `api/routers/customer_success_os.py` | Internal adoption tracking. |
| Capital / Finance OS | INTERNAL | `api/routers/finance_os.py` | Internal; not a customer offer yet. |

### Outreach and acquisition (constrained by hard rules)

| Module | Status | Backend reference | Notes |
|---|---|---|---|
| Lead inbox / ICP scoring | INTERNAL | `auto_client_acquisition/icp_scorer.py`, `lead_inbox.py` | Internal pipeline support; not sold as targeting. |
| WhatsApp safe send | INTERNAL | `auto_client_acquisition/whatsapp_safe_send.py` | Approval-first, windowed. No auto-send. No cold automation. |
| Outreach window controls | INTERNAL | `auto_client_acquisition/outreach_window.py` | Governs timing; not a bulk-outreach feature. |

### Future layers (do not sell, do not demo as available)

| Layer | Status | Notes |
|---|---|---|
| Enterprise OS | FUTURE | Multi-entity, advanced RBAC. |
| Partner OS | FUTURE | Reseller / implementation partners. |
| Academy OS | FUTURE | Enablement and certification. |

### Rules this register enforces
- Nothing marked INTERNAL, DOCS_ONLY, FUTURE, or BLOCKED is described to customers as available.
- WhatsApp and outreach modules are approval-first and windowed — never auto-send, cold automation, or scraping behind login.
- A module can only move to LIVE after the go/no-go criteria pass (see [LAUNCH_CONTROL_TOWER.md](LAUNCH_CONTROL_TOWER.md) and `docs/05_founder/LAUNCH_GO_NO_GO.md`).

---

## AR — حالة الوحدات

**التصنيف:** LIVE = جاهز · BETA = قريب الجهوزية · INTERNAL = داخلي فقط · DOCS_ONLY = موثّق فقط · FUTURE = لاحقاً · BLOCKED = يحتاج إصلاحاً · DEPRECATED = لا يُستخدم.

### الإسفين القابل للبيع (السطح المدفوع الوحيد عند الإطلاق)
- **Dealix Command Sprint** — BETA — نقطة الدخول المدفوعة، يُسلَّم كدورة محدّدة النطاق.
- **التشخيص (Diagnostic)** — BETA — قراءة موجّهة تغذّي الـ Sprint.
- **Business OS Score** — BETA — إشارة ذاتية توجّه إلى التشخيص / الـ Sprint.

### وحدات الـ Command Sprint
جميعها **BETA**: Market Intelligence Lite (مصادر مسموحة، لا كشط)، Revenue Map (تقديري لا مضمون)، Proof Register (مُتحقَّق مقابل تقديري)، Executive Command Brief، Approval Register (الاعتماد أولاً)، Next Action Board (مالك مُسمّى)، Delivery Lite، Upsell Recommendation (مُثبت، والقرار للعميل).

### طبقات Business OS
Revenue OS / Proof OS / Governance OS / Data OS / Delivery OS / Command OS — جميعها **BETA**. Adoption OS وCapital/Finance OS — **INTERNAL** (ليست عرضاً للعميل بعد).

### التواصل والاكتساب (محكوم بالقواعد الصارمة)
سجل الفرص وتقييم ICP وWhatsApp safe send وضوابط نوافذ التواصل — جميعها **INTERNAL**: الاعتماد أولاً ومحكومة بالنوافذ. لا إرسال تلقائي، لا أتمتة باردة، لا كشط خلف الدخول.

### الطبقات المستقبلية (لا تُباع ولا تُعرض كمتاحة)
Enterprise OS / Partner OS / Academy OS — جميعها **FUTURE**.

### قواعد يفرضها هذا السجل
- لا يُوصف للعميل أي وحدة INTERNAL أو DOCS_ONLY أو FUTURE أو BLOCKED كمتاحة.
- وحدات WhatsApp والتواصل بالاعتماد أولاً ومحكومة بالنوافذ — لا إرسال تلقائي ولا أتمتة باردة ولا كشط.
- لا تنتقل وحدة إلى LIVE إلا بعد اجتياز معايير القرار (انظر [LAUNCH_CONTROL_TOWER.md](LAUNCH_CONTROL_TOWER.md) و`docs/05_founder/LAUNCH_GO_NO_GO.md`).

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
