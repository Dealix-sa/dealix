# Launch Go-Live Runbook — كتيب قرار الإطلاق والتشغيل المباشر

> **Status / الحالة:** Verified state as of 2026-05-18 — حالة متحقَّقة بتاريخ 2026-05-18
> **Owner / المالك:** Founder — المؤسس
> **Supersedes / يحل محل:** [`PUBLIC_LAUNCH_CHECKLIST.md`](PUBLIC_LAUNCH_CHECKLIST.md) — that file is now folded into Section 2 below.

**EN —** This is the single executable document for the launch decision. It answers
one question: *are we ready to officially launch — yes or no?* It then drives the
launch itself. It consolidates the public launch checklist, the 11 readiness gates,
and the commercial gates into one place.

**AR —** هذا هو المستند التنفيذي الوحيد لقرار الإطلاق. يجيب عن سؤال واحد:
*هل نحن جاهزون للإطلاق الرسمي — نعم أم لا؟* ثم يقود الإطلاق نفسه. يجمع قائمة
التدشين العامة، وبوابات الجاهزية الإحدى عشرة، والبوابات التجارية في مكان واحد.

**Non-negotiables held in this runbook / الثوابت المحكومة في هذا الكتيب:**
human approval before any external send; no scraping; estimates labelled;
bilingual AR+EN; no PII — موافقة بشرية قبل أي إرسال خارجي؛ لا scraping؛ القيم
التقديرية موسومة؛ ثنائي اللغة؛ لا بيانات شخصية.

---

## 1. Go/No-Go Verdict — جدول قرار الإطلاق

**EN —** Launch is GO only when every row marked **launch-critical** is `DONE`.
A single `BLOCKED` row in a launch-critical line forces NO-GO.

**AR —** الإطلاق يكون "نعم" فقط عندما يكون كل بند **حرج للإطلاق** بحالة `DONE`.
وجود بند واحد `BLOCKED` في سطر حرج يفرض "لا".

| # | Item — البند | Launch-critical | Status | Owner — المالك |
|---|---------------|-----------------|--------|----------------|
| 1 | Production API live (`https://api.dealix.me`, v3.0.0, env=production) — واجهة الإنتاج | Yes | DONE | Founder |
| 2 | Landing site live (`https://dealix.me`, 77 static pages) — موقع التعريف | Yes | DONE | Founder |
| 3 | Backend CI quick-regression gate green (94 passed, 1 skipped) — بوابة CI | Yes | DONE | Founder |
| 4 | Approval-gated autonomy engine wired, `draft_only` mode — محرك الأتمتة المحكوم | Yes | DONE | Founder |
| 5 | **Moyasar payment KYC active** — تفعيل KYC للمدفوعات | Yes | **BLOCKED** | Founder |
| 6 | Frontend console deployed to a host — نشر واجهة الكونسول | Yes | PENDING | Founder |
| 7 | Sentry `SENTRY_DSN` configured — تهيئة Sentry | Yes | PENDING | Founder |
| 8 | UptimeRobot monitoring on API + landing — مراقبة التوفّر | Yes | PENDING | Founder |
| 9 | `RESEND_API_KEY` set for founder daily digest — مفتاح بريد الملخّص | No | PENDING | Founder |
| 10 | `DEALIX_API_BASE` / `DEALIX_API_KEY` GitHub secrets for revenue-machine cron — أسرار الجدولة | No | PENDING | Founder |
| 11 | LinkedIn / X social API keys — مفاتيح النشر الاجتماعي | No | PENDING | Founder |
| 12 | Legal pack published (privacy, terms, DPA, PDPL procedures) — الحزمة القانونية | Yes | PENDING | Founder |
| 13 | Public pricing page consistent with `pricing.py` — صفحة التسعير | Yes | PENDING | Founder |
| 14 | Backup + restore test passed — اختبار النسخ والاستعادة | Yes | PENDING | Founder |
| 15 | Broader pytest debt tracked (~59 pre-existing failures) — متابعة الدين التقني | No | PENDING | Founder |

**Current verdict — القرار الحالي: `NO-GO`.**
**EN —** Reason: row 5 (Moyasar KYC) is `BLOCKED`. Dealix cannot collect live
payment, and the commercial gate "no revenue before payment" cannot be satisfied.
Rows 6, 7, 8, 12, 13, 14 are launch-critical and `PENDING`.

**AR —** السبب: البند 5 (KYC ميسّر) بحالة `BLOCKED`. لا يمكن لـDealix تحصيل
مدفوعات مباشرة، ولا يمكن استيفاء البوابة التجارية "لا إيراد قبل الدفع".
البنود 6 و7 و8 و12 و13 و14 حرجة وما زالت `PENDING`.

---

## 2. Consolidated Pre-Launch Checklist — قائمة ما قبل الإطلاق الموحّدة

**EN —** This merges and replaces [`PUBLIC_LAUNCH_CHECKLIST.md`](PUBLIC_LAUNCH_CHECKLIST.md).
Status reflects the verified state of 2026-05-18.

### Legal — قانوني

- [ ] Privacy policy published — سياسة خصوصية منشورة *(PENDING)*
- [ ] Terms of use published — شروط استخدام *(PENDING)*
- [ ] Company DPA available — اتفاقية معالجة بيانات للشركات *(PENDING)*
- [ ] PDPL procedures (export / delete / suppress) documented and tested — إجراءات PDPL موثقة ومُختبرة *(PENDING)*

### Product — منتج

- [x] Production API live, version 3.0.0, env=production, providers=[groq] — واجهة الإنتاج مباشرة *(DONE)*
- [x] Landing site live, 77 static pages on GitHub Pages — موقع التعريف مباشر *(DONE)*
- [ ] Frontend console deployed (Next.js 15, currently builds/typechecks/lints clean, not hosted) — نشر الكونسول *(PENDING)*
- [ ] Public pricing page consistent with `pricing.py` and `PRICING_STRATEGY.md` — صفحة تسعير متسقة *(PENDING)*
- [ ] Repeatable onboarding (self-serve or internal sales) — onboarding قابل للتكرار *(PENDING)*
- [ ] Clear usage limits (rate limits, quotas) documented — حدود استخدام واضحة *(PENDING)*

### Billing — فوترة

- [ ] **Moyasar payment account KYC active** — تفعيل KYC لحساب ميسّر *(BLOCKED — P0)*
- [ ] Moyasar webhooks monitored — مراقبة webhooks *(PENDING — depends on KYC)*
- [ ] Invoice + refund process defined — مسار الفواتير والاسترداد *(PENDING)*

### Ops — تشغيل

- [x] Backend CI quick-regression gate green — بوابة CI خضراء *(DONE — 94 passed, 1 skipped)*
- [ ] SLOs defined (uptime, API latency) — أهداف مستوى الخدمة *(PENDING)*
- [ ] UptimeRobot monitoring on API + landing — مراقبة التوفّر *(PENDING)*
- [ ] Sentry `SENTRY_DSN` configured (code wired, no-ops until set) — تهيئة Sentry *(PENDING)*
- [ ] On-call + runbooks linked (`docs/ops/DEPLOY_NOW.md`, `docs/ops/`) — استدعاء وكتيبات *(PENDING)*
- [ ] Backup + restore test passed — نسخ احتياطي واختبار استعادة *(PENDING)*
- [ ] `RESEND_API_KEY` set for daily founder digest — مفتاح الملخّص اليومي *(PENDING — degrades gracefully)*
- [ ] `DEALIX_API_BASE` / `DEALIX_API_KEY` GitHub secrets for daily revenue-machine cron — أسرار الجدولة *(PENDING — degrades gracefully)*

### GTM — الانطلاق للسوق

- [ ] "First 100" path active from `docs/GTM_PLAYBOOK.md` — مسار «أول 100» *(PENDING)*
- [ ] Agency partnerships defined if applicable — شراكات وكالة عند الانطباق *(PENDING)*
- [ ] LinkedIn / X social API keys (manual posting works without them) — مفاتيح النشر الاجتماعي *(PENDING — optional)*
- [ ] Repeatable successful pilot evidenced — تجربة pilot ناجحة متكررة بدليل *(PENDING)*

### Autonomy guardrails — ضوابط الأتمتة

- [x] Autonomy engine runs `draft_only`; no automated cold sends — المحرك في وضع المسودة فقط *(DONE)*
- [x] All external sends require explicit approval via `/api/v1/approvals/*` — كل إرسال خارجي يمر بموافقة *(DONE)*
- [x] No scraping, no cold WhatsApp/LinkedIn automation in any offered service — لا scraping ولا أتمتة تواصل بارد *(DONE)*
- [x] Estimated values labelled "Estimated value is not Verified value" — القيم التقديرية موسومة *(DONE — enforced in templates)*

> Commercial guardrails reference — البوابات التجارية: [`empire/COMMERCIAL_GATES.md`](empire/COMMERCIAL_GATES.md).
> Rule held: **no revenue before payment** — قاعدة محكومة: لا إيراد قبل الدفع.

### "Ready for Public Launch" criteria — معيار «جاهز للإطلاق العام»

- [ ] Repeatable successful pilot — تجربة pilot ناجحة متكررة *(PENDING)*
- [x] CI green on the required quick-regression gate — CI أخضر على البوابة المطلوبة *(DONE)*
- [ ] External security review (recommended) — مراجعة أمنية خارجية (موصى بها) *(PENDING)*

> **Tech-debt note — ملاحظة الدين التقني:** the broader pytest suite has ~59
> pre-existing failures (environment-dependent + stale tests out of sync with
> refactored code). These are not blockers for the required CI gate but must be
> tracked. — حزمة الاختبارات الأوسع بها نحو 59 إخفاقاً مسبقاً؛ ليست معرقلات
> للبوابة المطلوبة لكنها تتطلّب متابعة.

---

## 3. The 11-Gate Summary — ملخّص البوابات الإحدى عشرة

**EN —** Each gate has a dedicated certificate file. Update Status / Score in each
file before launch; this table is the index. Verification script:
[`../scripts/verify_dealix_ready.py`](../scripts/verify_dealix_ready.py).

**AR —** لكل بوابة ملف شهادة مستقل. حدّث الحالة والنتيجة في كل ملف قبل الإطلاق؛
هذا الجدول هو الفهرس.

| Gate | Name — الاسم | Pass bar | Gate file | Status |
|------|---------------|----------|-----------|--------|
| 0 | Founder Clarity — وضوح المؤسس | ≥ 85 | [`readiness/gate_0_founder_clarity.md`](readiness/gate_0_founder_clarity.md) | Update before launch |
| 1 | Offer Readiness — جاهزية العرض | ≥ 85 / offer | [`readiness/gate_1_offer_readiness.md`](readiness/gate_1_offer_readiness.md) | Update before launch |
| 2 | Delivery Readiness — جاهزية التسليم | ≥ 85 | [`readiness/gate_2_delivery_readiness.md`](readiness/gate_2_delivery_readiness.md) | Update before launch |
| 3 | Product Readiness — جاهزية المنتج | ≥ 80 MVP | [`readiness/gate_3_product_readiness.md`](readiness/gate_3_product_readiness.md) | Update before launch |
| 4 | Governance Readiness — جاهزية الحوكمة | ≥ 90 | [`readiness/gate_4_governance_readiness.md`](readiness/gate_4_governance_readiness.md) | Update before launch |
| 5 | Demo Readiness — جاهزية العرض التوضيحي | ≥ 85 | [`readiness/gate_5_demo_readiness.md`](readiness/gate_5_demo_readiness.md) | Update before launch |
| 6 | Sales Readiness — جاهزية المبيعات | ≥ 85 | [`readiness/gate_6_sales_readiness.md`](readiness/gate_6_sales_readiness.md) | Update before launch |
| 7 | Client Delivery Readiness — جاهزية تسليم العميل | Pass | [`readiness/gate_7_client_delivery_readiness.md`](readiness/gate_7_client_delivery_readiness.md) | Update before launch |
| 8 | Retainer Readiness — جاهزية العقد المستمر | ≥ 85 | [`readiness/gate_8_retainer_readiness.md`](readiness/gate_8_retainer_readiness.md) | Update before launch |
| 9 | Scale Readiness — جاهزية التوسّع | ≥ 85 | [`readiness/gate_9_scale_readiness.md`](readiness/gate_9_scale_readiness.md) | Update before launch |
| 10 | World-Class Readiness — معيار طموح | aspirational | [`readiness/gate_10_world_class_readiness.md`](readiness/gate_10_world_class_readiness.md) | Update before launch |

**Launch sell-rule — قاعدة البيع عند الإطلاق:** sell officially only what passed
Gates 0, 1, 2, 4, 5, 6 plus Gate 3 as MVP. — بِع رسمياً فقط ما اجتاز البوابات
0 و1 و2 و4 و5 و6 إضافة إلى البوابة 3 كـMVP. Index: [`readiness/README.md`](readiness/README.md).

---

## 4. Launch-Day Sequence — تسلسل يوم الإطلاق

**EN —** Execute strictly in order. Do not advance to the next step until the
current step is confirmed. Each step has a verify action.

**AR —** نفّذ بالترتيب الصارم. لا تنتقل للخطوة التالية قبل تأكيد الحالية.
لكل خطوة فعل تحقّق.

| Step | Action — الإجراء | Verify — التحقق |
|------|------------------|-----------------|
| 1 | Confirm Moyasar KYC active and live keys in place — تأكيد تفعيل KYC | Test charge in Moyasar sandbox-to-live, then refund it |
| 2 | Publish legal pack (privacy, terms, DPA, PDPL) and link from landing footer — نشر الحزمة القانونية | Open each URL, confirm HTTP 200 |
| 3 | Publish public pricing page; confirm it matches `pricing.py` — نشر صفحة التسعير | Diff page values against `pricing.py` |
| 4 | Deploy frontend console to host; set API base to `https://api.dealix.me` — نشر الكونسول | Load console, confirm login + API call succeed |
| 5 | Set `SENTRY_DSN` on API; trigger a test error — تهيئة Sentry | Confirm event appears in Sentry |
| 6 | Configure UptimeRobot monitors for API health + landing — تهيئة المراقبة | Confirm both monitors report UP |
| 7 | Set `RESEND_API_KEY` and GitHub secrets `DEALIX_API_BASE` / `DEALIX_API_KEY` — تهيئة الأسرار | Run digest + revenue-machine cron once manually |
| 8 | Run backup, then a restore drill to a scratch environment — اختبار الاستعادة | Confirm restored data integrity |
| 9 | Re-run `python scripts/verify_dealix_ready.py` and update the 11 gate files — إعادة التحقق | All launch-critical gates PASS |
| 10 | Flip Section 1 verdict to `GO`; record date and approver — تحويل القرار إلى نعم | Verdict table updated |
| 11 | Announce launch — drafted in `draft_only`, approved manually via `/api/v1/approvals/*`, then sent — إعلان الإطلاق | No automated cold sends; every post human-approved |

> **Guardrail — ضابط:** step 11 announcement copy is generated as a draft only.
> No external message leaves Dealix without explicit human approval. — نسخة
> الإعلان تُولَّد كمسودة فقط؛ لا تخرج أي رسالة خارجية دون موافقة بشرية صريحة.

---

## 5. First 72 Hours Watch — مراقبة أول 72 ساعة

**EN —** Monitor these signals every 6 hours for the first 72 hours. A threshold
breach triggers the matching action in Section 6.

**AR —** راقب هذه المؤشرات كل 6 ساعات خلال أول 72 ساعة. تجاوز العتبة يُفعّل
الإجراء المقابل في القسم 6.

| Signal — المؤشر | Source — المصدر | Healthy — سليم | Rollback trigger — عتبة التراجع |
|-----------------|------------------|----------------|--------------------------------|
| API health — صحة الواجهة | `https://api.dealix.me` health endpoint | HTTP 200 | Non-200 for > 5 min |
| API latency — زمن الاستجابة | UptimeRobot | p95 stable | p95 doubles vs baseline > 15 min |
| Error rate — معدّل الأخطاء | Sentry | Near zero new issues | New unhandled error affecting payments or auth |
| Payment success — نجاح الدفع | Moyasar dashboard + webhooks | Charges succeed, webhooks received | Any failed charge or missing webhook |
| Landing site — الموقع | UptimeRobot | HTTP 200 | Down > 10 min |
| Autonomy mode — وضع الأتمتة | Approvals queue `/api/v1/approvals/*` | All sends `draft_only`, queued for approval | Any send dispatched without an approval record |
| Founder digest — الملخّص اليومي | Daily Resend email | Arrives once daily | Two consecutive missed digests |

**Watch discipline — انضباط المراقبة:** log every check with timestamp and
result. Estimated impact figures in any launch report are labelled estimates —
كل قيمة أثر في أي تقرير إطلاق موسومة كقيمة تقديرية.

---

## 6. Rollback Plan — خطة التراجع

**EN —** Rollback is reversible and staged. Prefer the narrowest action that
removes the risk. Founder approves any rollback before execution.

**AR —** التراجع قابل للعكس ومرحلي. فضّل أضيق إجراء يزيل الخطر. المؤسس يعتمد
أي تراجع قبل تنفيذه.

| Failure — العطل | Rollback action — إجراء التراجع |
|-----------------|--------------------------------|
| Payment / Moyasar failure — عطل المدفوعات | Disable the public pricing/checkout link; revert to manual invoicing; keep API live. الدفع متوقف، الواجهة تبقى مباشرة |
| API regression — انحدار الواجهة | Redeploy the last known-good API release; if unavailable, hold at maintenance page; follow `docs/ops/DEPLOY_NOW.md` |
| Frontend console broken — كسر الكونسول | Take the console offline; landing site and API stay live; console is not required for API customers |
| Autonomy sends a message without approval — إرسال بلا موافقة | Halt all automation crons immediately; confirm engine returns to `draft_only`; audit `/api/v1/approvals/*` log; do not resume until cause is fixed |
| Sentry / monitoring blind — انقطاع المراقبة | Switch to manual 30-minute health checks until monitoring restored |
| Legal page error or PDPL gap — خطأ قانوني | Unpublish the affected page; pause new signups until corrected |

**Full launch abort — إلغاء الإطلاق الكامل:** if two or more launch-critical
signals breach at once, revert Section 1 verdict to `NO-GO`, take the pricing
page offline, notify any active customers in plain language, and re-enter at
Section 4 step 1 after the root cause is fixed. — عند تجاوز مؤشرين حرجين أو
أكثر معاً، أعِد القرار إلى "لا"، وأوقف صفحة التسعير، وأبلغ العملاء النشطين
بلغة واضحة، وأعِد الدخول من القسم 4 الخطوة 1 بعد إصلاح السبب الجذري.

---

## Cross-links — روابط ذات صلة

- [`PUBLIC_LAUNCH_CHECKLIST.md`](PUBLIC_LAUNCH_CHECKLIST.md) — superseded by Section 2
- [`readiness/README.md`](readiness/README.md) — 11-gate certificate index
- [`empire/COMMERCIAL_GATES.md`](empire/COMMERCIAL_GATES.md) — commercial proof gates
- [`../DEALIX_READINESS.md`](../DEALIX_READINESS.md) — readiness control center
- [`GTM_PLAYBOOK.md`](GTM_PLAYBOOK.md) — "First 100" go-to-market path
- [`ops/DEPLOY_NOW.md`](ops/DEPLOY_NOW.md) — deploy / on-call runbook

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
