# تقرير مطابقة حزمة الإطلاق (Launch Package Reconciliation)

**التاريخ:** 2026-06-07 · **الحزمة:** Dealix Launch Package V1 + V2 (مولّدة بأداة خارجية)
**القرار:** دمج آمن انتقائي — أرشفة كاملة كمرجع + ترقية القطع الجديدة المتوافقة فقط، بلا أي كتابة فوق أو كسر للاصطلاحات.

---

## 1) الخلاصة التنفيذية

الحزمة بُنيت دون رؤية للريبو الفعلي، فجاءت تكرّر **~90%** مما هو موجود مسبقًا في
Dealix — لكن **بصيغة أنضج ومحكومة (governed)**. تعليمات الدمج الأصلية (`cp -R` +
الكتابة فوق صفحات الفرونت + إضافة CI على كل PR) كانت ستضر الريبو:

1. **كسر الفرونت** — استبدال صفحات Next.js ثنائية اللغة (`generateMetadata` + `AppLayout` + async `params`) بنسخ RTL ناقصة.
2. **تعارض تسعير** — الحزمة تخترع أرقامًا (499–2,500 / 4,500–18,000 / 1,500–3,000 SAR) تتعارض مع تسعير الريبو الرسمي → 3 نماذج متناقضة.
3. **CI على كل PR** — `dealix-launch-readiness.yml` يشغّل سكربتات تكتب ملفات `data/` على كل push/PR.
4. **تكرار/تشتت وثائقي** — خطة 100 يوم مقابل 90، war room مرتين، objection-handling مرتين.

لذلك: أُرشفت الحزمة كاملة في [`launch_package_v2/`](launch_package_v2/) كمرجع خامل،
ورُقّيت فقط القطع الجديدة المتوافقة مع الدستور.

---

## 2) ما الذي رُقّي فعليًا (net-new + متوافق مع الدستور)

| من الحزمة | إلى الريبو | المواءمة |
| --- | --- | --- |
| `compliance/OUTBOUND_AND_DATA_POLICY_AR.md` | `docs/compliance/OUTBOUND_AND_DATA_POLICY_AR.md` | ربط بالدستور + PDPL guide؛ `docs/compliance/` لم يكن فيه سياسة outbound |
| `scripts/dealix_daily_prospect_drafts.py` | `scripts/launch_package/` | مسارات namespaced، argparse، تحمّل أعمدة ناقصة |
| `scripts/dealix_lead_scoring.py` | `scripts/launch_package/` | قراءة `public_contact`، مخرجات إلى `reports/launch_package/` |
| `scripts/dealix_daily_command_center.py` | `scripts/launch_package/` | يقرأ الملف المُقيَّم من `reports/launch_package/` |
| `data/prospects/icp_seed_accounts_saudi.csv` | `scripts/launch_package/sample_data/` | `data/` مُستثنى في `.gitignore` فنُقلت كبذرة أمثلة متتبعة |
| `data/prospects/icp_seed_accounts_schema.md` | `scripts/launch_package/ICP_SEED_SCHEMA_AR.md` | مواءمة الأعمدة مع ما تشغّله السكربتات فعليًا |

> **ملاحظة جودة:** الحزمة كانت متعارضة داخليًا في أسماء الأعمدة (بذرة CSV ≠ سكربت
> scoring ≠ dataclass الـdrafts ≠ ملف المخطط). تمت مواءمتها على **9 أعمدة** موحّدة
> حتى تعمل السكربتات الثلاثة معًا على نفس البذرة.

---

## 3) مكرّر — موجود مسبقًا وأنضج (أُرشف فقط، لم يُدمج)

| ملف الحزمة | المعادل المعتمد في الريبو |
| --- | --- |
| `landing/dealix_full_website_ar.html` (صفحة واحدة) | `landing/` — **80+ صفحة** (`index`, `pricing`, `privacy`, `terms`, `services`, `case-study`, `verticals`, `diagnostic`, `robots.txt`, `sitemap.xml`...) |
| `frontend/.../pricing/page.tsx` | `frontend/src/app/[locale]/pricing/page.tsx` (ثنائي اللغة + `PricingPlans`) |
| `frontend/.../privacy/page.tsx` | `frontend/src/app/[locale]/privacy/page.tsx` (186 سطرًا) |
| `frontend/.../services/page.tsx` | `frontend/src/app/[locale]/services/page.tsx` |
| `frontend/public/robots.txt` · `sitemap.xml` | `landing/robots.txt` · `landing/sitemap.xml` |
| `docs/launch/DEALIX_100_DAY_EXECUTION_MAP_AR.md` | `docs/commercial/operations/CEO_90_DAY_OKR_AR.md` + خطة 138 مهمة |
| `docs/launch/FOUNDER_DAILY_WAR_ROOM_AR.md` | `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md` (19KB) + `/[locale]/ops/war-room` |
| `docs/launch/CRM_PIPELINE_AND_FIELDS_AR.md` | `/[locale]/crm` + HubSpot sync + pipeline |
| `docs/launch/DEALIX_FULL_LAUNCH_MASTER_PLAN_AR.md` | `docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md` + خطط commercial |
| `docs/launch/OFFER_PACKAGES_PUBLIC_AR.md` | `docs/pricing.md` + `docs/commercial/sales/` ⚠️ **تعارض تسعير** |
| `docs/launch/WEBSITE_CONVERSION_BLUEPRINT_AR.md` | `landing/` + GTM funnel (`/dealix-diagnostic`, `/risk-score`, `/proof-pack`) |
| `docs/launch/DAILY_PROSPECTING_OPERATING_SYSTEM_AR.md` | `docs/ops/SAUDI_LEAD_MACHINE_AR.md` + `FOUNDER_DAILY_OPERATING_RHYTHM.md` |
| `sales/CALL_SCRIPT_AR.md` | `docs/commercial/sales/DEALIX_DISCOVERY_SCRIPT_AR.md` |
| `sales/OBJECTION_HANDLING_AR.md` | `docs/commercial/sales/DEALIX_OBJECTION_HANDLING_AR.md` |
| `sales/{WHATSAPP,EMAIL}_SEQUENCE_AR.md` | `data/templates/` (warm intros) + warm_intro_generator |
| `sales/{PROPOSAL,SOW}_TEMPLATE_AR.md` | `dealix/commercial/` (proposal/proof) + `data/templates/` |
| `marketing/LINKEDIN_CONTENT_30_DAYS_AR.md` | `docs/content/LINKEDIN_CADENCE_PLAN.md` + content factory |
| `marketing/SEO_AND_UTM_PLAN_AR.md` | `landing/` SEO + analytics/UTM |
| `marketing/BRAND_MESSAGING_SYSTEM_AR.md` | وثائق التموضع/الهوية القائمة |
| `ops/CLIENT_ONBOARDING_CHECKLIST_AR.md` | `docs/03_commercial_mvp/CLIENT_ONBOARDING_PLAYBOOK.md` |
| `ops/WEEKLY_EXECUTIVE_REPORT_TEMPLATE_AR.md` | `scripts/run_executive_weekly_checklist.sh` + founder weekly metrics |

---

## 4) مرفوض — تدميري أو مخالف للدستور (أُرشف فقط، لم يُفعّل)

| ملف الحزمة | السبب |
| --- | --- |
| `.github/workflows/dealix-launch-readiness.yml` | يشغّل سكربتات تكتب `data/` على **كل PR/push** → يفشّل PRs غير مرتبطة. الريبو فيه CI شامل أصلًا. |
| `.github/workflows/dealix-daily-growth-os.yml` | أتمتة cron خارجية تكرّر ops اليومية القائمة؛ تُركت مرجعية. |
| `scripts/dealix_launch_readiness_check.py` | مساراته مرتبطة بهيكل الحزمة نفسه (تعيش في الأرشيف)؛ الريبو فيه `scripts/launch_readiness_check.py` + عشرات المدقّقات. |
| `scripts/dealix_create_launch_issues.py` | طابع نص بسيط خاص بالحزمة؛ مرجعي. |
| `frontend/.../{industries,case-studies,contact,custom-ai-systems}/page.tsx` | مسارات غير موجودة في الفرونت، لكنها نسخ RTL ناقصة (بلا `AppLayout`/i18n/metadata/async `params`) قد تكسر `next build`. الأفضل بناؤها على الاصطلاحات لاحقًا (انظر §6). |

---

## 5) تنبيه تعارض التسعير (مهم)

ثلاثة نماذج تسعير ظهرت أثناء المطابقة — **يجب توحيدها قبل أي نشر عام:**

1. **تسعير الريبو الرسمي** (`docs/pricing.md` + `PricingPlans`): Sprint لمرة واحدة · Managed Ops شهري · Enterprise AI مخصص.
2. **حزمة V2** (`OFFER_PACKAGES_PUBLIC_AR.md`): Free Diagnostic → 499 Pilot → 1,500–3,000 Data → setup 4,500–18,000 → retainer.
3. **سلّم 5 باقات** (مذكور في وصف العمليات): Free → 499 Sprint → 1,500 Data Pack → 2,999–4,999/mo Managed → 5K–25K Custom AI.

> القناة المعتمدة للتسعير هي `docs/pricing.md` + `PricingPlans` + Service Readiness Matrix.
> لم يُغيَّر أي تسعير في هذا الدمج.

---

## 6) الخطوة التالية الموصى بها (بأدوات الريبو المعتمدة)

```bash
# المسار اليومي المحكوم (موجود مسبقًا)
bash scripts/run_founder_commercial_day.sh
python3 scripts/run_dealix_daily_ops.py --skip-api

# مساعدات الحزمة (approval-first، بلا إرسال)
python3 scripts/launch_package/dealix_daily_prospect_drafts.py
python3 scripts/launch_package/dealix_lead_scoring.py
python3 scripts/launch_package/dealix_daily_command_center.py
```

- إن أردت صفحات `/industries` أو `/contact` في الفرونت: تُبنى على الاصطلاحات
  (`AppLayout` + ثنائي اللغة + `generateMetadata` + async `params`) كمهمة منفصلة — لا تُلصق نسخ الحزمة.
- وحّد التسعير على مصدر واحد (`docs/pricing.md`) قبل أي تحديث للموقع.
