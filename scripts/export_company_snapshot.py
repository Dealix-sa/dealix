import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _safe_import():
    try:
        from ops_runtime.business_audit import calculate_business_score
        from ops_runtime.execution_assurance import calculate_execution_assurance
        from ops_runtime.finance_calculator import calculate_finance
        from control_plane.control_tower import build_control_tower_signal

        return (
            calculate_business_score,
            calculate_finance,
            calculate_execution_assurance,
            build_control_tower_signal,
        )
    except ImportError as exc:
        print(f"WARN: snapshot dependencies not available: {exc}")
        return None, None, None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    parser.add_argument("--out", default="dashboard_data/company_snapshot.json")
    args = parser.parse_args()
    private_root = Path(args.private_ops).resolve()

    (
        calculate_business_score,
        calculate_finance,
        calculate_execution_assurance,
        build_control_tower_signal,
    ) = _safe_import()

    snapshot = {
        "date": date.today().isoformat(),
        "private_ops": str(private_root),
    }

    if calculate_business_score is not None:
        score = calculate_business_score(str(private_root))
        snapshot["business_score"] = score
        snapshot["finance"] = calculate_finance(str(private_root))
        snapshot["execution_assurance"] = calculate_execution_assurance(str(private_root))
        snapshot["control_tower"] = build_control_tower_signal(score)
    else:
        snapshot["status"] = "pending_modules"
        snapshot["note"] = (
            "Snapshot scaffolded. Business score, finance, assurance, and "
            "control tower modules will populate this snapshot once they are wired."
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"PASS: company snapshot written to {out}")


if __name__ == "__main__":
    main()
