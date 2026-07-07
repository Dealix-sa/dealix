"""Authorized, human-sourced company collectors (CSV + manual seed).

No scraping, no automated harvesting. Collectors only read files the founder
has explicitly provided under ``data/opportunity_graph/``.
"""

from __future__ import annotations

from dealix.opportunity_graph.collectors.csv_importer import import_companies_csv
from dealix.opportunity_graph.collectors.manual_seed_loader import load_seed_companies

__all__ = ["import_companies_csv", "load_seed_companies"]
