# رادار الإيراد المتكرّر · Recurring Revenue Radar

> الرافعة الأقوى لنموّ الإيراد: تحويل العملاء من خدمات لمرّة واحدة (Sprint بـ 499 ر.س)
> إلى عقود **متكرّرة** (Managed Ops بـ 2,999 / 3,999 / 4,999 ر.س شهرياً) — ضمن الحوكمة،
> بمسودات تتطلب موافقة المؤسس، وبدون أي إرسال آلي.

---

## لماذا؟ (The lever)

الإيراد الذي **يتراكم من نفسه** ليس إرسالاً بارداً آلياً — بل تحويل العملاء الراضين
أصحاب الـ Proof إلى عقود شهرية متجدّدة (NRR / Net Revenue Retention). كل عميل أكمل
Sprint بنجاح هو فرصة عقد متكرّر. الرادار يمسح **كل المحفظة يومياً**، ويرتّب الفرص حسب
الإيراد الشهري الإضافي المتوقّع، ويجهّز مسودة إجراء لكل حساب — لتركّز على أعلى قيمة أولاً.

---

## الثوابت (Doctrine — مفروضة في الكود والاختبارات)

| الثابت | التطبيق |
|--------|---------|
| **لا إيراد قبل السداد** | `realized_mrr_sar` يجمع فقط الحسابات التي فاتورتها **مدفوعة**. أرقام التوسّع تُسمّى **PIPELINE** (فرصة) ولا تُخلط أبداً بالإيراد المحقّق. |
| **لا ترقية قبل Proof** | الحساب لا يصبح فرصة إلا إذا كان مؤهّلاً لعقد (Proof ≥ L1، رضا ≥ 7، نتيجة قابلة للقياس) — بإعادة استخدام `RetainerEligibilityEngine`. |
| **الموافقة أولاً** | كل إجراء مُقترح **مسودة** (`mode=draft_only`, `requires_approval=true`). لا إرسال ولا فوترة آلية. |

معايير التأهيل والتسعير: `GET /api/v1/recurring-revenue/doctrine`.

---

## التشغيل اليومي

```bash
# يقرأ المحفظة، يكتب موجزاً للمؤسس، ويسجّل التشغيل في السجلّ
python scripts/run_recurring_revenue_radar.py
```

مصدر الحسابات (أول موجود يُستخدم):

1. `--accounts <path>`
2. `data/recurring_revenue/accounts_seed.json` — **كتابك الحقيقي** (مُتجاهَل في git؛ ضع بياناتك هنا)
3. `data/demo/recurring_revenue_accounts_seed.json` — بيانات تجريبية صناعية (لا PII)

المخرجات:

- `data/founder_briefs/recurring_revenue_radar_<YYYY-MM-DD>.md` — موجز ثنائي اللغة
- إلحاق لقطة مُختصرة إلى `data/recurring_revenue/radar_log.json` (السجلّ)

**أتمتة:** `.github/workflows/recurring-revenue-radar-daily.yml` يشغّله يومياً (الأحد–الخميس
05:00 UTC) ويرفع الموجز كـ artifact — بدون أسرار وبدون إرسال خارجي.

### شكل ملف الحسابات

```json
{
  "accounts": [
    {
      "account_id": "acc_001",
      "company_name": "Najd Clinics",
      "proof_level": "L3",
      "satisfaction_score": 9.0,
      "measurable_result_achieved": true,
      "current_mrr_sar": 0.0,
      "latest_invoice_paid": false
    }
  ]
}
```

---

## واجهة البرمجة (API)

كل المسارات تتطلب `X-Admin-API-Key` (تمرّ تلقائياً في وضع التطوير/الاختبار).

| المسار | الوصف |
|--------|-------|
| `POST /api/v1/recurring-revenue/radar` | يُقيّم محفظة ويعيد الرادار المُرتّب |
| `POST /api/v1/recurring-revenue/radar/markdown` | نفس التقييم كموجز Markdown جاهز |
| `GET /api/v1/recurring-revenue/doctrine` | المعايير، الأسعار، والثوابت |
| `GET /api/v1/recurring-revenue/history` | تشغيلات الرادار السابقة من السجلّ |

---

## التحقّق (CI)

```bash
python scripts/verify_recurring_revenue_radar.py   # RECURRING_REVENUE_RADAR_VERIFY=PASS
```

بوّابة في `.github/workflows/ci.yml` (خطوة "Verify Recurring Revenue Radar")، واختبارات
شاملة في `tests/test_recurring_revenue_radar.py` (محرّك + حوكمة + سجلّ + API).

---

## English summary

The **Recurring Revenue Radar** is the compounding-revenue lever: it scans the whole
book of business daily and ranks which accounts should convert from one-off Sprints into
recurring Managed-Ops retainers (2,999 / 3,999 / 4,999 SAR/mo), by expected incremental
MRR. It reuses the existing `RetainerEligibilityEngine` so eligibility and tier selection
stay the single source of truth.

Three non-negotiables are enforced in code and tests: **no revenue before paid** (unpaid
recurring is excluded from realised MRR and from the expansion baseline; expansion is
labelled PIPELINE), **proof before upsell** (only retainer-eligible accounts become
opportunities), and **approval-first** (every action is a `draft_only` proposal awaiting
founder approval — nothing is sent or charged automatically).

- Engine + ledger: `dealix/revenue_ops_autopilot/recurring_revenue_radar.py`
- Daily script: `scripts/run_recurring_revenue_radar.py`
- CI gate: `scripts/verify_recurring_revenue_radar.py`
- API router: `api/routers/recurring_revenue.py`
- Tests: `tests/test_recurring_revenue_radar.py`
