# Launch Scorecard — بطاقة قياس الإطلاق

> Scores below are working estimates for founder planning. The authoritative numeric audit is produced by `scripts/final_launch_control_verify.py`. Axes that depend on external setup (live SEO ranking, paid ads, live server) are scored lower on purpose.
>
> الدرجات أدناه تقديرات عمل لتخطيط المؤسس. التدقيق الرقمي المرجعي ينتجه `scripts/final_launch_control_verify.py`. المحاور التي تعتمد على إعداد خارجي (ترتيب SEO الحي، الإعلانات المدفوعة، الخادم الحي) تُمنح درجة أقل عمدًا.

---

## EN — Scorecard

| Axis | Score /100 | Evidence | Blockers | Owner | Next action |
|---|---|---|---|---|---|
| Website | 80 | `scripts/site_launch_static_check.py` | Final copy review, live deploy | Founder | Run static check, deploy to production |
| SEO | 45 | site metadata in static check | No live ranking yet; needs time + backlinks | Founder | Submit sitemap, track first indexed pages |
| Commercial Offer | 85 | `docs/03_commercial_mvp/*`, offer ladder | Pricing copy on site | Founder | Confirm ladder on pricing page |
| First 5 Verticals | 80 | `outputs/commercial_launch/latest/draft_queue.jsonl` | Real leads not yet loaded | Founder | Load first 100 real leads |
| Draft Factory | 90 | `scripts/commercial_generate_400_drafts.py`, draft_queue.jsonl | None — review-only by design | Founder | Run daily, confirm 400+ count |
| Founder Review | 85 | `outputs/commercial_launch/latest/founder_review.md`, `top_50_priority.md` | Depends on daily founder time | Founder | Review top 50 each morning |
| Media OS | 75 | `outputs/media_social/`, calendar config | Press kit assets pending | Founder | Approve content pillars |
| Social OS | 70 | `scripts/media_social_calendar_generate.py` | Manual posting cadence to confirm | Founder | Generate 30-day calendar |
| Ads OS | 30 | `docs/media-social-os/15_ADS_READINESS_GATE.md` | Tracking, UTM, conversion event, budget all pending | Founder | Complete ads readiness gate before any spend |
| CRM OS | 85 | `scripts/commercial_crm_schema_verify.py`, `config/crm_pipeline_schema.json` | Real lead data | Founder | Run schema verify, load leads |
| Delivery OS | 75 | `docs/03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md` | First diagnostic not yet delivered | Founder | Deliver first paid diagnostic |
| Compliance | 85 | `config/crm_pipeline_schema.json` rules, PDPL docs | Consent capture in live flow | Founder | Confirm suppression + consent process |
| Safety | 90 | `scripts/commercial_safety_audit.py`, `safety_audit.json` | None known | Founder | Run audit daily, keep zero violations |
| GitHub Actions | 85 | `.github/workflows/final-launch-control.yml` | Artifact-only; no secrets by design | Founder | Confirm daily run is green |
| Server / API | 60 | `scripts/api_commercial_static_check.py` | Static scan only; no live server proven here | Founder | Run static check; verify /health separately |
| Documentation | 85 | `docs/launch-control/*`, `docs/commercial-launch/*` | Cross-links to confirm | Founder | Review doc set |
| Tests | 70 | repo test suite | Coverage for new launch scripts | Founder | Run full suite, record result |
| External Requirements | 50 | this scorecard | Domain, hosting, payment, ad accounts pending | Founder | Track external setup checklist |

---

## AR — بطاقة القياس

| المحور | الدرجة /100 | الدليل | المعوّقات | المسؤول | الإجراء التالي |
|---|---|---|---|---|---|
| الموقع | 80 | `scripts/site_launch_static_check.py` | مراجعة النص النهائي، النشر الحي | المؤسس | تشغيل الفحص الثابت والنشر للإنتاج |
| SEO | 45 | بيانات الموقع الوصفية في الفحص الثابت | لا ترتيب حي بعد؛ يحتاج وقتًا وروابط | المؤسس | إرسال خريطة الموقع وتتبع أول صفحات مفهرسة |
| العرض التجاري | 85 | `docs/03_commercial_mvp/*`، سلّم العروض | نص التسعير على الموقع | المؤسس | تأكيد السلّم في صفحة التسعير |
| القطاعات الخمسة الأولى | 80 | `outputs/commercial_launch/latest/draft_queue.jsonl` | لم تُحمَّل عملاء حقيقيون بعد | المؤسس | تحميل أول 100 عميل حقيقي |
| مصنع المسودات | 90 | `scripts/commercial_generate_400_drafts.py` | لا شيء — للمراجعة فقط بالتصميم | المؤسس | التشغيل يوميًا وتأكيد عدد 400+ |
| مراجعة المؤسس | 85 | `founder_review.md`، `top_50_priority.md` | يعتمد على وقت المؤسس اليومي | المؤسس | مراجعة أعلى 50 كل صباح |
| نظام الإعلام | 75 | `outputs/media_social/` | أصول الحقيبة الصحفية معلقة | المؤسس | اعتماد ركائز المحتوى |
| نظام التواصل الاجتماعي | 70 | `scripts/media_social_calendar_generate.py` | إيقاع النشر اليدوي للتأكيد | المؤسس | توليد تقويم 30 يومًا |
| نظام الإعلانات | 30 | `docs/media-social-os/15_ADS_READINESS_GATE.md` | التتبع وUTM وحدث التحويل والميزانية معلقة | المؤسس | إكمال بوابة جاهزية الإعلانات قبل أي إنفاق |
| نظام CRM | 85 | `scripts/commercial_crm_schema_verify.py` | بيانات عملاء حقيقية | المؤسس | تشغيل تحقق المخطط وتحميل العملاء |
| نظام التسليم | 75 | `docs/03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md` | لم يُسلَّم أول تشخيص بعد | المؤسس | تسليم أول تشخيص مدفوع |
| الامتثال | 85 | قواعد `config/crm_pipeline_schema.json`، مستندات PDPL | التقاط الموافقة في التدفق الحي | المؤسس | تأكيد عملية القمع والموافقة |
| الأمان | 90 | `scripts/commercial_safety_audit.py` | لا شيء معروف | المؤسس | التدقيق يوميًا والإبقاء على صفر مخالفات |
| GitHub Actions | 85 | `.github/workflows/final-launch-control.yml` | مخرجات فقط؛ بدون أسرار بالتصميم | المؤسس | تأكيد أن التشغيل اليومي أخضر |
| الخادم / الواجهة البرمجية | 60 | `scripts/api_commercial_static_check.py` | فحص ثابت فقط؛ لا خادم حي مثبت هنا | المؤسس | تشغيل الفحص؛ التحقق من /health منفصلًا |
| التوثيق | 85 | `docs/launch-control/*` | روابط متقاطعة للتأكيد | المؤسس | مراجعة مجموعة المستندات |
| الاختبارات | 70 | مجموعة اختبارات المستودع | تغطية سكربتات الإطلاق الجديدة | المؤسس | تشغيل المجموعة الكاملة وتسجيل النتيجة |
| المتطلبات الخارجية | 50 | هذه البطاقة | النطاق والاستضافة والدفع وحسابات الإعلان معلقة | المؤسس | تتبع قائمة الإعداد الخارجي |

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
