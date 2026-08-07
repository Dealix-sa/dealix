"""Dealix Company Operating System — Daily revenue, intake, and operations automation.

This module provides the core operating engines for Dealix business automation:

- **micro**: Quick-win opportunity identification and CEO daily pack generation
- **revenue_engine**: Full commercial pipeline, lead scoring, and approval queues
- **intake**: Client intake processing and diagnostic session preparation
- **crm**: Customer relationship management and follow-up automation
- **master_stable**: Stable daily operating layer (lead queue + CEO report)
- **leads**: Real lead sourcing (Google Places) into runtime CSVs
- **sales**: Lead qualification and BANT scoring helpers
- **delivery**: 14-day pilot delivery orchestrator and proof logging
- **automation**: Approval-gated WhatsApp + Moyasar payment helpers

Wave Assignment:
- Waves 1-2: Core revenue and intake engines (production-ready)
- Waves 3-5: CRM, follow-up, and delivery OS
- Waves 6-7: Trust pack and launch readiness

Each engine exposes a ``main()`` entry point and runs standalone:

    python company/micro/micro_master.py
    python company/revenue_engine/revenue_engine_v2.py
    python company/intake/intake_engine.py

Or run the whole safe daily sequence + Command Room with one command:

    bash scripts/dealix_command_day.sh

Configuration:
    All engines respect .env variables for API keys, database URLs, and operational modes.
    See .env.example for complete configuration reference.

    Critical env vars:
    - DATABASE_URL: PostgreSQL connection for customer/lead data
    - OPENROUTER_API_KEY: LLM provider for scoring and decision making
    - SLACK_API_TOKEN: For notifications and reporting
    - WHATSAPP_API_KEY: For customer outreach (Wave 5+)

Output:
    All daily runtime outputs are written to company/runtime/ (gitignored).
    Generated reports go to company/reports/ (checked in as static snapshots).
    Customer data never committed; lives in company/runtime/customers/ (gitignored).

See Also:
    - docs/DEALIX_BUSINESS_MODEL.md: Business context and offer ladder
    - docs/CEO_OPERATING_CONTEXT.md: Strategic context and priorities
    - scripts/README.md: Daily operation script reference
"""

__version__ = "2.0.0"
__author__ = "Dealix Team"
__email__ = "team@dealix.ai"

# Public API — names of the engine sub-packages that ship in this distribution.
__all__ = [
    "micro",
    "revenue_engine",
    "intake",
    "crm",
    "master_stable",
    "leads",
    "sales",
    "delivery",
    "automation",
]
