# Data Boundaries — Sample — حدود البيانات (عيّنة)

> **Sample — illustrative.** Used as the default data-handling boundary for Dealix engagements. Customer-specific boundaries are derived from this baseline and ratified in the Commercial Terms.
>
> **عيّنة توضيحية.** الحدود الافتراضية لمعالجة البيانات في ارتباطات ديلكس. تُستمدّ الحدود الخاصة بكل عميل من هذا الأساس وتُعتمد في الشروط التجارية.

---

## 1. Data Classes — فئات البيانات

| Class | Examples | Default Handling | الفئة | الأمثلة |
|---|---|---|---|---|
| **Public** | Marketing pages, public sector reports | Free use within the agent's scope. | عامة | الصفحات التسويقية، التقارير العامة |
| **Internal** | Memos, SOPs, internal dashboards | Use only within approved tools and tenants. | داخلية | المذكرات، إجراءات التشغيل، اللوحات الداخلية |
| **Customer-Tenant** | Customer records, communications, deal artifacts | Strict tenant isolation; never crosses tenants. | بيانات مستأجر العميل | السجلات والمراسلات وأصول الصفقات |
| **Regulated** | PDPL personal data, financial ledger entries, contracts | Redaction required; Founder-class approval for any model exposure. | مُنظَّمة | بيانات شخصية وفق نظام حماية البيانات، السجلات المالية، العقود |
| **Secret** | Credentials, encryption keys, board materials | Never exposed to any model or tool; vault-only. | سرية | بيانات الاعتماد، المفاتيح، وثائق المجلس |

---

## 2. Residency — إقامة البيانات

- **Default.** KSA-first residency. Storage, processing, and audit logs are kept inside Saudi Arabia for KSA customer engagements.
- **PDPL alignment.** All personal data handling follows PDPL principles by default: lawful basis, minimization, purpose limitation, retention boundaries, and data-subject rights.
- **Cross-border.** Any cross-border flow requires explicit Founder-class approval and is recorded in the Approval Center with a documented purpose.

**AR.** الإقامة الافتراضية داخل المملكة لارتباطات السعودية. التوافق مع نظام حماية البيانات الشخصية افتراضيًا. أي تدفق عابر للحدود يستوجب اعتماد المؤسس وتسجيله مع غرضه الموثّق.

---

## 3. Cross-Tenant Rules — قواعد العبور بين المستأجرين

- Customer data never crosses tenant boundaries.
- Agents are scoped to a single tenant per invocation; cross-tenant prompts are denied at the MCP gateway.
- Aggregation for sector reports is methodology-only; no per-customer identifiers leave the tenant.
- A shared dictionary of patterns (not data) may be referenced across engagements, after redaction and review.

**AR.** لا تعبر بيانات العميل حدود المستأجرين. يُحصر الوكيل في مستأجر واحد لكل استدعاء؛ وتُرفض الموجّهات العابرة عند البوابة. التجميع لتقارير القطاعات منهجي فقط، بلا معرّفات فردية. يُحال إلى قاموس أنماط مشتركة (لا بيانات) بعد التعمية والمراجعة.

---

## 4. Retention — الاحتفاظ

| Data Class | Default Retention | Notes |
|---|---|---|
| Public | Indefinite (subject to source restrictions) | — |
| Internal | 36 months | Reviewed annually. |
| Customer-Tenant | Per contract; default 24 months post-engagement | Customer may request earlier deletion. |
| Regulated | Per regulatory requirement | Erasure on lawful request. |
| Secret | Minimum required; rotate quarterly | Vault-managed. |
| Audit logs | 7 years | Tamper-evident; required for evidence integrity. |

Customer-specific retention is set in the Commercial Terms and may shorten — never extend — the defaults without explicit approval.

---

## 5. Export Controls — ضوابط التصدير

- File exports from any tool are logged with destination, data class, and approver.
- External delivery (to anyone outside the tenant) requires a named human operator to send.
- No bulk export of Customer-Tenant or Regulated data is permitted to consumer storage providers.
- Encrypted export to the customer's approved storage is the default channel.

**AR.** تُسجَّل صادرات الملفات بالوجهة والفئة والمعتمد. التسليم الخارجي يستوجب مُشغِّلًا بشريًا مُسمّى. لا تصدير ضخم لبيانات مستأجر العميل أو المُنظَّمة إلى مزوّدي تخزين استهلاكي. التصدير المُشفَّر إلى تخزين العميل المعتمد هو القناة الافتراضية.

---

## 6. Agent Data Scopes — نطاقات بيانات الوكلاء

Each agent declares the data classes it is permitted to read and the classes it is permitted to write or transmit. The declared scope is enforced at:

1. The MCP gateway (tool calls).
2. The runtime sandbox (in-memory access).
3. The audit log (post-action verification).

Out-of-scope access attempts are denied, logged, and surface as S1 incidents if repeated.

**AR.** يعلن كل وكيل فئات القراءة والكتابة المسموح بها، وتُفرَض عند البوابة والصندوق الرملي وسجل التدقيق. الوصول خارج النطاق يُرفَض ويُسجَّل، وتُعدّ تكراريته حادثة S1.

---

## 7. Redaction Rules — قواعد التعمية

- Personal identifiers (national ID, phone, email) are tokenized before any model invocation, unless the agent's declared scope and the action's approval class permit the raw value.
- Free-text fields are screened with a redaction filter for PII patterns.
- Contract text is redacted of counterparty identifiers when shared with sector-aggregation pipelines.
- Redaction failures are S1 incidents.

**AR.** تُرمَّز المعرّفات الشخصية قبل استدعاء النموذج إلا حين تجيز فئة الوكيل وفئة الموافقة القيم الخام. تُمسح الحقول الحرّة بمرشّح تعمية. تُعمَّى نصوص العقود من معرّفات الأطراف عند مشاركتها مع خطوط تجميع القطاعات. إخفاقات التعمية حوادث S1.

---

## 8. Customer Rights — حقوق العميل

- Request a current snapshot of declared boundaries at any time.
- Request a redaction or deletion within the agreed retention boundary.
- Inspect the audit log for any action within the customer's tenant.
- Invoke the kill switch via the executive sponsor channel.

**AR.** للعميل: طلب لقطة من الحدود في أي وقت، طلب تعمية أو حذف ضمن نافذة الاحتفاظ، فحص سجل التدقيق داخل مستأجره، واستخدام مفتاح الإيقاف عبر قناة الراعي التنفيذي.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/AI_USE_POLICY_SAMPLE.md` · `/home/user/dealix/docs/trust/MCP_REVIEW_CHECKLIST.md` · `/home/user/dealix/docs/enterprise/SECURITY_OVERVIEW.md`
