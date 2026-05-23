"""Bootstrap the public Dealix OS scaffold.

Creates the master docs, doc trees, env example, and Python module packages
required by the Implementation Automation Pack. Idempotent: never overwrites
existing files. Safe to run repeatedly.
"""

from pathlib import Path

FILES = {
    "DEALIX_MASTER_OPERATING_BLUEPRINT.md": "# Dealix Master Operating Blueprint\n\n",
    "DEALIX_INTEGRATION_MAP.md": "# Dealix Integration Map\n\n",
    "DEALIX_FINAL_REPO_TREE.md": "# Dealix Final Repository Tree\n\n",
    "DEALIX_SYSTEM_COMPLETION_MATRIX.md": "# Dealix System Completion Matrix\n\n",
    "DEALIX_EXECUTION_ROADMAP_FINAL.md": "# Dealix Final Execution Roadmap\n\n",
    "DEALIX_DEFINITION_OF_DONE.md": "# Dealix Definition of Done\n\n",
    "DEALIX_IMPLEMENTATION_SPRINT_PACK.md": "# Dealix Implementation Sprint Pack\n\n",
    "DEALIX_IMPLEMENTATION_MASTER_CHECKLIST.md": "# Dealix Implementation Master Checklist\n\n",
    "docs/ops/MASTER_COMMAND_SYSTEM.md": "# Master Command System\n\n",
    "docs/ops/GITHUB_GOVERNANCE_SYSTEM.md": "# GitHub Governance System\n\n",
    "docs/security/SECURITY_BASELINE.md": "# Security Baseline\n\n",
    "docs/data/COMPANY_DATA_ARCHITECTURE.md": "# Company Data Architecture\n\n",
    "docs/founder/MASTER_DAILY_CEO_LOOP.md": "# Master Daily CEO Loop\n\n",
    "docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md": "# Revenue Operations Playbook\n\n",
    "docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md": "# Delivery & Client Success OS\n\n",
    "docs/finance/FINANCE_PRICING_CAPITAL_OS.md": "# Finance Pricing Capital OS\n\n",
    "docs/trust/TRUST_COMPLIANCE_AI_RISK_OS.md": "# Trust Compliance AI Risk OS\n\n",
    "docs/content/BRAND_PROOF_CONTENT_OS.md": "# Brand Proof Content OS\n\n",
    "docs/product/PRODUCTIZATION_ENGINEERING_OS.md": "# Productization Engineering OS\n\n",
    "docs/people/PEOPLE_DELEGATION_PARTNER_OS.md": "# People Delegation Partner OS\n\n",
    ".env.example": "# Example only. Never commit real keys.\nMINIMAX_API_KEY=\nOPENAI_API_KEY=\n",
    "SECURITY.md": "# Security Policy\n\nNo secrets, private customer data, or real payment data should be committed.\n",
}

DIRS = [
    "dealix_cli",
    "ops_runtime",
    "control_plane",
    "execution_engine",
    "scripts",
    "schemas",
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/delivery",
    "docs/client_success",
    "docs/finance",
    "docs/trust",
    "docs/ai_management",
    "docs/data",
    "docs/product",
    "docs/engineering",
    "docs/content",
    "docs/people",
    "docs/partners",
    "docs/ops",
    "docs/security",
    "docs/control_plane",
    ".github/workflows",
    "dashboard_data/demo",
    "internal_dashboard",
]


def write_if_missing(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(content, encoding="utf-8")
        print(f"created: {path}")
    else:
        print(f"exists:  {path}")


def main() -> None:
    for directory in DIRS:
        Path(directory).mkdir(parents=True, exist_ok=True)
    for path, content in FILES.items():
        write_if_missing(path, content)
    for init_dir in ["dealix_cli", "ops_runtime", "control_plane", "execution_engine"]:
        write_if_missing(f"{init_dir}/__init__.py", "")
    print("\nPASS: Dealix OS public bootstrap completed.")


if __name__ == "__main__":
    main()
