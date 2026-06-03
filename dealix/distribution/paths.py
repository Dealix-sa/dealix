"""Canonical filesystem paths for the Revenue Execution OS (distribution layer).

Config / example data is tracked in git; runtime JSONL ledgers are gitignored
(only ``.gitkeep`` is tracked) so no prospect/customer PII is ever committed.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# ── Config + example data (tracked) ────────────────────────────────────
DISTRIBUTION_DATA_DIR = REPO_ROOT / "data" / "distribution"
SECTORS_YAML = DISTRIBUTION_DATA_DIR / "sectors.yaml"
CHANNEL_POLICY_YAML = DISTRIBUTION_DATA_DIR / "channel_policy.yaml"
PROSPECTS_EXAMPLE_JSON = DISTRIBUTION_DATA_DIR / "prospects.example.json"

# Per-sector AR message templates (tracked, no PII).
TEMPLATES_DIR = REPO_ROOT / "data" / "templates" / "distribution"

# Canonical enterprise offers catalog (reused, not duplicated).
OFFERS_YAML = REPO_ROOT / "os" / "03_OFFERS.yml"

# JSON Schemas (tracked).
SCHEMAS_DIR = REPO_ROOT / "schemas"

# ── Runtime ledgers (JSONL contents gitignored; dirs tracked via .gitkeep) ──
DRAFTS_LEDGER = REPO_ROOT / "data" / "drafts" / "drafts.jsonl"
FOLLOWUPS_LEDGER = REPO_ROOT / "data" / "followups" / "followups.jsonl"
PROPOSALS_LEDGER = REPO_ROOT / "data" / "proposals" / "proposals.jsonl"
PROOF_PACKS_LEDGER = REPO_ROOT / "data" / "proof_packs" / "proof_packs.jsonl"
PAYMENTS_LEDGER = REPO_ROOT / "data" / "payments" / "payment_handoffs.jsonl"
RENEWALS_LEDGER = REPO_ROOT / "data" / "renewals" / "renewals.jsonl"
WIN_LOSS_LEDGER = REPO_ROOT / "data" / "win_loss" / "win_loss.jsonl"

# ── Reports (tracked dir via .gitkeep; generated markdown written at runtime) ──
REPORTS_DIR = REPO_ROOT / "reports" / "distribution"

__all__ = [
    "CHANNEL_POLICY_YAML",
    "DISTRIBUTION_DATA_DIR",
    "DRAFTS_LEDGER",
    "FOLLOWUPS_LEDGER",
    "OFFERS_YAML",
    "PAYMENTS_LEDGER",
    "PROOF_PACKS_LEDGER",
    "PROPOSALS_LEDGER",
    "PROSPECTS_EXAMPLE_JSON",
    "RENEWALS_LEDGER",
    "REPORTS_DIR",
    "REPO_ROOT",
    "SCHEMAS_DIR",
    "SECTORS_YAML",
    "TEMPLATES_DIR",
    "WIN_LOSS_LEDGER",
]
