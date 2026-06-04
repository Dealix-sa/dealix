# Site Manual QA Checklist — قائمة الفحص اليدوي للموقع

> Manual QA for the website (`apps/web`, Next.js). The automated static check is `scripts/site_launch_static_check.py`; this list covers what a human must confirm. Forms must never request sensitive personal data, and no copy may make unproven claims.
>
> فحص يدوي للموقع (`apps/web`، Next.js). الفحص الثابت الآلي هو `scripts/site_launch_static_check.py`؛ تغطي هذه القائمة ما يجب أن يؤكده إنسان. يجب ألا تطلب النماذج بيانات شخصية حساسة، ولا يجوز لأي نص تقديم ادعاءات غير مُثبتة.

---

## EN — Checklist

### Pages
- [ ] Homepage renders correctly
- [ ] Commercial page complete
- [ ] Services page complete
- [ ] Verticals pages (all five) present and accurate
- [ ] Pricing page reflects the offer ladder
- [ ] Trust page present
- [ ] Contact page works (no sensitive data requested)
- [ ] Status page reachable

### Layout & language
- [ ] Mobile layout correct on small screens
- [ ] Arabic text renders right-to-left and reads correctly
- [ ] English text reads correctly
- [ ] CTA buttons present and functional

### SEO & metadata
- [ ] SEO metadata (title, description) on every page
- [ ] `sitemap.xml` present and valid
- [ ] `robots.txt` present and correct
- [ ] OpenGraph tags present
- [ ] Structured data present where applicable

### Integrity
- [ ] No exaggerated or unproven claims (no guarantees, no fixed ROI)
- [ ] No broken links
- [ ] No form requests sensitive personal data (no national ID, no sensitive fields)
- [ ] Disclosure present where value is estimated

### Automated companion
Run `python scripts/site_launch_static_check.py` before launch; this manual list complements it.

---

## AR — القائمة

### الصفحات
- [ ] الصفحة الرئيسية تُعرض بشكل صحيح
- [ ] الصفحة التجارية مكتملة
- [ ] صفحة الخدمات مكتملة
- [ ] صفحات القطاعات (الخمسة) موجودة ودقيقة
- [ ] صفحة التسعير تعكس سلّم العروض
- [ ] صفحة الثقة موجودة
- [ ] صفحة الاتصال تعمل (لا طلب بيانات حساسة)
- [ ] صفحة الحالة قابلة للوصول

### التخطيط واللغة
- [ ] تخطيط الجوال صحيح على الشاشات الصغيرة
- [ ] النص العربي يُعرض من اليمين لليسار ويُقرأ بشكل صحيح
- [ ] النص الإنجليزي يُقرأ بشكل صحيح
- [ ] أزرار CTA موجودة وتعمل

### SEO والبيانات الوصفية
- [ ] بيانات SEO الوصفية (العنوان، الوصف) في كل صفحة
- [ ] `sitemap.xml` موجود وصالح
- [ ] `robots.txt` موجود وصحيح
- [ ] وسوم OpenGraph موجودة
- [ ] البيانات المهيكلة موجودة حيث ينطبق

### النزاهة
- [ ] لا ادعاءات مبالغ فيها أو غير مُثبتة (لا ضمانات، لا عائد ثابت)
- [ ] لا روابط مكسورة
- [ ] لا نموذج يطلب بيانات شخصية حساسة (لا هوية وطنية، لا حقول حساسة)
- [ ] الإفصاح موجود حيث تكون القيمة تقديرية

### الرفيق الآلي
شغّل `python scripts/site_launch_static_check.py` قبل الإطلاق؛ هذه القائمة اليدوية تكمّله.

---

Related: [Final Launch Control Tower](../launch-control/00_FINAL_LAUNCH_CONTROL_TOWER.md) · [API Commercial Launch QA](../ops/API_COMMERCIAL_LAUNCH_QA.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
