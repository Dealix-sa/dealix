from datetime import date


def generate_weekly_review(metrics, bottlenecks):
    bottleneck_lines = "\n".join(
        f"- {b['area']}: {b['issue']} -> {b['recommendation']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    return f"""# Weekly Intelligence Review

## Week Ending
{date.today().isoformat()}

## What Happened?
- Leads sourced: {metrics.get('lead_count', 0)}
- Contacted: {metrics.get('contacted', 0)}
- Replies: {metrics.get('replied', 0)}
- Calls booked: {metrics.get('call_booked', 0)}
- Proposals sent: {metrics.get('proposal_sent', 0)}
- Paid: {metrics.get('paid', 0)}
- Delivered: {metrics.get('delivered', 0)}
- Retainers: {metrics.get('retainer', 0)}

## What Worked?
- Best visible signal: Update after reviewing replies and calls.

## What Failed?
- Review weak conversion points.

## Bottlenecks
{bottleneck_lines}

## Learning Decision
| Learning | Decision | Update Needed |
|---|---|---|
| Weekly bottleneck review | Fix highest bottleneck | Update relevant playbook |

## What Will Change Next Week?
- ICP:
- Message:
- Pricing:
- Delivery:
- Product:
- Trust:
"""
