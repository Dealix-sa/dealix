#!/usr/bin/env python3
"""Build a founder-first Dealix GTM packet from a governed company directory.

The command performs research, service matching, objection preparation,
negotiation planning, approval routing, and proof logging. It never sends,
publishes, charges, or mutates production.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deal