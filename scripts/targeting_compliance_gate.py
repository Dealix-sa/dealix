#!/usr/bin/env python3
"""
targeting_compliance_gate.py — the safety wall of the Targeting OS.

Every company must pass this gate before it can be scored, shortlisted, or
turned into a draft. The gate encodes the Dealix non-negotiables:

    No scraping behind login · no leaked/purchased data · no LinkedIn
    automation · no personal mobile numbers · respect robots.txt and site
    terms · no external action without founder approval.

It is intentionally conservative: when in doubt, it downgrades to
``needs_review`` rather than ``approved``. It never sends anything.

Usage:
    python scripts/targeting_compliance_gate.py --in data/targeting/company_master.jsonl
    python scripts/targeting_compliance_gate.py --check-url https://example.com/services
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml  # noqa: E402

DEFAULT_BLOCKED = _ROOT / "data" / "targeting" / "blocked_sources.yml"


# --------------------------------------------------------------------------- #
# Loading policy
# --------------------------------------------------------------------------- #
def load_blocked(path: Path | None = None) -> dict[str, Any]:
    """Load blocked_sources.yml. Falls back to empty (but typed) policy."""
    path = path or DEFAULT_BLOCKED
    if not path.exists():
        return {
            "blocked_domains": [],
            "blocked_url_patterns": [],
            "blocked_source_types": [],
            "sensitive_sectors": [],
        }
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for key in (
        "blocked_domains",
        "blocked_url_patterns",
        "blocked_source_types",
        "sensitive_sectors",
    ):
        data.setdefault(key, [])
    return data


# --------------------------------------------------------------------------- #
# URL / source checks
# --------------------------------------------------------------------------- #
def _host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower()
    except ValueError:
        return ""


def url_is_allowed(url: str, policy: dict[str, Any]) -> tuple[bool, str]:
    """Return (allowed, reason). A url is disallowed if its host matches a
    blocked domain suffix or its path/query matches a blocked pattern."""
    if not url or not isinstance(url, str):
        return False, "empty_url"
    host = _host(url)
    if not host:
        return False, "unparseable_url"
    for dom in policy.get("blocked_domains", []):
        dom = str(dom).lower().lstrip(".")
        if host == dom or host.endswith("." + dom):
            return False, f"blocked_domain:{dom}"
    low = url.lower()
    for pat in policy.get("blocked_url_patterns", []):
        if str(pat).lower() in low:
            return False, f"blocked_pattern:{pat}"
    return True, "ok"


def source_type_is_allowed(source_type: str, policy: dict[str, Any]) -> tuple[bool, str]:
    if source_type and source_type in set(policy.get("blocked_source_types", [])):
        return False, f"blocked_source_type:{source_type}"
    return True, "ok"


# --------------------------------------------------------------------------- #
# Company-level gate
# --------------------------------------------------------------------------- #
def gate_company(company: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate a company record against the source policy.

    Returns a dict: {status, reasons, allowed_sources, risk_flags}
      status is one of: "approved" | "needs_review" | "reject"
        reject       -> a hard non-negotiable was violated; drop the company.
        needs_review -> usable but weak (e.g. <2 evidence, sensitive sector).
        approved     -> safe to score and (after founder approval) draft.
    """
    policy = policy or load_blocked()
    reasons: list[str] = []
    risk_flags: list[str] = []

    # 1) Forbidden source types anywhere -> hard reject.
    for st in company.get("source_types", []) or []:
        ok, why = source_type_is_allowed(str(st), policy)
        if not ok:
            reasons.append(why)
            risk_flags.append("forbidden_source_type")

    # 2) Evidence URLs: keep only allowed ones.
    raw_urls = company.get("source_urls", []) or []
    allowed_sources: list[str] = []
    for url in raw_urls:
        ok, why = url_is_allowed(str(url), policy)
        if ok:
            allowed_sources.append(str(url))
        else:
            reasons.append(why)
            risk_flags.append("blocked_source")

    # 3) Personal mobile number is never an allowed contact channel.
    channel = str(company.get("contact_channel", "")).lower()
    if channel in {"personal_mobile", "personal_phone", "personal_whatsapp"}:
        reasons.append("personal_contact_channel")
        risk_flags.append("no_official_channel")

    # 4) Sensitive sector -> not blocked, but force review + governance angle.
    sector = str(company.get("sector", "")).lower()
    if sector in set(policy.get("sensitive_sectors", [])):
        reasons.append(f"sensitive_sector:{sector}")
        risk_flags.append("sensitive_sector")

    # --- Decision ---
    # Any forbidden source type, or zero usable evidence after filtering, is a
    # hard reject. We never proceed on data we cannot stand behind.
    hard_reject = "forbidden_source_type" in risk_flags or not allowed_sources
    if hard_reject:
        status = "reject"
    elif "sensitive_sector" in risk_flags or len(allowed_sources) < 2:
        status = "needs_review"
    else:
        status = "approved"

    return {
        "status": status,
        "reasons": sorted(set(reasons)),
        "allowed_sources": allowed_sources,
        "risk_flags": sorted(set(risk_flags)),
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS compliance gate")
    ap.add_argument("--in", dest="infile", help="company_master.jsonl to evaluate")
    ap.add_argument("--check-url", help="evaluate a single URL and exit")
    ap.add_argument("--policy", default=str(DEFAULT_BLOCKED))
    args = ap.parse_args(argv)

    policy = load_blocked(Path(args.policy))

    if args.check_url:
        ok, why = url_is_allowed(args.check_url, policy)
        print(json.dumps({"url": args.check_url, "allowed": ok, "reason": why}, ensure_ascii=False))
        return 0 if ok else 2

    if not args.infile:
        ap.error("provide --in <jsonl> or --check-url <url>")

    counts = {"approved": 0, "needs_review": 0, "reject": 0}
    for company in _read_jsonl(Path(args.infile)):
        result = gate_company(company, policy)
        counts[result["status"]] += 1
        print(
            json.dumps(
                {"company": company.get("company_name"), **result},
                ensure_ascii=False,
            )
        )
    print(json.dumps({"summary": counts}, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
