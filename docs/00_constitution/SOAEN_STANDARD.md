# SOAEN Standard — معيار SOAEN

> Version 1 — 2026-05-18 — Canonical documentation of the SOAEN framework
> already enforced in `dealix/commercial_ops/doctrine.py`
> (`SOAEN_FIELDS_AR`, `SOAEN_CHECKLIST_AR`) and surfaced by
> `scripts/founder_soaen_daily.py`. The **code is authoritative**; this doc
> is the human-readable single source of truth that explains it.

This document is the single source of truth for the **SOAEN Standard** — the
governance check applied to every lead, every AI action, and every external
draft at Dealix.

هذه الوثيقة هي المصدر الوحيد للحقيقة لمعيار **SOAEN** — فحص الحوكمة المطبّق
على كل lead، وكل إجراء AI، وكل مسودة خارجية في Dealix.

---

## 1. The five fields — الحقول الخمسة

SOAEN is five questions that must have an answer before any workflow step is
considered governed. Field labels are taken verbatim from
`SOAEN_FIELDS_AR` in `dealix/commercial_ops/doctrine.py`.

| Letter | English | العربية | What it answers |
|---|---|---|---|
| **S** | Source | مصدر | Where did this lead / idea / action originate? (call · Proof · objection) |
| **O** | Owner | مالك | Who owns the next step and the reply to comments? |
| **A** | Approval | موافقة | Was the draft reviewed and approved before it left Dealix? |
| **E** | Evidence | دليل | What proof backs any number or claim? (no revenue without `invoice_paid`) |
| **N** | Next Action | الخطوة التالية | What is the single next step / CTA? |

---

## 2. Operating checklist — قائمة التشغيل

Reproduced verbatim from `SOAEN_CHECKLIST_AR` in
`dealix/commercial_ops/doctrine.py`. Run this before any post or external
draft ships:

- مصدر الفكرة موثّق (call / Proof / اعتراض)
- مالك النشر والرد على التعليقات محدد
- مراجعة المسودة قبل النشر (Approval)
- لا أرقام إيراد بدون دفع مثبت (Evidence)
- CTA واحد: Risk Score أو Sample Proof أو ديمو 10 دقائق (Next Action)

---

## 3. The four governing rules — القواعد الحاكمة الأربع

Use these one-liners in the website, demo, sales calls, and Proof Packs:

- **Lead without an owner is not pipeline.** — Lead بلا owner ليس pipeline.
- **AI action without approval is a risk.** — AI action بلا approval خطر.
- **Dashboard without a next action is a report.** — Dashboard بلا next action تقرير فقط.
- **Follow-up without evidence is not operations.** — Follow-up بلا evidence ليس تشغيل.

---

## 4. Where SOAEN is enforced — أين يُطبّق SOAEN

- `dealix/commercial_ops/doctrine.py` — canonical fields + checklist + daily snapshot.
- `scripts/founder_soaen_daily.py` — daily SOAEN block for the founder digest.
- `tests/test_commercial_doctrine.py` — CI assertion that the checklist and
  the "SOAEN" marker are present in the doctrine snapshot.

---

## 5. Related docs — وثائق ذات صلة

- [NON_NEGOTIABLES.md](NON_NEGOTIABLES.md) — حدود الأمان والثقة
- [../COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md) §3 — the 11 non-negotiables
- [../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md](../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md) — Commercial Proof Mode canonical doc

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
