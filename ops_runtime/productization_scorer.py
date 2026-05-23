def score_productization_candidate(candidate: dict) -> dict:
    score = 0
    try:
        frequency = int(candidate.get("manual_frequency") or 0)
    except ValueError:
        frequency = 0
    if frequency >= 3:
        score += 20
    if frequency >= 5:
        score += 20
    if frequency >= 10:
        score += 20
    if (candidate.get("client_demand") or "").lower() in {"yes", "true", "high"}:
        score += 20
    if (candidate.get("risk_level") or "").lower() in {"low", "medium"}:
        score += 20
    if score >= 80:
        decision = "Automate or productize"
    elif score >= 50:
        decision = "Template and test"
    elif score >= 30:
        decision = "Document"
    else:
        decision = "Defer"
    return {
        "score": score,
        "decision": decision,
    }
