# Dealix — Execution Board

> **النوع:** لوحة تنفيذ يومية/أسبوعية (ماذا ننفّذ اليوم / هذا الأسبوع).
> **آخر تحديث:** 2026-06-05
> **المرجع:** [`DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md`](DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md) (frozen v1)
> **الأمر اليومي:** `/dealix-launch-review` ثم `/dealix-verify`.

---

## نظرة سريعة (Snapshot)

| المؤشر | القيمة |
|---|---|
| Launch status | PRE-LAUNCH |
| PR in flight | PR 1 (Company OS Scaffolding) |
| Next PR | PR 2 (Brand & Visual Identity) — معلّق على موافقة المؤسس |
| Pages ready | 0 / 4 core |
| Free tools ready | 0 / 3 |
| Proof Packs | 0 |
| Paid Command Sprints | 0 |
| Go/No-Go | **NO-GO** (انظر Go/No-Go doc) |

---

## 🟢 Today
- [x] تنفيذ PR 1: `CLAUDE.md` + 10 commands + الوثائق الثلاث المؤسِّسة.
- [ ] المؤسس يحسم القرارات الخمسة الحرجة (#1–#5 في Blueprint §16).
- [ ] المؤسس يوافق على تجميد الخطة (Plan Freeze v1).

## 📅 This Week
- [ ] موافقة على PR 1 ودمجه.
- [ ] بدء PR 2 (Brand) فور حسم Visual style (قرار #4).
- [ ] تجهيز قائمة "First 30 targets" (يدوي، دافئ — لا scraping).
- [ ] مسودة `sales/COMMAND_SPRINT_ONE_PAGER.md` (تُدمج رسميًا في PR 2/3).

## ⛔ Blocked
- PR 3 (Website) — محجوب على: قرار CTA (#1) + ICP (#2) + Price (#3) + Brand (PR 2).
- PR 4 (Free Tools) — محجوب على: قرار أولوية الأداة (#5).

## ⏳ Waiting for Founder Approval
- تجميد الخطة (Plan Freeze v1).
- القرارات الخمسة الحرجة (#1–#5).
- موافقة دمج PR 1.

## 🔼 Ready for PR
- PR 1 — **جاهز** (هذا الـ commit): وثائق + OS scaffolding فقط، لا كود مصدري.

## 🚀 Ready for Launch
- لا شيء بعد. شرط الإطلاق الأدنى = PR 3 مكتمل + أول Proof Pack (انظر Go/No-Go).

## 🗑️ Deprecated / Stop Doing
- أي توسّع في عدد الصفحات قبل بيع أول Command Sprint.
- أي أتمتة تواصل بارد (WhatsApp/LinkedIn/scraping) — محرّمة دائمًا.
- إعادة التخطيط من الصفر كل جلسة — الخطة مجمّدة v1.

---

## تتبّع الـ PRs

| PR | الحالة | المالك | الـ gate القادم |
|----|--------|--------|------------------|
| PR 1 — Company OS | ✅ READY-FOR-APPROVAL | dealix-pm | موافقة المؤسس |
| PR 2 — Brand | ⏸ BLOCKED (قرار #4) | dealix-content | حسم Visual style |
| PR 3 — Website | ⏸ BLOCKED (PR2 + قرارات #1-3) | dealix-engineer | Brand done |
| PR 4 — Free Tools | ⏸ BLOCKED (قرار #5) | dealix-engineer | أولوية الأداة |
| PR 5 — Growth OS | ⏳ PLANNED | content+engineer | PR 3 done |
| PR 6 — Delivery/Proof | ⏳ PLANNED | dealix-delivery | — (مستقل، يمكن التوازي) |
| PR 7 — CI Gates | ⏳ PLANNED | dealix-engineer | PR 3+5 موجودة |

> ملاحظة: PR 6 (Delivery Factory + Proof + Governance docs) مستقل ولا يلمس كودًا — يمكن تقديمه بالتوازي مع PR 2 لتسريع جاهزية أول عميل دافع (الـ 7-day sellable version).

---

## الإيقاع اليومي للمؤسس (بعد التنفيذ)

| الوقت | الفعل | الأمر |
|---|---|---|
| 08:00 | launch review | `/dealix-launch-review` |
| 08:30 | growth brief | `/dealix-growth-os` (brief) |
| 09:00 | مراجعة top targets | يدوي |
| 10:00 | تواصل دافئ يدوي | يدوي (لا أتمتة) |
| 13:00 | diagnostics | مكالمات |
| 15:00 | delivery | `/dealix-delivery-proof` |
| 17:00 | proof pack | `/dealix-delivery-proof` |
| 18:00 | learning loop | تحديث هذه اللوحة |
