# docs/_archive/2026_pre_revenue — Archived Pre-Revenue Documents

**Purpose:** أرشيف الوثائق التشغيلية الـ pre-revenue (قبل أول دفعة 499 SAR). تبقى للرجوع التاريخي، **ليست active** للعمليات اليومية.

**Master plan:** [/MASTER_PLAN.md](../../../MASTER_PLAN.md)

---

## القاعدة

- لا يُؤرشف ملف هنا إلا بعد التحقق:
  - **لا** ملف من active 25 يُشير إليه (`grep -r "OLD_FILE" docs/`)
  - **لا** commit في آخر 30 يوم لمسه (`git log --since="30 days ago" --oneline -- OLD_FILE`)
- الأرشفة تتم بـ `git mv OLD_PATH docs/_archive/2026_pre_revenue/OLD_FILE` للحفاظ على git history.
- لا حذف فيزيائي. الرجوع متاح دائماً.

---

## موجات التنظيف المُجدوَلة

| الموجة | تاريخ مُقترح | عدد الملفات | المصدر |
|---|---|---|---|
| Wave 1 | 2026-05-24 | (هذه الموجة: 0 ملف فيزيائي — فقط إنشاء 00_ACTIVE indices) | — |
| Wave 2 | 2026-06-26 (آخر أربعاء يونيو) | ~ 10 ملفات | docs/ops/ القديمة |
| Wave 3 | 2026-07-31 | ~ 10 ملفات | docs/sales-kit/ القديمة |
| Wave 4 | 2026-08-28 | ~ 15 ملفات | docs/03_commercial_mvp/ القديمة |
| Waves 5+ | شهرياً | حتى التقليل من 2,238 ملف إلى < 500 | حسب الحاجة |

كل موجة تُنفَّذ في PR منفصل بمراجعة المؤسس قبل الدمج.

---

## السجل (يُحدَّث مع كل موجة)

| Wave | Date | Files Archived | Verified-no-refs | Verified-no-recent-commits | PR |
|---|---|---|---|---|---|
| 1 | 2026-05-24 | 0 (index creation only) | N/A | N/A | (current) |

---

*Version 1.0 — 2026-05-24*
