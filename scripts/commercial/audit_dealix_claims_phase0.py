#!/usr/bin/env python3
"""Create a reviewable claim-and-proof registry without mutating public copy."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_SURFACES = (
    "apps/web",
    "frontend",
    "landing",
    "sales",
    "docs/commercial",
    "docs/product",
    "data/templates",
)
EXTENSIONS = {
    ".md",
    ".html",
    ".htm",
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
}
SKIP_PARTS = {"node_modules", ".next", "dist", "build", ".git", "reports", "coverage", ".venv", "venv"}
POLICY_CONTEXT = re.compile(
    r"(?:لا\s+نضمن|ممنوع|غير\s+مضمون|do\s+not\s+guarantee|not\s+guaranteed|must\s+not|forbidden|without\s+claiming)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ClaimFinding:
    claim_id: str
    claim_text: str
    surface: str
    line: int
    category: str
    evidence: str
    status: str
    allowed_wording: str
    owner: str
    expiry: str


PATTERNS = (
    (
        "guaranteed_outcome",
        re.compile(r"\bguarantee(?:d|s)?\b|\bنضمن\b|مضمون(?:ة)?", re.IGNORECASE),
        "Use: target, hypothesis, measured result, or verified outcome.",
    ),
    (
        "risk_free",
        re.compile(r"risk[- ]?free|no risk|بدون مخاطر|بلا مخاطر", re.IGNORECASE),
        "Describe the specific risk controls and remaining uncertainty.",
    ),
    (
        "absolute_data_residency",
        re.compile(r"data (?:never|does not) leave|البيانات لا تغادر|بياناتك لن تغادر", re.IGNORECASE),
        "State the verified deployment/data-flow scope and provider/subprocessor boundaries.",
    ),
    (
        "absolute_compliance",
        re.compile(
            r"fully compliant|100% compliant|متوافق بالكامل|امتثال كامل|ISO\s*27001 certified|NCA certified|PDPL compliant",
            re.IGNORECASE,
        ),
        "Use: control mapped, partially verified, or subject to legal/security review.",
    ),
    (
        "sla_or_capacity",
        re.compile(r"99\.9%|unlimited leads?|2,500 leads?|2500 leads?|4[- ]hour support|أربع ساعات", re.IGNORECASE),
        "Use only with an approved SLA/capacity test and dated evidence.",
    ),
    (
        "government_access",
        re.compile(r"government access|علاقات حكومية|وصول حكومي|نفوذ حكومي", re.IGNORECASE),
        "Use: B2G readiness, partner mapping, and public opportunity monitoring.",
    ),
    (
        "free_audit",
        re.compile(r"free audit|تدقيق مجاني|فحص مجاني", re.IGNORECASE),
        "Use only when the offer scope, cost owner, expiry, and operational capacity are approved.",
    ),
    (
        "testimonial_or_case",
        re.compile(r"testimonial|case study|شهادة عميل|دراسة حالة", re.IGNORECASE),
        "Attach consent, source, date, scope, and attributable outcome evidence.",
    ),
)


def iter_files(root: Path, surfaces: Iterable[str]) -> Iterable[Path]:
    for surface in surfaces:
        base = root / surface
        if not base.exists():
            continue
        candidates = [base] if base.is_file() else base.rglob("*")
        for path in candidates:
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.name.endswith(("package-lock.json", "pnpm-lock.yaml", "yarn.lock")):
                continue
            yield path


def audit(root: Path, surfaces: Iterable[str]) -> list[ClaimFinding]:
    findings: list[ClaimFinding] = []
    for path in iter_files(root, surfaces):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        relative = path.relative_to(root).as_posix()
        for line_number, line in enumerate(lines, start=1):
            compact = " ".join(line.split())
            if not compact:
                continue
            for category, pattern, allowed in PATTERNS:
                if not pattern.search(compact):
                    continue
                context_start = max(0, line_number - 2)
                context_end = min(len(lines), line_number + 1)
                context = " ".join(" ".join(value.split()) for value in lines[context_start:context_end])
                status = "policy_reference" if POLICY_CONTEXT.search(context) else "review_required"
                digest = hashlib.sha256(
                    f"{relative}:{line_number}:{category}:{compact}".encode()
                ).hexdigest()[:12]
                findings.append(
                    ClaimFinding(
                        claim_id=f"CLM-{digest}",
                        claim_text=compact[:500],
                        surface=relative,
                        line=line_number,
                        category=category,
                        evidence="",
                        status=status,
                        allowed_wording=allowed,
                        owner="commercial_truth_owner",
                        expiry="unverified",
                    )
                )
    return sorted(
        findings,
        key=lambda item: (item.status != "review_required", item.surface, item.line, item.category),
    )


def write_registry(output_dir: Path, findings: list[ClaimFinding]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "claim_id",
        "claim_text",
        "surface",
        "line",
        "category",
        "evidence",
        "status",
        "allowed_wording",
        "owner",
        "expiry",
    ]
    with (output_dir / "claim_and_proof_registry.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(item) for item in findings)
    review_count = sum(1 for item in findings if item.status == "review_required")
    policy_count = len(findings) - review_count
    lines = [
        "# Claim and Proof Registry — Phase 0",
        "",
        f"- Findings: `{len(findings)}`",
        f"- Review required: `{review_count}`",
        f"- Policy/reference context: `{policy_count}`",
        "- This audit does not auto-edit copy. Review-required claims remain blocked from approval until evidence or safer wording is recorded.",
        "",
        "| Claim ID | Status | Category | Surface | Line | Claim |",
        "|---|---|---|---|---:|---|",
    ]
    for item in findings[:200]:
        claim = item.claim_text.replace("|", "\\|")
        lines.append(
            f"| `{item.claim_id}` | {item.status} | {item.category} | `{item.surface}` | {item.line} | {claim} |"
        )
    (output_dir / "claim_and_proof_registry.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit Dealix claim surfaces and emit a proof registry."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--output-dir", default="reports/dealix_autonomous_company_os"
    )
    parser.add_argument("--surface", action="append", dest="surfaces")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = audit(root, args.surfaces or DEFAULT_SURFACES)
    write_registry(Path(args.output_dir), findings)
    review_count = sum(1 for item in findings if item.status == "review_required")
    print(
        f"DEALIX_CLAIM_AUDIT=PASS findings={len(findings)} review_required={review_count}"
    )


if __name__ == "__main__":
    main()
