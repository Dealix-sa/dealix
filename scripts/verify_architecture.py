from pathlib import Path
ALLOWED_TOP_LEVEL = {
    ".github",
    ".claude",
    ".cursor",
    "alembic",
    "api",
    "apps",
    "auto_client_acquisition",
    "autonomous_growth",
    "clients",
    "core",
    "dashboard",
    "data",
    "db",
    "dealix",
    "demos",
    "design-skills",
    "design-systems",
    "docs",
    "evals",
    "frontend",
    "integrations",
    "landing",
    "migrations",
    "platform_core",
    "projects",
    "readiness",
    "scripts",
    "simulations",
    "supabase",
    "templates",
    "tests",
}
ALLOWED_ROOT_FILES = {
    "README.md",
    "README.ar.md",
    "QUICK_START.md",
    "DEPLOYMENT.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "CHANGELOG.md",
    "DASHBOARD.md",
    "DEALIX_COMPANY_OPERATIONAL_STATE.md",
    "DEALIX_READINESS.md",
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "AGENTS.md",
    "Dockerfile",
    "Procfile",
    "Makefile",
    "docker-compose.yml",
    "alembic.ini",
    "cli.py",
    "lighthouserc.js",
    "locustfile.py",
    "pyproject.toml",
    "railway.json",
    "railway.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "v3_app.py",
    ".dockerignore",
    ".editorconfig",
    ".env.example",
    ".env.staging.example",
    ".gitignore",
    ".gitleaks.toml",
    ".pa11yrc.json",
    ".pre-commit-config.yaml",
    ".secrets.baseline",
}
violations = []
for item in Path(".").iterdir():
    name = item.name
    if name == ".git":
        continue
    if item.is_dir() and name not in ALLOWED_TOP_LEVEL:
        violations.append(f"Unexpected top-level directory: {name}")
    if item.is_file() and name not in ALLOWED_ROOT_FILES:
        violations.append(f"Unexpected root file: {name}")
if violations:
    print("Architecture violations:")
    for violation in violations:
        print(f"- {violation}")
    raise SystemExit(1)
print("PASS: repository architecture matches Dealix approved map.")
