"""Railway production config-as-code checks (repo + optional live API)."""

from __future__ import annotations

import json
import re
import subprocess
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


def probe_get(api_base: str, path: str, *, timeout_sec: float = 12.0, max_bytes: int = 4096) -> dict[str, Any]:
    """GET {api_base}{path} — returns status without raising."""
    base = (api_base or "").strip().rstrip("/")
    if not base:
        return {"probed": False, "reason": "no_api_base"}
    url = f"{base}{path}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = resp.getcode()
            body = resp.read(max_bytes).decode("utf-8", errors="replace")
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
    return probe_get(api_base, "/healthz", timeout_sec=timeout_sec)


VERSION_REQUIRED_FIELDS: tuple[str, ...] = ("service", "status", "version", "git_sha")
META_REQUIRED_FIELDS: tuple[str, ...] = ("service", "version", "surfaces", "canonical_links")


def validate_version_payload(probe: dict[str, Any]) -> dict[str, Any]:
    """Structural check for /version: JSON shape + required fields + status==ok."""
    if not probe.get("ok"):
        return {"valid": False, "reason": "probe_not_ok", "missing": []}
    snippet = probe.get("snippet") or ""
    try:
        payload = json.loads(snippet)
    except (TypeError, ValueError):
        return {"valid": False, "reason": "not_json", "missing": []}
    if not isinstance(payload, dict):
        return {"valid": False, "reason": "not_object", "missing": []}
    missing = [f for f in VERSION_REQUIRED_FIELDS if not payload.get(f)]
    if missing:
        return {"valid": False, "reason": "missing_fields", "missing": missing}
    if str(payload.get("status")).lower() != "ok":
        return {"valid": False, "reason": "status_not_ok", "missing": []}
    return {"valid": True, "reason": "", "missing": []}


def validate_meta_payload(probe: dict[str, Any]) -> dict[str, Any]:
    """Structural check for /api/v1/meta: JSON shape + non-empty surfaces."""
    if not probe.get("ok"):
        return {"valid": False, "reason": "probe_not_ok", "missing": []}
    snippet = probe.get("snippet") or ""
    try:
        payload = json.loads(snippet)
    except (TypeError, ValueError):
        return {"valid": False, "reason": "not_json", "missing": []}
    if not isinstance(payload, dict):
        return {"valid": False, "reason": "not_object", "missing": []}
    missing = [f for f in META_REQUIRED_FIELDS if f not in payload]
    if missing:
        return {"valid": False, "reason": "missing_fields", "missing": missing}
    surfaces = payload.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        return {"valid": False, "reason": "empty_surfaces", "missing": []}
    return {"valid": True, "reason": "", "missing": []}


def _shape_hint_ar(version_shape: dict[str, Any], meta_shape: dict[str, Any]) -> str:
    """Founder-facing Arabic hint when a trust endpoint returns 200 with bad shape."""
    parts: list[str] = []
    if not version_shape.get("valid"):
        reason = version_shape.get("reason")
        if reason == "not_json":
            parts.append("/version يرجع 200 لكن المحتوى ليس JSON — راجع CDN/Proxy.")
        elif reason == "missing_fields":
            missing = ", ".join(version_shape.get("missing") or [])
            parts.append(f"/version ناقص حقول: {missing}.")
        elif reason == "status_not_ok":
            parts.append("/version لا يعيد status=ok — تحقق من إعدادات النشر.")
    if not meta_shape.get("valid"):
        reason = meta_shape.get("reason")
        if reason == "not_json":
            parts.append("/api/v1/meta يرجع 200 لكن المحتوى ليس JSON.")
        elif reason == "missing_fields":
            missing = ", ".join(meta_shape.get("missing") or [])
            parts.append(f"/api/v1/meta ناقص حقول: {missing}.")
        elif reason == "empty_surfaces":
            parts.append("/api/v1/meta يرجع surfaces فارغ — راجع gtm_public_surfaces.")
    return " ".join(parts)


def probe_trust_layer(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """Probe GTM trust endpoints on production API."""
    paths = ("/healthz", "/version", "/api/v1/meta", "/health")
    probes = {p.strip("/").replace("/", "_") or "root": probe_get(api_base, p, timeout_sec=timeout_sec) for p in paths}
    healthz = probes.get("healthz") or {}
    snippet = (healthz.get("snippet") or "").lower()
    deploy_stale = healthz.get("ok") and "version" not in snippet
    version_missing = (probes.get("version") or {}).get("status") == 404
    meta_missing = (probes.get("api_v1_meta") or {}).get("status") == 404

    version_shape = validate_version_payload(probes.get("version") or {})
    meta_shape = validate_meta_payload(probes.get("api_v1_meta") or {})
    shape_hint = _shape_hint_ar(version_shape, meta_shape)

    ok = all(p.get("ok") for p in probes.values() if p.get("probed"))
    return {
        "probes": probes,
        "version_payload": version_shape,
        "meta_payload": meta_shape,
        "deploy_stale_hint_ar": (
            "النشر الحي قديم — /healthz بلا version أو /version غير منشور. انتظر CI + Railway deploy."
            if deploy_stale or version_missing or meta_missing
            else ""
        ),
        "shape_drift_hint_ar": shape_hint,
        "ok": (
            ok
            and not deploy_stale
            and not version_missing
            and version_shape["valid"]
            and meta_shape["valid"]
        ),
    }


def read_local_git_sha() -> str:
    """Return the current local HEAD SHA, or empty string if git is unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def extract_deployed_sha(version_probe: dict[str, Any]) -> str:
    """Parse the `git_sha` field out of a /version probe response snippet."""
    if not version_probe.get("ok"):
        return ""
    snippet = version_probe.get("snippet") or ""
    try:
        payload = json.loads(snippet)
    except (TypeError, ValueError):
        return ""
    sha = payload.get("git_sha") if isinstance(payload, dict) else ""
    if not isinstance(sha, str):
        return ""
    sha = sha.strip()
    if not sha or sha.lower() == "unknown":
        return ""
    return sha


def compare_deployed_sha(
    api_base: str,
    *,
    local_sha: str | None = None,
    timeout_sec: float = 12.0,
) -> dict[str, Any]:
    """Compare local HEAD SHA with the SHA reported by the live /version endpoint.

    Returns a dict with `verdict` in {MATCH, DRIFT, UNKNOWN, NOT_PROBED} plus an
    Arabic hint the founder can act on. UNKNOWN means we reached /version but
    the deployed SHA is missing/`unknown` (Railway env var not set).
    """
    base = (api_base or "").strip().rstrip("/")
    if not base:
        return {
            "verdict": "NOT_PROBED",
            "reason": "no_api_base",
            "hint_ar": "",
            "local_sha": "",
            "deployed_sha": "",
        }

    local = (local_sha if local_sha is not None else read_local_git_sha()).strip()
    version_probe = probe_get(base, "/version", timeout_sec=timeout_sec)
    deployed = extract_deployed_sha(version_probe)

    if not version_probe.get("ok"):
        status = version_probe.get("status")
        hint = (
            "/version غير منشور بعد — تأكد من اكتمال Railway deploy وأن git_sha مضبوط."
            if status == 404
            else "تعذّر الوصول إلى /version — تحقق من سلامة الـ API."
        )
        return {
            "verdict": "NOT_PROBED",
            "reason": "version_endpoint_unreachable",
            "status": status,
            "hint_ar": hint,
            "local_sha": local,
            "deployed_sha": "",
        }

    if not deployed:
        return {
            "verdict": "UNKNOWN",
            "reason": "deployed_sha_missing_or_unknown",
            "hint_ar": (
                "git_sha غير معروف على الإنتاج — اضبط GIT_SHA أو فعّل "
                "RAILWAY_GIT_COMMIT_SHA على الـ service variables."
            ),
            "local_sha": local,
            "deployed_sha": "",
        }

    if not local:
        return {
            "verdict": "UNKNOWN",
            "reason": "local_sha_unavailable",
            "hint_ar": "تعذّر قراءة git SHA المحلي — هل أنت داخل مستودع git؟",
            "local_sha": "",
            "deployed_sha": deployed,
        }

    # Normalize for short-vs-full SHA comparisons.
    short_local = local[:7]
    short_deployed = deployed[:7]
    if local == deployed or short_local == short_deployed:
        return {
            "verdict": "MATCH",
            "hint_ar": "",
            "local_sha": local,
            "deployed_sha": deployed,
        }

    return {
        "verdict": "DRIFT",
        "hint_ar": (
            f"الإنتاج يشغّل commit مختلف ({short_deployed}) عن HEAD المحلي ({short_local}). "
            "نفّذ git push وانتظر اكتمال Railway deploy."
        ),
        "local_sha": local,
        "deployed_sha": deployed,
    }


def analyze_railway_production(*, api_base: str | None = None) -> dict[str, Any]:
    repo = check_repo_railway_config()
    base = (api_base or DEFAULT_API_BASE) if api_base is not False else ""
    live = probe_healthz(base) if base else {"probed": False}
    trust = probe_trust_layer(base) if base else {"probed": False}
    sha = compare_deployed_sha(base) if base else {"verdict": "NOT_PROBED"}
    verdict = "PASS" if repo["ok"] else "FAIL"
    if repo["ok"] and live.get("probed") and not live.get("ok"):
        verdict = "WARN"
    if repo["ok"] and trust.get("deploy_stale_hint_ar"):
        verdict = "WARN"
    if repo["ok"] and trust.get("shape_drift_hint_ar"):
        verdict = "WARN"
    if repo["ok"] and sha.get("verdict") == "DRIFT":
        verdict = "WARN"
    return {
        "repo": repo,
        "live_healthz": live,
        "live_trust_layer": trust,
        "deployed_sha_check": sha,
        "canonical_start_command": CANONICAL_START,
        "canonical_predeploy": CANONICAL_PREDEPLOY,
        "verdict": verdict,
        "settings_doc": str(SETTINGS_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
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
