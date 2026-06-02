# Personalization Rules — قواعد التخصيص

Every draft must say something **true** about the company. Code:
[`../../dealix/market_production_os/personalization.py`](../../dealix/market_production_os/personalization.py).

## Levels — المستويات

| Level | Meaning | Example angle |
|---|---|---|
| P0 | Sector only / قطاع فقط | "وكالات التسويق غالباً…" |
| P1 | Company + sector / شركة + قطاع | "واضح أنكم تخدمون…" |
| P2 | Pain from their site / ألم من موقعهم | "عندكم أكثر من خدمة/نموذج…" |
| P3 | Trigger / حدث محفّز | "بعد إطلاقكم/حملتكم…" |
| P4 | Proof angle / زاوية إثبات | "ممكن نبدأ بتقرير يوضّح…" |

## The cold floor — الحدّ الأدنى للبارد

`personalization_floor_ok(level, touch_type)` returns true only at **P1 or
above** for cold messages. No `first_touch` below P1 may be sent. Warm / press /
general relationship messages are exempt (`is_warm=True`). This floor is the
Personalization Gate inside the
[compliance gate](COLD_EMAIL_COMPLIANCE_AR.md).

## How level is set — كيف يُحدّد المستوى

`infer_level(has_company, has_sector, has_pain_from_site, has_trigger,
has_proof_angle)` returns the highest level the evidence supports. A prospect's
`personalization_level` flows into the draft and is scored in
[Prospect Research](PROSPECT_RESEARCH_OS_AR.md) (P4=10 … P1=4 … P0=0 points).

## Practice — الممارسة

- Aim to lift every prospect to **P2+** before sending; it raises both the
  prospect score and the expected reply rate.
- Personalization must be honest — never fabricate a detail. A false
  personalization note is a fake claim (NO_FAKE_CLAIMS).
- Sector-specific personalization examples live in each
  [sector brief](../sectors/README.md).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
