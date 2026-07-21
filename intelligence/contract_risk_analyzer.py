"""
Contract Risk Analyzer

Reads contract-like text and extracts risk signals, missing clauses,
and Saudi-market specific concerns for approval-first deal review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskFinding:
    category: str
    level: RiskLevel
    description: str
    recommendation: str


@dataclass
class ContractAnalysis:
    overall_risk: RiskLevel
    findings: list[RiskFinding]
    missing_clauses: list[str]
    summary: str


class ContractRiskAnalyzer:
    """Deterministic contract risk analysis for Saudi B2B engagements."""

    REQUIRED_CLAUSES: list[str] = [
        "payment terms",
        "scope of work",
        "liability cap",
        "governing law",
        "data protection / PDPL",
        "termination clause",
        "intellectual property",
    ]

    RISK_PATTERNS: dict[str, tuple[RiskLevel, str, str]] = {
        "unlimited liability": (RiskLevel.CRITICAL, "Unlimited liability exposure detected", "Cap liability at 12 months fees or contract value"),
        "no liability cap": (RiskLevel.HIGH, "No liability cap found", "Add liability cap clause"),
        "net 60": (RiskLevel.MEDIUM, "Payment terms exceed Net 30", "Negotiate Net 15 or Net 30"),
        "net 90": (RiskLevel.HIGH, "Very long payment terms", "Reject or require milestone-based payments"),
        "auto-renewal": (RiskLevel.MEDIUM, "Automatic renewal clause detected", "Require 30-day notice and annual review"),
        "exclusive": (RiskLevel.MEDIUM, "Exclusive provider clause detected", "Limit exclusivity by geography or service type"),
        "governed by": (RiskLevel.LOW, "Governing law clause present", "Verify Saudi law is acceptable"),
        "pdpl": (RiskLevel.LOW, "PDPL/data protection mentioned", "Ensure Dealix PDPL addendum attached"),
        "intellectual property": (RiskLevel.LOW, "IP clause present", "Confirm customer retains pre-existing IP"),
    }

    def analyze(self, contract_text: str) -> ContractAnalysis:
        """Analyze contract text for risks."""
        text_lower = contract_text.lower()
        findings: list[RiskFinding] = []
        missing: list[str] = []

        for clause in self.REQUIRED_CLAUSES:
            if clause not in text_lower:
                missing.append(clause)

        for pattern, (level, desc, rec) in self.RISK_PATTERNS.items():
            if pattern in text_lower:
                findings.append(RiskFinding(category="contract", level=level, description=desc, recommendation=rec))

        # Check for PDPL specifically
        if "pdpl" not in text_lower and "data protection" not in text_lower:
            findings.append(RiskFinding(
                category="compliance",
                level=RiskLevel.HIGH,
                description="No PDPL or data protection clause detected",
                recommendation="Attach Dealix PDPL data processing addendum",
            ))

        # Check governing law
        if "saudi" not in text_lower and "governed by" in text_lower:
            findings.append(RiskFinding(
                category="jurisdiction",
                level=RiskLevel.MEDIUM,
                description="Governing law may not be Saudi Arabia",
                recommendation="Confirm Saudi governing law or add arbitration clause",
            ))

        overall = RiskLevel.LOW
        for level in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW]:
            if any(f.level == level for f in findings):
                overall = level
                break

        if missing:
            findings.append(RiskFinding(
                category="completeness",
                level=RiskLevel.MEDIUM if len(missing) <= 2 else RiskLevel.HIGH,
                description=f"Missing clauses: {', '.join(missing)}",
                recommendation="Add missing clauses before signing",
            ))

        summary = (
            f"Overall risk: {overall.value}. "
            f"{len(findings)} findings, {len(missing)} missing clauses. "
            f"{'Review required before approval' if overall in (RiskLevel.HIGH, RiskLevel.CRITICAL) else 'Looks acceptable with minor updates'}."
        )

        return ContractAnalysis(
            overall_risk=overall,
            findings=findings,
            missing_clauses=missing,
            summary=summary,
        )

    def to_dict(self, analysis: ContractAnalysis) -> dict[str, Any]:
        return {
            "overall_risk": analysis.overall_risk.value,
            "summary": analysis.summary,
            "missing_clauses": analysis.missing_clauses,
            "findings": [
                {"category": f.category, "level": f.level.value, "description": f.description, "recommendation": f.recommendation}
                for f in analysis.findings
            ],
        }
