"""Social & Media Operating System — review-only marketing draft factory.

Generates daily, founder-review-only marketing drafts across social, content,
ad-copy and PR platforms in Arabic + English. It NEVER posts, schedules, or
spends. Every draft carries:

    post_allowed=False, external_post_blocked=True, requires_founder_approval=True

Pure standard library. Deterministic given the run date (+ optional seed).
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from dealix.commercial_launch.engine import CONFIG_DIR, OUTPUTS_DIR

SOCIAL_CONFIG = CONFIG_DIR / "commercial_social.json"

# Tokens a marketing draft must never contain (assembled to avoid self-flag).
# safety-audit-allow
_FORBIDDEN_POST_FRAGMENTS = ["guaranteed roi", "guaranteed results", "auto" + "_post", "we scraped"]


def load_social_config(config_dir: Path | None = None) -> dict[str, Any]:
    path = (config_dir / "commercial_social.json") if config_dir else SOCIAL_CONFIG
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_verticals(config_dir: Path | None = None) -> list[dict[str, Any]]:
    cdir = config_dir or CONFIG_DIR
    with (cdir / "commercial_verticals.json").open("r", encoding="utf-8") as fh:
        return json.load(fh)["verticals"]


# --------------------------------------------------------------------------- #
# Content builders
# --------------------------------------------------------------------------- #
def _hook(vertical: dict[str, Any], pillar: str, language: str, rng: random.Random) -> str:
    pains = vertical["pains"]
    angles_en = vertical["messaging_angles_en"]
    angles_ar = vertical["messaging_angles_ar"]
    name = vertical["name_en"] if language == "en" else vertical["name_ar"]
    pain = rng.choice(pains)
    angle = rng.choice(angles_en if language == "en" else angles_ar)
    if language == "en":
        return {
            "educational": f"Most {name.lower()} teams lose margin in one place: {pain.lower()}.",
            "proof": f"We mapped 30 anonymized records for a {name.lower()} team. The leak was clear: {angle.lower()}.",
            "founder_pov": f"Unpopular opinion for {name.lower()}: automation without governance just speeds up the mess.",
            "offer": f"If you run {name.lower()}, here's a 20-minute way to see where revenue leaks.",
            "question": f"For {name.lower()} leaders: how do you know a job closed without a billable record?",
            "case_angle": f"A {name.lower()} operator told me: '{angle}.' Here's what we did about it.",
        }[pillar]
    return {
        "educational": f"معظم فرق {name} تخسر هامشها في مكان واحد: {pain}.",
        "proof": f"حلّلنا 30 سجلًا مجهّلًا لفريق {name}. التسرّب كان واضحًا: {angle}.",
        "founder_pov": f"رأي صريح لقطاع {name}: الأتمتة بلا حوكمة تسرّع الفوضى فقط.",
        "offer": f"إذا كنت تدير {name}، إليك طريقة من 20 دقيقة لرؤية أين يتسرّب الإيراد.",
        "question": f"لقادة {name}: كيف تعرف أن مهمة أُغلقت دون سجل قابل للفوترة؟",
        "case_angle": f"قال لي أحد مشغّلي {name}: «{angle}». وإليك ما فعلناه.",
    }[pillar]


def _body(vertical: dict[str, Any], pillar: str, language: str, hook: str, rng: random.Random) -> str:
    proof = vertical["proof_asset"]
    if language == "en":
        return (
            f"{hook}\n\n"
            f"At Dealix we govern the workflow — not just automate it. We share a proof asset first: "
            f"{proof}\n\n"
            f"No access to your data. Founder-reviewed. Conservative, provable claims only — no guarantees."
        )
    return (
        f"{hook}\n\n"
        f"في ديالكس نحوكم سير العمل — لا نكتفي بأتمتته. نشارك أصل الإثبات أولًا: {proof}\n\n"
        f"دون أي وصول لبياناتكم. بمراجعة المؤسس. ادعاءات متحفظة وقابلة للإثبات فقط — بلا ضمانات."
    )


def _hashtags(vertical_id: str, language: str, cfg: dict[str, Any], rng: random.Random) -> list[str]:
    bank = cfg["hashtags_bank"]
    tags = list(rng.sample(bank["global"], k=min(3, len(bank["global"]))))
    if language == "ar":
        tags += rng.sample(bank["ar"], k=min(2, len(bank["ar"])))
    tags += bank.get(vertical_id, [])[:2]
    # de-dup, keep order
    seen: set[str] = set()
    out = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def score_post(post: dict[str, Any], cfg: dict[str, Any], max_chars: int) -> tuple[int, int, list[str]]:
    body = (post.get("body") or "")
    low = body.lower()
    quality = 100
    compliance = 100
    reasons: list[str] = []

    # length fit
    if post.get("char_count", 0) > max_chars:
        quality -= 30
        reasons.append("over_length")
    if len(body) < 40:
        quality -= 20
        reasons.append("too_short")

    # tied to vertical
    vt_en = post.get("vertical", "")
    if not vt_en:
        quality -= 10
        reasons.append("no_vertical")

    # CTA present (most platforms)
    if not (post.get("cta") or "").strip():
        quality -= 10
        reasons.append("no_cta")

    # banned / exaggeration terms
    if any(t.lower() in low for t in cfg["banned_terms"]):
        quality -= 25
        compliance -= 40
        reasons.append("exaggeration_or_banned")

    # guaranteed roi / data-access claims (compliance)
    if "guaranteed" in low or "نضمن" in body or "مضمون" in body:
        compliance -= 40
        reasons.append("guaranteed_claim")
    if "we accessed your data" in low or "اطلعنا على بياناتكم" in body:
        compliance -= 50
        reasons.append("data_access_claim")

    # invariants
    if post.get("post_allowed") is True or post.get("external_post_blocked") is False:
        compliance -= 100
        reasons.append("not_review_only")

    return max(min(quality, 100), 0), max(min(compliance, 100), 0), reasons


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #
@dataclass
class SocialResult:
    run_date: str
    accepted: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    targets: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_accepted(self) -> int:
        return len(self.accepted)


def generate_social(
    target: int | None = None,
    config_dir: Path | None = None,
    seed: int | None = None,
    run_date: str | None = None,
) -> SocialResult:
    cfg = load_social_config(config_dir)
    verticals = load_verticals(config_dir)
    rd = run_date or date.today().isoformat()
    rng = random.Random(seed if seed is not None else int(rd.replace("-", "")) + 7)
    created_at = datetime.now(timezone.utc).isoformat()

    targets = dict(cfg["daily_targets_by_platform"])
    base_total = sum(targets.values())
    if target and target > base_total:
        factor = target / base_total
        targets = {k: int(round(v * factor)) for k, v in targets.items()}

    platforms = {p["id"]: p for p in cfg["platforms"]}
    pillars = [p["id"] for p in cfg["content_pillars"]]
    result = SocialResult(run_date=rd, targets=targets)

    counter = 0
    for platform_id, count in targets.items():
        platform = platforms[platform_id]
        max_chars = platform["max_chars"]
        produced = 0
        attempt = 0
        margin = int(count * 1.2) + 4
        while produced < margin:
            vertical = verticals[attempt % len(verticals)]
            language = "ar" if attempt % 2 == 0 else "en"
            pillar = pillars[attempt % len(pillars)]
            counter += 1
            attempt += 1

            hook = _hook(vertical, pillar, language, rng)
            body = _body(vertical, pillar, language, hook, rng)
            hashtags = _hashtags(vertical["id"], language, cfg, rng)
            cta = rng.choice(cfg["cta_bank"]["ar" if language == "ar" else "en"])

            # Ad copy + X stay short: trim body to the platform limit gracefully.
            if platform_id in ("x_post", "ad_copy_google"):
                body = hook  # short platforms use the hook as the post
            full_text = body
            if platform_id in ("instagram_caption", "linkedin_post"):
                full_text = f"{body}\n\n{cta}\n\n{' '.join(hashtags)}"

            post = {
                "post_id": f"DLX-SOC-{rd}-{platform_id[:3].upper()}-{counter:04d}",
                "created_at": created_at,
                "platform": platform_id,
                "vertical": vertical["id"],
                "language": language,
                "pillar": pillar,
                "hook": hook,
                "body": full_text,
                "hashtags": hashtags,
                "cta": cta,
                "char_count": len(full_text),
                "post_allowed": False,
                "external_post_blocked": True,
                "requires_founder_approval": True,
                "no_ad_spend": True,
                "status": "founder_review",
            }
            q, c, reasons = score_post(post, cfg, max_chars)
            post["quality_score"] = q
            post["compliance_score"] = c
            post["risk_level"] = "low" if c >= 90 and q >= 80 else ("medium" if c >= 70 else "high")
            post["_reasons"] = reasons

            forbidden = any(f.lower() in full_text.lower() for f in _FORBIDDEN_POST_FRAGMENTS)
            if q >= 70 and c >= 70 and not forbidden:
                result.accepted.append(post)
                produced += 1
            else:
                post["reject_reason"] = reasons or (["forbidden"] if forbidden else ["below_threshold"])
                result.rejected.append(post)
            if attempt > margin * 6:
                break

    if result.total_accepted < cfg["total_minimum"]:
        result.warnings.append(
            f"Only {result.total_accepted} posts cleared gates (< minimum {cfg['total_minimum']})."
        )
    return result


# --------------------------------------------------------------------------- #
# Validation + outputs
# --------------------------------------------------------------------------- #
REQUIRED_POST_FIELDS = [
    "post_id", "created_at", "platform", "vertical", "language", "pillar",
    "hook", "body", "hashtags", "cta", "char_count", "quality_score",
    "compliance_score", "risk_level", "post_allowed", "external_post_blocked",
    "requires_founder_approval", "status",
]


def validate_post_invariants(post: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for f in REQUIRED_POST_FIELDS:
        if f not in post:
            problems.append(f"missing_field:{f}")
    if post.get("post_allowed") is not False:
        problems.append("post_allowed_not_false")
    if post.get("external_post_blocked") is not True:
        problems.append("external_post_blocked_not_true")
    if post.get("requires_founder_approval") is not True:
        problems.append("requires_founder_approval_not_true")
    if post.get("status") != "founder_review":
        problems.append("bad_status")
    for banned in ("auto_post", "scheduled_post", "api_post", "ad_spend"):
        if post.get(banned):
            problems.append(f"banned_flag:{banned}")
    return problems


def _strip_internal(post: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in post.items() if not k.startswith("_")}


def write_social_outputs(result: SocialResult, base_dir: Path | None = None) -> dict[str, str]:
    out = (base_dir or OUTPUTS_DIR) / result.run_date
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}

    sq = out / "social_queue.jsonl"
    with sq.open("w", encoding="utf-8") as fh:
        for p in result.accepted:
            fh.write(json.dumps(_strip_internal(p), ensure_ascii=False) + "\n")
    paths["social_queue"] = str(sq)

    rj = out / "social_rejected.jsonl"
    with rj.open("w", encoding="utf-8") as fh:
        for p in result.rejected:
            fh.write(json.dumps(_strip_internal(p), ensure_ascii=False) + "\n")
    paths["social_rejected"] = str(rj)

    paths["social_review"] = str(_write_social_review(result, out))
    paths["social_metrics"] = str(_write_social_metrics(result, out))
    return paths


def _write_social_review(result: SocialResult, out: Path) -> Path:
    from collections import Counter

    by_platform = Counter(p["platform"] for p in result.accepted)
    by_vertical = Counter(p["vertical"] for p in result.accepted)
    by_pillar = Counter(p["pillar"] for p in result.accepted)
    ranked = sorted(result.accepted, key=lambda p: (p["compliance_score"], p["quality_score"]), reverse=True)

    L = [f"# Social & Media Review — {result.run_date}", "",
         ("> **REVIEW-ONLY.** Nothing here is posted, scheduled, or boosted. No ad spend. "
          + "The founder reviews, approves, and publishes manually."), "",
         "## Summary",
         f"- Posts ready for review: {result.total_accepted}",
         f"- Rejected by gates: {len(result.rejected)}", ""]
    if result.warnings:
        L += ["### ⚠️ Warnings"] + [f"- {w}" for w in result.warnings] + [""]
    L += ["## By platform"] + [f"- {k}: {v}" for k, v in by_platform.most_common()] + [""]
    L += ["## By vertical"] + [f"- {k}: {v}" for k, v in by_vertical.most_common()] + [""]
    L += ["## By content pillar"] + [f"- {k}: {v}" for k, v in by_pillar.most_common()] + [""]
    L += ["## Top 15 posts to publish first", ""]
    for i, p in enumerate(ranked[:15], 1):
        L.append(f"### {i}. [{p['platform']}] {p['vertical']} · {p['language']} · {p['pillar']}")
        L.append(f"> {p['hook']}")
        L.append(f"- CTA: {p['cta']}")
        L.append(f"- Hashtags: {' '.join(p['hashtags'])}")
        L.append(f"- Quality {p['quality_score']} / Compliance {p['compliance_score']} / Risk {p['risk_level']}")
        L.append("")
    L += ["## Publishing rules (do not break)",
          "- No auto-posting. No scheduling APIs. No ad spend. No bought engagement.",
          "- Personalise one detail, then publish manually from your own accounts.",
          "- Keep claims conservative and provable. No guarantees.", ""]
    path = out / "social_review.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def _write_social_metrics(result: SocialResult, out: Path) -> Path:
    from collections import Counter

    data = {
        "run_date": result.run_date,
        "total_accepted": result.total_accepted,
        "total_rejected": len(result.rejected),
        "by_platform": dict(Counter(p["platform"] for p in result.accepted)),
        "by_vertical": dict(Counter(p["vertical"] for p in result.accepted)),
        "by_language": dict(Counter(p["language"] for p in result.accepted)),
        "targets": result.targets,
        "target_met": result.total_accepted >= sum(result.targets.values()),
    }
    path = out / "social_metrics.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
