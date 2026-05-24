# إطلاق Railway السريع — المؤسس

مرجع كامل: [`docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md`](RAILWAY_PRODUCTION_SETTINGS_AR.md) · [`DEPLOYMENT.md`](../../DEPLOYMENT.md)

## أمر واحد (A→D)

```bash
export DEALIX_API_BASE=https://api.dealix.me
export DEALIX_ADMIN_API_KEY=<admin-key>
bash scripts/launch_execution_railway.sh
```

## متغيرات AI Runtime على Railway

```bash
MINIMAX_API_KEY=sk-api-...
MINIMAX_BASE_URL=https://api.minimax.io/v1
MINIMAX_MODEL=MiniMax-M2.7
AI_PRIMARY_PROVIDER=minimax
AI_FALLBACK_PROVIDER=openai
DEALIX_LLM_PROFILE=minimax
# اختياري: DEEPSEEK_API_KEY=... (كود/احتياط)
ADMIN_API_KEYS=...
```

تفاصيل: [`MINIMAX_DEALIX_AR.md`](MINIMAX_DEALIX_AR.md) · تحقق: `python3 scripts/verify_minimax_dealix.py --ping`

## فرونت اند ops

```bash
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1
DEALIX_ADMIN_API_KEY=<same as ADMIN_API_KEYS>
```

## تحقق

```bash
bash scripts/founder_production_smoke.sh
bash scripts/official_launch_verify.sh --api-base "$DEALIX_API_BASE"
bash scripts/founder_launch_definition_of_done.sh
```
