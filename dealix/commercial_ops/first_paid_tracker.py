"""First paid Diagnostic DoD — evidence CSV + KPI import (no invented revenue)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from dealix.commercial_ops.evidence_csv import real_evidence_rows
from dealix.commercial_ops.paths import REPO_ROOT

EVIDENCE = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
KPI_YAML = REPO_ROOT / "