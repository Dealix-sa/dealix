#!/usr/bin/env python3
"""
Client Delivery — Diagnostic Generator

Generates the Revenue Leakage Map and diagnostic report for a client.
Output goes to company/runtime/clients/{slug}/diagnostic/

Usage:
    python company/client_delivery/diagnostic_generator.py \
        --client <slug> \
        --leads-total 120 \
        --leads-quoted 45 \
        --leads-closed 18 \
        --avg-deal-size 15000 \
        --followup-delay-days 4 \
        --gap1 "متابعة متأخرة" \
        --gap2 "لا تقرير يومي" \
        --gap3 "فرص تضيع في واتساب"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = ROOT / "company" / "runtime" / "clients"


def _load_intake(slug: str) -> dict:
    path = CLIENTS_DIR / slug / "intake.json"
    if not path.exists():
        raise FileNotFoundError(f"Client not found: {slug}. Run intake_flow.py first.")
    return json.loads(path.read_text())


def calculate_leakage(
    leads_total: int,
    leads_quoted: int,
    leads_closed: int,
    avg_deal_size: float,
    followup_delay_days: int,
) -> dict:
    quote_rate = round(leads_quoted / leads_total * 100, 1) if leads_total else 0
    close_rate = round(leads_closed / leads_quoted * 100, 1) if leads_quoted else 0
    overall_rate = round(leads_closed / leads_total * 100, 1) if leads_total else 0

    # Potential at industry benchmark (assume 60% quote rate, 40% close rate)
    potential_quoted = int(leads_total * 0.60)
    potential_closed = int(potential_quoted * 0.40)
    actual_revenue = leads_closed * avg_deal_size
    potential_revenue = potential_closed * avg_deal_size
    leakage_estimate = potential_revenue - actual_revenue

    delay_cost = followup_delay_days * (avg_deal_size * 0.03)

    return {
        "leads_total": leads_total,
        "leads_quoted": leads_quoted,
        "leads_closed": leads_closed,
        "quote_rate_pct": quote_rate,
        "close_rate_pct": close_rate,
        "overall_conversion_pct": overall_rate,
        "avg_deal_size_sar": avg_deal_size,
        "actual_revenue_sar": actual_revenue,
        "potential_revenue_sar": potential_revenue,
        "leakage_estimate_sar": max(0, leakage_estimate),
        "followup_delay_days": followup_delay_days,
        "delay_cost_sar": round(delay_cost, 0),
        "benchmark_quote_rate_pct": 60,
        "benchmark_close_rate_pct": 40,
    }


def generate_diagnostic(
    slug: str,
    leads_total: int,
    leads_quoted: int,
    leads_closed: int,
    avg_deal_size: float,
    followup_delay_days: int,
    gaps: list[str],
    priorities: list[str] | None = None,
    recommendation: str = "",
) -> dict:
    intake = _load_intake(slug)
    metrics = calculate_leakage(
        leads_total, leads_quoted, leads_closed, avg_deal_size, followup_delay_days
    )

    if not priorities:
        priorities = gaps[:3]

    diagnostic = {
        "client_slug": slug,
        "company_name": intake["company_name"],
        "sector": intake["sector"],
        "diagnostic_date": date.today().isoformat(),
        "metrics": metrics,
        "gaps": gaps,
        "top_priorities": priorities[:3],
        "recommendation": recommendation or _auto_recommend(metrics, intake["sector"]),
        "analyst": "Dealix",
    }

    out_dir = CLIENTS_DIR / slug / "diagnostic"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "diagnostic.json").write_text(
        json.dumps(diagnostic, ensure_ascii=False, indent=2)
    )

    report_md = _render_report(diagnostic)
    (out_dir / "DIAGNOSTIC_REPORT.md").write_text(report_md)

    leakage_map = _render_leakage_map(diagnostic)
    (out_dir / "REVENUE_LEAKAGE_MAP.md").write_text(leakage_map)

    intake["diagnostic_start"] = diagnostic["diagnostic_date"]
    (CLIENTS_DIR / slug / "intake.json").write_text(
        json.dumps(intake, ensure_ascii=False, indent=2)
    )

    return diagnostic


def _auto_recommend(metrics: dict, sector: str) -> str:
    if metrics["quote_rate_pct"] < 40:
        return "WhatsApp Revenue OS — لتحويل الاستفسارات إلى عروض أسعار بسرعة"
    if metrics["followup_delay_days"] > 2:
        return "CRM Follow-Up OS — لتنظيم المتابعة وتقليل وقت الاستجابة"
    return "Revenue Command Center — لوحة يومية للأولويات والمتابعة"


def _render_leakage_map(d: dict) -> str:
    m = d["metrics"]
    gaps_text = "\n".join(f"- {g}" for g in d["gaps"])
    priorities_text = "\n".join(
        f"{i+1}. {p}" for i, p in enumerate(d["top_priorities"])
    )

    return f"""# خريطة تسرب الإيراد — {d['company_name']}

**التاريخ**: {d['diagnostic_date']}

---

## الأرقام الحالية

| المقياس | القيمة الحالية | المعيار |
|--------|--------------|---------|
| إجمالي الاستفسارات | {m['leads_total']} | — |
| معدل تحويل إلى عرض | {m['quote_rate_pct']}% | 60% |
| معدل الإغلاق | {m['close_rate_pct']}% | 40% |
| معدل التحويل الكلي | {m['overall_conversion_pct']}% | 24% |
| متوسط تأخر المتابعة | {m['followup_delay_days']} أيام | <24 ساعة |

---

## تقدير الخسارة الشهرية

| البند | المبلغ |
|-------|-------|
| الإيراد الفعلي | {m['actual_revenue_sar']:,.0f} SAR |
| الإيراد المحتمل (بالمعيار) | {m['potential_revenue_sar']:,.0f} SAR |
| **تقدير نزيف الإيراد** | **{m['leakage_estimate_sar']:,.0f} SAR** |
| تكلفة تأخر المتابعة | {m['delay_cost_sar']:,.0f} SAR/شهر |

---

## الفجوات الرئيسية

{gaps_text}

---

## الأولويات الثلاث للإصلاح الفوري

{priorities_text}

---

## التوصية المبدئية

{d['recommendation']}

---

*أُعدّت بواسطة Dealix — للاطلاع الداخلي فقط*
"""


def _render_report(d: dict) -> str:
    m = d["metrics"]
    return f"""# تقرير التشخيص الكامل — {d['company_name']}

**التاريخ**: {d['diagnostic_date']}
**القطاع**: {d['sector']}
**المُعدّ**: Dealix

---

## ملخص تنفيذي

بناءً على تحليل عمليات {d['company_name']}، رصدنا فجوة تقديرية بين الإيراد الحالي
والإيراد المحتمل تبلغ **{m['leakage_estimate_sar']:,.0f} SAR شهريًا**.

السبب الرئيسي: تحويل {m['quote_rate_pct']}% فقط من الاستفسارات إلى عروض أسعار
(المعيار: 60%)، مع متوسط تأخر {m['followup_delay_days']} أيام في المتابعة.

---

## تفاصيل التحليل

### مسار المبيعات الحالي

```
{m['leads_total']} استفسار
    ↓ ({m['quote_rate_pct']}%)
{m['leads_quoted']} عرض أسعار
    ↓ ({m['close_rate_pct']}%)
{m['leads_closed']} صفقة مغلقة
```

### المقارنة بالمعيار

| المرحلة | الحالي | المعيار | الفجوة |
|--------|--------|---------|-------|
| الاستفسار → عرض | {m['quote_rate_pct']}% | {m['benchmark_quote_rate_pct']}% | {m['benchmark_quote_rate_pct'] - m['quote_rate_pct']:.0f}% |
| عرض → إغلاق | {m['close_rate_pct']}% | {m['benchmark_close_rate_pct']}% | {m['benchmark_close_rate_pct'] - m['close_rate_pct']:.0f}% |

---

## الفجوات المرصودة

{"".join(f"{i+1}. {g}" + chr(10) for i, g in enumerate(d['gaps']))}

---

## الأولويات للإصلاح الفوري

{"".join(f"{i+1}. **{p}**" + chr(10) for i, p in enumerate(d['top_priorities']))}

---

## التوصية المبدئية

**{d['recommendation']}**

---

## الخطوة التالية

الانتقال إلى مرحلة Pilot — بناء النظام واختباره مع بياناتكم الفعلية خلال 7 أيام.

---

*تقرير سري — Dealix — {d['diagnostic_date']}*
"""


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate client diagnostic report")
    p.add_argument("--client", required=True, help="Client slug")
    p.add_argument("--leads-total", type=int, required=True)
    p.add_argument("--leads-quoted", type=int, required=True)
    p.add_argument("--leads-closed", type=int, required=True)
    p.add_argument("--avg-deal-size", type=float, required=True)
    p.add_argument("--followup-delay-days", type=int, default=3)
    p.add_argument("--gap1", default="")
    p.add_argument("--gap2", default="")
    p.add_argument("--gap3", default="")
    p.add_argument("--recommendation", default="")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    gaps = [g for g in [args.gap1, args.gap2, args.gap3] if g]

    try:
        result = generate_diagnostic(
            slug=args.client,
            leads_total=args.leads_total,
            leads_quoted=args.leads_quoted,
            leads_closed=args.leads_closed,
            avg_deal_size=args.avg_deal_size,
            followup_delay_days=args.followup_delay_days,
            gaps=gaps,
            recommendation=args.recommendation,
        )
        print(f"DIAGNOSTIC_OK | client={result['client_slug']}")
        print(f"Leakage estimate: {result['metrics']['leakage_estimate_sar']:,.0f} SAR/month")
        print(f"Files: company/runtime/clients/{result['client_slug']}/diagnostic/")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
