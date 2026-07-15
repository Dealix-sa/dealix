#!/usr/bin/env python3
"""Verify the master-startup Phase-0 consolidation contract."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED_OUTPUTS = {
    "latest.json",
    "latest.md",
    "current_state_and_drift.md",
    "blockers.json",
    "proof_log.json",
    "capability_reality_matrix.csv",
    "approval_queue.csv",
    "opportunity_graph.csv",
    "claim_and_proof_registry.csv",
    "claim_and_proof_registry.md",
}


def fail