# بنية Dealix Business OS — Dealix Business OS Architecture

> راجع [مصدر الحقيقة للمنصة](./PLATFORM_SOURCE_OF_TRUTH.md) للتموضع المعتمد. هذا المستند يصف البنية الطبقية للمنصة الأم وأنظمتها الاثني عشر.
>
> See [Platform Source of Truth](./PLATFORM_SOURCE_OF_TRUTH.md) for canonical positioning. This document describes the layered architecture of the mother platform and its twelve systems.

---

## القسم العربي (أساسي)

### المنصة الأم

Dealix AI Business OS هي المنصة الأم. تنتظم تحتها اثنا عشر نظام تشغيل في خمس طبقات:

- **الطبقة التنفيذية:** Command OS.
- **طبقة الثقة والأمان:** Proof OS + Governance OS + Data OS.
- **المدخل التجاري:** Revenue OS.
- **طبقة التوسّع:** Client OS + Delivery OS + Support OS + Finance OS.
- **طبقة المنظومة:** Partner OS + Academy OS + Venture OS.

### الأنظمة، الغرض، والمخرجات، والوحدة الداعمة

| النظام | الغرض | أبرز المخرجات | الوحدة في المستودع |
|---|---|---|---|
| Command OS | قيادة تنفيذية وقرارات | ملخص المدير اليومي، حزمة المجلس الأسبوعية، سجل المخاطر، سجل القرارات، ترتيب الأولويات | `auto_client_acquisition/command_os` |
| Proof OS | إثبات القيمة بالأدلة | حزمة إثبات، فهرس أدلة، بطاقات قيمة موثّقة | `auto_client_acquisition/proof_os` |
| Governance OS | حوكمة وموافقات وامتثال | سجل الموافقات، فحوصات السياسة، سجل الامتثال (PDPL/ZATCA) | `auto_client_acquisition/governance_os` |
| Data OS | جودة وتدفّق البيانات | تقرير جودة البيانات، خريطة المصادر، سجل النواقص | `auto_client_acquisition/data_os` |
| Revenue OS | تتبّع تسرّب الفرص | خريطة الإيرادات، لوحة الفرص، موجز الاستهداف اليومي (مسودّة فقط) | `auto_client_acquisition/revenue_os` |
| Client OS | معرفة العميل المنظّمة | ملف العميل الموحّد، مؤشّر صحة العلاقة | `auto_client_acquisition/client_os` |
| Sales OS | دعم دورة البيع | لوحة المسار، سجل العروض | `auto_client_acquisition/sales_os` |
| Delivery OS | تتبّع التسليم | لوحة الالتزامات، حالة التسليم | — |
| Support OS | الدعم بعد البيع | لوحة الحالات، اتفاق مستوى الخدمة | — |
| Finance OS | ربط الإيراد بالمال | لوحة التدفّق، حالة الفوترة | — |
| Academy OS | المعرفة والتدريب | مسارات التمكين، مكتبة المعرفة | — |
| Partner OS | الشركاء والقنوات | سجل الشركاء، لوحة القنوات | — |
| Venture OS | بناء مشاريع جديدة | دفتر الفرص (استراتيجية فقط) | — |

---

## English Section

### Mother platform

Dealix AI Business OS is the mother platform. Twelve operating systems organize beneath it across five layers:

- **Executive layer:** Command OS.
- **Trust / safety layer:** Proof OS + Governance OS + Data OS.
- **Commercial wedge:** Revenue OS.
- **Expansion layer:** Client OS + Delivery OS + Support OS + Finance OS.
- **Ecosystem layer:** Partner OS + Academy OS + Venture OS.

### Systems — purpose, key outputs, backing module

| System | Purpose | Key outputs | Repo module |
|---|---|---|---|
| Command OS | Executive command and decisions | CEO Daily Brief, Weekly Board Pack, Risk Register, Decision Log, Priority Stack | `auto_client_acquisition/command_os` |
| Proof OS | Prove value with evidence | Proof Pack, Evidence Index, evidenced value cards | `auto_client_acquisition/proof_os` |
| Governance OS | Governance, approvals, compliance | Approval Register, policy checks, compliance register (PDPL/ZATCA) | `auto_client_acquisition/governance_os` |
| Data OS | Data quality and flow | Data Quality Report, Source Map, gap register | `auto_client_acquisition/data_os` |
| Revenue OS | Track where opportunities leak | Revenue Map, Opportunity Board, Daily Targeting Brief (draft-only) | `auto_client_acquisition/revenue_os` |
| Client OS | Structured customer knowledge | Unified Client Profile, relationship health index | `auto_client_acquisition/client_os` |
| Sales OS | Support the sales cycle | Pipeline board, offer log | `auto_client_acquisition/sales_os` |
| Delivery OS | Track delivery | Commitments board, delivery status | — |
| Support OS | Post-sale support | Case board, SLA tracking | — |
| Finance OS | Connect revenue to cash | Cash board, billing status | — |
| Academy OS | Knowledge and training | Enablement tracks, knowledge library | — |
| Partner OS | Partners and channels | Partner register, channel board | — |
| Venture OS | Build new ventures | Opportunity ledger (strategy only) | — |

### Layering principle

The Executive layer reads from every system. The Trust/safety layer wraps every external action: nothing reaches a customer without passing through Governance OS approval, backed by Proof OS evidence and Data OS quality. The commercial wedge (Revenue OS) is what a customer buys first; the expansion and ecosystem layers are sold later as the relationship matures.

---

### Related docs

- [Platform Source of Truth](./PLATFORM_SOURCE_OF_TRUTH.md)
- [Product Family Map](./PRODUCT_FAMILY_MAP.md)
- Per-OS detail: [Command](../02_operating_systems/COMMAND_OS.md), [Revenue](../02_operating_systems/REVENUE_OS.md), [Proof](../02_operating_systems/PROOF_OS.md), [Client](../02_operating_systems/CLIENT_OS.md), [Delivery](../02_operating_systems/DELIVERY_OS.md), [Governance](../02_operating_systems/GOVERNANCE_OS.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
