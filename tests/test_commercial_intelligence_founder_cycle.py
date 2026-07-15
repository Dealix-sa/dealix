import csv
from datetime import date

from scripts.commercial.run_commercial_intelligence_founder_cycle import (
    OPERATING_TABLE_COLUMNS,
    build_cycle,
    write_operating_tables,
)


def test_founder_cycle_fails_closed_on_offer_price_and_real_contacts() -> None:
    payload = build_cycle(run_date=date(2026, 7, 15))

    assert payload["first_launch_offer_gate"]["status"] == "founder_approval_required"
    assert payload["first_launch_offer_gate"]["pricing_experiment"]["public_amount_sar"] is None
    assert payload["opportunity_graph"] == []
    assert payload["contacts_radar"] == []
    assert payload["external_actions_executed"] == 0
    assert {"strategy_backlog", "action_queue", "approval_queue", "proof_ledger"} <= payload.keys()


def test_founder_cycle_exports_all_seven_sheet_compatible_tables(tmp_path) -> None:
    payload = build_cycle(run_date=date(2026, 7, 15))
    write_operating_tables(payload, tmp_path, "2026-07-15")

    for table_name, columns in OPERATING_TABLE_COLUMNS.items():
        path = tmp_path / f"{table_name}_2026-07-15.csv"
        assert path.is_file()
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            assert tuple(next(reader)) == columns
