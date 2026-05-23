def compare_latest_weeks(history_rows):
    if len(history_rows) < 2:
        return {
            "has_comparison": False,
            "summary": "Not enough weekly history yet.",
            "changes": {},
        }

    previous = history_rows[-2]
    current = history_rows[-1]

    keys = [
        "lead_count",
        "contacted",
        "replied",
        "call_booked",
        "sample_sent",
        "proposal_sent",
        "paid",
        "delivered",
        "retainer",
        "mrr",
        "approvals_pending",
    ]

    changes = {}

    for key in keys:
        try:
            prev = float(previous.get(key) or 0)
            cur = float(current.get(key) or 0)
        except ValueError:
            prev = 0
            cur = 0

        changes[key] = {
            "previous": prev,
            "current": cur,
            "delta": cur - prev,
        }

    biggest_gain = max(changes.items(), key=lambda item: item[1]["delta"])
    biggest_drop = min(changes.items(), key=lambda item: item[1]["delta"])

    return {
        "has_comparison": True,
        "summary": f"Biggest gain: {biggest_gain[0]} ({biggest_gain[1]['delta']}). Biggest drop: {biggest_drop[0]} ({biggest_drop[1]['delta']}).",
        "changes": changes,
        "biggest_gain": biggest_gain[0],
        "biggest_drop": biggest_drop[0],
    }
