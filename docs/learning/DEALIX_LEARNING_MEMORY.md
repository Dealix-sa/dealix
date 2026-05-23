# Dealix Learning Memory — System

## الدور — Role

الذاكرة المؤسسية لكل ما تعلّمته Dealix من السوق. لا يكفي "memory" داخل LLM — هذه الذاكرة قابلة للمراجعة والاسترجاع.

## السجلات — Logs

- [MARKET_LEARNING_LOG.md](./MARKET_LEARNING_LOG.md) — ما تعلمناه عن السوق ككل.
- [MESSAGE_LEARNING_LOG.md](./MESSAGE_LEARNING_LOG.md) — أداء الرسائل.
- [OFFER_LEARNING_LOG.md](./OFFER_LEARNING_LOG.md) — أداء العروض.
- [SECTOR_LEARNING_LOG.md](./SECTOR_LEARNING_LOG.md) — أداء القطاعات.

## مصدر الحقيقة — Source of truth

```
<private_ops>/learning/market_learning.csv
<private_ops>/learning/message_learning.csv
<private_ops>/learning/offer_learning.csv
<private_ops>/learning/sector_learning.csv
```

## واجهة API الداخلية

- `GET /api/v1/internal/learning/summary` — admin-key gated.

## الحقول — Fields (مشتركة)

`date,source,insight,evidence,decision,next_action,owner`

## القواعد — Rules

- لا "تعلّم" بدون evidence مكتوب.
- كل قرار Kill/Fix/Scale يستند لـ row في أحد السجلات.
- لا حذف rows — `decision: superseded` بدلًا.
- مراجعة كل جمعة (Learning loop sync).

## الملكية — Ownership

- Owner: Founder.
- Backup: Sales lead.
