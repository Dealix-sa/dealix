"""Railway production config-as-code checks (repo + optional live API)."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import REPO_ROOT

RAILWAY_TOML = REPO_ROOT / "railway.toml"
RAILWAY_JSON = REPO_ROOT / "railway.json"
DOCKERFILE = REPO_ROOT / "Dockerfile"
PREDEPLOY_SH = REPO_ROOT / "scripts" / "railway_predeploy.sh"
SETTINGS_DOC = REPO_ROOT / "docs" / "ops" / "RAILWAY_PRODUCTION_SETTINGS_AR.md"
DEFAULT_API_BASE = "https://api.dealix.me"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


CANONICAL_PREDEPLOY = "sh /app/scripts/railway_predeploy.sh"
CANONICAL_PREDEPLOY_MARKER = "/app/scripts/railway_predeploy.sh"
CANONICAL_START = "/app/start.sh"
BAD_UI_PREDEPLOY_SNIPPETS = (
    "no migration needed",
    'echo "no migration needed"',
)


def _has_canonical_predeploy(text: str) -> bool:
    return CANONICAL_PREDEPLOY_MARKER in text and "railway_predeploy" in text


def check_repo_railway_config() -> dict[str, Any]:
    """Validate railway.toml, Dockerfile CMD, and predeploy script."""
    issues: list[str] = []
    warnings: list[str] = []

    toml = _read(RAILWAY_TOML)
    if not toml.strip():
        issues.append("missing railway.toml")
    elif 'healthcheckPath = "/healthz"' not in toml:
        issues.append('railway.toml must set healthcheckPath = "/healthz"')
    if not _has_canonical_predeploy(toml):
        issues.append(f"railway.toml preDeployCommand must invoke {CANONICAL_PREDEPLOY_MARKER}")
    if "startCommand" in toml and "NO startCommand" not in toml:
        warnings.append("railway.toml should not set startCommand (use Dockerfile CMD)")

    jsn = _read(RAILWAY_JSON)
    if jsn and "/healthz" not in jsn:
        issues.append("railway.json healthcheckPath should be /healthz")
    if jsn and not _has_canonical_predeploy(jsn):
        issues.append(f"railway.json preDeployCommand must invoke {CANONICAL_PREDEPLOY_MARKER}")

    docker = _read(DOCKERFILE)
    if "/app/start.sh" not in docker:
        issues.append("Dockerfile must CMD /app/start.sh")
    if 'healthz' not in docker and '/health' in docker:
        warnings.append("Dockerfile HEALTHCHECK should prefer /healthz")

    if not PREDEPLOY_SH.is_file():
        issues.append("missing scripts/railway_predeploy.sh")
    elif "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in _read(PREDEPLOY_SH):
        warnings.append("railway_predeploy.sh should gate migrations on RUN_RAILWAY_PRE_DEPLOY_MIGRATE")

    for cfg_name, cfg_text in (("railway.toml", toml), ("railway.json", jsn)):
        if not cfg_text:
            continue
        if "railway_predeploy" not in cfg_text:
            issues.append(f"{cfg_name} must set preDeployCommand to railway_predeploy.sh")
        lowered = cfg_text.lower()
        for bad in BAD_UI_PREDEPLOY_SNIPPETS:
            if bad in lowered:
                issues.append(
                    f"{cfg_name} must not use echo no-migration stub — use {CANONICAL_PREDEPLOY}"
                )
                break

    if not SETTINGS_DOC.is_file():
        issues.append("missing docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md")

    return {
        "issues": issues,
        "warnings": warnings,
        "ok": len(issues) == 0,
    }


def probe_http_json(
    api_base: str,
    path: str,
    *,
    timeout_sec: float = 12.0,
) -> dict[str, Any]:
    """GET {api_base}{path} — lightweight probe."""
    base = (api_base or "").strip().rstrip("/")
    if not base:
        return {"probed": False, "reason": "no_api_base"}
    url = f"{base}{path}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = resp.getcode()
            body = resp.read(512).decode("utf-8", errors="replace")
            return {
                "probed": True,
                "url": url,
                "status": code,
                "ok": code == 200,
                "snippet": body[:200],
            }
    except urllib.error.HTTPError as exc:
        return {"probed": True, "url": url, "status": exc.code, "ok": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"probed": True, "url": url, "ok": False, "error": str(exc)}


def probe_healthz(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """GET {api_base}/healthz — returns status without raising."""
    return probe_http_json(api_base, "/healthz", timeout_sec=timeout_sec)


def probe_version(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    return probe_http_json(api_base, "/version", timeout_sec=timeout_sec)


def analyze_railway_production(*, api_base: str | None = None) -> dict[str, Any]:
    repo = check_repo_railway_config()
    base = (api_base or DEFAULT_API_BASE) if api_base is not False else ""
    live_hz = probe_healthz(base) if base else {"probed": False}
    live_ver = probe_version(base) if base else {"probed": False}
    live_meta = probe_http_json(base, "/api/v1/meta") if base else {"probed": False}

    verdict = "PASS" if repo["ok"] else "FAIL"
    live_failures: list[str] = []
    for label, probe in (("healthz", live_hz), ("version", live_ver), ("meta", live_meta)):
        if probe.get("probed") and not probe.get("ok"):
            live_failures.append(label)
    if repo["ok"] and live_failures:
        verdict = "WARN"

    deploy_note_ar = None
    if live_ver.get("status") == 404:
        deploy_note_ar = (
            "إذا /version=404 فالإنتاج لم يدمج آخر main — ادفع وانتظر CI ثم أعد النشر"
        )
        if live_hz.get("ok") and live_hz.get("snippet"):
            import json

            try:
                hz_body = json.loads(live_hz["snippet"])
            except json.JSONDecodeError:
                hz_body = {}
            if hz_body.get("version") or hz_body.get("git_sha"):
                live_ver = {
                    **live_ver,
                    "ok": True,
                    "via_healthz_fallback": True,
                    "version": hz_body.get("version"),
                    "git_sha": hz_body.get("git_sha"),
                }
                live_failures = [x for x in live_failures if x != "version"]
                if not live_failures and repo["ok"]:
                    verdict = "PASS"
                deploy_note_ar = (
                    "استخدم /healthz للإصدار حتى يُنشر /version — ادفع main ثم أعد النشر"
                )

    return {
        "repo": repo,
        "live_healthz": live_hz,
        "live_version": live_ver,
        "live_meta": live_meta,
        "live_failures": live_failures,
        "canonical_start_command": CANONICAL_START,
        "canonical_predeploy": CANONICAL_PREDEPLOY,
        "verdict": verdict,
        "settings_doc": str(SETTINGS_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
        "deploy_note_ar": deploy_note_ar,
    }


def parse_railway_ui_predeploy_drift(predeploy: str) -> str | None:
    """Return Arabic hint if Railway UI pre-deploy drifts from railway.toml."""
    cmd = (predeploy or "").strip()
    if not cmd:
        return None
    lower = cmd.lower()
    if CANONICAL_PREDEPLOY in cmd or cmd == CANONICAL_PREDEPLOY:
        return None
    for bad in BAD_UI_PREDEPLOY_SNIPPETS:
        if bad in lower:
            return (
                f"استبدل Pre-deploy في Railway UI بـ {CANONICAL_PREDEPLOY} "
                "(أو اتركه فارغاً ليأخذ railway.toml). "
                "للترحيل التلقائي: RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1"
            )
    if "railway_predeploy" in lower and "/app/scripts" not in lower:
        return f"استخدم مسار الحاوية: {CANONICAL_PREDEPLOY}"
    if "railway_predeploy" in lower:
        return None
    return f"Pre-deploy يجب أن يطابق railway.toml: {CANONICAL_PREDEPLOY}"


def parse_railway_ui_drift_hint(start_command: str) -> str | None:
    """Return Arabic hint if UI start command likely breaks PORT expansion."""
    cmd = (start_command or "").strip()
    if not cmd:
        return None
    if cmd in ("/app/start.sh", "bash /app/start.sh", "sh /app/start.sh"):
        return None
    if re.match(r"^\./start\.sh$", cmd):
        return "امسح Start Command أو استبدل ./start.sh بـ /app/start.sh"
    if "uvicorn" in cmd and "$PORT" not in cmd and "${PORT" not in cmd:
        return "لا تضع uvicorn مباشرة في Start Command — استخدم /app/start.sh"
    return "امسح Start Command في Railway UI لاستخدام Dockerfile CMD"
