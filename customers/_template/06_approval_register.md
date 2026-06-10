# 06 — Approval Register — سجلّ الموافقات

**الغرض / Purpose:** تسجيل كل إجراء خارجي يحتاج موافقة بشرية صريحة قبل تنفيذه. لا إجراء خارجي بدون صف هنا. / Log every external action that needs explicit human approval before it happens. No external action without a row here.
**اليوم / Day:** Day 5.
**يُعِدّه / Owner:** Governance lead + Decision owner (customer).

> «القيمة التقديرية ليست قيمة مُتحقَّقة» — *Estimated value is not Verified value.*
> **موافقة بشرية مطلوبة قبل أي إجراء خارجي.** لا auto-send، لا واتساب بارد، لا blast، لا scraping.
> **Human approval is required before every external action.** No auto-send, cold WhatsApp, blasting, or scraping.

---

## 1. مبدأ الموافقة — Approval principle

- Dealix يُعِدّ مسودات جاهزة للمراجعة البشرية فقط / Dealix prepares human-review-ready drafts only.
- لا يُرسَل أي شيء نيابةً عن العميل إلا بموافقة مسجّلة هنا / Nothing is sent on the customer's behalf without an approval recorded here.
- الموافقة تخصّ إجراءً محدّداً ومحتوىً محدّداً — لا موافقة مفتوحة / Approval is for a specific action and specific content — never a blanket approval.

## 2. سجلّ الموافقات — Approval log

| # | الإجراء الخارجي المقترح / Proposed external action | المحتوى/المسودة (مرجع) / Content draft (ref) | يحتاج موافقة؟ / Approval required | المُوافِق (دور) / Approver (role) | القرار / Decision | التاريخ / Date |
|---|---|---|---|---|---|---|
| 1 | [fill] | [fill] | نعم — yes | [fill] | معلّق/موافَق/مرفوض — pending/approved/rejected | [fill] |
| 2 | [fill] | [fill] | نعم — yes | [fill] | [fill] | [fill] |

> كل إجراء خارجي افتراضه «يحتاج موافقة = نعم» حتى يوقّع المُوافِق. Every external action defaults to "approval required = yes" until the approver signs off.

## 3. إجراءات ممنوعة دائماً — Permanently forbidden actions

- ❌ إرسال تلقائي / auto-send — ❌ واتساب بارد / cold WhatsApp — ❌ scraping / blast / قوائم مشتراة.
- هذه لا يجوز اعتمادها حتى بموافقة. These are never approvable, even with sign-off.

---

## الحقول التسعة — Nine fields

| الحقل / Field | القيمة / Value |
|---|---|
| `source` | [fill — request origin] |
| `evidence` | [fill / missing] |
| `assumption` | [fill] |
| `confidence` | low / medium / high — [fill] |
| `recommendation` | [fill — safe framing] |
| `approval_required` | **yes** (this register exists for external actions) |
| `next_action` | [fill — only after approval recorded] |
| `owner` | [fill — role] |
| `due_date` | [fill] |

→ متابعة: [`07_next_action_board.md`](07_next_action_board.md)
