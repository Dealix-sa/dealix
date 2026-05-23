from datetime import date


def build_scorecard(metrics, bottlenecks):
    bottleneck_lines = "\n".join(
        f"- {b['area']}: {b['issue']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    return f"""# Company OS Scorecard

## Updated
{date.today().isoformat()}

## Revenue
- MRR: {metrics.get('mrr', 0)}
- Active retainers: {metrics.get('active_retainers', 0)}
- Paid opportunities: {metrics.get('paid', 0)}

## Pipeline Health
- Lead count: {metrics.get('lead_count', 0)}
- Contacted: {metrics.get('contacted', 0)}
- Replied: {metrics.get('replied', 0)}
- Calls booked: {metrics.get('call_booked', 0)}
- Proposals sent: {metrics.get('proposal_sent', 0)}

## Trust
- Approvals total: {metrics.get('approvals_total', 0)}
- Approvals pending: {metrics.get('approvals_pending', 0)}
- High-risk approvals: {metrics.get('high_risk_approvals', 0)}

## Bottlenecks
{bottleneck_lines}
"""
