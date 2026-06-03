# Market Production OS — فهرس الطبقة — Index

نظام إنتاج سوق محكوم للشركات السعودية: ينتج بكثافة (250 مسودة/يوم)، يفلتر بصرامة،
**يرسل بصفر إرسال تلقائي** — فقط بموافقة المؤسس وضمن تدرّج الإرسال.

ابدأ من المرجع الرئيسي: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

## المكوّنات (الوثائق)

| # | الوثيقة | المرحلة |
|---|---|---|
| 00 | [المرجع الرئيسي / Master](00_MARKET_PRODUCTION_OS_MASTER_AR.md) | — |
| 01 | [Brand OS](01_BRAND_OS_AR.md) | 1 — السوق والهوية |
| 02 | [Product Catalog OS](02_PRODUCT_CATALOG_OS_AR.md) | 1 |
| 03 | [Sector Intelligence OS](03_SECTOR_INTELLIGENCE_OS_AR.md) | 1 |
| 04 | [Prospect Research OS](04_PROSPECT_RESEARCH_OS_AR.md) | 2 — البحث والإنتاج |
| 05 | [Signal Detection OS](05_SIGNAL_DETECTION_OS_AR.md) | 2 |
| 06 | [Cold Email Draft Factory (250/day)](06_COLD_EMAIL_DRAFT_FACTORY_AR.md) | 2 |
| 07 | [Compliance & Deliverability OS](07_COMPLIANCE_DELIVERABILITY_OS_AR.md) | 3 — الحماية والإرسال |
| 08 | [Approval Queue & Sending Ramp](08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md) | 3 |
| 09 | [Reply Handling OS](09_REPLY_HANDLING_OS_AR.md) | 4 — الرد والتحويل |
| 10 | [WhatsApp Post-Reply OS](10_WHATSAPP_POST_REPLY_OS_AR.md) | 4 |
| 11 | [Content Production OS](11_CONTENT_PRODUCTION_OS_AR.md) | 5 — القنوات الإضافية |
| 12 | [Press OS](12_PRESS_OS_AR.md) | 5 |
| 13 | [Partnerships OS](13_PARTNERSHIPS_OS_AR.md) | 5 |
| 14 | [GTM Metrics & Learning](14_GTM_METRICS_AND_LEARNING_AR.md) | 6 — الإدارة |
| 17 | [Saudi PDPL Privacy Guard](17_PDPL_PRIVACY_GUARD_AR.md) | حوكمة |

## الكود والتشغيل

- الوحدة: `auto_client_acquisition/market_production_os/` (schemas, prospect_score, quality_gate,
  draft_factory, sending_ramp, approval_queue, reply_router, stores, report).
- المخططات: [`../../schemas/`](../../schemas/README.md).
- السكربتات: `scripts/run_gtm_draft_day.py` · `scripts/gtm_quality_gate.py` ·
  `scripts/register_market_production_agents.py` · `scripts/generate_market_production_schemas.py`.
- سير عمل CI: `.github/workflows/gtm-quality-gate.yml` · `gtm-draft-day.yml` · `weekly-gtm-review.yml`.

```bash
python3 scripts/run_gtm_draft_day.py --dry-run     # 250 مسودة + تقرير، لا إرسال
python3 scripts/gtm_quality_gate.py                # بوابة العقيدة (تفشل عند أي خرق)
APP_ENV=test pytest tests/test_market_production_os.py tests/test_no_auto_send_market_production.py -q
```

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
