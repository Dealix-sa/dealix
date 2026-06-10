# Forbidden Actions — الإجراءات الممنوعة

> Hard limits on what Dealix and its agents may do. These are non-negotiable.
> حدود صارمة على ما يمكن لـ Dealix ووكلائه فعله. غير قابلة للتفاوض.
>
> Aligned with `docs/00_platform_truth/PLATFORM_TRUTH.md` §3–4 and enforced by
> `auto_client_acquisition/governance_os/draft_gate.py`.

---

## القاعدة العليا — Top rule

كل إجراء خارجي يتطلب موافقة بشرية صريحة. لا استثناءات. القراءة والتصنيف وإعداد المسودات والتوصية مسموحة تحت مراجعة الجودة؛ تنفيذ أي إجراء خارجي محظور أو بموافقة فقط.

Every external action requires explicit human approval. No exceptions. Read, classify, draft, and recommend are allowed under QA; executing any external action is blocked or approval-only.

---

## The forbidden list — القائمة الممنوعة

| # | Forbidden action | الإجراء الممنوع |
|---|---|---|
| 1 | **No auto-send** — no automatic external sending of any message | لا إرسال تلقائي لأي رسالة خارجية |
| 2 | **No cold WhatsApp automation** — no unconsented or automated WhatsApp outreach | لا أتمتة واتساب بارد أو بلا موافقة |
| 3 | **No LinkedIn automation** — no automated connections, messages, or actions | لا أتمتة على لينكدإن |
| 4 | **No scraping** — no harvesting data without permission; no purchased lists | لا كشط بيانات بلا إذن ولا قوائم مشتراة |
| 5 | **No fake proof** — no fabricated testimonials, metrics, or case studies | لا إثبات مزيف أو شهادات مفبركة |
| 6 | **No guaranteed revenue** — never promise sales, results, or ROI as fact | لا وعد بإيراد أو نتائج أو ROI مضمونة |
| 7 | **No customer data used for model training** | لا استخدام بيانات العملاء لتدريب النماذج |
| 8 | **No public case study without approval** — written, signed customer consent first | لا دراسة حالة علنية بلا موافقة موثقة |
| 9 | **Human approval required for every external action** | موافقة بشرية إلزامية لكل إجراء خارجي |
| 10 | **Module status required** — never present a future or non-live module as live | حالة الوحدة إلزامية — لا عرض وحدة غير فعّالة كأنها فعّالة |
| 11 | **Claims Register required** — all copy must pass the Claims Register check | سجل الادعاءات إلزامي — كل نص يمر بفحص السجل |

---

## التفصيل — Detail

### 1–4. Outreach and data
لا نقوم بالكشط، ولا الواتساب البارد، ولا أتمتة لينكدإن، ولا الإرسال الجماعي. هذه ليست خدمات نقدمها أبداً.
We do not scrape, send cold WhatsApp, automate LinkedIn, or blast lists. These are never offered services.

### 5–6. Truth in claims
لا إثبات مزيف ولا أرقام مبيعات مضمونة. كل قيمة "تقديرية" حتى تُتحقَّق. راجع `CLAIMS_REGISTER.md`.
No fake proof and no guaranteed sales numbers. Every value is "estimated" until Verified. See `CLAIMS_REGISTER.md`.

### 7. Data boundaries
بيانات العملاء لا تُستخدم لتدريب النماذج. راجع `DATA_RETENTION.md` و `PDPL_DATA_RULES.md`.
Customer data is never used for model training. See `DATA_RETENTION.md` and `PDPL_DATA_RULES.md`.

### 8. Case studies
لا تُنشر دراسة حالة علنية إلا بموافقة مكتوبة. غير المعتمد يبقى "نموذج افتراضي / Hypothetical, case-safe".
No public case study without written approval. Unapproved stays "Hypothetical / case-safe template".

### 9–11. Governance gates
كل إجراء خارجي يمر عبر `APPROVAL_MATRIX.md` و `HUMAN_IN_THE_LOOP_MATRIX.md`. حالة الوحدات تُحكم بـ `docs/00_platform_truth/MODULE_STATUS.md`.
Every external action passes `APPROVAL_MATRIX.md` and `HUMAN_IN_THE_LOOP_MATRIX.md`. Module status is governed by `docs/00_platform_truth/MODULE_STATUS.md`.

---

## Cross-references — مراجع

- `docs/governance/CLAIMS_REGISTER.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/governance/DATA_RETENTION.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/00_platform_truth/PLATFORM_TRUTH.md`
- `docs/00_platform_truth/MODULE_STATUS.md`

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
