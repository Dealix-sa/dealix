# 07 — Support OS

**Status: FUTURE** · نظام دعم العميل — The Customer Support System

> Support OS يُصنّف، يقترح، ويصعّد — لكنه **لا يرسل**. كل ردّ خارجي مسودّة تنتظر موافقة. الدعم مصدر ذكاء، لا قناة إرسال آلي.

## الغرض — Purpose

Support OS هو النظام الذي يستقبل طلبات الدعم ويحوّلها إلى **عمل مُحوكَم**: تصنيف التذاكر، مسودّات ردود، تصعيد ما يستحق، رصد المشكلات المتكرّرة، وتنبيهات تجاوز المهلة. مُخرَجه الأهم ليس الردّ نفسه، بل **ذكاء الدعم**: ما الذي يكسر، كم مرّة، وأين يجب أن يتغيّر المنتج أو التسليم.

## القيمة للعميل — Value to Customer

- **ردّ أسرع وأدقّ** — مسودّة جاهزة تستند إلى تاريخ الحساب، يراجعها المؤسس قبل الإرسال.
- **لا تكرار للمشكلة نفسها** — المشكلات المتكرّرة تُرصَد وتُعالَج عند الجذر.
- **التزام بالمهلة** — تنبيهات SLA تمنع التذاكر المنسيّة.

## القدرات الأساسية — Core Capabilities

- **Ticket classification** — تصنيف التذكرة (نوع، خطورة، نظام مسؤول).
- **Response drafts** — مسودّات ردود ثنائية اللغة للمراجعة.
- **Escalation** — تصعيد ما يتجاوز حدود الدعم العادي.
- **Recurring issues** — رصد الأنماط المتكرّرة وتجميعها.
- **SLA alerts** — تنبيهات قرب/تجاوز المهلة.
- **Support intelligence** — تحويل التذاكر إلى مُدخَل للمنتج والتسليم.

## مسار التذكرة — Ticket Flow

1. **Intake** — استلام التذكرة وربطها بـ Account brain من [CLIENT_OS.md](CLIENT_OS.md).
2. **Classify** — نوع، خطورة، النظام المسؤول.
3. **Draft** — مسودّة ردّ مبنية على السياق والدليل.
4. **Approve** — موافقة المؤسس (بوّابة إلزامية).
5. **Send (manual)** — إرسال يدوي بعد الموافقة فقط.
6. **Learn** — قيد في Support intelligence إن كان نمطًا متكرّرًا.

## المُدخلات والمُخرجات — Inputs / Outputs

| المُدخلات — Inputs | المُخرجات — Outputs |
|---|---|
| تذاكر/طلبات العميل | Classified tickets |
| Account brain من [CLIENT_OS.md](CLIENT_OS.md) | Response drafts (للموافقة) |
| معايير القبول من [DELIVERY_OS.md](DELIVERY_OS.md) | Escalation list |
| سجل التسليم | Recurring-issue report + SLA alerts |

## البوّابات والقواعد — Gates / Rules

- **No auto-send** — كل ردّ خارجي مسودّة تنتظر موافقة؛ إرسال يدوي.
- **No mass WhatsApp, no bulk outreach** — الدعم ردّ على طلب قائم، لا حملة.
- **No external customer-facing action without founder approval.**
- **No customer data for model training** — تذاكر الدعم لخدمة العميل فقط.
- **No fake proof** — تنبيهات SLA تعكس الحالة الفعلية، لا حالة مُجمَّلة.

راجع: [../05_governance_os/CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md) و [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).

## ذكاء الدعم — Support Intelligence Loop

```
tickets  →  recurring patterns  →  product / delivery fix
   ↑_______________________________________________|
```

المشكلة المتكرّرة ليست عبئًا — هي إشارة. ما يتكرّر في الدعم يصبح تحسينًا في التسليم أو مُدخَلًا لخارطة المنتج.

## الربط بالأنظمة الأخرى — Connects To

- يقرأ Account brain من [CLIENT_OS.md](CLIENT_OS.md) ويُغذّيه بتنبيهات الرضا.
- يربط التذاكر بمعايير القبول في [DELIVERY_OS.md](DELIVERY_OS.md).
- يُسلّم تنبيهات SLA والتصعيد إلى [COMMAND_OS.md](COMMAND_OS.md).
- يُغذّي الأنماط المتكرّرة إلى [KNOWLEDGE_OS.md](KNOWLEDGE_OS.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
