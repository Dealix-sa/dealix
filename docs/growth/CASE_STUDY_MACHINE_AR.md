# Case Study Machine — مصنع دراسات الحالة

> Section 47. ستّة أنواع دراسات حالة، قالب Before/Action/Output/Outcome/Learning/Next، وهيكل أوّل دراسة داخليّة.
> Module path: `dealix/growth_os/case_studies/`

---

## مبدأ تشغيل — Operating Principle

كل دراسة حالة في Dealix إمّا:
- **Real & Anonymized** — عميل حقيقي، اسم مُستبدَل ("Agency X")، أرقام مُتحقَّقة أو "estimated".
- **Hypothetical / case-safe template** — لتوضيح المنهج، مع وسم واضح.

لا اختراع لعملاء. لا أرقام بلا مصدر. كل ادعاء مرتبط بـ `ProofPack` أو موسوم `<TBD: founder fill>`.

---

## أنواع دراسات الحالة الستّ — 6 Case Study Types

| # | النوع | الغرض | الجمهور |
|---|---|---|---|
| 1 | Sprint Outcome | يوثّق نتيجة sprint واحد | عملاء محتملون |
| 2 | Governance Win | يوثّق منع risk قبل وقوعه | C-suite |
| 3 | Partner Success | شريك نجح في إعادة بيع | شركاء محتملون |
| 4 | Internal (Dealix-on-Dealix) | كيف استخدم Dealix أدواته على نفسه | الكلّ |
| 5 | Refusal Case | لماذا رفضنا صفقة | جمهور الثقة |
| 6 | Sector Pattern | نمط متكرّر عبر عدّة عملاء | تقارير قطاعيّة |

---

## القالب الموحَّد — Unified Template

كل دراسة حالة تتبع 6 أقسام:

### 1) Before — ما كان قبل

السياق، الألم، ما الذي حاوله العميل سابقاً.

### 2) Action — ما تمّ

ما الذي قام به Dealix (أو الشريك) — منهج، أدوات، مدّة.

### 3) Output — المخرجات

deliverables محسوسة: ProofPack، تقرير، playbook، عدد ادّعاءات موثَّقة.

### 4) Outcome — النتيجة

ما الذي تغيّر للعميل. إن الرقم مُتحقَّق → اذكره مع المصدر. إن تقديري → اوسمه "estimated".

### 5) Learning — التعلّم

ما الذي أضاف Dealix للـ playbook نتيجة هذه الحالة.

### 6) Next — الخطوة التالية

ما الذي يحدث للعميل بعد ذلك (retention / expansion / referral)، وما الذي نختبره داخلياً.

---

## Disclosure Block — كلّ دراسة تنتهي بـ:

```
- Customer name anonymized.
- Numbers marked "estimated" until reconciled by third party.
- ProofPack reference: <PP-ID or "internal-only">.
- Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
```

---

## أوّل دراسة حالة داخليّة — Dealix Hermes Internal Case

> Type: Internal (Dealix-on-Dealix). Status: case-safe template. All numbers `<TBD: founder fill>`.

### 1) Before

قبل تشغيل Hermes داخل Dealix، كان توليد leads + صياغة الرسائل + تحضير المقترحات يستهلك `<TBD>` ساعات/أسبوع من المؤسس. الـ pipeline متذبذب، الـ follow-up غير منتظم.

### 2) Action

- شغّلنا `signal_radar_agent` على RSS قطاعيّة + صفحات SDAIA العامة.
- بنينا AccountCards لـ `<TBD>` حساب مرشَّح عبر `account_enricher_agent`.
- صاغ `message_drafter_agent` `<TBD>` رسالة LinkedIn DM مسوّدة.
- راجع المؤسس وأرسل `<TBD>` منها يدويّاً.
- صاغ `proposal_drafter_agent` `<TBD>` مقترح بناءً على templates معتمدة.

### 3) Output

- `<TBD>` SignalCard.
- `<TBD>` AccountCard.
- `<TBD>` MessageDraft.
- `<TBD>` ProposalDraft.
- `<TBD>` AI Run Ledger entry موثَّق.

### 4) Outcome (estimated)

- محادثات مفتوحة: `<TBD>`.
- اجتماعات محجوزة: `<TBD>`.
- مقترحات أُرسلت: `<TBD>`.
- ساعات المؤسس المُحرَّرة/أسبوع: `<TBD>`.

> كل الأرقام تقديريّة قبل audit طرف ثالث.

### 5) Learning

- زاوية "Compliance angle" أعلى reply_rate في وكالات الرياض من زاوية "Revenue angle" (تجربة EXP-2026-0001).
- المقترح بـ scope أصغر (Snapshot فقط، بدون pilot) close_rate أعلى لـ ICP الوكالات.
- Founder approval خلال 24 ساعة يضاعف الـ conversion، بعدها يضعف.

### 6) Next

- توسعة Hermes ليشمل partner-led drafts.
- تجربة EXP-2026-0017 (price test 5K vs 8K).
- نشر هذه الدراسة كـ case-safe template للشركاء.

### Disclosure Block

```
- Customer name: Dealix (internal use).
- All numbers estimated; placeholders <TBD: founder fill>.
- ProofPack reference: internal-only.
- Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
```

---

## دورة الإنتاج — Production Cadence

- **شهرياً.** 1 Sprint Outcome + 1 Internal.
- **ربع سنوي.** 1 Sector Pattern + 1 Refusal Case.
- **عند الحدوث.** Partner Success + Governance Win.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
