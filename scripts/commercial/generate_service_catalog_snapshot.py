#!/usr/bin/env python3
"""Generate service catalog TypeScript snapshot from the Python registry.

Reads auto_client_acquisition.service_catalog.registry (Wave 13 truth source)
and writes apps/web/lib/service-catalog-snapshot.ts for the frontend.

Article 4: no external calls.
Article 8: all pricing carries is_estimate flag.
Article 11: thin adapter — no new business logic.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "apps" / "web" / "lib" / "service-catalog-snapshot.ts"


def main() -> int:
    from auto_client_acquisition.service_catalog import list_offerings

    offerings = list_offerings()
    serialized = []
    for o in offerings:
        entry: dict = {
            "id": o.id,
            "name_ar": o.name_ar,
            "name_en": o.name_en,
            "price_sar": o.price_sar,
            "price_unit": o.price_unit,
            "duration_days": o.duration_days,
            "customer_journey_stage": o.customer_journey_stage,
            "deliverables": list(o.deliverables),
            "kpi_commitment_en": o.kpi_commitment_en,
            "kpi_commitment_ar": o.kpi_commitment_ar,
            "refund_policy_en": o.refund_policy_en,
            "hard_gates": list(o.hard_gates),
            "is_estimate": True,
        }
        if hasattr(o, "price_sar_max") and o.price_sar_max is not None:
            entry["price_sar_max"] = o.price_sar_max
        if hasattr(o, "price_monthly_sar_min") and o.price_monthly_sar_min is not None:
            entry["price_monthly_sar_min"] = o.price_monthly_sar_min
        if hasattr(o, "price_monthly_sar_max") and o.price_monthly_sar_max is not None:
            entry["price_monthly_sar_max"] = o.price_monthly_sar_max
        serialized.append(entry)

    snapshot = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_offerings": len(offerings),
        "is_estimate": True,
        "funnel_offerings": [o for o in serialized if o["customer_journey_stage"] != "transformation"],
        "transformation_offerings": [o for o in serialized if o["customer_journey_stage"] == "transformation"],
        "all_offerings": serialized,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "export const serviceCatalogSnapshot = "
        + json.dumps(snapshot, ensure_ascii=False, indent=2)
        + " as const;\n",
        encoding="utf-8",
    )
    print(f"SERVICE_CATALOG_SNAPSHOT={OUT.relative_to(ROOT)}")
    print(f"TOTAL_OFFERINGS={len(offerings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
