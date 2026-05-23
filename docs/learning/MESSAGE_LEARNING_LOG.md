# Message Learning Log — Dealix

## الدور

أداء كل رسالة معتمدة — reply rate, sentiment, objection.

## المصدر

```
<private_ops>/learning/message_learning.csv
```

## الحقول

`date,source,insight,evidence,decision,next_action,owner`

يُضاف بشكل تفصيلي في `<private_ops>/distribution/message_performance.csv` مع `message_id, sent_count, reply_count, replies_positive, replies_negative, objections`.

## أمثلة على insights

- "subject line بالعربية يحصل reply rate 2x أعلى من English".
- "ذكر ZATCA في أول جملة يقلل reply rate".
- "CTA = '15-دقيقة مكالمة' > '30-دقيقة demo'".

## القواعد

- لا "improvement" بدون اختبار A/B على ≥20 رسالة.
- لا "best message" بدون evidence من ≥3 paid customers.

## الملكية

- Owner: Founder.
