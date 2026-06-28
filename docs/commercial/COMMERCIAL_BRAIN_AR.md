# العقل التجاري (Commercial Brain)

العقل هو نواة التفكير في المنظومة الحيّة: يحلّل الحساب/المحادثة، يقرّر **الخطوة
التالية الأفضل** عبر أي حركة تجارية، يختار زاوية إقناع صادقة، يخطّط للتفاوض ضمن
الحدود، ويصيغ الرد التالي — مع تتبّع للأسباب (rationale) دائماً.

## نوعان من العقل

### 1) HeuristicBrain (الافتراضي)
- حتمي (deterministic) وقابل للتفسير وبدون أي اعتماديات خارجية.
- قرار حقيقي مبني على الحالة + الإشارات (وليس قالباً ثابتاً):
  - نية واردة `interested` → اقتراح حجز (booking).
  - `price_objection` → مكتب التفاوض (negotiation).
  - `contract_request` → تصعيد للمؤسس (A3) — لا قبول.
  - `unsubscribe` → احترام الإلغاء فوراً (terminal).
  - لا نية واردة → افتتاحية بأولوية حسب درجة ICP.
- هذا ما تختبره مجموعة الاختبارات (سلوك ثابت 100%).

### 2) LLMBrain (اختياري)
- يُفعّل فقط عند `COMMERCIAL_LLM_ENABLED=true` ووجود مفتاح مزوّد.
- يستخدم نموذجاً حقيقياً عبر `core.llm` **للصياغة وزاوية الإقناع فقط**.
- التوجيه والأمان وحارس الادعاءات والموافقات تبقى في المسار الحتمي.
- عند أي خطأ (لا مفتاح، استيراد، مهلة) يعود تلقائياً إلى `HeuristicBrain`.
  السلوك دائماً معرّف وآمن وقابل للاختبار بدون مفتاح.

## ماذا يُنتج العقل؟

`ActionRecommendation`:
- `recommended_action` (مثل `send_opener`, `propose_booking`, `handle_objection`, `escalate_to_founder`, `honour_optout`)
- `motion`, `channel`, `next_stage`
- `rationale[]` (لماذا)
- `confidence` (0..1) و`priority` (1 الأعلى)
- `persuasion_angle`, `risk_level`, `requires_approval`

## الاستخدام

```python
from app.commercial.reasoning import get_brain
brain = get_brain()                 # heuristic افتراضياً
rec = brain.recommend_action(context)
draft = brain.draft_reply(context)  # نص ثنائي اللغة، خالٍ من الادعاءات
```

> العقل لا يرسل ولا يلتزم بسعر/خصم/عقد. يقترح فقط، والإرسال يمرّ ببوابات الأمان.
