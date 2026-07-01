# قائمة جاهزية الإطلاق الشاملة — Dealix

آخر تحديث: 2026-07-01
الحالة العامة: **جاهز للانطلاق اليدوي (Manual Outreach)** — بانتظار فقط إجراءات المؤسس المذكورة أدناه.

هذا المستند هو نقطة تجميع واحدة لحالة الإطلاق: ماذا تم التحقق منه في الكود، ماذا
تم إصلاحه، وأي إجراءات متبقية لا يمكن لأحد غير المؤسس (سامي) تنفيذها.

---

## 1. الكود والدمج (Merge Status)

- كل فروع الـ Wave السبعة (`feat/ceo-operating-context` … `feat/trust-launch-os`)
  **مدموجة بالفعل** في `origin/main`. لا توجد فروع عمل معلّقة تحتاج دمجًا.
- هذا الفرع (`claude/launch-readiness-checklist-5mga6w`) كان متطابقًا تمامًا مع
  `origin/main` قبل هذا التحديث؛ التغييرات هنا (هذا الملف + أيقونة الموقع) تمت
  إضافتها كطبقة تحقق وإغلاق فجوات فقط، وليست دمجًا لعمل جديد.
- الدمج النهائي إلى `main` هو قرار المؤسس فقط (انظر القسم 4) — لا يتم دمج أي PR
  تلقائيًا في هذا المشروع.

## 2. نتائج التحقق (Verification Results — 2026-07-01)

جميع البوابات الإلزامية في `make full-repo-test` **PASS**:

```
PASS: python-version
PASS: python-compileall-core-surfaces
PASS: env-contract
PASS: security-smoke
PASS: no-auto-external-send
PASS: company-launch-ready
PASS: pytest-launch-critical-suite
PASS: apps-web-npm-ci
PASS: apps-web-verify
FULL_REPO_TEST_MATRIX=PASS
```

البوابات الاختيارية/التشخيصية (`pytest-full-suite-diagnostic`,
`launch-os-dry-runs`, `production-verify-bundle`, `testsprite-*`) SKIP —
هذا متوقع ومتوافق مع القاعدة (فشلها غير حاجز)، ومعظمها يحتاج مفاتيح API
اختيارية غير مطلوبة للإطلاق اليدوي.

تحققات إضافية منفصلة (كلها PASS):
```
CI_SECURITY_SMOKE=PASS
NO_AUTO_EXTERNAL_SEND_GATE=PASS   (OUTBOUND_MODE=draft_only)
COMPANY_LAUNCH_READY=READY_FOR_MANUAL_OUTREACH
```

`scripts/ops/check_railway_production_env.py` يعطي `FAIL` في هذه الجلسة
المحلية — وهذا متوقع تمامًا، لأن متغيرات Railway الإنتاجية (APP_SECRET_KEY،
DATABASE_URL، إلخ) لا تُحفظ أبدًا في الكود أو الجلسات المحلية؛ تُضبط فقط داخل
لوحة Railway مباشرة (انظر القسم 4).

## 3. الهوية البصرية (Visual Identity)

تم تدقيق الهوية البصرية بشكل شامل:

| العنصر | الحالة |
|---|---|
| الشعار (Logo set) | مكتمل — `brand/logo*.svg`, `apps/web/public/dealix-*.svg` |
| نظام التصميم | مكتمل — `docs/brand/DESIGN_SYSTEM.md`, `BRAND_GUIDELINES.md` |
| الألوان والخطوط | مكتملة — Navy/Gold + خطوط Cairo/Tajawal للعربي في Tailwind theme |
| دعم RTL/العربي | مكتمل وجاهز للإنتاج — صفحات `/ar/*` (15+ صفحة فرعية) |
| توافق النسخ مع نموذج العمل | متطابق مع `docs/DEALIX_BUSINESS_MODEL.md` |
| **الأيقونة (Favicon)** | **الفجوة الوحيدة المؤكدة — تم إصلاحها في هذا التحديث** |

**الإصلاح:** أُضيف `apps/web/app/icon.svg` (يستخدم علامة Dealix الموجودة في
`apps/web/public/dealix-mark.svg` دون أي تصميم جديد)، ويُلتقط تلقائيًا بواسطة
Next.js 15 كأيقونة للموقع. تم التحقق: `npm --prefix apps/web run verify`
ناجح، ومسار `/icon.svg` يظهر في مخرجات البناء.

لا توجد فجوات أخرى في الهوية البصرية — بقية العناصر (الشعار، الألوان، الخطوط،
صفحات التسويق، دعم RTL) مكتملة ولم تُلمس.

## 4. جاهزية الإطلاق التشغيلي — فهرس القوائم الموجودة

بدل تكرار المحتوى، هذا فهرس للقوائم التفصيلية الموجودة فعليًا في الريبو:

- `docs/ops/RAILWAY_GO_LIVE_CHECKLIST.md` — إعداد Railway، متغيرات البيئة، فحوصات الإنتاج
- `docs/ops/GO_LIVE_CHECKLIST_AR.md` — Moyasar، ZATCA، الفوترة، الامتثال
- `docs/PUBLIC_LAUNCH_CHECKLIST.md` — القانوني (سياسة الخصوصية، الشروط، DPA)، المنتج، الفوترة
- `docs/ops/PRODUCTION_READINESS_CHECKLIST.md` — حماية الفروع، CI، الأسرار، خطة التراجع
- `docs/ops/RELEASE_READINESS_CHECKLIST.md` — رحلات المستخدم، معايير القبول، العقود

## 5. إجراءات لا يمكن لأحد غير المؤسس (سامي) تنفيذها

هذه القائمة **غير قابلة للأتمتة** بواسطة Claude أو أي أداة في هذا الريبو —
تتطلب دفعًا ماليًا، مفاتيح حية، أو موافقة بشرية صريحة:

1. **دفع فاتورة Railway المتأخرة** وإعادة ربط مصدر GitHub (`Dealix-sa/dealix`).
2. **لصق أسرار الإنتاج** (`APP_SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`,
   `API_KEYS`, `ADMIN_API_KEYS`) داخل لوحة Railway مباشرة — لا تُنشأ أو تُخزّن
   في الكود أبدًا.
3. **الحصول على مفاتيح Moyasar الحية** و **ZATCA CSID/secret** للفوترة والامتثال.
4. **المراجعة القانونية النهائية** ونشر سياسة الخصوصية، الشروط، واتفاقية معالجة
   البيانات (DPA) بما يتوافق مع PDPL.
5. **الموافقة على دمج هذا الـ PR** إلى `main` بالضغط اليدوي على زر الدمج.
6. **أي قرار مستقبلي** بتفعيل الإرسال الحي (`OUTBOUND_MODE=controlled_live`,
   `EXTERNAL_SEND_ENABLED=true`) — يبقى `draft_only` حتى إشعار آخر.

## 6. البحث عن عملاء اليوم (Client Search — Draft-Only)

الأدوات جاهزة وتعمل بنظام مسودات فقط (لا إرسال تلقائي أبدًا):

```bash
bash scripts/dealix_command_day.sh   # يشغّل كل المحركات + يبني لوحة Command Room
```

هذا الأمر:
- يجمع عملاء محتملين عبر Google Custom Search / Places API (لا سكرابينغ).
- يصنّفهم ويقترح العرض المناسب (من السلم الخماسي).
- يولّد مسودات متابعة/عروض في `company/outbox/` — كل صف بحالة
  `needs_review`، ولا يُرسل شيء إلا بعد موافقة صريحة عبر `approval.py`.
- يبني تقرير HTML في `reports/command_room/index.html` للمراجعة اليومية.

اتبع `CRM_SOP.md` لإدارة حالات القمع (11 حالة من `research_needed` إلى
`won`/`lost`)، وراجع كل مسودة يدويًا قبل أي إرسال فعلي.

**تذكير أخير:** كل مخرجات هذه الأدوات هي مسودات فقط بانتظار موافقتك — لا يوجد
إرسال آلي لأي واتساب/إيميل/SMS تحت أي ظرف ما لم تُغيّر أعلام البيئة يدويًا
وبموافقتك الصريحة.
