# غرفة قيادة الإيراد للمؤسس — Founder Revenue Control Room (UI Spec)

واجهة واحدة يفتحها المؤسس صباحاً فيعرف: من يتواصل، ماذا يوافق، من يتابع، أي
مقترح يولّد، أي إثبات يعرض، أي تسليم دفع جاهز، وأي قطاع/قناة يحوّل.

> **القاعدة الذهبية في الواجهة:** الذكاء يجهّز، المؤسس يوافق، النظام يتتبّع.
> **لا يوجد زر «إرسال» في v1.** الأزرار: Approve / Reject / Needs-edit /
> Mark-copied / Generate proposal / Generate proof / Prepare payment handoff.

هذه وثيقة مواصفات (Spec). الـ backend جاهز عبر `/api/v1/distribution/*`؛ بناء
صفحات Next.js يتبع نمط `frontend/src/app/[locale]/ops/*` الموجود (proxy عبر
`NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1` + `DEALIX_ADMIN_API_KEY` على الخادم).

## المسارات / Routes

```text
/[locale]/ops/revenue-control     ← الشاشة الرئيسية (Today's revenue command)
/[locale]/ops/drafts              ← قائمة المسودات + Approve/Reject/Needs-edit/Mark-copied
/[locale]/ops/followups           ← المتابعات المستحقة + Complete
/[locale]/ops/proposals           ← المقترحات + Generate/Approve
/[locale]/ops/proof-packs         ← حزم الإثبات + Generate
/[locale]/ops/payments            ← تسليمات الدفع (handoff) + Prepare/Approve — لا شحن
/[locale]/ops/renewals            ← قائمة التجديد + سلّم الـ upsell
/[locale]/ops/win-loss            ← دروس الفوز/الخسارة + أسئلة الأسبوع
```

## الشاشة الرئيسية — البلوكات / Home blocks

| البلوك | المصدر (API) |
|--------|--------------|
| Today's revenue command | `GET /api/v1/distribution/overview` |
| Pending drafts | `GET /api/v1/distribution/drafts?status=pending_approval` |
| Due follow-ups | `GET /api/v1/distribution/followups` |
| Proposal drafts | `GET /api/v1/distribution/proposals?approval_status=pending_approval` |
| Proof packs | `GET /api/v1/distribution/proof-packs` |
| Payment handoffs | `GET /api/v1/distribution/payments?status=pending_approval` |
| Renewal queue | `GET /api/v1/distribution/renewals` |
| Distribution metrics | `GET /api/v1/distribution/metrics` |
| Win/loss lessons | `GET /api/v1/distribution/win-loss` |

## الأزرار → نقاط النهاية / Buttons → endpoints

| الزر | نقطة النهاية |
|------|--------------|
| Approve draft | `POST /api/v1/distribution/drafts/{id}/approve` |
| Reject draft | `POST /api/v1/distribution/drafts/{id}/reject?reason=…` |
| Needs edit | (يضبط الحالة عبر إعادة التوليد/التحرير اليدوي) |
| Mark copied | `POST /api/v1/distribution/drafts/{id}/mark-copied` |
| Complete follow-up | `POST /api/v1/distribution/followups/{id}/complete` |
| Generate proposal | `POST /api/v1/distribution/proposals/generate` |
| Generate proof pack | `POST /api/v1/distribution/proof-packs/generate` |
| Prepare payment handoff | `POST /api/v1/distribution/payments/handoff` |

كل استجابة تحمل `governance_decision`. مسودة بحالة `blocked` لا يظهر لها زر
Approve إطلاقاً (الـ API يرفضها بـ 409). تسليم الدفع يبقى
`requires_founder_approval` حتى تكتمل الموافقات الست — ولا يوجد أي مسار يشحن
بطاقة أو يرسل رابطاً تلقائياً.

## ملاحظات بناء / Build notes

- اقرأ نمط `frontend/src/app/[locale]/ops/founder` و`/approvals` كمرجع.
- استخدم `frontend/src/app/api/dealix-proxy/` لتمرير `X-Admin-API-Key` من الخادم.
- لا تضف أي زر «Send / إرسال خارجي» أو «Charge / شحن» — هذا انتهاك لعقيدة v1.
- اعرض `quality_issues` بجانب كل مسودة حتى يفهم المؤسس سبب `needs_edit`/`blocked`.

— صُمِّم وفق العقيدة: لا إرسال خارجي، لا شحن، لا ضمانات، كل شيء بانتظار موافقة المؤسس.
