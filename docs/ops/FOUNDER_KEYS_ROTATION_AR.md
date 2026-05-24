# تدوير مفاتيح المؤسس — بعد تسريب محتمل

> إذا ظهرت مفاتيح API في محادثة Cursor أو commit بالخطأ — نفّذ هذا الملف فورًا.

## 1) أين تُخزَّن المفاتيح (صحيح)

| البيئة | الملف / المكان |
|--------|----------------|
| محلي | `.env.local` (مستبعد من Git) — انسخ من [`.env.local.example`](../../.env.local.example) |
| إنتاج | Railway → Variables (Secrets) |
| Cursor IDE | **OpenAI فقط** — لا تضف MiniMax/DeepSeek في Cursor Models |

## 2) ماذا تدوّر

| مفتاح | أين تدوّره |
|-------|------------|
| OpenAI | platform.openai.com |
| DeepSeek | platform.deepseek.com |
| MiniMax | MiniMax Console |
| PostHog | PostHog → Project settings → API keys |
| Calendly PAT + webhook signing | Calendly → Integrations → API & webhooks |
| Calendly OAuth client secret | Calendly → OAuth app (regenerate if leaked) |
| HubSpot Private App | HubSpot → Settings → Private Apps |
| GitHub PAT | GitHub → Settings → Developer settings |
| `ADMIN_API_KEYS` | أنشئ مفتاحًا جديدًا وحدّث Railway + `frontend` proxy |

## 3) بعد التدوير

```bash
cp .env.local.example .env.local
# املأ القيم الجديدة فقط في .env.local

python3 scripts/verify_ai_runtime_providers.py
python3 scripts/verify_ai_runtime_providers.py --ping

bash scripts/founder_go_live_verify.sh
```

## 4) ممنوع

- لا تلصق مفاتيح في PR أو Issues أو Slack
- لا ترفع `.env.local` إلى Git
- لا تضع مفاتيح في `NEXT_PUBLIC_*` إلا admin key للتطوير المحلي فقط
