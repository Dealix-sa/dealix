# خطة الإطلاق التجاري الشامل / Commercial Launch Plan
**Dealix — Saudi-first AI Business Transformation**
آخر تحديث / Last updated: 2026-06-28

> وثيقة واحدة تجمع كل نواحي الإطلاق التجاري وتربط الوثائق التفصيلية القائمة.
> One document that unifies every angle of the commercial launch and links the
> detailed specs instead of duplicating them.

---

## 0) ملخص الحالة / Status summary

| البُعد / Dimension | الحالة / Status |
|---|---|
| الهندسة / Engineering | ✅ 100% (Waves 1–7 merged, 660 tests) |
| جاهزية الإطلاق / Launch readiness | 🟡 **PARTIAL** (Paid Private Beta) |
| عملاء مدفوعون / Paid customers | 0 / 3 (بوابة Article 13) |
| المتبقي / Blocking | 4 إجراءات للمؤسس (أدناه) |

التعريف: الإطلاق الآن **"بيتا خاصة مدفوعة"** وليس إطلاقاً عاماً، حتى تُؤكَّد المدفوعات والاستقرار.
The launch is a **Paid Private Beta / Launch Candidate** until payments + stability are confirmed.

---

## 1) الإجراءات الأربعة العالقة للمؤسس / The 4 pending founder actions
بترتيب التنفيذ — كلها تتطلب الموافقة/التنفيذ اليدوي من المؤسس (بوابات الموافقة):

1. **توقيع اتفاقية معالجة البيانات (DPA)** — Sign the Data Processing Agreement.
2. **إرسال 5 رسائل واتساب دافئة + تسجيلها** في `data/outreach/outreach_log.csv` (سقف 5/يوم، روابط دافئة فقط، لا رسائل باردة).
3. **ضبط سجلات DNS** (SPF/DKIM/DMARC) على `dealix.me` — تحقّق بـ `scripts/dealix_dns_verify.py`.
4. **دمج PR الانحدار المعلّق** (Wave 16 regression).

> تذكير العقيدة: لا إرسال تلقائي. الذكاء يصوغ، المؤسس يوافق ويرسل، النظام يتتبّع.

---

## 2) بوابات الإطلاق التسع / Nine launch gates
(مرجع: `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md`)

1. **التحقق بعد الدمج / Post-merge verify** — `scripts/verify_commercial_launch_ready.py`.
2. **Staging** — نشر بيئة التجربة + smoke.
3. **خط الأساس للامتثال / Compliance baseline** — خريطة البيانات، جاهزية PDPL، DPA تجريبي.
4. **الرصد والتقييم / Observability + evals**.
5. **WhatsApp beta** — اختبار محدود بموافقة.
6. **الفوترة / Billing** — Moyasar KYC أو تحويل بنكي كبديل.
7. **بيتا خاصة / Private beta**.
8. **مقاييس البيتا المدفوعة / Paid beta metrics**.
9. **قرار الانطلاق / Go/No-Go** للإطلاق العام.

---

## 3) الإيقاع اليومي ≤45 دقيقة / Daily rhythm
(مرجع: `docs/WAVE17_FOUNDER_DAY1_LAUNCH_KIT.md`)

```bash
bash scripts/dealix_command_day.sh        # يشغّل كل المحركات بأمان ثم يبني الغرفة
# ثم افتح: reports/command_room/index.html
```

1. شغّل الأمر أعلاه (10 د) → افتح **غرفة القيادة الموحّدة**.
2. راجع **إجراءات اليوم ذات الأولوية** + **المتابعات المستحقة**.
3. أرسل حتى 5 رسائل دافئة (يدوياً) وسجّلها في سجل الاستهداف.
4. ردّ خلال 30 دقيقة على أي رد وارد، واحجز اجتماعات اكتشاف.
5. حوّل الاهتمام إلى **Transformation Diagnostic Sprint** وسجّل أي دفعة في CRM.

**الإيقاع الأسبوعي:** بطاقة أداء المؤسس + مراجعة سجل الاحتكاك (friction log) + قرار واحد.

---

## 4) خطة 30/60/90 / 30-60-90 plan
(مرجع: `docs/03_30_60_90_DAY_PLAN.md`)

| المرحلة | الهدف | شرط التوقف / Stop condition |
|---|---|---|
| **1–30 إثبات الإسفين** | 1 تدقيق مُسلّم، 1 case study، 1 شريك | 0 تدقيقات بعد 30 تواصل → غيّر الإسفين |
| **31–60 المضاعفة** | 3 تجارب مدفوعة، 1 case study منشورة، 1 شريك بيع | إلغاء عميل → أصلح التسليم |
| **61–90 موتور قابل للتكرار** | 1 setter، 1 محادثة enterprise، 1 QBR | 0 عملاء جدد → أعد كتابة العرض |

مقاييس: يوم 30 (≈80 تواصل، ≥20% رد، 1 تجربة نشطة) → يوم 60 (3 تجارب، ≈180 تواصل) → يوم 90 (5+ تجارب، 2+ case studies، 2+ شركاء، ≈330 تواصل).

---

## 5) سلّم العروض / Offer ladder
(مرجع: `docs/DEALIX_BUSINESS_MODEL.md`)

| # | العرض | السعر |
|---|---|---|
| 1 | التشخيص المجاني / Free Diagnostic | مجاني (مغناطيس عملاء، 30 د) |
| 2 | Micro Sprint | 499 SAR |
| 3 | Data Pack | 1,500 SAR |
| 4 | Managed Ops | 2,999–4,999 SAR/شهر |
| 5 | **Transformation Diagnostic Sprint** | 7,500–25,000 SAR (المدخل المدفوع الأساسي) |
| 6 | Custom Enterprise System | 25,000–100,000+ SAR |

قواعد تجارية: التشخيص 100% مقدّماً؛ Starter OS بنسبة 70% مقدّماً و30% قبل الإطلاق؛ لا ضمان أرقام إيرادات؛ لا عمل مخصّص بدون تشخيص مدفوع أو عربون.

---

## 6) الأمان والموافقة / Safety & approval gates
(مرجع: `docs/DEALIX_SAFE_EXECUTION_RULES.md` + `docs/distribution/REVENUE_EXECUTION_OS_AR.md`)

**تلقائي:** الصياغة، التقييم، تحديث قوائم CRM، تقارير المدير التنفيذي، بناء الغرفة.
**يتطلب موافقة المؤسس:** إرسال أي رسالة، العروض، التسعير، الفواتير، العقود، تصدير البيانات، الدمج إلى main، تدوير الأسرار، النشر للإنتاج.

**الـ 11 non-negotiables (مختصرة):** الذكاء يصوغ والمؤسس يوافق والنظام يتتبّع · لا إرسال خارجي تلقائي في v1 · لا واتساب بارد · لا أتمتة LinkedIn · لا scraping · كل المسودات معلّقة للموافقة · لا ادعاءات مضمونة · لا PII في السجلات · إثبات مدعوم (L0–L5) · ربط كل عرض بمنتج كتالوج · لا نشر إنتاج ولا أسرار داخل نظام تنفيذ الإيرادات.

---

## 7) غرفة القيادة الموحّدة / Unified Command Room

```bash
python scripts/dealix_unified_command_room.py            # يبني اللوحة
python scripts/dealix_unified_command_room.py --dry-run  # ملخص بلا كتابة
```

لوحة HTML واحدة (للقراءة فقط، تعمل بدون إنترنت) تجمع: شريط الجاهزية + عدّاد العملاء المدفوعين، بطاقات KPI، إجراءات اليوم، الإجراءات العالقة، القمع، خط الأنابيب حسب المرحلة، المتابعات المستحقة، التوزيع حسب القطاع، وسلّم العروض. تُولَّد في `reports/command_room/index.html`.

---

## 8) الوثائق المرجعية / Reference docs
- `docs/CEO_OPERATING_CONTEXT.md` — السياق الاستراتيجي وأهداف الإيرادات.
- `docs/DEALIX_BUSINESS_MODEL.md` — سلّم العروض والاقتصاد الوحدوي.
- `docs/DEALIX_SAFE_EXECUTION_RULES.md` — قواعد الأمان الإلزامية.
- `docs/02_FIRST_7_DAYS_EXECUTION.md` — خطة الأسبوع الأول يوماً بيوم.
- `docs/03_30_60_90_DAY_PLAN.md` — خطة الدخول للسوق.
- `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md` — البوابات التسع.
- `docs/WAVE17_FOUNDER_DAY1_LAUNCH_KIT.md` — دليل التشغيل اليومي للمؤسس.
- `docs/WAVE17_EVIDENCE_TABLE.md` — جدول جاهزية الإطلاق.
- `docs/distribution/REVENUE_EXECUTION_OS_AR.md` — الـ 11 non-negotiables.
