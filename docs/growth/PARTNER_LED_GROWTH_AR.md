# Partner-Led Growth — النمو عبر الشركاء

> Section 46. الحركة، المؤشّرات، checklist التهيئة، ومحتوى White-label Kit.
> Module path: `dealix/growth_os/partner_growth/`

---

## مقدّمة — Introduction

الشركاء في Dealix ليسوا قناة تسويق إضافيّة. هم امتداد التشغيل تحت نفس طبقة الحوكمة. الوكالة التي تبيع Dealix باسمها يجب أن تلتزم بـ نفس claim-safety ونفس Proof Pack standard.

Partners are not an extra marketing channel — they are operating extensions under the same governance layer. A reseller agency must hold to the same claim-safety and ProofPack standard.

---

## الحركة — Partner Motion

| المرحلة | Stage | المخرج |
|---|---|---|
| 1 | Discover | partner-fit ICP (راجع `ICP_MATRIX_AR.md` rows 1, 6, 7) |
| 2 | Apply | PartnerApplication (نموذج عام) |
| 3 | Qualify | مكالمة 30 دقيقة + مراجعة محفظة |
| 4 | Onboard | Tier assignment + توقيع PartnerAgreement |
| 5 | Enable | White-label Kit + tasks تدريبيّة |
| 6 | First Deal | بمساندة Dealix delivery |
| 7 | Scale | 3+ deals → upgrade Tier |
| 8 | Review | Quarterly partner review |

---

## نظام الـ Tiers — Partner Tiers

| Tier | معيار الدخول | Commission Range | الفوائد |
|---|---|---|---|
| Referral | إحالة موثَّقة بدون تسليم | `<TBD>`% finder's fee | الاسم في صفحة الشركاء |
| Reseller | 1+ deals مغلقة | `<TBD>`% | White-label Kit أساسي |
| Authorized | 3+ deals، NPS ≥ 8 | `<TBD>`% + كو-مبيعات | Co-marketing + Sector Reports مبكّرة |
| Strategic | 10+ deals/سنة | تفاوض | بناء عروض مشتركة + co-branded events |

---

## Partner Onboarding Checklist

### Pre-onboard
- [ ] PartnerApplication مكتمل.
- [ ] محفظة عمل سابقة موثَّقة.
- [ ] عدم وجود تعارض ICP حادّ مع شريك حالي.
- [ ] قبول Constitution + WHAT_DEALIX_REFUSES.

### Onboard Day 1
- [ ] توقيع PartnerAgreement.
- [ ] Tier assignment.
- [ ] إعداد partner_id داخل CRM.
- [ ] إنشاء PartnerDealRecord template.

### Onboard Week 1
- [ ] جلسة Kit walkthrough (90 دقيقة).
- [ ] تسليم White-label assets.
- [ ] جلسة claim-safety + PDPL (60 دقيقة).
- [ ] تعيين Dealix delivery buddy لأوّل صفقة.

### First 30 days
- [ ] أوّل lead مُسجَّل.
- [ ] أوّل meeting محجوز.
- [ ] أوّل proposal مسوّد (يراجعه Dealix قبل الإرسال).

### First 90 days
- [ ] أوّل صفقة موقَّعة.
- [ ] ProofPack مُسلَّم.
- [ ] Quarterly review مُجدوَل.

---

## White-label Kit — ما يدخل

| المكوّن | الوصف |
|---|---|
| Offer Templates | OfferCard معتمد قابل لإعادة العلامة |
| Proposal Templates (.j2) | بنفس بنية Dealix، علامة الشريك |
| ProofPack Template | بنفس standard، علامة مشتركة |
| GEO Page Templates | أمثلة لمواقع الشريك |
| Message Drafts | Templates ABM (للمراجعة قبل الإرسال) |
| Claim-Safety Guide | قواعد ادعاء + أمثلة |
| PDPL Quick Reference | ملخّص للشريك |
| Sales Talk Track | 60-90 دقيقة فيديو + سيناريو محادثة |
| Pricing Guide | نطاقات السعر + قواعد الخصم |
| Co-brand Style Guide | حدود استخدام الشعارين |

---

## White-label Kit — ما لا يدخل

- بيانات عملاء Dealix.
- Source code من `dealix/growth_os/`.
- Sector Reports داخليّة غير منشورة.
- Pricing models الكاملة (فقط النطاقات).
- AI Run Ledger الخام.

---

## مؤشّرات الشركاء — Partner KPIs

| KPI | الوصف | Target |
|---|---|---|
| `partner_sourced_revenue_sar` | إيراد عبر الشركاء | track |
| `partner_sourced_share` | % من الإيراد الكلّي | 20–40% (متوسّط المدى) |
| `active_partners` | الشركاء بصفقة آخر 90 يوم | track |
| `partner_first_deal_days` | متوسط الأيام للصفقة الأولى | ≤ 60 |
| `partner_nps` | NPS الشريك ربع سنوي | ≥ 30 |
| `partner_claim_safety_incidents` | حوادث ادعاء | 0 |

---

## شروط الإنهاء — Termination Triggers

- خرق claim-safety موثَّق.
- خرق PDPL.
- استخدام بيانات Dealix خارج نطاق العقد.
- 180 يوم بدون صفقة + بدون نشاط onboarding.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
