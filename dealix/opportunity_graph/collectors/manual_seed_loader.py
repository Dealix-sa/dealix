"""Load the committed seed company list for the Opportunity Command Room.

Combines the seed CSV (``data/opportunity_graph/companies.seed.csv``) with any
companies already persisted in the JSON store. Handles a missing or empty seed
gracefully by returning an empty list.
"""

from __future__ import annotations

from pathlib import Path

from dealix.opportunity_graph.collectors.csv_importer import import_companies_csv
from dealix.opportunity_graph.schemas import OpportunityCompany
from dealix.opportunity_graph.store import OpportunityGraphStore, default_data_dir


def seed_csv_path(data_dir: Path | None = None) -> Path:
    return (data_dir or default_data_dir()) / "companies.seed.csv"


def load_seed_companies(store: OpportunityGraphStore | None = None) -> list[OpportunityCompany]:
    """Return de-duplicated companies from the seed CSV plus the store.

    The seed CSV is resolved relative to the store's data dir, so a store
    pointed at a temp/alternate location looks for its own seed. Store rows win
    over seed rows for the same id so previously scored state (status, drafts)
    is not clobbered by a re-seed.
    """
    store = store or OpportunityGraphStore()
    from_csv = import_companies_csv(seed_csv_path(store.data_dir))
    from_store = store.load_companies()
    merged: dict[str, OpportunityCompany] = {c.id: c for c in from_csv}
    for c in from_store:
        merged[c.id] = c
    return list(merged.values())
