# Company Utilization Report (V7)

> AI prepares. Founder approves. Manual action only. No external sending.

## التقرير العربي
يقيس هذا التقرير مدى استخدام أدوات V7 فعليًا: هل المولّدات والمدقّقات والأصول
المساندة موجودة وجاهزة لتشغيل آلة الإيراد اليومية؟ كل المخرجات للمراجعة فقط.

## Summary (EN)
This report measures whether the V7 toolset is actually wired and usable: are
the generators, validators, and supporting assets present so the daily revenue
machine can run? All outputs are review-only.

## Generators tracked
- `commercial_generate_400_drafts.py`
- `founder_action_queue_generate.py`
- `founder_revenue_dashboard.py`
- `diagnostic_pack_generate.py`
- `proposal_seed_generate.py`
- `proof_asset_template_generate.py`
- `daily_ceo_brief_generate.py`
- `weekly_board_report_generate.py`
- `market_intelligence_brief_generate.py`

## Validators tracked
- `revenue_manual_events_validate.py`
- `operating_memory_validate.py`
- `revenue_execution_verify.py`
- `master_startup_command_verify.py`

## Supporting assets
- `config/market_intelligence_signals.json`
- `config/operating_memory_schemas.json`
- `data/revenue_manual_events.example.jsonl`

## Verification
Run `python scripts/company_utilization_verify.py`. Result is written to
`outputs/company_utilization/company_utilization_verification.json` with a
PASS/FAIL status and any missing components listed.

## Safety posture
Utilization tracking is read-only over the repo tree. No external sending, no
scraping, no secrets.
