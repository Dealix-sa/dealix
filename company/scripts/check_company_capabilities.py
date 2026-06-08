#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

CAPABILITIES = {
    "production_api": ["DATABASE_URL", "APP_SECRET_KEY", "JWT_SECRET_KEY", "API_KEYS"],
    "admin_api": ["DEALIX_ADMIN_API_KEY", "ADMIN_API_KEYS"],
    "secret_scanning": ["GITLEAKS_LICENSE"],
    "web_lead_research": ["GOOGLE_SEARCH_API_KEY", "GOOGLE_SEARCH_CX"],
    "places_lead_enrichment": ["GOOGLE_MAPS_API_KEY"],
    "crm_sync": ["HUBSPOT_ACCESS_TOKEN"],
    "whatsapp_green_api": ["GREEN_API_INSTANCE_ID", "GREEN_API_TOKEN"],
    "whatsapp_twilio": ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_WHATSAPP_FROM"],
    "email_sending": ["SMTP_PASSWORD"],
    "payments": ["MOYASAR_SECRET_KEY"],
    "ai_openai": ["OPENAI_API_KEY"],
    "ai_deepseek": ["DEEPSEEK_API_KEY"],
    "ai_minimax": ["MINIMAX_API_KEY"],
    "ai_groq": ["GROQ_API_KEY"],
    "railway_deploy": ["RAILWAY_TOKEN"],
}

def main() -> None:
    out = Path("company/reports")
    out.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Dealix Company Capability Check",
        "",
        "| Capability | Status | Missing |",
        "|---|---|---|",
    ]

    for name, keys in CAPABILITIES.items():
        missing = [k for k in keys if not os.getenv(k)]
        status = "READY" if not missing else "PARTIAL" if len(missing) < len(keys) else "MISSING"
        lines.append(f"| {name} | {status} | {', '.join(missing) if missing else '—'} |")

    path = out / "CAPABILITY_CHECK.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(path)

if __name__ == "__main__":
    main()
