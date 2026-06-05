# Human Approval Policy — سياسة الاعتماد البشري

**Status: INTERNAL**

> Purpose — الغرض: the human-approval-first policy for Dealix. It defines which actions require founder approval, the approval classes, the division of labor between AI / deterministic workflows / humans, and the audit-trail requirements. Grounded in `auto_client_acquisition/governance_os/` (`approval_matrix`, `claim_safety`, `draft_gate`, `forbidden_actions`) and the Approval Center. Cross-link: [CLAIMS_REGISTER.md](./CLAIMS_REGISTER.md), [../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md](../04_delivery/COMMAND_SPRINT_DELIVERY_OS.md), [../05_founder/FOUNDER_DAILY_COMMAND.md](../05_founder/FOUNDER_DAILY_COMMAND.md).

سياسة "الاعتماد البشري أولاً" في دِيلِكس. تحدّد الإجراءات التي تتطلب اعتماد المؤسس، وفئات الاعتماد، وتوزيع الأدوار بين الذكاء والمهام المُحدَّدة والبشر، ومتطلبات أثر التدقيق.

---

## The core rule — القاعدة الجوهرية

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.
>
> الذكاء يستكشف ويحلّل ويوصي. المهام المُحدَّدة تُنفِّذ. والبشر يعتمدون الالتزامات الخارجية الحرجة.

No layer crosses into another. AI does not send. A deterministic workflow does not invent a claim or commit externally without a human approval recorded first.

لا تتجاوز طبقة حدود الأخرى. الذكاء لا يُرسِل. والمهمة المُحدَّدة لا تُنشئ ادعاءً ولا تلتزم خارجياً دون اعتماد بشري مُسجَّل أولاً.

---

## What requires founder approval — ما يتطلب اعتماد المؤسس

Approval is mandatory, before execution, for:

الاعتماد إلزامي قبل التنفيذ لكل:

- Any customer-facing external action (message, send, publish). — أي إجراء خارجي موجه للعميل.
- Any claim that will appear in customer-facing copy. — أي ادعاء يظهر في مادة موجهة للعميل.
- Any send of any kind — Dealix never auto-sends. — أي إرسال من أي نوع — دِيلِكس لا تُرسِل تلقائياً.
- Any use of PII for external purposes. — أي استخدام لبيانات شخصية خارجياً.
- Any public reference to a customer or case study. — أي إشارة عامة لعميل أو دراسة حالة.

If it leaves Dealix or carries the customer's name outward, it waits for a recorded approval.

إن غادر دِيلِكس أو حمل اسم العميل للخارج، فهو ينتظر اعتماداً مُسجَّلاً.

---

## Approval classes — فئات الاعتماد

Routed deterministically by risk (`approval_matrix.approval_for_action`).

| Class — الفئة | Examples — أمثلة | Risk — الخطورة | Route — المسار |
|---|---|---|---|
| External action — إجراء خارجي | send email, publish — إرسال، نشر | medium–high | human approval |
| Claim — ادعاء | value statement, marketing line | medium | claim QA + human |
| Send — إرسال | any outbound message | medium–high | human approval, never auto |
| Data use (PII) — استخدام بيانات | external use of personal data | high | lawful basis + human |
| Channel — قناة | WhatsApp, outreach channel | high | consent required; cold WhatsApp blocked |

Forbidden by policy and blocked at the gate: cold WhatsApp automation, LinkedIn automation, scraping behind login, bulk outreach, auto-send. These are not approvable — they are blocked.

محظورة بالسياسة ومحجوبة عند البوابة: أتمتة واتساب الباردة، أتمتة لينكدإن، الاستخلاص خلف تسجيل الدخول، التواصل بالجملة، الإرسال التلقائي. هذه لا تُعتمَد — بل تُحجَب.

---

## The approval flow — مسار الاعتماد

1. A workflow proposes an action and attaches its draft. — تقترح المهمة إجراءً وترفق مسودتها.
2. The deterministic scan checks the draft (`claim_safety`, `draft_gate`). Forbidden claim → BLOCK; forbidden term → DRAFT_ONLY. — الفحص المُحدَّد يفحص المسودة.
3. The item enters the Approval Register with its class, evidence tier, and risk. — يدخل العنصر سجل الاعتماد.
4. The founder approves, edits, or rejects, with a one-line reason. — يعتمد المؤسس أو يعدّل أو يرفض بسبب من سطر.
5. Only on approval does the deterministic workflow execute. — لا تُنفِّذ المهمة إلا بعد الاعتماد.
6. The decision and execution are written to the audit trail. — يُكتَب القرار والتنفيذ في أثر التدقيق.

---

## Audit-trail requirements — متطلبات أثر التدقيق

Every approval decision is recorded immutably with:

كل قرار اعتماد يُسجَّل بشكل غير قابل للتعديل مع:

- Item and class. — العنصر وفئته.
- Evidence tier (estimated / observed / verified / client_confirmed). — درجة الدليل.
- Decision (approve / edit / reject) and reason. — القرار والسبب.
- Actor and timestamp. — الفاعل والوقت.
- The executed action's reference, if any. — مرجع الإجراء المُنفَّذ إن وُجد.

The control rule: **every external action must map to a prior recorded approval.** If the log shows a send without an approval, it is a P1 governance incident and leads the next [../05_founder/WEEKLY_BOARD_REVIEW.md](../05_founder/WEEKLY_BOARD_REVIEW.md).

القاعدة الحاكمة: كل إجراء خارجي يجب أن يقابله اعتماد مُسجَّل سابق. وإن ظهر إرسال بلا اعتماد، فهو حادثة حوكمة من الدرجة الأولى.

---

## What stays autonomous — ما يبقى ذاتياً

Low-risk, internal-only, non-claim work runs without per-item approval: internal analysis, draft preparation, ledger reads, the Revenue Map, the Executive Command Brief (internal). These produce drafts and reads, never external commitments.

العمل منخفض الخطورة الداخلي بلا ادعاء يجري دون اعتماد لكل عنصر: التحليل الداخلي، تجهيز المسودات، قراءة السجلات، خريطة الإيرادات، الموجز التنفيذي الداخلي. هذه تُنتج مسودات وقراءات لا التزامات خارجية.

---

This policy is enforced at the gate, not by goodwill. The gate is deterministic; the approval is human.

تُفرَض هذه السياسة عند البوابة لا بحسن النية. البوابة مُحدَّدة، والاعتماد بشري.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
