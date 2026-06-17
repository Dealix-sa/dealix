# Dealix — Launch Go / No-Go

> **النوع:** قرار الإطلاق النهائي — هل نطلق أو لا؟ ولماذا؟
> **آخر تحديث:** 2026-06-05
> **القرار الحالي:** 🔴 **NO-GO**
> **المرجع:** [`DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md`](DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md) · [`DEALIX_EXECUTION_BOARD.md`](DEALIX_EXECUTION_BOARD.md)
> **الأمر:** `/dealix-launch-review` يحدّث هذا القرار يوميًا.

---

## 1. Launch Control System (الحالة الحيّة)

| الحقل | القيمة الحالية |
|---|---|
| current launch status | PRE-LAUNCH (PR 1 only) |
| current ICP | TBD (قرار مؤسس #2) — افتراض عامل: وكالات/تسويق B2B |
| current offer | Command Sprint (7-day) |
| current price | 499 SAR (تأسيسي) — قرار مؤسس #3 |
| current pages ready | 0 / 4 core |
| current growth assets ready | 0 |
| current proof count | 0 |
| current paid sprint count | 0 |
| current blockers | قرارات المؤسس #1–#5 + Plan Freeze غير محسومة |
| Go/No-Go decision | 🔴 NO-GO |

---

## 2. بوابات القرار (Go Gates)

القرار = **GO** فقط عندما تكون كل البوابات الإلزامية PASS.

| # | البوابة | إلزامية؟ | الحالة | الدليل |
|---|---------|----------|--------|--------|
| G1 | الخطة مجمّدة (Plan Freeze v1) | نعم | ❌ | بانتظار موافقة المؤسس |
| G2 | القرارات الخمسة الحرجة محسومة | نعم | ❌ | Blueprint §16 |
| G3 | PR 3 (Core Website) مدموج و`npm run build` ينجح | نعم | ❌ | — |
| G4 | كل صفحة عامة: CTA واحد + لا ادعاء مضمون | نعم | ❌ | claims/positioning checkers |
| G5 | Delivery Factory جاهز (`customers/_template/`) | نعم | ❌ | PR 6 |
| G6 | Claims Register + Human Approval Policy موجودة | نعم | ❌ | PR 6 |
| G7 | أول Proof Pack حقيقي مكتمل | نعم (للإطلاق الكامل) | ❌ | — |
| G8 | Business OS Score حيّ (أو spec + مسار تشخيص) | نعم | ❌ | PR 4 |
| G9 | analytics events موصولة | لا (لكن مفضّل) | ❌ | PR 4/7 |
| G10 | CI launch-gates خضراء | نعم | ❌ | PR 7 |
| G11 | لا انتهاك لأي من الـ 11 محرّمًا | نعم (دائم) | ✅ | لا كود مصدري حتى الآن |

---

## 3. مستويات الإطلاق

### 🔓 Soft Launch (الحد الأدنى للبيع) — يتطلب
G1, G2, G3, G4, G5, G6, G8(spec على الأقل), G11.
→ يكفي لاستقبال أول عميل دافع للـ Command Sprint بإثبات وحوكمة.

### 🚀 Full Launch — يتطلب
كل بوابات Soft Launch + G7 (أول Proof Pack) + G10 (CI خضراء) + PR 5 (Growth/Answer Library).

---

## 4. القرار الحالي ولماذا

🔴 **NO-GO.**

**السبب الملزم:** نحن في PR 1 فقط (OS scaffolding). لا توجد صفحات، لا أدوات، لا proof، ولم تُحسم قرارات المؤسس الخمسة ولا تجميد الخطة. بوابات G1–G10 جميعها ❌.

**أقصر مسار إلى GO (Soft Launch):**
1. المؤسس يحسم القرارات الخمسة (#1–#5) ويجمّد الخطة → G1, G2.
2. تنفيذ PR 2 (Brand) ثم PR 3 (Website) + PR 6 (Delivery/Proof — بالتوازي) → G3, G4, G5, G6.
3. PR 4 (Business OS Score على الأقل كـ spec/v1) → G8.
4. أول عميل تأسيسي → أول Proof Pack → G7 → **Full Launch**.

---

## 5. سجل القرارات (Decision Log)

| التاريخ | القرار | السبب | بواسطة |
|---|---|---|---|
| 2026-06-05 | NO-GO | PR 1 فقط؛ قرارات المؤسس غير محسومة؛ G1–G10 ❌ | Dealix OS / blueprint freeze |

> يُحدّث هذا السجل في كل `/dealix-launch-review`. لا يُعلن GO إلا بموافقة مؤسس صريحة مع تحقّق كل البوابات الإلزامية للمستوى المستهدف.
