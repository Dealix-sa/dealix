# Paid Sprint Handoff — تسليم السبرنت المدفوع

> Purpose — الغرض: the SOP for moving a customer from sales into a paid Command Sprint. It defines the prerequisites that must be true before any delivery starts, the customer workspace files that get opened, the day-by-day flow, and the definition of done.
>
> إجراء تشغيلي قياسي لنقل العميل من البيع إلى سبرنت القيادة المدفوع. يحدد الشروط المسبقة قبل بدء أي تنفيذ، وملفات مساحة عمل العميل التي تُفتَح، والتدفق يومًا بيوم، وتعريف الإنجاز.

Cross-link: [DELIVERY_DAILY_RHYTHM.md](./DELIVERY_DAILY_RHYTHM.md), [PROOF_TO_UPSELL_PLAYBOOK.md](./PROOF_TO_UPSELL_PLAYBOOK.md), [COMMAND_SPRINT_TERMS.md](../../sales/COMMAND_SPRINT_TERMS.md), [NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md](../03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md), [SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md).

---

## Prerequisites — الشروط المسبقة

No delivery starts until all three are true and recorded:

- **Payment confirmed** — a `payment_received` event exists in `data/revenue/payments.jsonl` for this customer and tier.
- **Source Passport** — the customer's data has a completed Source Passport: provenance, permission, and PII classification established. No passport, no data work.
- **Scope signed** — the customer has reviewed and accepted the Command Sprint scope. The signed scope lives in the workspace as `03_command_sprint_scope`.

لا يبدأ التنفيذ حتى تتحقق الشروط الثلاثة وتُسجَّل: تأكيد الدفع (حدث `payment_received`)؛ جواز المصدر مكتمل (المنشأ، الإذن، تصنيف البيانات الشخصية) — بلا جواز لا عمل على البيانات؛ النطاق موقَّع ومحفوظ في `03_command_sprint_scope`.

---

## Customer workspace files — ملفات مساحة عمل العميل

The workspace is created with `create_customer_workspace.py` under `customers/<name>/`. The handoff touches these files in order:

| File | Role |
|---|---|
| `00_intake` | what the customer said they need; sector, city, goal |
| `01_source_passport` | provenance, permission, PII classification |
| `02_diagnostic_summary` | the free-diagnostic scorecard result that led here |
| `03_command_sprint_scope` | signed scope: what is and is not in the sprint |

تُنشأ مساحة العمل عبر `create_customer_workspace.py` تحت `customers/<name>/`. يلمس التسليم بالترتيب: الاستقبال؛ جواز المصدر؛ ملخص التشخيص؛ نطاق السبرنت الموقَّع.

---

## Day-by-day — يومًا بيوم

The Command Sprint runs across a short fixed window. A typical shape:

- **Day 1 — Setup.** Confirm prerequisites, open `09_delivery_log.md`, restate scope in the customer's words, agree the single outcome the sprint proves.
- **Day 2 — Data and structure.** Work only on passported data. Build the structure the outcome needs. Capture evidence as you go.
- **Day 3 — Build and govern.** Produce the deliverable. Every external-facing artifact is queued as a draft; nothing is sent without founder approval.
- **Day 4 — Proof pack.** Assemble `10_proof_pack.md`: what was done, what was observed, limitations, value tier.
- **Day 5 — Review and close.** Walk the customer through the proof pack; log the proof event; record the definition-of-done check.

يمتد السبرنت على نافذة قصيرة ثابتة: الإعداد؛ البيانات والبنية؛ البناء والحوكمة (كل ناتج خارجي مسودة بانتظار الموافقة)؛ حزمة الإثبات؛ المراجعة والإغلاق.

---

## Definition of done — تعريف الإنجاز

The sprint is done only when all of these are true:

- The agreed single outcome is delivered and demonstrable.
- `10_proof_pack.md` exists with an honest limitations section and a value tier (estimated / observed / verified / client_confirmed).
- A `proof_pack_delivered` revenue event is logged.
- No external action was taken without a logged approval.
- The customer has seen the proof pack and the next-offer recommendation is queued in `11_upsell_recommendation.md` — but only because a real proof pack now exists.

يكون السبرنت منجَزًا فقط عند: تسليم النتيجة المتفق عليها وقابليتها للعرض؛ وجود `10_proof_pack.md` بقسم قيود صادق وطبقة قيمة؛ تسجيل حدث تسليم الإثبات؛ عدم وجود إجراء خارجي بلا موافقة مُسجَّلة؛ ومراجعة العميل للحزمة قبل أي توصية بيع إضافي.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
