# 05 — Delivery OS

**Status: DOCS_ONLY** · من الوعد إلى التسليم — From Promise to Delivery

> Delivery OS يحوّل ما بِيع إلى ما سُلِّم — بمعيار قبول واضح، مهلة معلنة، ومجلّد عميل واحد هو مصدر الحقيقة. لا تسليم بلا مجلّد، ولا إغلاق بلا Proof Pack.

## الغرض — Purpose

Delivery OS هو النظام الذي يأخذ وعد البيع (Command Sprint) ويُنفّذه على مدى 7 أيام بانضباط: مجلّد عميل، خطة تسليم، اتفاق مستوى خدمة (SLA)، إدارة العوائق، معايير قبول، وحزمة إغلاق. مُخرَجه ليس "نشاطًا" بل **تسليمًا مقبولًا موثّقًا بالدليل**. كل تسليم يُغذّي Proof OS بالدليل، ويُغذّي Knowledge OS بالقالب.

## القيمة للعميل — Value to Customer

- **مهلة معلنة ومعيار قبول واضح** — يعرف العميل ماذا سيستلم ومتى، وما الذي يُعتبر "مكتملًا".
- **مجلّد عميل واحد** — لا رسائل متفرّقة؛ مصدر حقيقة واحد قابل للتدقيق.
- **Completion Pack** يُثبت ما سُلِّم فعلًا، لا ما وُعِد به.

## القدرات الأساسية — Core Capabilities

- **Customer folder** — مجلّد العميل الموحّد، مصدر الحقيقة.
- **Delivery plan** — خطة التسليم اليومية المربوطة بالـ 7 أيام.
- **SLA** — اتفاق مستوى الخدمة ومهلة كل مخرَج.
- **Blockers** — رصد العوائق ومالك حلّها وأثرها على المهلة.
- **Acceptance criteria** — معيار قبول لكل مخرَج، يُتّفق عليه مسبقًا.
- **Completion pack** — حزمة الإغلاق التي تُسلَّم للعميل.

## SLA سبرنت القيادة — The 7-Day Command Sprint SLA

التسليم مُحوكَم على 7 أيام، كل يوم له مخرَج ونقطة فحص للمؤسس. راجع كتاب التشغيل التفصيلي: [../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md).

- **اليوم 1:** الانطلاق + جواز المصدر (Source Passport). لا بيانات بلا جواز.
- **الأيام 2–5:** استيراد، فحص جودة، تحليل، بناء المخرجات كمسودّات.
- **الأيام 6–7:** مراجعة، اعتماد، تجميع Completion Pack + Proof Pack.

**قاعدة المهلة:** أي تأخير يُسجَّل كـ blocker في [COMMAND_OS.md](COMMAND_OS.md) Risk Register — لا تأخير صامت.

## تخطيط مجلّد العميل — Customer Folder Layout

مجلّد ثابت لكل عميل مدفوع، بترتيب موحّد:

| الملف | المحتوى |
|---|---|
| `00_intake.md` | الطلب، النطاق، مالك سير العمل |
| `01_source_passport.md` | مصدر كل بيانات + صلاحية الاستخدام |
| `02_data_quality.md` | درجة جودة البيانات (DQ) |
| `03_analysis.md` | التحليل والنتائج الأولية |
| `04_findings.md` | النتائج الموثّقة بالدليل |
| `05_drafts.md` | المسودّات للمراجعة (لا إرسال) |
| `06_approvals.md` | سجل الموافقات |
| `07_delivery_plan.md` | الخطة والمهلة |
| `08_blockers.md` | العوائق ومالكوها |
| `09_completion_pack.md` | حزمة الإغلاق |
| `10_proof_pack.md` | حزمة الإثبات (من Proof OS) |
| `11_upsell_recommendation.md` | توصية التوسّع (تُغذّي Client OS) |

## المُدخلات والمُخرجات — Inputs / Outputs

| المُدخلات — Inputs | المُخرجات — Outputs |
|---|---|
| وعد البيع من [REVENUE_OS.md](REVENUE_OS.md) | Customer folder مكتمل |
| جواز المصدر من Data OS | Completion Pack |
| تعريف معايير القبول | دليل تسليم لـ [PROOF_OS.md](PROOF_OS.md) |
| موافقات المؤسس | توصية upsell لـ [CLIENT_OS.md](CLIENT_OS.md) |

## البوّابات والقواعد — Gates / Rules

- **Every paid customer needs delivery folder + proof pack** — لا إغلاق بلا الاثنين.
- **No external customer-facing action without founder approval** — كل مخرَج خارجي يمرّ بالموافقة.
- **No fake proof** — Completion Pack يعكس ما سُلِّم فعلًا.
- **No silent delay** — التأخير يُسجَّل، لا يُخفى.
- **No customer data for model training.**

## حلقة تراكم القوالب — The Template Compounding Loop

```
delivery  →  reusable template  →  faster next delivery
   ↑__________________________________________|
```

كل تسليم يُنتج درسًا قابلًا للقولبة. ما تعلّمناه مرّة لا نُنفّذه من الصفر مرّة أخرى.

## الربط بالأنظمة الأخرى — Connects To

- يُغذّي الدليل إلى [PROOF_OS.md](PROOF_OS.md) (delivery feeds proof).
- يُغذّي القوالب إلى [KNOWLEDGE_OS.md](KNOWLEDGE_OS.md) (Template Compounding loop).
- يُسلّم حالة التسليم إلى [COMMAND_OS.md](COMMAND_OS.md).
- يُمرّر توصية التوسّع إلى [CLIENT_OS.md](CLIENT_OS.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
