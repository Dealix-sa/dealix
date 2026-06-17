# Market Agent Registry — سجل وكلاء السوق وصلاحياتهم — Market Production OS

أدوار وكلاء طبقة السوق وصلاحياتها. كل وكيل **له هوية** (محظور رقم 9) ويعمل ضمن
الحوكمة. القاعدة الذهبية للصلاحيات:

Roles and permissions for the market-layer agents. Every agent **has an identity**
(non-negotiable #9) and operates under governance. The golden permission rule:

> **يجوز:** المسودة · التصنيف · الترتيب · التقرير.
> **لا يجوز:** الإرسال · تثبيت السعر · الالتزام · تجاوز opt-out.
> **May:** draft · classify · rank · report.
> **May not:** send · price-finalize · commit · bypass opt-out.

أي إجراء خارجي يمرّ عبر `auto_client_acquisition/approval_center/` وبوابات
`governance_os/` + `safe_send_gateway/`. لا وكيل يتجاوزها.

---

## الأدوار — The roles

| الوكيل / Agent | يُنتج / Produces | مقيّد بـ / Bound by |
| --- | --- | --- |
| Brand Guard | فحص نبرة/claims | `governance_os/claim_safety.py` |
| Product Catalog | مطابقة عرض | `gtm_os/offer_catalog.py` (لا تثبيت سعر) |
| Sector Intelligence | playbook قطاعي | `vertical_playbooks/` |
| Signal Detection | إشارات (إدخال/عام) | `gtm_os/records.CompanySignal` (لا scraping) |
| Prospect Research | prospects مرتبة | `gtm_os/records.score_prospect` (بلا PII) |
| Draft Factory | 250 مسودة/يوم | `gtm_os/outreach_draft.py` (draft-only) |
| Compliance Gate | pass/fail | `gtm_os/draft_quality_gate.py` |
| Deliverability | خطة دفعات آمنة | `gtm_os/sending_ramp.py` (plan, لا إرسال) |
| Approval Queue | عرض للمراجعة | `approval_center/` (المؤسس يقرّر) |
| Reply Handling | تصنيف + إجراء | `gtm_os/records.route_reply` |
| WhatsApp Conversion | بطاقات بعد الموافقة | `whatsapp_decision_bot/` (consent-only) |
| Content / Press / Partnership | مسودات توزيع | `marketing_factory/`, `partnership_os/` |
| Privacy Guard | فحص PDPL/PII | `compliance_os/`, `data_os.pii_flags_for_row` |
| Finance GTM | اقتصاد الوحدة | `operating_finance_os/` |
| Delivery Handoff | تسليم بعد الفوز | `delivery_factory/` |
| GTM Metrics | تقرير يومي | `scripts/gtm_daily_command.py` |

---

## الإنفاذ — Enforcement

- الإرسال بلا موافقة → `send_without_approval` (محجوب في البوابة + التدرّج).
- ادعاء مضمون/مزيّف → `governance:forbidden_claim:*` (BLOCK).
- scraping / cold whatsapp / linkedin automation → `governance:*` (BLOCK).
- مستلم في قائمة الكبح → `suppression_hit` (BLOCK).

كل مخرج يحمل حقل `governance_decision`. مسودة نظيفة = `approval_required` (جاهزة
لإنسان، لا تُرسَل تلقائيًا).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
