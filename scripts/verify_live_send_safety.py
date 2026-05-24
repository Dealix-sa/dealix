"""Verify external sending (WhatsApp / Email / Moyasar) is fully gated.

Static checks against the integration registry + the codebase:
    * No frontend code (apps/web/**/*.{ts,tsx}) calls a forbidden API directly.
    * Every integration declared in registries/integration_registry.yaml
      with direction=outbound has its kill switches named and frontend_direct_call_allowed=false.
    * MOYASAR_SECRET_KEY / GREEN_API_TOKEN / SMTP_PASSWORD names do not
      appear in any apps/web file.
    * WhatsApp paths reference a suppression check + approval queue.

Writes /tmp/dealix_live_send_safety.PASS on PASS so verify_production_env.py
can refuse WHATSAPP_ALLOW_LIVE_SEND=true unless the certification is fresh.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    REPO_ROOT,
    VerifierReport,
    load_yaml,
    main_cli,
    must_be_file,
    iter_files,
    repo_path,
)

INTEGRATIONS = "registries/integration_registry.yaml"
FRONTEND_DIR = "apps/web"

FORBIDDEN_FRONTEND_TOKENS = re.compile(
    r"\b(MOYASAR_SECRET_KEY|GREEN_API_TOKEN|GREEN_API_INSTANCE_ID|SMTP_PASSWORD|"
    r"HUBSPOT_ACCESS_TOKEN|JWT_SECRET_KEY|GROQ_API_KEY)\b"
)
FORBIDDEN_FRONTEND_URLS = re.compile(
    r"https?://(api\.green-api\.com|api\.moyasar\.com|api\.hubapi\.com|graph\.facebook\.com)",
    re.I,
)


def run() -> VerifierReport:
    r = VerifierReport(verifier="Live Send Safety")
    if not must_be_file(r, "integration_registry", INTEGRATIONS):
        return r

    data = load_yaml(repo_path(INTEGRATIONS))
    integrations = data.get("integrations") or []
    if not integrations:
        r.fail("integrations_declared", "no integrations declared")
        return r
    r.pass_("integrations_declared", f"{len(integrations)} integrations")

    # per-integration audit
    for i in integrations:
        iid = i.get("id", "<unknown>")
        if i.get("frontend_direct_call_allowed", False):
            r.fail(f"integration[{iid}]_frontend", "frontend_direct_call_allowed must be false")
            continue
        if i.get("direction") in ("outbound", "bidirectional"):
            ks = i.get("kill_switches") or {}
            gates = i.get("gates") or {}
            if not gates.get("approval_required"):
                r.fail(f"integration[{iid}]_approval",
                       "approval_required must be set on outbound integrations")
                continue
            # A0 (read-only research / analytics) is exempt from per-call audit;
            # everything else must audit.
            if (not gates.get("requires_audit_write", False)
                    and gates.get("approval_required") != "A0"):
                r.warn(f"integration[{iid}]_audit",
                       "requires_audit_write should be true for outbound integrations")
            if iid in {"whatsapp_greenapi", "email_smtp", "moyasar_payments"}:
                if "live_send_enable_flag" not in ks or "mock_mode_flag" not in ks:
                    r.fail(f"integration[{iid}]_kill_switches",
                           "live_send_enable_flag + mock_mode_flag required")
                    continue
            r.pass_(f"integration[{iid}]",
                    f"gated A{gates.get('approval_required', '?')[-1]}")
        else:
            r.pass_(f"integration[{iid}]", "inbound/read-only")

    # frontend scan
    fe_root = repo_path(FRONTEND_DIR)
    if not fe_root.exists():
        r.warn("frontend_scan", f"{FRONTEND_DIR} not present — nothing to scan")
    else:
        leaked: list[tuple[Path, int, str]] = []
        for path in iter_files(fe_root, suffixes={".ts", ".tsx", ".js", ".jsx"}):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for lineno, line in enumerate(text.splitlines(), start=1):
                if FORBIDDEN_FRONTEND_TOKENS.search(line) or FORBIDDEN_FRONTEND_URLS.search(line):
                    leaked.append((path.relative_to(REPO_ROOT), lineno, line.strip()[:200]))
        if leaked:
            for p, ln, snippet in leaked[:20]:
                r.fail(f"frontend_leak:{p}:{ln}", snippet,
                       hint="move the call to a server route under api/internal")
            if len(leaked) > 20:
                r.fail("frontend_leak:more", f"+{len(leaked) - 20} additional leaks")
        else:
            r.pass_("frontend_scan", "no forbidden secret/url tokens in apps/web")

    # codebase reference checks for WhatsApp gates
    referenced_terms = {
        "approval_queue": False,
        "suppression": False,
        "WHATSAPP_MOCK_MODE": False,
        "WHATSAPP_ALLOW_LIVE_SEND": False,
        "WHATSAPP_DAILY_LIMIT": False,
    }
    for path in iter_files(REPO_ROOT, suffixes={".py", ".md", ".yaml", ".yml"},
                           skip_dirs=("apps/web",)):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for k in list(referenced_terms):
            if not referenced_terms[k] and k in text:
                referenced_terms[k] = True
    for k, ok in referenced_terms.items():
        if ok:
            r.pass_(f"references:{k}", "found in repo")
        else:
            r.warn(f"references:{k}", "not found — gate may be unimplemented",
                   hint=f"ensure {k} is checked before any live send")

    # write the PASS marker if green (used by verify_production_env.py)
    marker = Path("/tmp/dealix_live_send_safety.PASS")
    if r.overall == "PASS":
        try:
            marker.write_text("PASS\n", encoding="utf-8")
        except Exception:
            pass
    else:
        try:
            marker.unlink()
        except FileNotFoundError:
            pass

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_live_send_safety"))
