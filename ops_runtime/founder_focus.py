def choose_founder_focus(metrics, bottlenecks):
    if metrics.get("paid", 0) == 0 and metrics.get("proposal_sent", 0) > 0:
        return "Convert proposal to payment or PO."

    if metrics.get("contacted", 0) < 25:
        return "Reach 25 founder-led DMs today."

    if metrics.get("sample_sent", 0) < 3:
        return "Prepare 3 qualified sample packs."

    if metrics.get("replied", 0) > 0 and metrics.get("call_booked", 0) == 0:
        return "Convert replies into booked calls."

    if bottlenecks:
        return bottlenecks[0]["recommendation"]

    return "Maintain cadence and document one learning decision."
