# CEO Decision Protocol — Dealix

## الدور — Role

بروتوكول واضح لاتخاذ القرارات اليومية في Dealix بدون تردد وبدون "اجتماعات شبح".

## أنواع القرارات — Decision classes

| Class | أمثلة | المعتمد | المهلة |
| --- | --- | --- | --- |
| **D1 — يومي تشغيلي** | إرسال رسالة معتمدة، تأكيد اجتماع | Founder | ≤ ساعة |
| **D2 — أسبوعي** | قرار Kill/Fix/Scale لحملة | Founder + Trust | ≤ يومين |
| **D3 — استراتيجي** | تغيير ICP، إطلاق قطاع | Founder + Advisor | ≤ 5 أيام |
| **D4 — حدودي** | تجاوز Trust gate | محظور | — |

## نموذج القرار — Decision template

```
Decision ID: D-YYYYMMDD-<n>
Class: D1 | D2 | D3
Question: ?
Options:
  - A — ...
  - B — ...
  - C — Kill
Evidence:
  - learning/...
  - finance/...
Decision: A | B | C
Reversibility: reversible | one-way
Owner: founder
Review date: YYYY-MM-DD
```

## القواعد — Rules

- كل D2 و D3 يُسجَّل في `<private_ops>/founder/decisions.csv`.
- لا قرار D3 بدون evidence من learning memory.
- One-way doors تحتاج reasoning مكتوب صراحة.
- D4 ممنوع — أي طلب لتجاوز Trust gate يُرفض ويُسجَّل في `<private_ops>/trust/refusal_log.csv`.

## الملكية — Ownership

- Owner: Founder.
- Auditor: Trust gate.
