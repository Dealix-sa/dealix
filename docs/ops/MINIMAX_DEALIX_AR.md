# MiniMax كمحرّك AI الرئيسي في Dealix

Dealix يستخدم MiniMax داخل **Runtime** (`.env.local` / Railway) — وليس داخل Cursor. Cursor يبقى على OpenAI للبرمجة فقط.

## المرحلة 0 — حساب MiniMax (قبل الكود)

1. [platform.minimax.io](https://platform.minimax.io) → **API Keys** → **Reset** إذا ظهر المفتاح في شات أو PR.
2. انسخ مفتاح **Token Plan** بصيغة `sk-api-…` (لا تستخدم `sk-user-…` — يعطي 401 على chat/completions).
3. ضعه في `.env.local` فقط (لا commit):

```bash
MINIMAX_API_KEY=sk-api-...
MINIMAX_BASE_URL=https://api.minimax.io/v1
MINIMAX_MODEL=MiniMax-M2.7
# أو للسرعة: MiniMax-M2.7-highspeed
```

4. إذا ظهر `insufficient_balance (1008)`:
   - تحقق من **Credits** بجانب Token Plan (Starter: 1500 طلب / 5 ساعات قد لا يكفي بدون رصيد Credits).
   - جرّب نفس الطلب من Console MiniMax؛ إن فشل هناك = حساب، إن نجح = راجع `MINIMAX_BASE_URL` و`sk-api`.

## متغيرات Dealix

| المتغير | القيمة المقترحة |
|--------|------------------|
| `AI_PRIMARY_PROVIDER` | `minimax` |
| `AI_FALLBACK_PROVIDER` | `openai` أو `deepseek` |
| `DEALIX_LLM_PROFILE` | `minimax` |

يُفعَّل تلقائياً `profile=minimax` إذا وُجد `MINIMAX_API_KEY` ولا يوجد `ANTHROPIC_API_KEY`.

## حدود API

- `max_completion_tokens` ≤ **2048** (يضبطها `MiniMaxClient`).
- رسائل التفكير `<think>` تُزال من الرد قبل العرض.

## تحقق محلي

```bash
python3 scripts/verify_minimax_dealix.py
python3 scripts/verify_minimax_dealix.py --ping
python3 scripts/verify_ai_runtime_providers.py --ping
curl -s http://localhost:8000/api/v1/ai-runtime/status \
  -H "X-Admin-API-Key: YOUR_ADMIN_KEY"
```

## Railway (إنتاج)

على خدمة API في Railway:

```
MINIMAX_API_KEY=sk-api-...
MINIMAX_BASE_URL=https://api.minimax.io/v1
MINIMAX_MODEL=MiniMax-M2.7
AI_PRIMARY_PROVIDER=minimax
AI_FALLBACK_PROVIDER=openai
DEALIX_LLM_PROFILE=minimax
```

الواجهة الأمامية **لا** تحتاج مفتاح MiniMax — فقط `DEALIX_ADMIN_API_KEY` لاستدعاء `/api/v1/ai-runtime/chat`.

بعد النشر:

```bash
DEALIX_API_BASE=https://your-api.railway.app \
DEALIX_ADMIN_API_KEY=... \
python3 scripts/verify_minimax_dealix.py --ping
```

اختياري — ping في `/health/deep`:

```bash
DEALIX_HEALTH_MINIMAX_PING=1
```

## مسارات تستخدم MiniMax أولاً

- `core/llm/dealix_chat.py` — نقطة دخول موحّدة
- `POST /api/v1/ai-runtime/chat`
- `generate_llm_brief` (تقرير المؤسس اليومي)
- وكلاء: outreach، proposal، qualification (عند `DEALIX_LLM_PROFILE=minimax`)

التصنيف السريع (Groq) يبقى عبر `ModelRouter` لتوفير الحصة.

## أمان

- لا إرسال LinkedIn/WhatsApp تلقائي — مسودات + موافقة فقط.
- لا تضع المفاتيح في Git أو PR.
