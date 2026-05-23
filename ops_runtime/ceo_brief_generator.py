from datetime import date


def generate_ceo_brief(metrics, bottlenecks):
    top_focus = "Send 25 founder-led DMs and prepare 3 samples."

    if bottlenecks:
        top = bottlenecks[0]
        top_focus = f"{top['recommendation']}"

    bottleneck_lines = "\n".join(
        f"- **{b['area']} / {b['severity']}**: {b['issue']} -> {b['recommendation']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    return f"""# Daily CEO Brief

## Date
{date.today().isoformat()}

## One CEO Focus Today
{top_focus}

## Money
- MRR: {metrics.get('mrr', 0)}
- Active retainers: {metrics.get('active_retainers', 0)}
- Paid opportunities: {metrics.get('paid', 0)}
- Proposals sent: {metrics.get('proposal_sent', 0)}

## Sales
- Lead count: {metrics.get('lead_count', 0)}
- New: {metrics.get('new', 0)}
- Contacted: {metrics.get('contacted', 0)}
- Replied: {metrics.get('replied', 0)}
- Calls booked: {metrics.get('call_booked', 0)}
- Samples sent: {metrics.get('sample_sent', 0)}

## Delivery
- Delivered: {metrics.get('delivered', 0)}
- Retainers: {metrics.get('retainer', 0)}

## Trust
- Approvals total: {metrics.get('approvals_total', 0)}
- Approvals pending: {metrics.get('approvals_pending', 0)}
- High-risk approvals: {metrics.get('high_risk_approvals', 0)}

## Bottlenecks
{bottleneck_lines}

## Decisions Required
| Decision | Type | Risk | Recommendation |
|---|---|---:|---|
| Review top bottleneck | Fix | Medium | {top_focus} |

## End-of-Day Result
-
"""
