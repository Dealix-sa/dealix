from datetime import date


def generate_evidence_report(evidence: dict) -> str:
    rows = "\n".join(
        f"| {criterion} | {'PASS' if passed else 'PENDING'} |"
        for criterion, passed in evidence.items()
    )

    return f"""# Stage Evidence Report

## Date
{date.today().isoformat()}

## Evidence Status

| Criterion | Status |
|---|---|
{rows}

## CEO Review
-

## Trust Review
-

## Decision
Stay / Advance / Reset / Defer
"""
