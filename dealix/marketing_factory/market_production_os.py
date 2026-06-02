"""Market Production OS — governed core for the Saudi B2B go-to-market machine.

Pure functions only. No network, no sending, no charging. This module backs:

- the Cold Email Draft Factory quality gate (`draft_quality_gate`, `send_gate`),
- the Sending Ramp OS caps (`sending_ramp_cap`, `daily_draft_mix`),
- the suppression-first rule (`is_suppressed`),
- schema + seed-data validation (`validate_record`, `validate_dataset`, `validate_all`).

Hard rule encoded here: 250 DRAFTS/day is allowed, but SENDS/day are capped by the
warm-up ramp and domain health — 250 sends/day is only reachable at week 4+ when
health is within thresholds. Every external send still requires founder approval
(approval is recorded in the Founder Approval Queue, not here).

JSON Schema validation is done with a small dependency-free checker (required
fields + top-level types + enums); `jsonschema` is intentionally not required.
Claim/cold-channel safety reuses `auto_client_acquisition.governance_os`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

# Repo root: this file is <repo>/dealix/marketing_factory/market_production_os.py
REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = REPO_ROOT / "schemas"
DATA_DIR = REPO_ROOT / "data"

# --- Production targets -----------------------------------------------------

DRAFTS_PER_DAY = 250

# Daily draft production mix; the values sum to DRAFTS_PER_DAY.
DRAFT_MIX: dict[str, int] = {
    "first_touch": 100,
    "follow_up_1": 75,
    "follow_up_2": 50,
    "proposal_intro": 15,
    "close_loop": 10,
}

# Warm-up ramp: maximum SENDS/day by week. Independent of the drafts/day target.
RAMP_CAPS: dict[int, int] = {0: 20, 1: 50, 2: 100, 3: 150, 4: 250}

# Deliverability health thresholds (fractions of volume).
MAX_BOUNCE_RATE = 0.03
MAX_SPAM_COMPLAINT_RATE = 0.003  # 0.3%

# Minimum personalization level that is allowed to be sent.
SENDABLE_PERSONALIZATION = {"P1", "P2", "P3"}

# Subjects that imply a prior thread that does not exist are misleading.
MISLEADING_SUBJECT_PREFIXES = (
    "re:",
    "fwd:",
    "fw:",
    "رد:",
    "اعادة توجيه:",
    "إعادة توجيه:",
)

WARMUP_WEEK: dict[str, int] = {
    "week0": 0,
    "week1": 1,
    "week2": 2,
    "week3": 3,
    "week4": 4,
    "steady": 4,
}

# Local fallback only — used when the governance module cannot be imported.
_FORBIDDEN_SNIPPETS = (
    "نضمن",
    "ضمان مبيعات",
    "guaranteed sales",
    "guarantee sales",
    "scraping",
    "scrape emails",
    "cold whatsapp",
    "واتساب بارد",
    "linkedin automation",
    "أتمتة لينكدإن",
    "buy email list",
    "purchased list",
)


# --- Production targets -----------------------------------------------------


def daily_draft_mix() -> dict[str, int]:
    """Return a copy of the daily draft production mix (sums to DRAFTS_PER_DAY)."""
    return dict(DRAFT_MIX)


def draft_mix_total() -> int:
    """Total drafts/day across all sequence steps."""
    return sum(DRAFT_MIX.values())


# --- Sending ramp + health --------------------------------------------------


def health_ok(health: dict[str, Any] | None) -> bool:
    """True when deliverability health is within thresholds and no provider warning."""
    if not health:
        return True
    if health.get("provider_warning"):
        return False
    if float(health.get("bounce_rate", 0.0) or 0.0) >= MAX_BOUNCE_RATE:
        return False
    if float(health.get("spam_complaint_rate", 0.0) or 0.0) >= MAX_SPAM_COMPLAINT_RATE:
        return False
    return True


def sending_ramp_cap(week: int, health: dict[str, Any] | None = None) -> int:
    """Maximum SENDS/day for a warm-up `week` given current `health`.

    Drafts/day are never capped here; only sends. Unhealthy metrics force the
    cap to 0 (pause) regardless of week. Week 4+ steady state allows 250/day.
    """
    if not health_ok(health):
        return 0
    if week < 0:
        return 0
    if week >= 4:
        return RAMP_CAPS[4]
    return RAMP_CAPS[week]


def account_week(account: dict[str, Any]) -> int:
    """Map an email account's warmup_stage to a ramp week index."""
    return WARMUP_WEEK.get(str(account.get("warmup_stage", "week0")), 0)


# --- Suppression + subject safety ------------------------------------------


def is_suppressed(values: dict[str, str], suppression: Iterable[dict[str, Any]]) -> bool:
    """True if any of `values` (keys: email/domain/company) is on the suppression list."""
    for entry in suppression or []:
        etype = entry.get("type")
        target = str(entry.get("value", "")).strip().lower()
        candidate = str(values.get(etype, "") or "").strip().lower()
        if etype and target and candidate and candidate == target:
            return True
    return False


def subject_is_misleading(subject: str | None) -> bool:
    """True for empty subjects or fake reply/forward prefixes (no prior thread)."""
    if not subject or not subject.strip():
        return True
    lowered = subject.strip().lower()
    return lowered.startswith(MISLEADING_SUBJECT_PREFIXES)


def _contains_forbidden(text: str) -> bool:
    lowered = (text or "").lower()
    return any(snippet.lower() in lowered for snippet in _FORBIDDEN_SNIPPETS)


def governance_allows(text: str) -> bool:
    """Reuse governance_os claim/cold-channel guard; fall back to a local check."""
    try:
        from auto_client_acquisition.governance_os import policy_check_draft
    except Exception:
        return not _contains_forbidden(text)
    try:
        return bool(policy_check_draft(text).allowed)
    except Exception:
        return not _contains_forbidden(text)


# --- Draft + batch gates ----------------------------------------------------


def draft_quality_gate(
    draft: dict[str, Any],
    suppression: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Decide whether a draft is eligible to enter the approval queue.

    Returns ``{"allowed": bool, "reasons": list[str]}``. A draft is NOT eligible if
    it is missing an unsubscribe mechanism, is high-risk, fails compliance, is below
    P1 personalization, has a misleading subject, has no catalog offer, contains
    governance-blocked content, or targets a suppressed recipient.
    """
    reasons: list[str] = []
    if not draft.get("unsubscribe_included"):
        reasons.append("unsubscribe_missing")
    if draft.get("risk_level") == "high":
        reasons.append("risk_high")
    if draft.get("compliance_status") != "pass":
        reasons.append("compliance_not_pass")
    if draft.get("personalization_level") not in SENDABLE_PERSONALIZATION:
        reasons.append("personalization_below_P1")
    if subject_is_misleading(draft.get("subject")):
        reasons.append("misleading_subject")
    if not str(draft.get("offer", "") or "").strip():
        reasons.append("offer_missing")
    text = f"{draft.get('subject', '')}\n{draft.get('body', '')}"
    if not governance_allows(text):
        reasons.append("content_blocked_by_governance")
    if suppression is not None:
        values = {
            "company": str(draft.get("company", "") or ""),
            "email": str(draft.get("recipient_email", "") or ""),
            "domain": str(draft.get("domain", "") or ""),
        }
        if is_suppressed(values, suppression):
            reasons.append("recipient_suppressed")
    return {"allowed": not reasons, "reasons": reasons}


def send_gate(
    draft: dict[str, Any],
    suppression: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Decide whether an approved draft may actually be sent.

    Requires the quality gate to pass AND an explicit founder approval AND a
    non-suppressed send status.
    """
    quality = draft_quality_gate(draft, suppression)
    reasons = list(quality["reasons"])
    if draft.get("approval_status") != "approved":
        reasons.append("not_approved")
    if draft.get("send_status") == "suppressed":
        reasons.append("suppressed")
    return {"allowed": not reasons, "reasons": reasons}


def batch_send_allowed(
    batch: dict[str, Any],
    account: dict[str, Any],
) -> dict[str, Any]:
    """Decide whether a sending batch may run on a given account.

    Returns ``{"allowed": bool, "reasons": list[str], "cap": int}``. A batch may
    not run unless it is approved, the account's domain is healthy, and the batch
    size respects the warm-up ramp cap for the account's week.
    """
    reasons: list[str] = []
    if batch.get("status") not in ("approved", "sending"):
        reasons.append("batch_not_approved")
    if not batch.get("approved_at"):
        reasons.append("no_approval_timestamp")
    health = {
        "bounce_rate": account.get("bounce_rate", 0.0),
        "spam_complaint_rate": account.get("spam_complaint_rate", 0.0),
        "provider_warning": account.get("provider_warning", False),
    }
    cap = sending_ramp_cap(account_week(account), health)
    if cap <= 0:
        reasons.append("domain_unhealthy_or_paused")
    if int(batch.get("batch_size", 0) or 0) > cap:
        reasons.append("exceeds_ramp_cap")
    return {"allowed": not reasons, "reasons": reasons, "cap": cap}


# --- Reply routing ----------------------------------------------------------

REPLY_ACTION_MAP: dict[str, str] = {
    "positive": "discovery_invite",
    "interested_later": "nurture",
    "price_question": "offer_card",
    "send_more_info": "proof_pack",
    "wrong_person": "referral_ask",
    "not_interested": "close_polite",
    "unsubscribe": "suppress",
    "angry": "apologize_and_suppress",
    "auto_reply": "ignore",
    "bounce": "suppress",
}


def reply_next_action(category: str) -> str:
    """Map a reply category to its next action (suppress for unsubscribe/angry/bounce)."""
    return REPLY_ACTION_MAP.get(category, "founder_review")


# --- Schema + data validation (dependency-free) -----------------------------

_JSON_TYPES: dict[str, Any] = {
    "string": str,
    "object": dict,
    "array": list,
    "null": type(None),
}


def _type_ok(value: Any, type_spec: Any) -> bool:
    if isinstance(type_spec, list):
        return any(_type_ok(value, t) for t in type_spec)
    if type_spec == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_spec == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_spec == "boolean":
        return isinstance(value, bool)
    py = _JSON_TYPES.get(type_spec)
    if py is None:
        return True
    return isinstance(value, py)


def validate_record(record: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Validate a record against a JSON schema (required, top-level types, enums)."""
    if not isinstance(record, dict):
        return ["record is not an object"]
    errors: list[str] = []
    for key in schema.get("required", []):
        if key not in record:
            errors.append(f"missing required field: {key}")
    props: dict[str, Any] = schema.get("properties", {})
    allow_additional = schema.get("additionalProperties", True)
    for key, val in record.items():
        spec = props.get(key)
        if spec is None:
            if allow_additional is False:
                errors.append(f"unexpected field: {key}")
            continue
        if "type" in spec and val is not None:
            if not _type_ok(val, spec["type"]):
                errors.append(f"field {key}: wrong type (expected {spec['type']})")
        if "enum" in spec and val is not None:
            if val not in spec["enum"]:
                errors.append(f"field {key}: '{val}' not in enum")
    return errors


def load_schema(name: str) -> dict[str, Any]:
    """Load schemas/<name>.schema.json."""
    path = SCHEMAS_DIR / f"{name}.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path | str) -> list[dict[str, Any]]:
    """Load a JSONL file into a list of dicts (blank lines skipped)."""
    p = Path(path)
    if not p.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def load_yaml_list(path: Path | str, key: str | None = None) -> list[dict[str, Any]]:
    """Load a YAML file into a list of dicts; optionally unwrap a top-level key."""
    import yaml

    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and key and key in data:
        data = data[key]
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                return value
        return [data]
    return data or []


# schema name -> (relative path, loader kind, optional yaml key)
DATASETS: dict[str, tuple[str, str, str | None]] = {
    "sector": ("data/sectors/sectors.yaml", "yaml", "sectors"),
    "prospect": ("data/prospects/prospects.jsonl", "jsonl", None),
    "suppression": ("data/prospects/suppression_list.jsonl", "jsonl", None),
    "outreach_draft": ("data/outreach/drafts.jsonl", "jsonl", None),
    "email_account": ("data/outreach/email_accounts.jsonl", "jsonl", None),
    "approval_action": ("data/outreach/approval_actions.jsonl", "jsonl", None),
    "sending_batch": ("data/outreach/sending_batches.jsonl", "jsonl", None),
    "reply": ("data/outreach/replies.jsonl", "jsonl", None),
    "job_signal": ("data/signals/job_signals.jsonl", "jsonl", None),
    "partner": ("data/partners/partners.jsonl", "jsonl", None),
    "content_idea": ("data/content/post_ideas.jsonl", "jsonl", None),
}


def load_dataset(name: str) -> list[dict[str, Any]]:
    """Load the seed records for a dataset name."""
    rel, kind, key = DATASETS[name]
    path = REPO_ROOT / rel
    if kind == "yaml":
        return load_yaml_list(path, key)
    return load_jsonl(path)


def validate_dataset(name: str) -> list[str]:
    """Validate every seed record in a dataset against its schema."""
    schema = load_schema(name)
    records = load_dataset(name)
    errors: list[str] = []
    for idx, record in enumerate(records):
        for err in validate_record(record, schema):
            errors.append(f"{name}[{idx}]: {err}")
    return errors


def validate_all() -> dict[str, list[str]]:
    """Validate all datasets; returns {dataset: [errors]} (empty lists = clean)."""
    return {name: validate_dataset(name) for name in DATASETS}


def summary() -> dict[str, Any]:
    """A compact status summary for the verify script / control room."""
    results = validate_all()
    total_errors = sum(len(v) for v in results.values())
    return {
        "schemas": sorted(DATASETS.keys()),
        "drafts_per_day": DRAFTS_PER_DAY,
        "draft_mix_total": draft_mix_total(),
        "ramp_caps": dict(RAMP_CAPS),
        "datasets": {name: len(load_dataset(name)) for name in DATASETS},
        "validation_errors": total_errors,
        "errors_by_dataset": {k: v for k, v in results.items() if v},
        "ok": total_errors == 0 and draft_mix_total() == DRAFTS_PER_DAY,
    }
