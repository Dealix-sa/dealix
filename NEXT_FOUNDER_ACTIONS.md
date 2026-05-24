# NEXT FOUNDER ACTIONS — قائمة المؤسس / Founder Action List

**التاريخ / Date:** 2026-05-24
**الفرع / Branch:** `claude/sharp-sagan-TdtJw`
**الحالة / State:** v5 مغلق هندسياً. كل بند أدناه يفتح طبقة جديدة من الإيراد أو الموثوقية. اتّبع الترتيب — العائد الأعلى أولاً.

> هذا الملف هو **مصدر الحقيقة الوحيد** للبنود المعلَّقة على المؤسس. كل وثيقة أخرى تشير إليه. لا تكرّر القائمة في أي مكان آخر — حدِّث هنا فقط.
>
> This file is the **single source of truth** for items waiting on the founder. Every other doc references it. Do not duplicate the list elsewhere — update here only.

---

## 1) Capital Activation — Moyasar live keys (HIGHEST ROI)

**اللوحة / Dashboard:** https://dashboard.moyasar.com

**العنوان (AR):** تفعيل رأس المال — مفاتيح Moyasar الحيّة (أعلى عائد فوري).
**Title (EN):** Capital Activation — Moyasar live keys.

**الخطوات / Steps:**

1. أكمل KYC على لوحة Moyasar: السجل التجاري (CR)، الهوية الوطنية، IBAN، عنوان النشاط. / Complete KYC: CR, National ID, IBAN, business address.
2. اضغط "Submit for review". المراجعة عادة 1–3 أيام عمل. / Submit for review (typically 1–3 business days).
3. عند التفعيل، دوِّر `MOYASAR_SECRET_KEY` من لوحة Moyasar، ثم سلّم المفتاح الجديد للـ ops عبر القناة الآمنة (ضع `<paste-from-dashboard>` في أي ملف يُلتزم به في git). / On activation, rotate `MOYASAR_SECRET_KEY` and send the new key only via secure channel — use literal `<paste-from-dashboard>` in any committed doc.
4. ops يحدّث Railway env عبر GraphQL (المفتاح فقط، لا أكواد كاملة في القناة). / Ops updates Railway env via GraphQL (key only, never full code in chat).
5. اضبط الـ webhook على `https://api.dealix.me/api/v1/webhooks/moyasar` للأحداث: `payment_paid`, `payment_failed`, `payment_refunded`. / Configure webhook for those three events.
6. نفّذ شحنة اختبارية بقيمة 1 ريال (self-charge) ثم تحقّق من رحلة الـ webhook نهاية إلى نهاية. / Run a 1 SAR self-charge and verify webhook round-trip.

**المخرج المتوقع / Expected output:**

- `POST /api/v1/checkout` يُرجع 200 بـ payment_url. / Returns 200 with payment_url.
- الـ webhook يطلق حدث `payment_paid` خلال أقل من 60 ثانية. / Webhook fires `payment_paid` within 60s.
- إدخال جديد في ProofLedger (`docs/proof-events/`). / New ProofLedger entry written.

**سلسلة التبعيات / Dependency chain:**

`KYC → Live keys → 1 SAR self-charge → webhook verified → REVENUE_VERIFIED`

**ما الذي يفتحه / What it unlocks for Dealix:**

- Capital OS → أخضر / green.
- Gate 8 Retainer → أخضر (في `docs/DEALIX_READINESS.md`). / Green in scorecard.
- أوّل فاتورة حقيقية. / First real invoice.
- M-6 يصبح قابلاً للتنفيذ بعد 5 ProofEvents → Postgres ProofLedger swap. / M-6 unblocked toward Postgres swap.
- M-7 يفتح مسار 90 يوم من البيانات التشغيلية للـ role-brief enrichment. / M-7 opens 90-day operating-data path.

---

## 2) Observability — Sentry DSN

**اللوحة / Dashboard:** https://sentry.io

**الخطوات / Steps:**

1. أنشئ مشروعاً باسم `dealix` على Sentry. / Create a project named `dealix`.
2. انسخ DSN (يبدأ بـ `https://...@...ingest.sentry.io/...`). / Copy the DSN.
3. أرسل DSN إلى ops عبر القناة الآمنة. / Send DSN to ops via secure channel.
4. ops يضيفه إلى Railway env عبر GraphQL. / Ops adds it to Railway env via GraphQL.
5. اطلق `/_test_sentry` وتحقّق من ظهور الحدث في واجهة Sentry. / Trigger `/_test_sentry` and verify the event in Sentry UI.

**المخرج المتوقع / Expected output:**

- حدث الاختبار يظهر في Sentry خلال 60 ثانية. / Test event appears in Sentry within 60s.

**ما الذي يفتحه / Unlocks:**

- تنبيهات إنتاج، تنبيهات Slack/email للمؤسس عند الأخطاء، دليل موثوقية للمحادثات المؤسسية. / Prod alerts, founder Slack/email error notifications.

---

## 3) Uptime — UptimeRobot HTTPS monitor

**اللوحة / Dashboard:** https://uptimerobot.com

**الخطوات / Steps:**

1. سجّل دخول / أنشئ حساب. / Sign in / create account.
2. **Add Monitor** → نوع **HTTPS**. / Add HTTPS monitor.
3. URL: `https://api.dealix.me/healthz` (مسار صحّة خفيف). / URL: `https://api.dealix.me/healthz`.
4. الفاصل / Interval: 5 دقائق / 5 minutes.
5. التنبيه على الهاتف والبريد. / Alert via phone + email.
6. احفظ. / Save.

**المخرج المتوقع / Expected output:**

- يصبح المراقب أخضر خلال 5 دقائق. / Monitor goes green within 5 min.
- تنبيه يصل عند أوّل إيقاف يدوي للاختبار. / First manual stop triggers alert.

**ما الذي يفتحه / Unlocks:**

- دليل SLO قابل للعرض في مكالمات المبيعات للشركات. / SLO evidence for enterprise sales conversations.

---

## 4) GTM — First LinkedIn DM (identity-only)

**القالب المصدر / Source template:** `docs/ops/launch_content_queue.md` — DM #1 لعبدالله العسيري (Lucidya, CEO). / DM #1 for عبدالله العسيري · Lucidya · CEO.

**الخطوات / Steps:**

1. افتح LinkedIn من حساب المؤسس الشخصي (هوية حقيقية، بدون أتمتة). / Open LinkedIn on the founder's personal account (real identity, no automation).
2. الصق نص DM #1 كما هو. / Paste DM #1 verbatim.
3. أرسل. / Send.
4. حدِّث `docs/ops/pipeline_tracker.csv` الصف 1: `sent_at=<ISO-timestamp>` و`reply_status=awaiting`. / Update tracker row 1 with ISO timestamp + status.

**المخرج المتوقع / Expected output:**

- إشعار "Seen" أو ردّ خلال 48 ساعة. / Read receipt or reply within 48h.
- احترام قاعدة الـ 48 ساعة للمتابعة (لا إلحاح). / Respect the 48h follow-up rule (no chasing).

**ما الذي يفتحه / Unlocks:**

- Adoption OS → أخضر. / Green.
- Gate 6 Sales PASS → PASS-verified. / Sales gate verified.
- مسار فتح M-9 (تبديل `whatsapp_allow_live_send` للوضع المهيّأ بالـ env بعد العميل #3). / M-9 unblock path.

---

## 5) Warm intros — 3 from founder network

**القائمة المصدر / Source priority list:** `docs/ops/pipeline_tracker.csv` الصفوف 1-5 / rows 1-5 (Lucidya, Foodics, Salla, Lean, BRKZ).

**الخطوات / Steps:**

1. اختر 3 من الشبكة الشخصية بأعلى دفء حقيقي (تعارف سابق، صلة قرابة، مرجع مشترك). / Pick 3 with strongest real warmth (prior intro, common contact, family/region affinity).
2. أرسل رسالة قصيرة ثنائية اللغة من القوالب في `docs/ops/launch_content_queue.md`. / Send a short bilingual message using a template from `docs/ops/launch_content_queue.md`.
3. سجّل `sent_at` لكل صف في `docs/ops/pipeline_tracker.csv`. / Log `sent_at` per row.
4. احترم قاعدة الـ 48 ساعة قبل أي متابعة. / Respect 48h before any follow-up.

**المخرج المتوقع / Expected output:**

- 1 من 3 ترد خلال 7 أيام (وفق رياضيات التحويل التقديرية في `docs/DEALIX_COMPANY_OPERATIONAL_STATE.md`). / 1 of 3 replies within 7 days (per estimated conversion math).

**ما الذي يفتحه / Unlocks:**

- Sales OS → أخضر. / Green.
- مسار العميل #3 → فتح M-9. / Customer #3 path → M-9 default-flag flip.

---

## 6) Verification checklist (run after each unblock)

شغّل الأوامر التالية بعد كل فتح، وسجّل النتائج في `docs/V5_PHASE_E_CHECKLIST.md` إذا كانت متعلّقة بعميل:

Run the following after each unblock; log results in `docs/V5_PHASE_E_CHECKLIST.md` if customer-related:

```bash
python scripts/dealix_smoke_test.py --base-url https://api.dealix.me
python scripts/dealix_status.py
bash scripts/post_redeploy_verify.sh
python scripts/dealix_diagnostic.py --list-bundles
```

**معيار النجاح / Pass criteria:** smoke test ينتهي بـ exit 0، dealix_status يُظهر `live_gates` متّسقة، 22 نقطة في post_redeploy_verify كلها خضراء.

---

## 7) Non-negotiables reminder / تذكير القواعد غير القابلة للتفاوض

- لا شحنة حيّة بدون اختبار 1 ريال جاف أوّلاً. / No live charge without 1 SAR dry-run first.
- لا scraping ولا قوائم اتصال مشتراة. / No scraping or purchased contact lists.
- لا واتساب بارد — `whatsapp_allow_live_send` يبقى default-False. / No cold WhatsApp — `whatsapp_allow_live_send` stays default-False.
- لا أرقام وهمية في أي لوحة. / No fake metrics in any dashboard.
- العربية أوّلاً في كل محتوى للعميل. / AR primary in all customer-facing content.
- التسعير مغلق على Pilot 499 ريال حتى العميل #5. / Pricing locked at 499 SAR Pilot until customer #5.
- لا تفعيل `MOYASAR_ALLOW_LIVE_CHARGE` env flag بدون موافقة المؤسس الصريحة. / No `MOYASAR_ALLOW_LIVE_CHARGE` env flag without founder approval.
- لا رسائل خارجية بنيابة عميل بدون موافقة موثَّقة لكل رسالة. / No outbound messages on a customer's behalf without per-message documented approval.

---

## 8) ماذا يحدث بعد كل فتح / What happens after each unblock (closing the loop)

1. المؤسس يشغّل أوامر التحقّق في القسم 6. / Founder runs the verification commands in §6.
2. المؤسس يحدّث بطاقة `docs/DEALIX_READINESS.md`: البوّابة المعنيّة من **BLOCKED → PASS** مع استشهاد ملف الدليل الجديد. / Founder updates `docs/DEALIX_READINESS.md`: the relevant gate flips **BLOCKED → PASS** with the new evidence-file citation.
3. المؤسس يثبّت التحديث في commit واحد: `git add docs/DEALIX_READINESS.md && git commit -m "gate <N>: <BLOCKED|FIX> → PASS with <evidence-file>"`. / Founder commits the scorecard update with that exact message format.
4. المؤسس يفتح جلسة التكرار التالية (مع ops أو الفريق) لاختيار البند التالي من هذه القائمة. / Founder opens the next-iteration session to pick the next item.

---

## مذكّرة ختامية / Closing memo

هذا الملف هو مصدر الحقيقة الوحيد للبنود المعلَّقة على المؤسس. لا تنفِّذ أي بند من قائمة الـ NOT-IN-SCOPE في `V5_COMPLETION_ROADMAP.md` قبل قراءة هذا الملف.

This file is the single source of truth for items waiting on the founder. Do not execute any item from the NOT-IN-SCOPE list in `V5_COMPLETION_ROADMAP.md` before reading this file.

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
