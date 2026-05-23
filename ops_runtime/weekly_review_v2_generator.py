from datetime import date


def generate_weekly_review_v2(metrics, bottlenecks, comparison, learning_decision):
    bottleneck_lines = "\n".join(
        f"- **{b['area']} / {b['severity']}**: {b['issue']} -> {b['recommendation']}"
        for b in bottlenecks
    ) or "- No major bottlenecks detected."

    comparison_summary = comparison.get("summary", "No comparison available yet.")

    return f"""# Weekly CEO Review

## Week Ending
{date.today().isoformat()}

## 1. Scoreboard

| Metric | Value |
|---|---:|
| Leads | {metrics.get('lead_count', 0)} |
| Contacted | {metrics.get('contacted', 0)} |
| Replies | {metrics.get('replied', 0)} |
| Calls Booked | {metrics.get('call_booked', 0)} |
| Samples Sent | {metrics.get('sample_sent', 0)} |
| Proposals Sent | {metrics.get('proposal_sent', 0)} |
| Paid | {metrics.get('paid', 0)} |
| Delivered | {metrics.get('delivered', 0)} |
| Retainers | {metrics.get('retainer', 0)} |
| MRR | {metrics.get('mrr', 0)} |
| Approvals Pending | {metrics.get('approvals_pending', 0)} |

## 2. Weekly Comparison

{comparison_summary}

## 3. Bottlenecks

{bottleneck_lines}

## 4. Learning Decision

| Field | Value |
|---|---|
| Decision | {learning_decision['decision']} |
| Type | {learning_decision['type']} |
| Reason | {learning_decision['reason']} |
| Recommended File | {learning_decision['recommended_file']} |
| Update | {learning_decision['update']} |

## 5. Required Playbook Update

Update this file before closing the week:

```txt
{learning_decision['recommended_file']}
```

## 6. CEO Notes

-

## 7. Next Week Focus

-
"""
