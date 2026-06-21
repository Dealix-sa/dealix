"""Dealix Company Operating System — Daily revenue, intake, and operations automation.

This module provides the core operating engines for Dealix business automation:

- **micro_master**: Quick-win opportunity identification and CEO daily pack generation
- **revenue_engine_v2**: Full commercial pipeline, lead scoring, and approval queues
- **intake_engine**: Client intake processing and diagnostic session preparation
- **crm**: Customer relationship management and follow-up automation
- **proof_os**: Proof pack assembly and customer trust metric generation

Wave Assignment:
- Waves 1-2: Core revenue and intake engines (production-ready)
- Waves 3-5: CRM, follow-up, and delivery OS (in development)
- Waves 6+: Trust, governance, and enterprise systems

Usage:
    from company.micro.micro_master import run_micro_daily_pack
    from company.revenue_engine.revenue_engine_v2 import process_revenue_pipeline
    from company.intake.intake_engine import process_intake_forms

    await run_micro_daily_pack()
    await process_revenue_pipeline()
    await process_intake_forms()

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

# Public API
__all__ = [
    "micro_master",
    "revenue_engine_v2",
    "intake_engine",
    "crm",
    "proof_os",
]
