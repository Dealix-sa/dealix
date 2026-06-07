# بطاقة التأهيل المرجعية — Qualification Cheatsheet
## Dealix — العمليات الذكية المحوكَمة لقطاع B2B السعودي / Governed AI Operations for Saudi B2B

> **DRAFT — تتطلب موافقة الفاوندر / founder approval required.**
> هذه بطاقة داخلية للفاوندر فقط — لا تُرسَل للعميل. غرضها: تحويل إجابات مكالمة الاكتشاف إلى قرار واحد محكوم.
> *Internal founder-only sheet — never sent to a customer. Purpose: turn discovery answers into one governed decision.*
>
> المصدر الوحيد للحقيقة هو `auto_client_acquisition/sales_os/qualification.qualify(...)`. هذه البطاقة تشرح مخرجاته، ولا تستبدلها.
> *Single source of truth is `auto_client_acquisition/sales_os/qualification.qualify(...)`. This sheet explains its output; it does not replace it.*

---

## 1. الأسئلة الثمانية والأوزان / The 8 questions and weights

تُسأل أثناء مكالمة الاكتشاف. كل سؤال إجابته نعم/لا (Boolean)، ومجموع الأوزان = 100.
*Asked during discovery. Each is a yes/no flag; weights sum to 100.*

| # | العَلَم / Flag | الوزن / Weight | ما الذي يثبته / What it proves | كيف نسأله (عربي) / How to ask (Arabic) |
|---|---|---|---|---|
| 1 | `pain_clear` | 15 | الألم محدد وقابل للقياس، ليس فضولاً عاماً. / Pain is specific and measurable, not general curiosity. | "ما المشكلة الواحدة التي لو حُلّت هذا الشهر، تغيّر إيرادك؟" |
| 2 | `owner_present` | 15 | صاحب القرار على المكالمة أو ملتزم بها. / The decision-owner is on the call or committed to it. | "من يقرّر الميزانية لهذا؟ هل هو معنا الآن؟" |
| 3 | `data_available` | 15 | توجد بيانات جاهزة (CRM / CSV / سجلّات). / Real data is ready (CRM / CSV / records). | "هل بياناتكم في نظام يمكن تصديره، أم على ورق ومحادثات؟" |
| 4 | `accepts_governance` | 10 | يقبل الحوكمة: موافقة، PDPL، لا إرسال آلي. / Accepts governance: consent, PDPL, no auto-send. | "نعمل بموافقتك على كل خطوة، ووفق نظام حماية البيانات. هل هذا يناسبكم؟" |
| 5 | `has_budget` | 10 | ميزانية واقعية تتجاوز التشخيص المجاني. / Realistic budget beyond the free diagnostic. | "هل تخصيص 499 ريال لتجربة أولى محكومة وارد لديكم؟" |
| 6 | `wants_safe_methods` | 10 | **لا** يطلب سحب بيانات / سبام / ضمانات. / **NOT** asking for scraping / spam / guarantees. | "ما الذي جرّبتموه سابقاً؟ هل تتوقعون رسائل جماعية أم عمل محكوم بالموافقة؟" |
| 7 | `proof_path_visible` | 15 | يوجد مسار واضح لإثبات قابل للقياس خلال السبرنت. / A clear path to measurable proof inside the sprint. | "ما الرقم الذي لو تحرّك نعتبره دليلاً؟ هل يمكن قياسه خلال 7 أيام؟" |
| 8 | `retainer_path_visible` | 10 | يوجد عمل متكرر يبرّر اشتراكاً لاحقاً. / Recurring work that could justify a later retainer. | "بعد التجربة الأولى، هل هناك عمل شهري متكرر يستحق إدارته؟" |

> **قاعدة الصدق:** `wants_safe_methods = false` يعني العميل يطلب شيئاً نرفضه. هذا ليس نقصاً في النقاط فقط — راجع شجرة القرار في القسم 4.
> *Honesty rule: `wants_safe_methods = false` means the customer is asking for something we refuse. This is not just a low score — see the decision tree in Section 4.*

---

## 2. حساب النقاط / Scoring

اجمع وزن كل عَلَم إجابته "نعم". المجموع من 0 إلى 100.
*Sum the weight of every flag answered "yes." Total is 0–100.*

```
score = Σ weight[flag] حيث flag = true
```

مثال / Example: pain_clear + owner_present + data_available + proof_path_visible (نعم) = 15+15+15+15 = **60**.

| النطاق / Band | الدلالة / Meaning |
|---|---|
| 85–100 | ملاءمة قوية عبر معظم الإشارات. / Strong fit across most signals. |
| 70–84 | ملاءمة جزئية — شكّل خطوة أولى أصغر. / Partial fit — shape a smaller first step. |
| 45–69 | إشارة منخفضة — ابدأ بتشخيص. / Low signal — start with a diagnostic. |
| 0–44 | ملاءمة غير كافية للانخراط. / Not enough fit to engage. |

> النطاقات أعلاه تطابق الكود حرفياً (`qualify`): العتبات 85 / 70 / 45. لا تخترع عتبة سادسة.
> *Bands above mirror the code (`qualify`) exactly: thresholds 85 / 70 / 45. Do not invent a sixth band.*

---

## 3. القرارات الخمسة / The 5 decisions

هذه هي المجموعة الكاملة من `Decision` في الكود. لا قرار سادس.
*This is the complete `Decision` set in code. No sixth decision exists.*

| القرار / Decision | المعنى / Meaning | حركة الفاوندر / Founder move |
|---|---|---|
| **ACCEPT** | ملاءمة قوية، الحوكمة مقبولة، الألم والإثبات واضحان. / Strong fit; governance accepted; pain and proof clear. | ادعُ إلى التشخيص المجاني، ثم اعرض سبرنت 499 ريال. / Invite to Free Diagnostic, then offer the 499 SAR Sprint. |
| **DIAGNOSTIC_ONLY** | ملاءمة لكن الإشارة غير كافية للسبرنت بعد. / A fit, but signal not yet strong enough for the sprint. | شغّل التشخيص المجاني فقط. القرار بالسبرنت يأتي من نتيجة التشخيص. / Run the Free Diagnostic only. The sprint call comes from the diagnostic outcome. |
| **REFRAME** | نيّة حقيقية، إطار خاطئ — يطلب شيئاً لا نقدّمه لكن الحاجة الأساس تناسبنا. / Real intent, wrong frame — asks for something we do not offer, but the core need fits. | أعد التأطير في 3 أسطر، ثم أعد تشغيل `qualify` بالإطار الجديد. / Send a 3-line reframe, then re-run `qualify` with the new framing. |
| **REJECT** | خارج النطاق، أو انتهاك لأحد اللاءات الـ 11 (سحب بيانات / سبام / ضمانات). / Outside scope, or a violation of one of the 11 non-negotiables (scraping / spam / guarantees). | رفض مهذّب + بديل آمن. سجّل في `friction_log`. لا متابعة. / Polite refusal + safe alternative. Log in `friction_log`. No follow-up. |
| **REFER_OUT** | حاجة مشروعة لكنها أنسب لشريك، أو رفض الحوكمة. / Legitimate need better served by a partner, or governance refused. | حوّل لشريك مناسب. سجّل في `referral_ledger`. / Refer to a partner. Log in `referral_ledger`. |

---

## 4. شجرة القرار / Decision tree

اتبعها من أعلى لأسفل. أول شرط يتحقق يحسم القرار — تماماً كما في `qualify`.
*Top to bottom. The first matching condition decides — exactly as in `qualify`.*

```
START
  │
  ├─ هل النص أو الطلب يتضمن: سحب بيانات / سبام / واتساب بارد / أتمتة لينكدإن / ضمان مبيعات؟
  │  Does the request mention: scraping / spam / cold WhatsApp / LinkedIn automation / guaranteed sales?
  │     └─ نعم / yes ──────────────► REJECT  (انتهاك لائحة غير قابلة للتفاوض / non-negotiable violation)
  │                                          → اعرض البديل الآمن. الموصى به: not_a_fit_decline_politely
  │
  ├─ هل العميل يرفض الأساليب الآمنة؟ (wants_safe_methods = false)
  │  Does the customer refuse safe methods?
  │     └─ نعم / yes ──────────────► REJECT  (declined_safe_methods)
  │
  ├─ هل يقبل الحوكمة؟ (accepts_governance)
  │  Does the customer accept governance?
  │     └─ لا / no ───────────────► REFER_OUT  (governance_not_accepted)
  │
  ├─ احسب النقاط / compute score
  │     ├─ score ≥ 85 ───────────► ACCEPT            → Rung 1: سبرنت ذكاء الإيراد 499 ريال
  │     │                                              (revenue_intelligence_sprint)
  │     ├─ 70 ≤ score < 85 ───────► data_available?
  │     │                            ├─ نعم/yes → REFRAME          → شكّل تشخيص "البيانات إلى إيراد"
  │     │                            └─ لا/no  → DIAGNOSTIC_ONLY   → Rung 0: تشخيص مجاني
  │     │                                          (data_to_revenue_diagnostic)
  │     ├─ 45 ≤ score < 70 ───────► DIAGNOSTIC_ONLY  → Rung 0: تشخيص القدرات (capability_diagnostic)
  │     └─ score < 45 ────────────► REFER_OUT        → ملاءمة غير كافية (refer_out_not_enough_fit)
END
```

> **ترتيب البوابات يهم:** اللاءات تُفحص قبل النقاط. عميل بنقاط 95 يطلب سحب بيانات = REJECT، وليس ACCEPT.
> *Gate order matters: non-negotiables are checked before the score. A 95-point lead asking for scraping = REJECT, not ACCEPT.*

---

## 5. الربط بالسلّم / Mapping to the rung

| القرار + الإشارة / Decision + signal | الرُّتبة الموصى بها / Recommended rung | السعر / Price (SAR) |
|---|---|---|
| ACCEPT (ألم + مالك + بيانات جاهزة) | Rung 1 — سبرنت ذكاء الإيراد / Revenue Intelligence Sprint | 499 |
| ACCEPT + تصدير CSV/CRM + معالجة PII | Rung 2 — حزمة البيانات إلى إيراد / Data-to-Revenue Pack | 1,500 |
| DIAGNOSTIC_ONLY / REFRAME | Rung 0 — التشخيص المجاني / Free Diagnostic | 0 |
| بعد السبرنت: درجة الإثبات ≥ 80 + التبنّي ≥ 70 + مالك سير العمل | Rung 3 — إدارة عمليات الإيراد / Managed Revenue Ops | 2,999–4,999/شهر |
| نطاق يتجاوز السلّم | Rung 4 — إعداد ذكاء اصطناعي مخصّص / Custom AI Setup | 5,000–25,000 + 1K/شهر |
| بنك / شركة كبرى / قطاع منظَّم | Enterprise — مراجعة حوكمة الذكاء الاصطناعي / AI Governance Review | 25K–50K |
| REJECT | لا عرض — بديل آمن فقط / No offer — safe alternative only | — |
| REFER_OUT | لا عرض — إحالة لشريك / No offer — partner referral | — |

> بوابة Rung 3 (الاشتراك) لا تُفتح إلا بـ `adoption_os.retainer_readiness.evaluate(...).eligible == True`. لا تعرضها قبل ذلك.
> *The Rung 3 (retainer) gate opens only when `adoption_os.retainer_readiness.evaluate(...).eligible == True`. Do not pitch it before then.*

---

## 6. استدعاء الكود / Invoking the code

```python
from auto_client_acquisition.sales_os.qualification import qualify

result = qualify(
    pain_clear=True,
    owner_present=True,
    data_available=True,
    accepts_governance=True,
    has_budget=True,
    wants_safe_methods=True,
    proof_path_visible=True,
    retainer_path_visible=False,
    raw_request_text="<verbatim words the customer used>",
    sector="b2b_services",
    city="Riyadh",
)
# result.decision, result.score, result.recommended_offer,
# result.reasons, result.doctrine_violations
```

> سجّل القرار في `proof_ledger` كحدث `qualify_decision`. لا تتجاوز مخرجات الدالة بتقدير شخصي.
> *Log the decision in `proof_ledger` as a `qualify_decision` event. Do not override the function output with a personal hunch.*

---

> **حالة اليوم / Today's reality:** صفر عملاء مدفوعين. كل رقم في عرض هو تقدير، لا نتيجة مُتحقَّقة.
> *Zero paid customers. Every number in a proposal is an estimate, not a verified outcome.*

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
