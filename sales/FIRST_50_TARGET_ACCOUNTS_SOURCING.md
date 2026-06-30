# First 50 Target Accounts — Lawful Sourcing Note / مذكرة المصدر القانوني
<!-- PHASE: Sales | Owner: Founder | Date: 2026-06-07 -->
<!-- Arabic primary — العربية أولاً -->

> هذا متتبّع يدوي لأول 50 حسابًا مستهدفًا (`FIRST_50_TARGET_ACCOUNTS.csv`). يُملأ يدويًا
> ببحث قانوني فقط. **لا scraping**، ولا أتمتة مخالفة لشروط المنصّات. A manual tracker —
> lawful, manual research only. No scraping, no platform-ToS-violating automation.

## القواعد / Rules

- **مصادر مسموحة:** المواقع العامة للشركات، السجلات التجارية العامة، مراجعة يدوية لملفات
  LinkedIn/Google، الإحالات بموافقة، اللقاءات الشخصية/الفعاليات.
- **`lawful_basis` إلزامي لكل صف:** وثّق الأساس (مثل `public_business_listing`,
  `public_profile_manual_review`, `explicit_referral_consent`, `met_in_person_consent`).
- **لا تواصل بارد آليًا:** كل تواصل أول يكون warm + draft + موافقة المؤسس (approval-first).
- **PDPL-aware:** لا تُخزّن بيانات شخصية حسّاسة؛ اكتفِ بمعلومات العمل العامة وجهة الاتصال
  المعلنة. لا أرقام/بيانات مخترعة (non-negotiable: لا KPI/CRM مخترع).

## الأعمدة / Columns

`company_name, sector, city, decision_maker, source, lawful_basis, status, next_action, notes`

- `status`: `research` → `verified` → `warm_intro` → `contacted(approved)` → `qualified` → `won/lost`.
- `next_action`: خطوة واحدة واضحة فقط (CTA: Risk Score / Sample Proof / ديمو 10 دقائق).

## التدفق / Flow

1. املأ صفًا بمصدر قانوني موثّق.  2. تحقّق من جهة الاتصال يدويًا.  3. جهّز draft تواصل دافئ.
4. مرّره للموافقة (approval-first).  5. أرسل عبر القناة المعتمدة فقط بعد الموافقة.

> الصفوف الحالية أمثلة (`Example …`) — استبدلها بحسابات حقيقية. لا ترسل لأي صف قبل موافقة المؤسس.
