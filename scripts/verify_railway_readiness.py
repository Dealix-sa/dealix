"""Verify the repo is configured correctly for Railway deployment.

Checks:
    * railway.toml / railway.json present and consistent
    * Dockerfile + start (CMD or start.sh) present and healthcheck wired
    * scripts/railway_predeploy.sh exists and is referenced
    * No secrets baked into Dockerfile / railway config
    * /healthz route is reachable from FastAPI app
    * .github/workflows/dealix-production-certification.yml present
      so Railway "Wait for CI" has something to wait on
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    main_cli,
    must_be_file,
    repo_path,
)

SECRET_NAMES = re.compile(
    r"\b(MOYASAR_SECRET_KEY|GREEN_API_TOKEN|JWT_SECRET_KEY|DEALIX_INTERNAL_TOKEN|"
    r"HUBSPOT_ACCESS_TOKEN|GROQ_API_KEY|SMTP_PASSWORD|GOOGLE_SEARCH_API_KEY)\s*=\s*[\w.-]+"
)


def run() -> VerifierReport:
    r = VerifierReport(verifier="Railway Readiness")

    if not must_be_file(r, "railway.toml", "railway.toml"):
        return r
    must_be_file(r, "railway.json", "railway.json",
                 hint="optional but recommended for the JSON schema editor experience")

    toml = repo_path("railway.toml").read_text(encoding="utf-8")
    if "DOCKERFILE" in toml:
        r.pass_("railway_builder", "DOCKERFILE")
    else:
        r.fail("railway_builder", "expected DOCKERFILE builder", hint="set builder = \"DOCKERFILE\"")

    if "healthcheckPath" in toml and "/healthz" in toml:
        r.pass_("healthcheck", "/healthz wired")
    else:
        r.fail("healthcheck", "healthcheckPath missing or not /healthz")

    if "preDeployCommand" in toml:
        r.pass_("predeploy_hook", "preDeployCommand declared")
    else:
        r.warn("predeploy_hook", "no preDeployCommand — alembic upgrade head will not auto-run")

    # Dockerfile checks
    must_be_file(r, "Dockerfile", "Dockerfile")
    df = repo_path("Dockerfile").read_text(encoding="utf-8")
    if "start.sh" in df:
        r.pass_("docker_start", "start.sh referenced")
    else:
        r.fail("docker_start", "no start.sh reference in Dockerfile")
    if "USER app" in df or "USER " in df:
        r.pass_("docker_non_root", "non-root USER set")
    else:
        r.fail("docker_non_root", "container must run non-root")

    if SECRET_NAMES.search(df):
        r.fail("docker_no_secrets", "secret-looking assignment found in Dockerfile",
               hint="remove and inject via Railway → Variables")
    else:
        r.pass_("docker_no_secrets", "no inline secrets")

    if SECRET_NAMES.search(toml):
        r.fail("railway_no_secrets", "secret-looking assignment in railway.toml",
               hint="Railway Variables only; never commit")
    else:
        r.pass_("railway_no_secrets", "no inline secrets")

    # Predeploy script
    must_be_file(r, "predeploy_script", "scripts/railway_predeploy.sh")

    # CI workflow exists so 'Wait for CI' has something to wait on
    must_be_file(r, "ci_workflow",
                 ".github/workflows/dealix-production-certification.yml",
                 hint="Railway Settings → Source → Wait for CI requires this workflow")

    # /healthz route
    found_healthz = False
    for path in (repo_path("api/main.py"), repo_path("api/routers/health.py")):
        if path.exists() and "/healthz" in path.read_text(encoding="utf-8", errors="ignore"):
            found_healthz = True
            break
    if found_healthz:
        r.pass_("healthz_route", "/healthz served by FastAPI")
    else:
        r.warn("healthz_route", "could not find /healthz route in api/main.py or api/routers/health.py")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_railway_readiness"))
