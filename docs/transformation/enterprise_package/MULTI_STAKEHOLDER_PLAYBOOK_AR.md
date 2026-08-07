# Multi-Stakeholder Enterprise Playbook / دليل أصحاب القرار المتعددين

> بيع المؤسسات الكبيرة قرار جماعي. هذا الدليل يربط كل صاحب قرار بالقيمة التي
> تهمّه وبالـ `service_id` المناسب — **بقيادة المؤسس، بمسودات معتمدة فقط، بلا
> تواصل بارد**.

Founder-led, approval-gated. No cold outreach, no automation, no scraping
(doctrine-enforced). Complements
[procurement_response_kit_template.md](procurement_response_kit_template.md) and
[../08_gtm_system_playbook.md](../08_gtm_system_playbook.md).

## 1. Stakeholder map / خريطة أصحاب القرار

| Stakeholder | يهمّه | Anchor system(s) | Proof to bring |
|---|---|---|---|
| **CEO / الرئيس التنفيذي** | رؤية يومية + نمو | `ai_command_center_os`, `executive_reporting_os` | Executive dashboard demo |
| **CFO / المالي** | ROI، استرداد، مخاطر | ROI estimate (range) + `executive_reporting_os` | ROI worksheet + unit economics |
| **CTO / التقني** | معمارية، تكامل، أمان | `ai_agent_workforce_os`, `trust_governance_os` | Architecture + audit logs |
| **COO / العمليات** | كفاءة، أتمتة، SLA | `operations_automation_os`, `client_experience_os` | Workflow map + SOPs |
| **CMO / التسويق** | هوية، رسائل، نمو | `brand_intelligence_os`, `growth_engine_os` | Brand system + approved drafts |
| **Procurement / المشتريات** | عقود، PDPL، أمان | MSA + DPA + Trust Pack | [trust_compliance_pack](trust_compliance_pack_template.md) |

## 2. Engagement path / مسار التعامل

```text
تعريف (مؤسس → جهة اتصال دافئة) → جلسة تشخيص مدفوعة → عرض Transformation (مسودة، approval_required)
→ Pilot مقيّد → Proof Pack → عرض على أصحاب القرار → توسعة مشروطة بالإثبات
```

- العرض يُولَّد عبر `POST /api/v1/commercial/transformation-proposal/generate`
  (مسودة، تُراجَع قبل أي إرسال).
- لا التزام كبير قبل **تشخيص مدفوع**؛ لا إيراد قبل `invoice_paid`.

## 3. Objection map / خريطة الاعتراضات (مختصر)

| Objection | رد مبني على الإثبات |
|---|---|
| "غالي" | لا نخفض السعر أولًا — نخفّض النطاق: ابدأ بنظام واحد + Pilot. |
| "نخاف على بياناتنا" | DPA + PDPL + سجل تدقيق + لا PII في اللوقز. |
| "هل النتائج مضمونة؟" | لا نضمن نتائج أعمال — نلتزم بـ KPI والعمل حتى يتحقق؛ الأرقام تقديرية. |
| "عندنا أدوات" | لا نستبدل stackك — نربطه عبر facades محكومة. |

## 4. القاعدة الذهبية

اربط كل محادثة بـ **إثبات** و**خطوة تالية واحدة** (تشخيص / عيّنة Proof / ديمو ١٠
دقائق). لا وعود مضمونة. لا تواصل بارد.
