# Data Processing Agreement (DPA) — Template / قالب اتفاقية معالجة البيانات

> **Template only — lawyer review required.** قالب فقط — يُراجع قانونيًا.
> PDPL-aligned (Saudi Personal Data Protection Law). متوائم مع نظام حماية
> البيانات الشخصية السعودي.

Companion to the [MSA](MSA_TEMPLATE_AR_EN.md). Reference register:
`dealix/registers/compliance_saudi.yaml`.

## 1. Roles / الأدوار
- **Controller / المتحكم:** Client {{CLIENT_LEGAL_NAME}}
- **Processor / المعالِج:** Dealix

## 2. Subject & Purpose / الموضوع والغرض
Dealix processes personal data **only** to deliver the agreed Transformation OS
services per the SOW and documented instructions. لا معالجة خارج التعليمات.

## 3. Categories / الفئات
- Data subjects: Client's leads, customers, staff (as applicable).
- Data types: contact details, commercial interaction records. **Data
  minimization** applied — no collection beyond purpose.

## 4. Processor Obligations / التزامات المعالِج
- Process only on documented instructions; confidentiality of all personnel.
- Technical + organizational measures: encryption in transit, access controls
  (RBAC), audit logging, secret hygiene (no hardcoded keys).
- **No cross-border transfer** without Controller authorization + lawful basis.
- Assist with data-subject rights (access, correction, deletion) and breach
  notification **without undue delay** (target ≤72h to Controller).

## 5. Sub-processors / المعالِجون الفرعيون
Listed in the vendor/tool register; Controller notified of changes with a right to
object. مزوّدو الذكاء الاصطناعي يُدرجون في سجل المورّدين.

## 6. AI-specific Controls / ضوابط خاصة بالذكاء الاصطناعي
- No personal data used to train third-party models without explicit consent.
- Agent actions on personal data are logged + subject to approval gates.
- No PII in logs (heuristic enforced; see `tests/test_no_pii_in_logs.py`).

## 7. Retention & Deletion / الاحتفاظ والحذف
Retention per SOW schedule; on termination, data returned or securely deleted on
Controller request. حق طلب الحذف في أي وقت.

## 8. Audit / التدقيق
Controller may audit compliance (reasonable notice). Evidence available via the
Trust Pack ([trust_compliance_pack_template.md](trust_compliance_pack_template.md)).

## 9. Governing Law / القانون الحاكم
Kingdom of Saudi Arabia (PDPL + NCA where applicable).
