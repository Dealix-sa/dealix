#!/usr/bin/env python3
"""Print a Sovereign Console snapshot to stdout (no network, no DB).

Use this for a sanity check or to embed in CI output. Hermes state is
in-memory in Phase 1; the snapshot reflects a fresh process every run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repo root is importable when called directly from /scripts
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from dealix.hermes import ValueOutput  # noqa: E402
from dealix.hermes.console import render_console  # noqa: E402
from dealix.hermes.core.schemas import OpportunityKind, SignalSource  # noqa: E402
from dealix.hermes.orchestrator import HermesOrchestrator  # noqa: E402
from dealix.hermes.sovereignty import Action, SovereigntyLevel  # noqa: E402


def main() -> int:
    orch = HermesOrchestrator()

    # Seed a representative day so the snapshot isn't empty.
    s = orch.intake.capture(
        source=SignalSource.FOUNDER_NOTE,
        title="Warm intro — agency owner asked about Revenue Hunter",
        summary="Owner of a 12-person agency in Riyadh wants a 2-week pilot.",
        captured_by="sami",
    )
    orch.opportunities.register(
        source_signals=[s],
        kind=OpportunityKind.DIRECT_DEAL,
        title="Revenue Hunter Pilot — Riyadh Agency",
        buyer_segment="agency",
        estimated_value_sar=4999,
        close_probability=0.6,
        fit_score=0.8,
        urgency_score=0.7,
        risk_score=0.2,
        proposed_value_outputs=[ValueOutput.MONEY, ValueOutput.ASSET],
    )

    orch.propose(
        Action(
            action_type="send_external_message",
            payload={"to": "owner@riyadh-agency.sa"},
            proposed_by="followup_agent",
            sovereignty_level=SovereigntyLevel.S0_AUTONOMOUS,
        )
    )

    json.dump(render_console(orch), sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
