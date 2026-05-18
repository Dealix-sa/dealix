# Dealix — Affiliate Governance — حوكمة برنامج الإحالة الموزّعة (Affiliate)
<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** الـAffiliate يُحيل بإفصاح، لا يبيع بادعاء. العمولة تُدفع فقط
> بعد `invoice_paid`. لا قبول بلا موافقة يدوية. لا سكربت غير معتمد. الإفصاح إلزامي
> في كل رسالة — لا استثناء.

> **تنبيه — لا ضمانات.** هذا المستند يسدّ **البند 2 من سجل الفجوات** في
> [`DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md`](../DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md).
> يحكم برنامجاً **مستقل العلاقة (arms-length)** متميّزاً عن برامج الشريك/الإحالة
> الداخلية. أي رقم أداء لم يتحقق = `insufficient_data`.

---

## 1) ما هذا البرنامج ولماذا منفصل · Scope & Distinction

| البرنامج | العلاقة | المرجع |
|----------|---------|--------|
| **Agency Partner** | شريك يُنفّذ ويُسلِّم لعملائه | [`AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md) |
| **Referral** | معارف المؤسس يُقدّمون مقدّمة دافئة | [`sales-kit/dealix_referral_program.md`](../sales-kit/dealix_referral_program.md) |
| **Affiliate (هذا المستند)** | طرف **مستقل العلاقة** يُحيل عبر سكربت معتمد مقابل عمولة | هذا الملف |

الـAffiliate ليس موظفاً ولا شريك تنفيذ ولا يتحدّث باسم Dealix. هو قناة إحالة محكومة:
يُعرّف بـDealix، يُفصح عن علاقته، ويُوصل المهتمّ — لا أكثر.

---

## 2) القبول — Onboarding · Manual Approval Only

- ابدأ بـ**5–10 affiliates موثوقين فقط** — لا توسيع قبل إثبات النمط.
- كل affiliate يمرّ **موافقة يدوية** من المؤسس. لا تسجيل ذاتي مفتوح.
- شرط القبول: سمعة نظيفة، فهم للعقيدة، توقيع اتفاقية تتضمّن قواعد الإفصاح والممنوعات.
- يستلم الـaffiliate **حزمة سكربتات معتمدة فقط** — لا يكتب رسائله الخاصة.
- أي تعديل على السكربت يحتاج موافقة المؤسس قبل الاستخدام.

```text
طلب affiliate ──▶ مراجعة المؤسس اليدوية ──▶ اتفاقية موقّعة ──▶ حزمة سكربتات معتمدة
                                                                      │
                          إحالة بإفصاح ──▶ lead مؤهّل ──▶ عرض ──▶ invoice_paid
                                                                      │
                                                          عمولة مُوافَق عليها ──▶ دفعة
```

---

## 3) الإفصاح الإلزامي · Mandatory Disclosure

كل رسالة إحالة من affiliate **يجب** أن تحمل إفصاحاً واضحاً عن العلاقة. لا إفصاح =
خرق فوري. قالب الإفصاح ثنائي اللغة (يستخدم الـaffiliate المقطع المناسب للجمهور):

> **إفصاح — العربية:** «أنا شريك إحالة (affiliate) لـDealix وقد أحصل على عمولة
> إذا اشتركت عبري. هذه ليست شهادة من Dealix ولا ضمان نتائج — القيمة التقديرية
> ليست قيمة مُتحقَّقة. القرار قرارك، والتقييم مستقل.»

> **Disclosure — English:** "I am a Dealix affiliate and may earn a commission
> if you sign up through me. This is not a Dealix endorsement and not a
> guarantee of results — estimated value is not verified value. The decision is
> yours; please evaluate independently."

---

## 4) الممنوعات · Forbidden Actions

| ممنوع · Forbidden | لماذا |
|-------------------|-------|
| ضمان ROI أو نتائج أو امتثال | يخالف قاعدة «لا ضمانات» والـ11 غير القابلة للتفاوض |
| الـspam أو الرسائل الجماعية | يخالف عقيدة التوزيع |
| الـcold WhatsApp أو الرسائل الباردة | ممنوع صراحةً في الميثاق |
| إثبات مزيّف أو أرقام غير موثّقة | يخالف «الإثبات هو المنتج» |
| إخفاء علاقة الـaffiliate | الإفصاح إلزامي بلا استثناء |
| سكربت غير معتمد أو ادعاء خاص | كل رسالة من حزمة معتمدة فقط |
| التحدّث باسم Dealix أو الالتزام نيابةً عنها | الـaffiliate مستقل العلاقة لا متحدّث |

أي خرق ⟶ إيقاف فوري للحساب ومراجعة، وحجب أي عمولة مرتبطة بالإحالة المخالفة.

---

## 5) مسار العمولة · Commission Path

- العمولة تُحتسب **فقط بعد حدث `invoice_paid`** — لا دفع على lead ولا على عرض.
- الدفعة (`payout`) فعل **حرج مُبوَّب بالموافقة** عبر `dealix/governance/approvals.py` —
  موافقة بشرية مُسجَّلة قبل أي تحويل.
- كل عمولة تُسجَّل في سجل تتبّع؛ لا rev-share بلا تتبّع.
- استرداد العميل ⟶ تُلغى العمولة المرتبطة (clawback) ضمن نافذة معلنة في الاتفاقية.
- معدّلات العمولة قرار للمؤسس ولا تُذكر هنا — اتفاقية الـaffiliate هي المرجع.

---

## فهرس مراجع الريبو — Repo Cross-reference Index

| الموضوع | الملف المعتمد |
|---------|----------------|
| سجل الفجوات الأصلي (البند 2) | [DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md](../DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md) |
| ميثاق الثقة والسلامة | [governance/TRUST_SAFETY_CHARTER.md](../governance/TRUST_SAFETY_CHARTER.md) |
| برنامج الإحالة (Referral) | [sales-kit/dealix_referral_program.md](../sales-kit/dealix_referral_program.md) |
| برنامج شراكة الوكالات | [AGENCY_PARTNER_PROGRAM.md](../AGENCY_PARTNER_PROGRAM.md) |
| غير قابل للتفاوض (الـ11) | [00_foundation/NON_NEGOTIABLES.md](../00_foundation/NON_NEGOTIABLES.md) |
| الخطة الأم | [MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md](../MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md) |
| بوابة الموافقات (كود) | `dealix/governance/approvals.py` |

---

*Version 1.0 | Closes Gap #2 of the Distribution Gap Register | Arms-length
affiliate program — distinct from Partner & Referral | No guaranteed claims |
Disclosure mandatory | Commission only after invoice_paid | Missing data =
insufficient_data.*
