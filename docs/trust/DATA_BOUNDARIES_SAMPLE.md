# Dealix — Sample Data Boundary Declaration — إعلان حدود البيانات (نموذج)

> Bilingual declaration of where data may live, where it flows, and how long it stays. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
يُعلِن هذا المستند، لكل مستأجِر، أين تُجمع البيانات، ومن يستقبلها، وأين يُسمَح بتخزينها، ومدّة الاحتفاظ.

### المصادر (Sources)
- **CRM داخلي** — حسابات، صفقات، جهات اتصال (مع موافقة جمع).
- **Inbound channels** — نموذج الموقع، WhatsApp inbound، البريد الوارد.
- **Saudi sources** — الغرف التجارية، SDAIA (عام)، MCI، ZATCA (وفق إذن).
- **محوّلات Lead Engine** — Google Maps، CSE، Hunter، Firecrawl (بإذن)، Wappalyzer.

### المصارف (Sinks)
- AI Run Ledger داخلي.
- CRM المستأجِر.
- Evidence Pack store داخل المستأجِر.
- إخطارات إلى المُوافقين المُسمّين (داخل النطاق المُصرَّح).

### المناطق المسموح بها
- **افتراضي**: داخل المملكة العربية السعودية.
- **مسموح بشرط**: المنطقة الخليجية بموافقة مكتوبة.
- **ممنوع افتراضيًا**: خارج المنطقة الخليجية إلا بقرار العميل صراحةً ووفق قواعد النقل في PDPL.

### الاحتفاظ
| نوع البيانات | المدة | الأساس |
|---|---|---|
| Run Ledger metadata | 24 شهرًا | حوكمة AI |
| Evidence Packs | 36 شهرًا | تدقيق إيراد + PDPL |
| سجلات DSAR | 24 شهرًا | PDPL المادة 18 |
| محتوى مسودّات داخلية | 90 يومًا | الحدّ الأدنى التشغيلي |
| PII غير مطلوبة | 0 يوم | لا تُخزَّن |

### نقل البيانات
- لا نقل افتراضي خارج المملكة.
- النقل العابر للحدود يستوجب: (أ) إذنًا كتابيًا من المالك، (ب) أساسًا قانونيًا في PDPL، (ج) سجلًا في AI Run Ledger.

### حقوق الموضوع
- وصول، تصحيح، حذف، اعتراض — متاحة عبر DSAR endpoint.
- مدّة الاستجابة: 30 يومًا كحدّ أعلى.

---

## English

### Purpose
For each tenant, this document declares where data is collected, who receives it, where it may be stored, and how long it is retained.

### Sources
- **Internal CRM** — accounts, deals, contacts (with collection consent).
- **Inbound channels** — website form, inbound WhatsApp, inbound email.
- **Saudi sources** — Chambers, SDAIA (public), MCI, ZATCA (under permission).
- **Lead Engine adapters** — Google Maps, CSE, Hunter, Firecrawl (with consent), Wappalyzer.

### Sinks
- Internal AI Run Ledger.
- Tenant CRM.
- Evidence Pack store inside the tenant.
- Notifications to named approvers (within authorized scope).

### Allowed Regions
- **Default**: inside the Kingdom of Saudi Arabia.
- **Conditional**: GCC region with written consent.
- **Default-denied**: outside GCC unless the customer explicitly decides and PDPL transfer rules are met.

### Retention
| Data Type | Duration | Basis |
|---|---|---|
| Run Ledger metadata | 24 months | AI governance |
| Evidence Packs | 36 months | Revenue audit + PDPL |
| DSAR records | 24 months | PDPL Article 18 |
| Internal draft content | 90 days | Operational minimum |
| PII not required | 0 days | Not stored |

### Data Transfer
- No default transfer outside the Kingdom.
- Cross-border transfer requires: (a) written owner permission, (b) PDPL legal basis, (c) AI Run Ledger record.

### Subject Rights
- Access, correction, deletion, objection — available via DSAR endpoint.
- Response window: 30 days maximum.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
