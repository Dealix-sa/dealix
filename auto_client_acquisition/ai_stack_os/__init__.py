"""AI Stack OS — unified L1..L11 orchestrator for the Dealix AI stack.

The orchestrator binds together the eleven canonical AI layers under a
single, deterministic surface. Every customer-facing AI action the
business runs ultimately flows through :func:`run_ai_stack` (and its
helper, :class:`AIStackOrchestrator`), and every layer in the run is
recorded as a hashed link in a per-run evidence chain.

Layer map:

* **L1** — Source Passport (``data_os``)
* **L2** — Data Quality Score (``data_os``)
* **L3** — Intelligence / RAG (``intelligence_os``)
* **L4** — Model Router (``ai/model_router``)
* **L5** — Agent Mesh (``agent_os``)
* **L6** — Governance Gate (``governance_os``)
* **L7** — Proof Pack v2 (``proof_os``)
* **L8** — Value Ledger (``value_os``)
* **L9** — Capital Ledger (``capital_os``)
* **L10** — Adoption / Retainer (``adoption_os``)
* **L11** — Self-Evolving feedback (``self_evolving_os``, shadow-mode)
"""

from auto_client_acquisition.ai_stack_os.layer_health import (
    LayerHealth,
    StackHealth,
    layer_versions,
    snapshot_health,
)
from auto_client_acquisition.ai_stack_os.orchestrator import (
    AIStackOrchestrator,
    run_ai_stack,
)
from auto_client_acquisition.ai_stack_os.schemas import (
    AIStackInput,
    AIStackResult,
    LayerResult,
    LayerStatus,
    Offer,
    SourcePassportInput,
)

__all__ = [
    "AIStackInput",
    "AIStackOrchestrator",
    "AIStackResult",
    "LayerHealth",
    "LayerResult",
    "LayerStatus",
    "Offer",
    "SourcePassportInput",
    "StackHealth",
    "layer_versions",
    "run_ai_stack",
    "snapshot_health",
]
