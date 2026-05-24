"""Proposal Factory — renders a deterministic, bilingual proposal draft.

The factory does not send anything. It hands back markdown that the
sovereign console + approval flow then route. The intent is that the
*content* of a proposal is reproducible and reviewable, not stochastic.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.schemas import Opportunity
from dealix.hermes.money.pricing import PriceQuote


@dataclass(slots=True)
class ProposalDraft:
    opportunity_id: str
    title: str
    body_markdown: str
    target_price_sar: float
    floor_price_sar: float
    ceiling_price_sar: float
    language: str = "ar"


_AR_TEMPLATE = """# {title}

**العميل المستهدف:** {buyer}
**الألم المعالَج:** {pain}
**الوعد:** {promise}

## ما نسلّمه
{deliverables}

## السعر
- السقف: {ceiling:,.0f} ر.س
- المستهدف: {target:,.0f} ر.س
- الحد الأدنى: {floor:,.0f} ر.س

## الجدول الزمني
{timeline}

## ما لا ندّعيه
- لا أرقام إيراد قبل invoice_paid.
- لا شراكات أو شهادات لم نُثبتها بأدلة.
"""

_EN_TEMPLATE = """# {title}

**Buyer:** {buyer}
**Pain addressed:** {pain}
**Promise:** {promise}

## Deliverables
{deliverables}

## Pricing
- Ceiling: SAR {ceiling:,.0f}
- Target:  SAR {target:,.0f}
- Floor:   SAR {floor:,.0f}

## Timeline
{timeline}

## What we will *not* claim
- No revenue figures before invoice_paid.
- No partnerships or certifications we cannot evidence.
"""


def render(
    *,
    opportunity: Opportunity,
    offer_title: str,
    pain: str,
    promise: str,
    deliverables: list[str],
    timeline: str,
    price: PriceQuote,
    language: str = "ar",
) -> ProposalDraft:
    bullets = "\n".join(f"- {d}" for d in deliverables) or "- (TBD)"
    tmpl = _AR_TEMPLATE if language == "ar" else _EN_TEMPLATE
    body = tmpl.format(
        title=offer_title,
        buyer=opportunity.buyer_segment,
        pain=pain,
        promise=promise,
        deliverables=bullets,
        timeline=timeline,
        ceiling=price.ceiling_sar,
        target=price.target_sar,
        floor=price.floor_sar,
    )
    return ProposalDraft(
        opportunity_id=opportunity.opportunity_id,
        title=offer_title,
        body_markdown=body,
        target_price_sar=price.target_sar,
        floor_price_sar=price.floor_sar,
        ceiling_price_sar=price.ceiling_sar,
        language=language,
    )


__all__ = ["ProposalDraft", "render"]
