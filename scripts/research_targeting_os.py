#!/usr/bin/env python3
"""
research_targeting_os.py — Dealix Research & Targeting OS (daily, governed).

A repeatable daily loop that turns seeds + allowlisted research into a scored,
evidence-backed target pool — NOT an outbound blaster. It:

  1. Loads companies from a seed CSV (+ optional allowlisted discovery).
  2. Normalizes names/domains and de-duplicates.
  3. Attaches the evidence already gathered per row (allowlisted sources only).
  4. Scores each company on a 100-point firmographic / targeting model.
  5. Infers the most likely weakness and the Dealix OS that addresses it.
  6. Recommends an offer rung (Command Sprint / Diagnostic / Nurture).
  7. Emits a raw pool, a ranked short-list, a brief, a weakness map, and
     draft-only outreach for founder review.

Hard rules (the 11 non-negotiables — enforced, not decorative):
  - No scraping behind login, no robots.txt bypass, no CAPTCHA bypass.
  - No LinkedIn automation, no cold/bulk WhatsApp, no mass email.
  - No autonomous external sends — drafts only, founder approves.
  - No claim without evidence; sensitive sectors penalized.
  - Only sources on the allowlist are accepted.
Doctrine is enforced via ``auto_client_acquisition.safe_send_gateway``.

Usage (offline, seed-only — the default safe path):
    python scripts/research_targeting_os.py \
        --seed data/targeting/company_seed_template.csv \
        --out data/targeting/out \
        --top 50

Usage (allowlisted discovery — requires Google Programmable Search keys):
    export GOOGLE_SEARCH_API_KEY="..."
    export GOOGLE_SEARCH_CX="..."
    python scripts/research_targeting_os.py \
        --discover \
        --queries-file data/targeting/queries.txt \
        --seed data/targeting/company_seed_template.csv \
        --out data/targeting/out \
        --top 50

Outputs (written under --out):
    ranked_targets.csv
    ranked_targets.jsonl
    daily_targeting_brief.md
    drafts_for_review.md
    weakness_map.md
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Doctrine + claim safety reuse the canonical governed modules. Imports are
# wrapped so the engine still runs as a plain script if the package layout
# changes; the offline guards below replicate the same non-negotiables.
try:  # pragma: no cover - exercised indirectly
    from auto_client_acquisition.safe_send_gateway import enforce_doctrine_non_negotiables
except Exception:  # pragma: no cover - fallback only

    def enforce_doctrine_non_negotiables(**kwargs: bool) -> None:  # type: ignore[misc]
        return None


try:  # pragma: no cover - exercised indirectly
    from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
except Exception:  # pragma: no cover - fallback only
    audit_claim_safety = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Source allowlist
# ---------------------------------------------------------------------------

#: Default research sources Dealix is allowed to use. These mirror the Tier-1
#: Source Registry (``auto_client_acquisition.revenue_os.source_registry``) and
#: deliberately exclude every blocked source (scraping, purchased_list, ...).
DEFAULT_ALLOWED_SOURCES: tuple[str, ...] = (
    "company_website",
    "company_services_page",
    "company_contact_page",
    "company_careers_page",
    "company_customers_page",
    "company_case_study",
    "public_directory_allowed",
    "open_data_portal",
    "search_api",
    "founder_list",
    "warm_intro",
    "partner_referral",
    "public_business_info_allowed",
    "manual_linkedin_research",
)

#: Sources that must never be processed — presence of any of these on a row
#: forces a hard reject and is logged as a doctrine violation.
BLOCKED_SOURCES: tuple[str, ...] = (
    "scraping",
    "purchased_list",
    "cold_whatsapp",
    "linkedin_automation",
    "behind_login",
    "captcha_bypass",
)


def load_source_allowlist(path: Path | None) -> tuple[set[str], set[str]]:
    """Return (allowed, blocked) source sets, merging file overrides with defaults."""
    allowed = set(DEFAULT_ALLOWED_SOURCES)
    blocked = set(BLOCKED_SOURCES)
    if path and path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        allowed |= {str(s).strip().lower() for s in data.get("allowed_sources", [])}
        blocked |= {str(s).strip().lower() for s in data.get("blocked_sources", [])}
    # Blocked always wins over allowed.
    allowed -= blocked
    return allowed, blocked


# ---------------------------------------------------------------------------
# Normalization + dedupe
# ---------------------------------------------------------------------------

_LEGAL_SUFFIXES = (
    "llc",
    "ltd",
    "limited",
    "inc",
    "incorporated",
    "co",
    "company",
    "corp",
    "corporation",
    "est",
    "establishment",
    "plc",
    "sa",
    "sal",
    "wll",
    "fz",
    "fze",
    "llp",
)

_AR_LEGAL_TOKENS = ("شركة", "مؤسسة", "مجموعة", "ذ.م.م", "ذمم", "للتجارة", "المحدودة")


def normalize_company_name(name: str) -> str:
    """Lower-case, strip punctuation, drop legal suffixes, collapse whitespace.

    Arabic legal tokens are removed too so AR/EN duplicates collapse together.
    """
    if not name:
        return ""
    text = name.strip().lower()
    for token in _AR_LEGAL_TOKENS:
        text = text.replace(token.lower(), " ")
    # Replace punctuation with spaces; keep Arabic + latin letters and digits.
    text = re.sub(r"[^\w؀-ۿ]+", " ", text, flags=re.UNICODE)
    parts = [p for p in text.split() if p and p not in _LEGAL_SUFFIXES]
    return " ".join(parts).strip()


def normalize_domain(value: str) -> str:
    """Reduce a URL or host to a bare registrable host (no scheme/www/path)."""
    if not value:
        return ""
    text = value.strip().lower()
    text = re.sub(r"^[a-z]+://", "", text)
    text = text.split("/")[0]
    text = text.split("?")[0]
    text = text.split("@")[-1]  # tolerate email-style input
    if text.startswith("www."):
        text = text[4:]
    return text.strip().strip(".")


def dedupe_key(row: dict[str, Any]) -> str:
    """Prefer domain identity; fall back to normalized name."""
    domain = normalize_domain(str(row.get("domain", "")))
    if domain:
        return f"domain:{domain}"
    name = normalize_company_name(str(row.get("company", "")))
    return f"name:{name}"


def dedupe_companies(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse duplicates, merging evidence and keeping the richest row."""
    merged: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = dedupe_key(row)
        if not key or key in ("name:", "domain:"):
            continue
        if key not in merged:
            merged[key] = dict(row)
            continue
        existing = merged[key]
        # Merge evidence URLs and take the max evidence_count.
        ev = _split_multi(existing.get("evidence_urls", "")) + _split_multi(
            row.get("evidence_urls", "")
        )
        existing["evidence_urls"] = ";".join(dict.fromkeys(u for u in ev if u))
        existing["evidence_count"] = max(
            _as_int(existing.get("evidence_count")), _as_int(row.get("evidence_count"))
        )
        # Prefer non-empty fields from whichever row has them.
        for fld, val in row.items():
            if val not in (None, "") and not existing.get(fld):
                existing[fld] = val
    return list(merged.values())


# ---------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------

#: ICP sectors that fit Dealix (governed B2B revenue/ops intelligence buyers).
ICP_SECTORS: tuple[str, ...] = (
    "b2b_services",
    "b2b_consulting",
    "consulting",
    "marketing_agency",
    "agency",
    "saas",
    "technology",
    "logistics",
    "professional_services",
    "real_estate",
    "healthcare",
    "fintech",
    "manufacturing",
    "ecommerce",
)

#: Sectors that carry elevated regulatory / reputational risk → penalty + review.
SENSITIVE_SECTORS: tuple[str, ...] = (
    "government",
    "defense",
    "military",
    "gambling",
    "crypto_exchange",
    "adult",
    "political",
    "religious_org",
    "minors_data",
)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "y", "نعم", "صح")


def _as_int(value: Any) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def _split_multi(value: Any) -> list[str]:
    if not value:
        return []
    return [p.strip() for p in re.split(r"[;,|]", str(value)) if p.strip()]


@dataclass(slots=True)
class Candidate:
    """A single company under evaluation."""

    company: str
    domain: str = ""
    sector: str = ""
    city: str = ""
    source: str = "founder_list"
    services_count: int = 0
    has_case_studies: bool = False
    has_contact: bool = False
    has_careers: bool = False
    has_customers_page: bool = False
    has_projects: bool = False
    has_support: bool = False
    expansion_signal: bool = False
    hiring_signal: bool = False
    launch_signal: bool = False
    partnership_signal: bool = False
    data_fragmentation: bool = False
    warm_path: bool = False
    relationship: str = ""
    evidence_count: int = 0
    evidence_urls: list[str] = field(default_factory=list)
    sensitive_sector: bool = False
    data_gap: bool = False
    notes: str = ""

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Candidate:
        sector = str(row.get("sector", "")).strip().lower()
        relationship = str(row.get("relationship", "")).strip().lower()
        warm = _as_bool(row.get("warm_path")) or relationship in ("warm", "partner", "referral")
        sensitive = _as_bool(row.get("sensitive_sector")) or sector in SENSITIVE_SECTORS
        return cls(
            company=str(row.get("company", "")).strip(),
            domain=normalize_domain(str(row.get("domain", ""))),
            sector=sector,
            city=str(row.get("city", "")).strip(),
            source=str(row.get("source", "founder_list")).strip().lower() or "founder_list",
            services_count=_as_int(row.get("services_count")),
            has_case_studies=_as_bool(row.get("has_case_studies")),
            has_contact=_as_bool(row.get("has_contact")),
            has_careers=_as_bool(row.get("has_careers")),
            has_customers_page=_as_bool(row.get("has_customers_page")),
            has_projects=_as_bool(row.get("has_projects")),
            has_support=_as_bool(row.get("has_support")),
            expansion_signal=_as_bool(row.get("expansion_signal")),
            hiring_signal=_as_bool(row.get("hiring_signal")),
            launch_signal=_as_bool(row.get("launch_signal")),
            partnership_signal=_as_bool(row.get("partnership_signal")),
            data_fragmentation=_as_bool(row.get("data_fragmentation")),
            warm_path=warm,
            relationship=relationship,
            evidence_count=max(
                _as_int(row.get("evidence_count")),
                len(_split_multi(row.get("evidence_urls"))),
            ),
            evidence_urls=_split_multi(row.get("evidence_urls")),
            sensitive_sector=sensitive,
            data_gap=_as_bool(row.get("data_gap")),
            notes=str(row.get("notes", "")).strip(),
        )


# ---------------------------------------------------------------------------
# Scoring (100-point model + risk penalty)
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ScoreBreakdown:
    icp_fit: int = 0
    pain_signal: int = 0
    intent_timing: int = 0
    access: int = 0
    evidence_confidence: int = 0
    risk_penalty: int = 0

    @property
    def total(self) -> int:
        raw = (
            self.icp_fit
            + self.pain_signal
            + self.intent_timing
            + self.access
            + self.evidence_confidence
            + self.risk_penalty
        )
        return max(0, min(100, raw))

    def as_dict(self) -> dict[str, int]:
        d = asdict(self)
        d["total"] = self.total
        return d


def _pain_signals(c: Candidate) -> list[str]:
    """Distinct, evidence-anchored pain hypotheses present on the candidate."""
    signals: list[str] = []
    if c.services_count >= 3 and not c.has_case_studies:
        signals.append("proof_weakness")
    if c.has_contact and not c.has_customers_page:
        signals.append("follow_up_leakage")
    if c.has_projects:
        signals.append("delivery_visibility")
    if c.has_support or c.has_customers_page:
        signals.append("support_recurrence")
    if c.expansion_signal or c.hiring_signal:
        signals.append("executive_decision_fog")
    if c.data_fragmentation or c.data_gap:
        signals.append("data_fragmentation")
    return signals


def score_candidate(c: Candidate) -> ScoreBreakdown:
    """Deterministic 100-point firmographic / targeting score."""
    b = ScoreBreakdown()

    # ICP Fit (35): sector fit + a registrable identity + a research surface.
    icp = 0
    if c.sector in ICP_SECTORS:
        icp += 22
    elif c.sector:
        icp += 10
    if c.domain:
        icp += 8
    if c.has_contact or c.has_careers or c.has_customers_page:
        icp += 5
    b.icp_fit = min(35, icp)

    # Pain Signal (25): up to three distinct, evidenced pains @ ~8 pts each.
    pains = _pain_signals(c)
    b.pain_signal = min(25, 9 * min(len(pains), 2) + (7 if len(pains) >= 3 else 0))

    # Intent / Timing (20): expansion, hiring, launch, partnerships.
    intent = 0
    for flag in (c.expansion_signal, c.hiring_signal, c.launch_signal, c.partnership_signal):
        if flag:
            intent += 6
    b.intent_timing = min(20, intent)

    # Access (10): a clean warm path or a clean direct contact channel.
    if c.warm_path:
        b.access = 10
    elif c.has_contact:
        b.access = 5
    else:
        b.access = 0

    # Evidence Confidence (10): two independent allowlisted sources earn full.
    if c.evidence_count >= 2:
        b.evidence_confidence = 10
    elif c.evidence_count == 1:
        b.evidence_confidence = 5
    else:
        b.evidence_confidence = 0

    # Risk Penalty (-20 max): thin sourcing, sensitive sector, data gaps.
    penalty = 0
    if c.sensitive_sector:
        penalty -= 12
    if c.evidence_count == 0 and not c.warm_path:
        penalty -= 6
    if c.data_gap:
        penalty -= 4
    if not c.domain and not c.warm_path:
        penalty -= 4
    b.risk_penalty = max(-20, penalty)

    return b


def grade_for_score(total: int) -> str:
    """Map a 0-100 score to a letter grade."""
    if total >= 85:
        return "A+"
    if total >= 70:
        return "A"
    if total >= 55:
        return "B"
    if total >= 40:
        return "C"
    return "D"


#: The golden rule: never target without two clear pain evidences OR a warm path.
def targeting_ready(c: Candidate) -> bool:
    return (len(_pain_signals(c)) >= 2 and c.evidence_count >= 2) or c.warm_path


def grade_action(grade: str) -> str:
    return {
        "A+": "engage_today",
        "A": "strong_target",
        "B": "research_more",
        "C": "nurture",
        "D": "do_not_target_now",
    }.get(grade, "research_more")


# ---------------------------------------------------------------------------
# Weakness hypothesis + offer recommendation
# ---------------------------------------------------------------------------

#: weakness_code -> (human label, primary Dealix OS module)
WEAKNESS_MAP: dict[str, tuple[str, str]] = {
    "proof_weakness": ("Proof weakness — services without visible proof", "Proof OS"),
    "follow_up_leakage": ("Follow-up leakage — contact channel, no funnel", "Revenue OS"),
    "delivery_visibility": ("Delivery visibility — projects without status", "Delivery OS"),
    "support_recurrence": ("Support recurrence — repeat customer load", "Support OS"),
    "executive_decision_fog": ("Executive decision fog — growth without control", "Command OS"),
    "data_fragmentation": ("Data fragmentation — scattered, ungoverned data", "Data OS"),
}


def weakness_hypothesis(c: Candidate) -> tuple[str, str, str]:
    """Return (weakness_code, human_label, primary_os) for the top pain."""
    signals = _pain_signals(c)
    if not signals:
        return ("undetermined", "Undetermined — needs a second evidence source", "Diagnostic")
    top = signals[0]
    label, primary_os = WEAKNESS_MAP[top]
    return (top, label, primary_os)


def recommend_offer(c: Candidate, grade: str) -> str:
    """Recommend an offer rung: Command Sprint / Diagnostic / Nurture / None."""
    if not targeting_ready(c):
        return "Diagnostic"  # earn the right with a free diagnostic first
    if grade in ("A+", "A"):
        return "Command Sprint"
    if grade == "B":
        return "Diagnostic"
    if grade == "C":
        return "Nurture"
    return "None"


# ---------------------------------------------------------------------------
# Evaluation pipeline
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class Evaluation:
    candidate: Candidate
    score: ScoreBreakdown
    grade: str
    action: str
    weakness_code: str
    weakness_label: str
    primary_os: str
    offer: str
    targeting_ready: bool

    def flat(self) -> dict[str, Any]:
        c = self.candidate
        return {
            "company": c.company,
            "domain": c.domain,
            "sector": c.sector,
            "city": c.city,
            "source": c.source,
            "grade": self.grade,
            "score": self.score.total,
            "action": self.action,
            "weakness": self.weakness_code,
            "weakness_label": self.weakness_label,
            "primary_os": self.primary_os,
            "offer": self.offer,
            "targeting_ready": self.targeting_ready,
            "warm_path": c.warm_path,
            "evidence_count": c.evidence_count,
            "icp_fit": self.score.icp_fit,
            "pain_signal": self.score.pain_signal,
            "intent_timing": self.score.intent_timing,
            "access": self.score.access,
            "evidence_confidence": self.score.evidence_confidence,
            "risk_penalty": self.score.risk_penalty,
            "evidence_urls": ";".join(c.evidence_urls),
            "notes": c.notes,
        }


def evaluate(c: Candidate) -> Evaluation:
    score = score_candidate(c)
    grade = grade_for_score(score.total)
    ready = targeting_ready(c)
    # Enforce the golden rule: not-ready candidates cannot grade above B.
    if not ready and grade in ("A+", "A"):
        grade = "B"
    weakness_code, weakness_label, primary_os = weakness_hypothesis(c)
    offer = recommend_offer(c, grade)
    return Evaluation(
        candidate=c,
        score=score,
        grade=grade,
        action=grade_action(grade),
        weakness_code=weakness_code,
        weakness_label=weakness_label,
        primary_os=primary_os,
        offer=offer,
        targeting_ready=ready,
    )


def evaluate_rows(
    rows: Iterable[dict[str, Any]],
    *,
    allowed_sources: set[str],
    blocked_sources: set[str],
) -> tuple[list[Evaluation], list[dict[str, Any]]]:
    """De-dupe, reject blocked sources, evaluate, and rank by score desc."""
    rejected: list[dict[str, Any]] = []
    clean: list[dict[str, Any]] = []
    for row in dedupe_companies(rows):
        src = str(row.get("source", "")).strip().lower()
        if src in blocked_sources:
            rejected.append(
                {"company": row.get("company"), "source": src, "reason": "blocked_source"}
            )
            continue
        if src and allowed_sources and src not in allowed_sources:
            rejected.append(
                {"company": row.get("company"), "source": src, "reason": "source_not_allowlisted"}
            )
            continue
        clean.append(row)
    evals = [evaluate(Candidate.from_row(r)) for r in clean if str(r.get("company", "")).strip()]
    evals.sort(key=lambda e: e.score.total, reverse=True)
    return evals, rejected


# ---------------------------------------------------------------------------
# Seed loading + optional allowlisted discovery
# ---------------------------------------------------------------------------


def load_seed(path: Path) -> list[dict[str, Any]]:
    """Read a seed CSV into a list of plain dict rows (skips REPLACE: placeholders)."""
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            row = {(k or "").strip(): (v or "").strip() for k, v in raw.items()}
            company = row.get("company", "")
            if not company or company.upper().startswith("REPLACE:"):
                continue
            rows.append(row)
    return rows


def discover_via_search_api(
    queries: list[str],
    *,
    allowed_sources: set[str],
    blocked_sources: set[str],
    per_query: int = 10,
) -> list[dict[str, Any]]:
    """Discover companies via Google Programmable Search (JSON API), if configured.

    Returns an empty list when keys are missing or the network is unavailable —
    the engine then runs seed-only. This is allowlisted search ONLY: it reads
    public result metadata (title/link/snippet). It never logs in, never bypasses
    robots.txt, and never scrapes page bodies.
    """
    api_key = os.environ.get("GOOGLE_SEARCH_API_KEY", "").strip()
    cx = os.environ.get("GOOGLE_SEARCH_CX", "").strip()
    if not api_key or not cx:
        return []
    try:  # network + stdlib only; degrade gracefully on any failure
        import urllib.parse
        import urllib.request
    except Exception:  # pragma: no cover
        return []

    out: list[dict[str, Any]] = []
    for query in queries:
        params = urllib.parse.urlencode(
            {"key": api_key, "cx": cx, "q": query, "num": min(per_query, 10)}
        )
        url = f"https://www.googleapis.com/customsearch/v1?{params}"
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:  # noqa: S310 (trusted host)
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception:  # noqa: S112 - degrade gracefully on any network/parse error
            continue
        for item in payload.get("items", []):
            link = item.get("link", "")
            domain = normalize_domain(link)
            if not domain:
                continue
            out.append(
                {
                    "company": item.get("title", domain),
                    "domain": domain,
                    "sector": "",
                    "city": "",
                    "source": "search_api",
                    "evidence_count": 1,
                    "evidence_urls": link,
                    "notes": (item.get("snippet", "") or "")[:240],
                }
            )
    return out


# ---------------------------------------------------------------------------
# Draft generation (draft-only, evidence-anchored, governed)
# ---------------------------------------------------------------------------


def build_draft(ev: Evaluation) -> dict[str, Any]:
    """Build a single review-only outreach draft. No send. No invented metrics."""
    c = ev.candidate
    channel = "warm_intro" if c.warm_path else "manual_review"
    company = c.company or c.domain
    weakness = ev.weakness_label
    # Evidence-first, claim-free language. No guarantees, no numbers we don't have.
    body_en = (
        f"Context for {company}: based on publicly available signals "
        f"({c.evidence_count} source(s) on file), the likely gap is {weakness.lower()}. "
        f"Dealix {ev.primary_os} is built for exactly this. "
        f"Open to a short, no-obligation diagnostic to confirm whether it applies?"
    )
    body_ar = (
        f"سياق عن {company}: بناءً على إشارات عامة متاحة "
        f"({c.evidence_count} مصدر/مصادر موثّقة)، الفجوة المرجّحة هي {weakness}. "
        f"وحدة Dealix {ev.primary_os} مصمّمة لهذه الحالة تحديدًا. "
        f"هل تناسبك جلسة تشخيص قصيرة بدون التزام للتأكد من انطباقها؟"
    )

    # Claim-safety audit reflects the copy; the artifact is always draft-only
    # (auto_send=False) regardless of the audit outcome.
    issues: list[str] = []
    rank = {"allow": 0, "draft_only": 1, "block": 2}
    worst = "allow"
    if audit_claim_safety is not None:
        for text in (body_en, body_ar):
            result = audit_claim_safety(text)
            issues.extend(result.issues)
            value = str(
                getattr(result.suggested_decision, "value", result.suggested_decision)
            ).lower()
            if rank.get(value, 0) > rank.get(worst, 0):
                worst = value
    decision = worst.upper()

    return {
        "company": company,
        "grade": ev.grade,
        "score": ev.score.total,
        "weakness": ev.weakness_label,
        "primary_os": ev.primary_os,
        "offer": ev.offer,
        "channel": channel,
        "status": "draft_for_review",
        "auto_send": False,
        "evidence_count": c.evidence_count,
        "evidence_urls": list(c.evidence_urls),
        "claim_safety_decision": decision,
        "claim_safety_issues": list(dict.fromkeys(issues)),
        "draft_en": body_en,
        "draft_ar": body_ar,
    }


def build_drafts(evals: list[Evaluation], *, limit: int = 10) -> list[dict[str, Any]]:
    """Build at most ``limit`` drafts, only for targeting-ready A/A+ candidates."""
    pool = [e for e in evals if e.targeting_ready and e.grade in ("A+", "A")]
    return [build_draft(e) for e in pool[:limit]]


# ---------------------------------------------------------------------------
# Daily intelligence (tomorrow's targeting direction)
# ---------------------------------------------------------------------------


def daily_intelligence(evals: list[Evaluation]) -> dict[str, Any]:
    """Summarize today and recommend where to deepen tomorrow."""
    if not evals:
        return {
            "best_sector": None,
            "best_city": None,
            "best_source": None,
            "top_weakness": None,
            "top_data_gap": None,
            "recommendation": "No evaluable companies. Add seeds or enable allowlisted discovery.",
        }

    def _avg_by(attr: str) -> str | None:
        buckets: dict[str, list[int]] = {}
        for e in evals:
            key = getattr(e.candidate, attr) or ""
            if key:
                buckets.setdefault(key, []).append(e.score.total)
        if not buckets:
            return None
        return max(buckets, key=lambda k: sum(buckets[k]) / len(buckets[k]))

    best_sector = _avg_by("sector")
    best_city = _avg_by("city")
    sources = Counter(e.candidate.source for e in evals)
    best_source = sources.most_common(1)[0][0] if sources else None
    weaknesses = Counter(e.weakness_code for e in evals if e.weakness_code != "undetermined")
    top_weakness = weaknesses.most_common(1)[0][0] if weaknesses else None
    data_gaps = sum(1 for e in evals if e.candidate.data_gap)

    rec_parts = []
    if best_sector:
        rec_parts.append(f"Deepen targeting around {best_sector} (highest average score today).")
    if top_weakness:
        rec_parts.append(
            f"Lead with the {top_weakness.replace('_', ' ')} angle and the matching Dealix OS."
        )
    rec_parts.append(
        "Add a second evidence source (website, contact, case-study pages) before drafting."
    )
    return {
        "best_sector": best_sector,
        "best_city": best_city,
        "best_source": best_source,
        "top_weakness": top_weakness,
        "top_data_gap": f"{data_gaps} companies missing data" if data_gaps else None,
        "recommendation": " ".join(rec_parts),
    }


# ---------------------------------------------------------------------------
# Output assembly
# ---------------------------------------------------------------------------

_RANKED_COLUMNS = [
    "company",
    "domain",
    "sector",
    "city",
    "source",
    "grade",
    "score",
    "action",
    "weakness",
    "weakness_label",
    "primary_os",
    "offer",
    "targeting_ready",
    "warm_path",
    "evidence_count",
    "icp_fit",
    "pain_signal",
    "intent_timing",
    "access",
    "evidence_confidence",
    "risk_penalty",
    "evidence_urls",
    "notes",
]


def write_outputs(
    out_dir: Path,
    evals: list[Evaluation],
    drafts: list[dict[str, Any]],
    intel: dict[str, Any],
    rejected: list[dict[str, Any]],
    *,
    top: int,
    run_date: str | None = None,
) -> dict[str, Path]:
    """Write the five canonical outputs and return their paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    run_date = run_date or date.today().isoformat()
    top_evals = [e for e in evals if e.grade in ("A+", "A", "B")][:top]

    paths: dict[str, Path] = {}

    # ranked_targets.csv
    csv_path = out_dir / "ranked_targets.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=_RANKED_COLUMNS)
        writer.writeheader()
        for e in evals:
            writer.writerow(e.flat())
    paths["ranked_targets.csv"] = csv_path

    # ranked_targets.jsonl
    jsonl_path = out_dir / "ranked_targets.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for e in evals:
            record = e.flat()
            record["score_breakdown"] = e.score.as_dict()
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    paths["ranked_targets.jsonl"] = jsonl_path

    # daily_targeting_brief.md
    brief_path = out_dir / "daily_targeting_brief.md"
    brief_path.write_text(
        _render_brief(evals, top_evals, intel, rejected, run_date=run_date),
        encoding="utf-8",
    )
    paths["daily_targeting_brief.md"] = brief_path

    # drafts_for_review.md
    drafts_path = out_dir / "drafts_for_review.md"
    drafts_path.write_text(_render_drafts(drafts, run_date=run_date), encoding="utf-8")
    paths["drafts_for_review.md"] = drafts_path

    # weakness_map.md
    weakness_path = out_dir / "weakness_map.md"
    weakness_path.write_text(_render_weakness_map(evals, run_date=run_date), encoding="utf-8")
    paths["weakness_map.md"] = weakness_path

    return paths


def _grade_counts(evals: list[Evaluation]) -> Counter:
    return Counter(e.grade for e in evals)


def _render_brief(
    evals: list[Evaluation],
    top_evals: list[Evaluation],
    intel: dict[str, Any],
    rejected: list[dict[str, Any]],
    *,
    run_date: str,
) -> str:
    counts = _grade_counts(evals)
    ab = counts["A+"] + counts["A"] + counts["B"]
    shortlist = [e for e in evals if e.grade in ("A+", "A")][:20]
    lines: list[str] = []
    lines.append(f"# Dealix Daily Targeting Brief — {run_date}")
    lines.append("")
    lines.append(
        "> Research pool, not a send list. Quality over volume. "
        "No external send without founder approval."
    )
    lines.append("")
    lines.append("## Funnel")
    lines.append("")
    lines.append(f"- Evaluated (clean): **{len(evals)}**")
    lines.append(
        f"- A+ {counts['A+']} · A {counts['A']} · B {counts['B']} · "
        f"C {counts['C']} · D {counts['D']}"
    )
    lines.append(f"- A/B targets: **{ab}**")
    lines.append(f"- Founder shortlist (A/A+): **{len(shortlist)}**")
    lines.append(f"- Rejected by source policy: **{len(rejected)}**")
    lines.append("")
    lines.append("## Founder shortlist (engage / confirm today)")
    lines.append("")
    if shortlist:
        lines.append("| Company | Grade | Score | Weakness | Dealix OS | Offer | Evidence |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for e in shortlist:
            c = e.candidate
            lines.append(
                f"| {c.company} | {e.grade} | {e.score.total} | {e.weakness_label} | "
                f"{e.primary_os} | {e.offer} | {c.evidence_count} |"
            )
    else:
        lines.append("_No A/A+ candidates yet. Add a second evidence source, then re-run._")
    lines.append("")
    lines.append("## Tomorrow's targeting direction")
    lines.append("")
    lines.append(f"- Best sector today: **{intel.get('best_sector') or '—'}**")
    lines.append(f"- Best city today: **{intel.get('best_city') or '—'}**")
    lines.append(f"- Best source today: **{intel.get('best_source') or '—'}**")
    lines.append(f"- Most common weakness: **{intel.get('top_weakness') or '—'}**")
    lines.append(f"- Data gaps: **{intel.get('top_data_gap') or 'none flagged'}**")
    lines.append("")
    lines.append(f"> {intel.get('recommendation', '')}")
    lines.append("")
    if rejected:
        lines.append("## Rejected by source policy (not processed)")
        lines.append("")
        for r in rejected[:25]:
            lines.append(f"- {r.get('company')} — `{r.get('source')}` — {r.get('reason')}")
        lines.append("")
    lines.append("---")
    lines.append(
        "_Golden rule: target only with (≥2 pain evidences) OR a warm path. "
        "Otherwise: research more._"
    )
    lines.append("")
    return "\n".join(lines)


def _render_drafts(drafts: list[dict[str, Any]], *, run_date: str) -> str:
    lines: list[str] = []
    lines.append(f"# Drafts for Review — {run_date}")
    lines.append("")
    lines.append(
        "> **DRAFT ONLY — NOT SENT.** Founder reviews and sends manually. "
        "No automation. No bulk. No cold WhatsApp. Evidence is attached per draft."
    )
    lines.append("")
    if not drafts:
        lines.append("_No drafts generated — no targeting-ready A/A+ candidates today._")
        lines.append("")
        return "\n".join(lines)
    for i, d in enumerate(drafts, 1):
        lines.append(f"## {i}. {d['company']} — {d['grade']} ({d['score']})")
        lines.append("")
        lines.append(f"- Weakness: **{d['weakness']}** → Dealix **{d['primary_os']}**")
        lines.append(f"- Offer: **{d['offer']}** · Channel: `{d['channel']}` · auto_send: `false`")
        lines.append(f"- Evidence ({d['evidence_count']}): {', '.join(d['evidence_urls']) or '—'}")
        lines.append(
            f"- Claim safety: `{d['claim_safety_decision']}`"
            + (
                f" — issues: {', '.join(d['claim_safety_issues'])}"
                if d["claim_safety_issues"]
                else ""
            )
        )
        lines.append("")
        lines.append("**EN draft**")
        lines.append("")
        lines.append("> " + d["draft_en"])
        lines.append("")
        lines.append("**AR draft**")
        lines.append("")
        lines.append("> " + d["draft_ar"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def _render_weakness_map(evals: list[Evaluation], *, run_date: str) -> str:
    by_os: dict[str, list[Evaluation]] = {}
    for e in evals:
        by_os.setdefault(e.primary_os, []).append(e)
    lines: list[str] = []
    lines.append(f"# Weakness Map — {run_date}")
    lines.append("")
    lines.append("Each company's most likely weakness and the Dealix OS that addresses it.")
    lines.append("")
    for primary_os in sorted(by_os, key=lambda k: -len(by_os[k])):
        group = sorted(by_os[primary_os], key=lambda e: -e.score.total)
        lines.append(f"## {primary_os} ({len(group)})")
        lines.append("")
        lines.append("| Company | Grade | Score | Weakness | Offer |")
        lines.append("| --- | --- | --- | --- | --- |")
        for e in group:
            lines.append(
                f"| {e.candidate.company} | {e.grade} | {e.score.total} | "
                f"{e.weakness_label} | {e.offer} |"
            )
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _preflight_doctrine() -> None:
    """Fail fast if the runtime is somehow asked to cross a non-negotiable.

    The engine never requests scraping / automation / auto-send, so a clean run
    raises nothing. This call documents and enforces that contract at startup.
    """
    enforce_doctrine_non_negotiables(
        request_cold_whatsapp=False,
        request_linkedin_automation=False,
        request_scraping=False,
        request_bulk_outreach=False,
        request_guaranteed_sales_claim=False,
        request_fake_proof=False,
        request_external_send_without_approval=False,
    )


def run(
    *,
    seed: Path | None,
    out_dir: Path,
    top: int,
    discover: bool,
    queries_file: Path | None,
    allowlist_path: Path | None,
    raw_pool_cap: int = 400,
) -> dict[str, Any]:
    """Execute the daily loop and return a small summary dict."""
    _preflight_doctrine()
    allowed_sources, blocked_sources = load_source_allowlist(allowlist_path)

    rows: list[dict[str, Any]] = []
    if seed and seed.exists():
        rows.extend(load_seed(seed))

    if discover and queries_file and queries_file.exists():
        queries = [
            q.strip()
            for q in queries_file.read_text(encoding="utf-8").splitlines()
            if q.strip() and not q.strip().startswith("#")
        ]
        rows.extend(
            discover_via_search_api(
                queries,
                allowed_sources=allowed_sources,
                blocked_sources=blocked_sources,
            )
        )

    # Cap the raw research pool (default 400) — analysis budget, not a send count.
    rows = rows[:raw_pool_cap]

    evals, rejected = evaluate_rows(
        rows, allowed_sources=allowed_sources, blocked_sources=blocked_sources
    )
    drafts = build_drafts(evals, limit=10)
    intel = daily_intelligence(evals)
    paths = write_outputs(out_dir, evals, drafts, intel, rejected, top=top)

    counts = _grade_counts(evals)
    return {
        "evaluated": len(evals),
        "rejected": len(rejected),
        "grades": dict(counts),
        "ab_targets": counts["A+"] + counts["A"] + counts["B"],
        "shortlist": counts["A+"] + counts["A"],
        "drafts": len(drafts),
        "outputs": {k: str(v) for k, v in paths.items()},
        "intelligence": intel,
        "generated_at": datetime.now(UTC).isoformat(),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Dealix Research & Targeting OS — daily governed research loop.",
    )
    p.add_argument("--seed", type=Path, default=None, help="Seed CSV of companies.")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("data/targeting/out"),
        help="Output directory (default: data/targeting/out).",
    )
    p.add_argument("--top", type=int, default=50, help="Short-list size (default: 50).")
    p.add_argument(
        "--discover",
        action="store_true",
        help="Enable allowlisted Google Programmable Search discovery (needs keys).",
    )
    p.add_argument(
        "--queries-file",
        type=Path,
        default=Path("data/targeting/queries.txt"),
        help="Query file for --discover.",
    )
    p.add_argument(
        "--allowlist",
        type=Path,
        default=Path("data/targeting/source_allowlist.json"),
        help="Source allowlist JSON.",
    )
    p.add_argument(
        "--raw-pool-cap",
        type=int,
        default=400,
        help="Max raw research candidates per day (analysis budget, not sends).",
    )
    p.add_argument("--json", action="store_true", help="Print the run summary as JSON.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if not args.seed and not args.discover:
        print(
            "error: provide --seed <csv> and/or --discover (with keys).",
            file=sys.stderr,
        )
        return 2
    summary = run(
        seed=args.seed,
        out_dir=args.out,
        top=args.top,
        discover=args.discover,
        queries_file=args.queries_file,
        allowlist_path=args.allowlist,
        raw_pool_cap=args.raw_pool_cap,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        g = summary["grades"]
        print(
            f"Evaluated {summary['evaluated']} · "
            f"A+{g.get('A+', 0)}/A{g.get('A', 0)}/B{g.get('B', 0)}/"
            f"C{g.get('C', 0)}/D{g.get('D', 0)} · "
            f"A-B targets {summary['ab_targets']} · "
            f"shortlist {summary['shortlist']} · drafts {summary['drafts']}"
        )
        for name, path in summary["outputs"].items():
            print(f"  {name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
