# Delivery Operating System — نظام تشغيل التسليم

How work gets done after a deal closes. AI drafts and ranks; the client's team reviews and acts.

## Delivery loop — حلقة التسليم

**English.** Intake → AI drafts → human review → manual action → measure → log. The loop repeats per workflow. Nothing is sent externally by the system.

**عربي.** الاستلام ← مسودات الذكاء الاصطناعي ← مراجعة بشرية ← إجراء يدوي ← قياس ← تسجيل. الحلقة تتكرر لكل سير عمل. لا شيء يُرسَل خارجيًا من النظام.

## Roles — الأدوار

| Role | Responsibility |
|---|---|
| Dealix delivery lead | Configure drafts, set review steps |
| Client reviewer | Approve or edit each draft |
| Client sender | Send manually after approval |
| Founder | Governance and value ledger |

## Review steps — خطوات المراجعة

**English.** Each draft passes a role-based review before use. Higher-risk documents get a second reviewer. See [APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md).

**عربي.** تمرّ كل مسودة بمراجعة حسب الدور قبل الاستخدام. المستندات الأعلى مخاطرة تحصل على مراجع ثانٍ.

## Value ledger — سجل القيمة

**English.** We log estimated time saved per workflow, then observed results during delivery, then verified value at handover. See [VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md).

**عربي.** نسجّل الوقت المُوفَّر التقديري لكل سير عمل، ثم النتائج المُلاحَظة أثناء التنفيذ، ثم القيمة المُتحقَّقة عند التسليم.

## Quality gates — بوابات الجودة

- No draft used without review.
- No forbidden phrases in any client-facing output.
- Estimated value labeled.

لا مسودة تُستخدم دون مراجعة. لا عبارات محظورة في أي مُخرَج للعميل. القيمة التقديرية مُوسومة.

## Cross-links — روابط

- [15_PILOT_DELIVERY_CHECKLIST.md](15_PILOT_DELIVERY_CHECKLIST.md)
- [16_HANDOVER_SUCCESS_REPORT.md](16_HANDOVER_SUCCESS_REPORT.md)
- [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
