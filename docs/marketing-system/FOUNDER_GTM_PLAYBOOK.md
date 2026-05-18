# Founder GTM Playbook — Dealix

**الدور:** مؤسس يبيع تشغيل إيرادات مُحوكَم — ليس SaaS عام ولا وكالة AI.

**المبدأ:** كل لمسة خارجية = مسودة + موافقة. كل إغلاق = Proof Pack.

---

## 1) منظومة الأصول (أين كل شيء)

| الطبقة | المجلد | متى |
|--------|--------|-----|
| هوية | [`brand/`](brand/) | قبل أي تصميم |
| عرض مباشر B2B | [`presentations/live-deck-b2b-ar.md`](presentations/live-deck-b2b-ar.md) | Discovery → Demo |
| مسح سريع | [`presentations/leave-behind-b2b-ar.md`](presentations/leave-behind-b2b-ar.md) | بعد الاجتماع 24h |
| لجنة شراء | [`presentations/committee/`](presentations/committee/) | CFO / IT / RevOps |
| مستثمر | [`fundraising/`](fundraising/) | VC / شريك استراتيجي |
| تنفيذي | [`collateral/`](collateral/) | One-pager، قصة، تسعير |
| تمكين مبيعات | [`sales-enablement/`](sales-enablement/) | قبل كل مكالمة |
| بريد | [`email-sequences/`](email-sequences/) | متابعة مُحكمة |
| LinkedIn | [`linkedin/`](linkedin/) | 3× أسبوع |
| غرفة عميل | [`digital-sales-room/hub.html`](digital-sales-room/hub.html) | بعد التأهيل |
| ويب | [`web/`](web/) | هبوط + CTA |

---

## 2) سير أسبوع المؤسس (تشغيل)

### الاثنين — Pipeline
- راجع 10 حسابات Top من Revenue Memory / CSV
- حدّث MAP لكل صفقة نشطة
- أرسل متابعة واحدة فقط لكل عميل (لا إغراق)

### الثلاثاء — محتوى
- منشور LinkedIn واحد ([`linkedin/post-templates-ar.md`](linkedin/post-templates-ar.md))
- ربط بـ Proof أو رفض واعٍ (لا بارد)

### الأربعاء — Demo
- Demo بسكربت [`sales-enablement/demo-runbook-ar.md`](sales-enablement/demo-runbook-ar.md)
- اخرج بـ CTA: Diagnostic أو Sprint

### الخميس — إغلاق
- One-pager + Leave-behind + hub link
- [`sales-enablement/mutual-close-checklist-ar.md`](sales-enablement/mutual-close-checklist-ar.md)

### الجمعة — تعلّم
- سجّل اعتراضاً جديداً في [`sales-enablement/objection-matrix-ar.md`](sales-enablement/objection-matrix-ar.md)
- حدّث حالة Proof Pack

---

## 3) سلم العروض (لا تقفز)

```
تشخيص مجاني/مدفوع → Revenue Diagnostic (3,500) → Sprint (9,500) → Pilot (22,000) → Retainer (15,000+)
```

**مرجع أسعار:** [`../commercial/DEALIX_REVOPS_PACKAGES_AR.md`](../commercial/DEALIX_REVOPS_PACKAGES_AR.md)

---

## 4) إقناع لجنة الشراء (CDP)

| الدور | الملف | الرسالة |
|-------|-------|---------|
| Champion | Live deck | نتيجة 7 أيام |
| CFO | [`committee/cfo-slide-ar.md`](presentations/committee/cfo-slide-ar.md) | ROI + مراحل |
| IT/Legal | [`committee/it-slide-ar.md`](presentations/committee/it-slide-ar.md) | PDPL + مسودات |
| RevOps | [`committee/revops-slide-ar.md`](presentations/committee/revops-slide-ar.md) | Pipeline + scoring |

---

## 5) ما لا تفعله (NON_NEGOTIABLES في التسويق)

- لا وعد بعدد صفقات أو إيراد مضمون
- لا «AI-powered» بدون سياق سعودي + حوكمة
- لا إرسال بارد من اسم Dealix أو نيابة عن العميل
- لا قوائم مشتراة في القصة التسويقية

---

## 6) تحقق الإنتاج (قبل Demo كبير)

```powershell
py -3 scripts/verify_railway_production_config.py
curl.exe -fsS https://api.dealix.me/healthz
curl.exe -fsS https://api.dealix.me/version
```

إذا `/version` يعيد 404: استخدم `/health` مؤقتاً — أعد نشر API بعد إضافة `/version` على `health` router.

---

## 7) مقاييس المؤسس (أسبوعياً)

| المقياس | هدف مبكر |
|---------|----------|
| Diagnostics مُسلّمة | 2+ |
| Sprints موقّعة | 1 |
| MAPs محدّثة | 100% صفقات نشطة |
| Proof Packs مكتملة | كل Sprint |
| منشورات LinkedIn | 3 |

---

## 8) رفع Executive

عند طلب «ملخص للإدارة»:

1. [`collateral/executive-one-pager-ar.html`](collateral/executive-one-pager-ar.html) — PDF
2. [`presentations/leave-behind-b2b-ar.md`](presentations/leave-behind-b2b-ar.md)
3. [`collateral/pricing-table-ar.md`](collateral/pricing-table-ar.md)

---

**الإصدار:** 1.0 · مايو 2026
