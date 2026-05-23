import argparse
import csv
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ops_runtime.productization_scorer import score_productization_candidate


def read_candidates(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    candidates = read_candidates(root / "productization/candidates.csv")
    rows = []
    for candidate in candidates:
        scored = score_productization_candidate(candidate)
        rows.append({
            "workflow": candidate.get("workflow", ""),
            "pain": candidate.get("pain", ""),
            "score": scored["score"],
            "decision": scored["decision"],
            "next_action": candidate.get("next_action", ""),
        })
    table = "\n".join(
        f"| {r['workflow']} | {r['score']} | {r['decision']} | {r['next_action']} |"
        for r in rows
    ) or "| None | 0 | Defer | Add repeated workflow evidence |"
    content = f"""# Productization Review
## Date
{date.today().isoformat()}
## Candidates
| Workflow | Score | Decision | Next Action |
|---|---:|---|---|
{table}
## CEO Rule
Do not automate unless the workflow is repeated, valuable, and safe.
## Next Productization Decision
-
"""
    out = root / "productization/productization_review.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("PASS: productization review generated.")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
