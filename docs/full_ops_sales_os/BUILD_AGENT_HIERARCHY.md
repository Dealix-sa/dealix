# Build Agent Hierarchy — هرم أجينتس وقت-البناء
<!-- WAVE 18 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> هذه أجينتس **Claude Code** في `.claude/agents/` — تبني وتختبر وتطوّر نظام
> Dealix نفسه. ليست أجينتس وقت-التشغيل (تلك في
> [RUNTIME_AGENT_HIERARCHY.md](RUNTIME_AGENT_HIERARCHY.md)).

---

## 1. الهرم — The Pyramid

```
              dealix-pm  (المنسّق — نقطة المسؤولية الوحيدة)
                   │
        ┌──────────┼──────────────┐
   dealix-architect      dealix-governance      ← طبقة التصميم والسياسة
   (يصمّم)               (يحرس الدوكترين)
        │
   ┌────┴────┬───────────┬───────────┬──────────┬──────────┐
 dealix-   dealix-     dealix-     dealix-    dealix-    dealix-
 engineer  frontend    data        sales      content    delivery
        └──────────────┴───────────┴───────────┴──── + dealix-qa (يتحقّق)
                  طبقة التنفيذ
```

عشرة أجينتس: ١ منسّق + ٢ تصميم/سياسة + ٧ تنفيذ.

---

## 2. الأدوار — Roles

| الأجينت | الطبقة | يملك |
|---------|--------|------|
| `dealix-pm` | تنسيق | الخطة، الموجات، التفويض، بوابات القرار، مراجعة الاحتكاك |
| `dealix-architect` | تصميم | معمارية النظام، العقود، حدود الوحدات، توصيف الموجات |
| `dealix-governance` | سياسة | الـ11 non-negotiables، حدّ الأتمتة، هوية الأجينتس، سجلّ التدقيق |
| `dealix-engineer` | تنفيذ | كود Python، موجِّهات FastAPI، الهجرات |
| `dealix-frontend` | تنفيذ | واجهة Next.js 15، Full Ops Console |
| `dealix-data` | تنفيذ | `data_os`، التخصيب، جودة البيانات، السجلّات |
| `dealix-sales` | تنفيذ | حركة المبيعات، التأهيل، عرض المقترحات |
| `dealix-content` | تنفيذ | وثائق ثنائية اللغة، case studies، محتوى |
| `dealix-delivery` | تنفيذ | playbook الـSprint، تجميع Proof Pack، Capital Asset |
| `dealix-qa` | تحقّق | التغطية، بوابات الدوكترين، صحّة CI، الدخان |

---

## 3. نموذج التفويض — Delegation Model

`dealix-pm` هو نقطة الدخول. تسلسل أي موجة:

```
1. dealix-pm        → يقرأ الخطة، يحدّد الموجة، يفتح TodoWrite
2. dealix-architect → يصمّم الموجة، يحدّث docs/full_ops_sales_os/
3. dealix-governance→ يصنّف كل إجراء جديد (A/R/S)، يراجع التصميم
4. dealix-engineer / dealix-data / dealix-frontend → ينفّذون بالتوازي
5. dealix-qa        → يختبر، يشغّل بوابات الدوكترين، يصدر حكم البوابة
6. dealix-pm        → يلتزم ويدفع، أو يعيد للخطوة المناسبة
```

التفويض المتوازي مسموح حين لا توجد تبعية (engineer + data + frontend معاً).

---

## 4. القواعد المشتركة — Shared Rules

كل أجينت من العشرة:

- يحترم الـ11 non-negotiables؛ يرفض الطلب المخالف ويقترح بديلاً آمناً.
- لا يرسل اتصالاً خارجياً، لا يشحن العميل (Moyasar live بيد المؤسس).
- يوسّع الوحدات القانونية ولا يعيد تسميتها.
- يبلّغ بصدق — لا تضخيم تقدّم، لا claim أخضر غير حقيقي.

`dealix-qa` و`dealix-governance` لهما حقّ النقض: لا موجة تُغلَق ببوابة حمراء.

---

## 5. خرائط — Maps

- معمارية النظام → [ARCHITECTURE.md](ARCHITECTURE.md)
- أجينتس وقت-التشغيل → [RUNTIME_AGENT_HIERARCHY.md](RUNTIME_AGENT_HIERARCHY.md)
- خطة الموجات → [WAVE_PLAN.md](WAVE_PLAN.md)
- ملفّات الأجينتس → `.claude/agents/dealix-*.md`

---

*Version 1.0 | 10 build-time agents | dealix-qa + dealix-governance hold veto.*
