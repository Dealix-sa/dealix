def calculate_target_score(metrics, targets):
    total = 0
    achieved = 0

    for key, target in targets.items():
        total += 1
        if metrics.get(key, 0) >= target:
            achieved += 1

    if total == 0:
        return 0

    return round((achieved / total) * 100)
