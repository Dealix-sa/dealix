import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import csv
from _v5util import ensure_chain


def test_founder_review_csv_columns():
    d = ensure_chain()
    with (d / "founder_review.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 400
    assert "requires_founder_approval" in rows[0]
    assert "external_send_blocked" in rows[0]
