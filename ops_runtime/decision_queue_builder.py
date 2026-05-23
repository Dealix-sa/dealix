def build_decision_queue(bottlenecks):
    rows = []

    for idx, b in enumerate(bottlenecks, start=1):
        rows.append(
            f"| {idx} | {b['recommendation']} | Fix | {b['severity']} | {b['issue']} | {b['recommendation']} | Pending |"
        )

    if not rows:
        rows.append("| 1 | Continue weekly operating cadence | Continue | Low | No major bottleneck | Keep execution consistent | Pending |")

    return "# CEO Decision Queue\n\n| Priority | Decision | Type | Risk | Evidence | Recommendation | CEO Decision |\n|---:|---|---|---:|---|---|---|\n" + "\n".join(rows) + "\n"
