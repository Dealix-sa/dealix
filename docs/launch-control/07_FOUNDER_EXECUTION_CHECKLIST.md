# Founder Execution Checklist — قائمة تنفيذ المؤسس

> Daily and weekly checkboxes for the founder. Every outreach action is manual and follows approval. No item authorizes automated external sending.
>
> مربعات تحقق يومية وأسبوعية للمؤسس. كل إجراء تواصل يدوي ويتبع الموافقة. لا بند يصرّح بإرسال خارجي آلي.

---

## EN — Daily checklist

- [ ] 08:00 — Generate drafts: `python scripts/commercial_generate_400_drafts.py`
- [ ] 08:15 — Run safety audit; confirm **zero** violations
- [ ] 08:30 — Review `top_50_priority.md`; approve or reject each draft
- [ ] 10:00 — Send approved drafts manually, one at a time
- [ ] 13:00 — Run discovery calls and reply follow-ups
- [ ] 16:00 — Post approved content from `outputs/media_social/` by hand
- [ ] 18:00 — Update CRM stages, reply classification, disqualifications
- [ ] 20:00 — Review `daily_metrics.json`; write tomorrow's top 3 actions
- [ ] Confirm no draft was auto-sent and no forbidden PII was stored

## EN — Weekly checklist

- [ ] Run master verifier: `python scripts/final_launch_control_verify.py`
- [ ] Run secret + risk scan: `python scripts/final_secret_and_risk_scan.py`
- [ ] Run site, API, and CRM static checks
- [ ] Generate / refresh the 30-day content calendar
- [ ] Review reply patterns; improve outreach copy (no PII in notes)
- [ ] Update the Launch Scorecard with the week's evidence
- [ ] Hold one pilot/diagnostic review; record case-safe learnings
- [ ] Confirm the GitHub Actions daily run is green, artifact-only, no secrets
- [ ] Identify the strongest vertical by evidenced opportunities
- [ ] Prepare the weekly summary (and monthly board report at week 4)

---

## AR — القائمة اليومية

- [ ] 08:00 — توليد المسودات: `python scripts/commercial_generate_400_drafts.py`
- [ ] 08:15 — تشغيل تدقيق الأمان؛ تأكيد **صفر** مخالفات
- [ ] 08:30 — مراجعة `top_50_priority.md`؛ اعتماد أو رفض كل مسودة
- [ ] 10:00 — إرسال المسودات المعتمدة يدويًا، واحدة تلو الأخرى
- [ ] 13:00 — إجراء مكالمات الاستكشاف ومتابعات الردود
- [ ] 16:00 — نشر المحتوى المعتمد من `outputs/media_social/` يدويًا
- [ ] 18:00 — تحديث مراحل CRM، تصنيف الردود، الاستبعادات
- [ ] 20:00 — مراجعة `daily_metrics.json`؛ كتابة أعلى 3 إجراءات للغد
- [ ] تأكيد عدم إرسال أي مسودة تلقائيًا وعدم تخزين PII ممنوع

## AR — القائمة الأسبوعية

- [ ] تشغيل المدقق الرئيسي: `python scripts/final_launch_control_verify.py`
- [ ] تشغيل فحص الأسرار والمخاطر: `python scripts/final_secret_and_risk_scan.py`
- [ ] تشغيل فحوصات الموقع والواجهة البرمجية ومخطط CRM الثابتة
- [ ] توليد / تحديث تقويم المحتوى لـ30 يومًا
- [ ] مراجعة أنماط الردود؛ تحسين نص التواصل (دون PII في الملاحظات)
- [ ] تحديث بطاقة قياس الإطلاق بأدلة الأسبوع
- [ ] عقد مراجعة تجريبية/تشخيصية واحدة؛ تسجيل تعلّم آمن للحالة
- [ ] تأكيد أن تشغيل GitHub Actions اليومي أخضر، مخرجات فقط، بدون أسرار
- [ ] تحديد أقوى قطاع بالفرص المُثبتة بأدلة
- [ ] إعداد الملخص الأسبوعي (وتقرير المجلس الشهري في الأسبوع الرابع)

---

Related: [Daily Command Center](05_DAILY_COMMAND_CENTER.md) · [30-Day War Room](04_30_DAY_WAR_ROOM.md) · [Evidence Pack](03_EVIDENCE_PACK.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
