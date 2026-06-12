# Web Surface Consolidation — توحيد واجهات الويب

_Decided: 2026-06-07 · Status: Canonical_

## المشكلة / Problem

Dealix كان يملك **ثلاث واجهات ويب منفصلة**، ما سبّب تشظّياً في الرسالة والهوية وجهد الصيانة:

| Surface | Tech | الدور السابق | المشكلة |
|---|---|---|---|
| `frontend/` | Next.js (App Router, i18n `[locale]`, عربي أولاً) | المنتج + القمع التسويقي + cockpit | الأكمل والأقوى |
| `apps/web/` | Next.js (إنجليزي أولاً) | "Control plane" showcase | مكرّر، إنجليزي، يشتّت |
| `landing/` | HTML ثابت (~80 صفحة) | موقع تسويقي قديم | إرث، يصعب صيانته |

## القرار / Decision

1. **`frontend/` = الموقع القانوني الوحيد (canonical).** كل الاستثمار التسويقي والمنتجي والتشغيلي هنا. عربي أولاً، إنجليزي ثانياً، عبر `[locale]`. هو ما يُربَط بالنطاق الحيّ.
2. **`apps/web/` = عرض المنصة/الـControl Plane فقط (secondary).** يبقى يُبنى (الـCI وRailway يعتمدان عليه) لكن صفحته الرئيسية توجّه الزائر بوضوح إلى الموقع القانوني والقمع. لا يُطوَّر كموقع تسويقي مستقل.
3. **`landing/` = مؤرشف (legacy/archived).** يبقى للرجوع التاريخي والروابط القديمة؛ لا تُضاف صفحات جديدة. انظر `landing/README.md`.

## لماذا `frontend/` / Why frontend

- عربي أولاً عبر `[locale]` — مطابق للسوق السعودي المستهدف.
- يحوي القمع العام كاملاً: `/[locale]`, `/dealix-diagnostic`, `/risk-score`, `/proof-pack`, `/pricing`, `/services`, `/offer`, `/learn`, `/partners`, `/trust-center`.
- يحوي cockpit المؤسس والعمليات: `/[locale]/ops/*`, `/cloud`, `/crm`, `/customer-portal`.
- README و AGENTS.md يعاملانه كـ"الواجهة الأساسية".
- يطبّق الهوية (Navy + Gold) عبر `frontend/tailwind.config.ts` + `design-systems/dealix/tokens`.

## قواعد التنفيذ / Implementation rules

- روابط تسويقية جديدة → `frontend/` فقط.
- النطاق الحيّ (مثل `dealix.me`) → يخدم `frontend/`.
- `apps/web/` يحتفظ بـ CTA بارز للموقع القانوني (مطبّق في `apps/web/app/page.tsx`).
- لا تُحذف `apps/web` أو `landing` في هذه الدفعة (تبعيات CI/Railway + روابط قديمة)؛ الإزالة قرار لاحق منفصل.

## خطوات لاحقة (اختيارية) / Future

- 301 redirects من مسارات `landing/*.html` إلى مسارات `frontend/` المكافئة عند ربط النطاق.
- دمج أي محتوى فريد متبقٍّ في `landing/` داخل `frontend/src/app/[locale]/learn`.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
