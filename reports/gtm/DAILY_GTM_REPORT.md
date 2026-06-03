# التقرير اليومي للسوق — Daily GTM Report

> قالب يُجمَّع نهاية اليوم (21:00 Asia/Riyadh). المقاييس مُعرّفة في
> [GTM_METRICS_AR](../../docs/gtm/GTM_METRICS_AR.md). كحالة: {{as_of}}.

## مقاييس اليوم
| المقياس | القيمة | الاتجاه الصحي |
|---|---|---|
| drafts generated | {{n}} | = 250 |
| drafts quality-passed | {{n}} | ↑ |
| drafts approved | {{n}} | 30–50 |
| emails sent | {{n}} | ضمن سقف المنحنى |
| bounces | {{n}} | bounce < 3% |
| unsubscribes | {{n}} | مُراقب |
| replies | {{n}} | ↑ |
| positive replies | {{n}} | ↑ |
| meetings booked | {{n}} | ↑ |
| proposals requested | {{n}} | ↑ |
| job signals found | {{n}} | ↑ |
| content posts drafted | {{n}} | ≥ 4 |
| partner prospects | {{n}} | ↑ |

## قرار الغد
- ماذا نرسل غدًا؟ {{tomorrow_send}}
- أي قطاع نوقفه؟ {{pause_sector}}
- أي عرض نحسّنه؟ {{improve_offer}}
- تحذيرات السمعة/الكبت: {{warnings}}

> التحقق: `python3 scripts/verify_market_production_os.py`.

---
القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
