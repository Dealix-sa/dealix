"""Draft-only Dealix Full Company OS kernel.

This module intentionally uses only Python's standard library and performs only
internal file/report generation. It does not send messages, charge payments,
post content, merge pull requests, deploy, or read secrets.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import json
import os
from pathlib import Path
from typing import Any, Iterable

DANGEROUS_ENV_FLAGS = {
    "EXTERNAL_SEND_ENABLED",
    "LIVE_OUTBOUND_ENABLED",
    "AUTO_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "LINKEDIN_AUTOPOST_ENABLED",
    "PAYMENT_CAPTURE_ENABLED",
    "PRODUCTION_MUTATION_ENABLED",
    "PR_AUTO_MERGE_ENABLED",
}

FORBIDDEN_CLAIM_PATTERNS = (
    "we guarantee revenue",
    "guaranteed roi",
    "guaranteed government contract",
    "guaranteed b2g win",
    "we have official government access",
    "fake proof",
)

OFFER_LADDER = (
    "Saudi Opportunity Snapshot",
    "Revenue Proof Sprint 499 SAR",
    "Revenue Command Pilot",
    "Saudi Market Access Sprint",
    "Revenue Command Room Retainer",
    "AI Company OS Setup",
    "B2G Readiness Sprint",
    "Partner / Distributor Desk",
)

AUTONOMY_LEVELS = {
    0: "observe",
    1: "analyze",
    2: "draft",
    3: "internal_execute",
    4: "repo_execute",
    5: "external_execute_blocked",
}


@dataclass(slots=True)
class RunConfig:
    """Runtime settings for a safe Company OS cycle."""

    client: str = "dealix"
    mode: str = "draft-only"
    limit: int = 50
    autonomy_level: int = 3
    output_root: str = "reports/full_company_os"
    today: str = field(default_factory=lambda: datetime.now(UTC).date().isoformat())

    def validate(self) -> None:
        if self.mode != "draft-only":
            raise RuntimeError("Only draft-only mode is supported by this runner.")
        if self.autonomy_level >= 5:
            raise RuntimeError("Autonomy level 5 is blocked. External execution is not implemented.")
        if self.limit < 1:
            raise RuntimeError("limit must be at least 1")


@dataclass(slots=True)
class CompanyBrain:
    client: str
    positioning: str
    primary_offers: list[str]
    target_segments: list[str]
    restrictions: list[str]
    tone: str


@dataclass(slots=True)
class TargetCard:
    company: str
    segment: str
    source: str
    source_confidence: int
    pain_hypothesis: str
    buying_signal: str
    risk_level: str
    proof_to_show: str


@dataclass(slots=True)
class Opportunity:
    company: str
    segment: str
    score: int
    bucket: str
    offer_match: str
    reason: str
    recommended_channel: str
    next_action: str
    risk_level: str
    approval_required: bool = True


@dataclass(slots=True)
class DraftMessage:
    company: str
    channel: str
    subject: str
    body: str
    status: str = "pending_founder_review"


@dataclass(slots=True)
class ApprovalItem:
    item_type: str
    company: str
    summary: str
    risk_level: str
    decision_options: list[str]
    status: str = "pending"


@dataclass(slots=True)
class ProofEvent:
    event_type: str
    entity: str
    evidence: str
    source: str
    risk_level: str
    timestamp: str


@dataclass(slots=True)
class ImprovementItem:
    area: str
    failure_type: str
    root_cause_hypothesis: str
    recommended_improvement: str
    autonomy_bucket: str
    status: str = "proposed"


@dataclass(slots=True)
class CycleResult:
    config: dict[str, Any]
    company_brain: dict[str, Any]
    opportunities: list[dict[str, Any]]
    drafts: list[dict[str, Any]]
    approvals: list[dict[str, Any]]
    proof_log: list[dict[str, Any]]
    improvements: list[dict[str, Any]]
    blocked_actions: list[str]
    output_files: dict[str, str]


class FullCompanyOS:
    """Safe internal operating loop for Dealix.

    This runner is deliberately conservative. It creates reviewable operating
    artifacts only. Any action that would leave the repo or contact a human is
    converted into an approval item.
    """

    def __init__(self, config: RunConfig) -> None:
        config.validate()
        self.config = config
        self.generated_at = datetime.now(UTC).isoformat()
        self.output_dir = Path(config.output_root) / config.today
        self.blocked_actions: list[str] = []

    def run(self) -> CycleResult:
        self._safety_tripwire()
        brain = self._build_company_brain()
        targets = self._load_targets()[: self.config.limit]
        opportunities = [self._score_target(target) for target in targets]
        opportunities.sort(key=lambda item: item.score, reverse=True)
        drafts = [self._draft_message(opportunity) for opportunity in opportunities[:10]]
        approvals = self._approval_queue(opportunities[:10], drafts)
        proof = self._proof_log(opportunities, drafts, approvals)
        improvements = self._self_improvement(opportunities, approvals)
        files = self._write_outputs(brain, opportunities, drafts, approvals, proof, improvements)
        return CycleResult(
            config=asdict(self.config),
            company_brain=asdict(brain),
            opportunities=[asdict(item) for item in opportunities],
            drafts=[asdict(item) for item in drafts],
            approvals=[asdict(item) for item in approvals],
            proof_log=[asdict(item) for item in proof],
            improvements=[asdict(item) for item in improvements],
            blocked_actions=self.blocked_actions,
            output_files={key: str(value) for key, value in files.items()},
        )

    def _safety_tripwire(self) -> None:
        unsafe = [name for name in DANGEROUS_ENV_FLAGS if os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}]
        if unsafe:
            raise RuntimeError(f"Unsafe live execution flags are enabled: {', '.join(sorted(unsafe))}")
        outbound_mode = os.environ.get("OUTBOUND_MODE", "draft-only").lower().replace("_", "-")
        if outbound_mode not in {"draft-only", "dry-run", "disabled"}:
            raise RuntimeError(f"Unsupported OUTBOUND_MODE for this runner: {outbound_mode}")

    def _build_company_brain(self) -> CompanyBrain:
        return CompanyBrain(
            client=self.config.client,
            positioning="Saudi B2B AI Company OS that prepares daily revenue, market-access, partnership, and proof actions for founder approval.",
            primary_offers=list(OFFER_LADDER),
            target_segments=[
                "local_b2b_services",
                "clinics_and_healthcare_admin",
                "training_centers",
                "foreign_saas_market_entry",
                "b2g_readiness",
                "partner_distributor_candidates",
            ],
            restrictions=[
                "draft_only_external_actions",
                "founder_approval_required",
                "no_cold_whatsapp",
                "no_mass_linkedin_automation",
                "no_fake_proof",
                "no_promised_results",
                "no_payment_capture_without_evidence",
                "no_production_mutation",
            ],
            tone="clear, Saudi-market practical, proof-backed, low-risk, and direct",
        )

    def _load_targets(self) -> list[TargetCard]:
        sample_path = Path("data/full_company_os/targets.example.json")
        if sample_path.exists():
            try:
                raw = json.loads(sample_path.read_text(encoding="utf-8"))
                return [TargetCard(**item) for item in raw.get("targets", [])]
            except (json.JSONDecodeError, TypeError, OSError) as exc:
                self.blocked_actions.append(f"target_seed_load_failed:{exc.__class__.__name__}")
        return [
            TargetCard(
                company="Riyadh Clinic Group",
                segment="clinics_and_healthcare_admin",
                source="founder_seed_example",
                source_confidence=70,
                pain_hypothesis="Patient inquiries and follow-ups may be spread across WhatsApp, calls, and front-desk notes.",
                buying_signal="Local service business with recurring inquiries and appointment operations.",
                risk_level="medium",
                proof_to_show="Revenue leak checklist plus draft follow-up queue, not promised financial results.",
            ),
            TargetCard(
                company="Saudi Training Center",
                segment="training_centers",
                source="founder_seed_example",
                source_confidence=68,
                pain_hypothesis="Enrollment leads may lose momentum when follow-up is not structured by urgency and decision stage.",
                buying_signal="Training businesses benefit from clear follow-up, scripts, and proof of activity.",
                risk_level="low",
                proof_to_show="Sample enrollment follow-up command report.",
            ),
            TargetCard(
                company="MENA SaaS Vendor",
                segment="foreign_saas_market_entry",
                source="founder_seed_example",
                source_confidence=64,
                pain_hypothesis="A foreign SaaS company may need Saudi market-entry targeting, partner mapping, and localized proof.",
                buying_signal="International B2B software entering or testing GCC/Saudi expansion.",
                risk_level="medium",
                proof_to_show="Saudi opportunity snapshot and partner-readiness checklist.",
            ),
        ]

    def _score_target(self, target: TargetCard) -> Opportunity:
        segment_weights = {
            "clinics_and_healthcare_admin": 86,
            "training_centers": 80,
            "foreign_saas_market_entry": 84,
            "b2g_readiness": 78,
            "partner_distributor_candidates": 76,
            "local_b2b_services": 74,
        }
        base = segment_weights.get(target.segment, 60)
        score = max(1, min(100, int((base + target.source_confidence) / 2)))
        risk_penalty = {"low": 0, "medium": 5, "high": 15}.get(target.risk_level, 10)
        score = max(1, score - risk_penalty)
        bucket = "hot" if score >= 80 else "warm" if score >= 65 else "research"
        offer = self._offer_for_segment(target.segment, score)
        return Opportunity(
            company=target.company,
            segment=target.segment,
            score=score,
            bucket=bucket,
            offer_match=offer,
            reason=f"{target.buying_signal} Pain hypothesis: {target.pain_hypothesis}",
            recommended_channel="email_or_linkedin_draft_only",
            next_action="Prepare a one-page snapshot and founder-reviewed message draft.",
            risk_level=target.risk_level,
        )

    def _offer_for_segment(self, segment: str, score: int) -> str:
        if segment == "foreign_saas_market_entry":
            return "Saudi Market Access Sprint" if score >= 80 else "Saudi Opportunity Snapshot"
        if segment == "b2g_readiness":
            return "B2G Readiness Sprint"
        if segment == "partner_distributor_candidates":
            return "Partner / Distributor Desk"
        if score >= 80:
            return "Revenue Command Pilot"
        return "Revenue Proof Sprint 499 SAR"

    def _draft_message(self, opportunity: Opportunity) -> DraftMessage:
        subject = f"Draft: {opportunity.offer_match} for {opportunity.company}"
        body = (
            f"Hi {{Name}},\n\n"
            f"I am testing a practical Dealix workflow for {opportunity.segment.replace('_', ' ')} teams. "
            f"The goal is simple: identify the most important follow-ups or market-entry opportunities, prepare the next-message drafts, "
            f"and deliver a proof-backed action report without changing your existing systems.\n\n"
            f"For {opportunity.company}, the relevant starting point looks like {opportunity.offer_match}. "
            f"Would it be useful if I send a one-page snapshot for review?\n\n"
            f"Note: this is a draft prepared for founder approval; it must not be sent automatically."
        )
        self._assert_no_forbidden_claims(body)
        return DraftMessage(company=opportunity.company, channel=opportunity.recommended_channel, subject=subject, body=body)

    def _approval_queue(self, opportunities: Iterable[Opportunity], drafts: Iterable[DraftMessage]) -> list[ApprovalItem]:
        queue: list[ApprovalItem] = []
        draft_by_company = {draft.company: draft for draft in drafts}
        for opportunity in opportunities:
            draft = draft_by_company.get(opportunity.company)
            queue.append(
                ApprovalItem(
                    item_type="external_message_review",
                    company=opportunity.company,
                    summary=(
                        f"Review {opportunity.offer_match} draft for {opportunity.company}. "
                        f"Score={opportunity.score}, risk={opportunity.risk_level}, channel={opportunity.recommended_channel}. "
                        f"Draft exists={bool(draft)}."
                    ),
                    risk_level=opportunity.risk_level,
                    decision_options=["approve_for_manual_send", "edit", "reject", "ask_for_more_research"],
                )
            )
        return queue

    def _proof_log(
        self,
        opportunities: list[Opportunity],
        drafts: list[DraftMessage],
        approvals: list[ApprovalItem],
    ) -> list[ProofEvent]:
        now = self.generated_at
        return [
            ProofEvent(
                event_type="company_os_cycle_created",
                entity=self.config.client,
                evidence=f"opportunities={len(opportunities)} drafts={len(drafts)} approvals={len(approvals)}",
                source="dealix.full_company_os.kernel",
                risk_level="low",
                timestamp=now,
            ),
            ProofEvent(
                event_type="external_actions_blocked_by_design",
                entity=self.config.client,
                evidence="All external work is routed to approval queue; no send adapter exists in this kernel.",
                source="dealix.full_company_os.kernel",
                risk_level="low",
                timestamp=now,
            ),
        ]

    def _self_improvement(self, opportunities: list[Opportunity], approvals: list[ApprovalItem]) -> list[ImprovementItem]:
        improvements: list[ImprovementItem] = []
        if not opportunities:
            improvements.append(
                ImprovementItem(
                    area="data",
                    failure_type="no_targets_loaded",
                    root_cause_hypothesis="No safe founder seed, CRM row, or example target was available.",
                    recommended_improvement="Add opted-in or founder-provided target cards to data/full_company_os/targets.example.json or a future private inbox.",
                    autonomy_bucket="approval_required",
                )
            )
        if approvals:
            improvements.append(
                ImprovementItem(
                    area="sales",
                    failure_type="approval_queue_pending",
                    root_cause_hypothesis="Drafts are ready but cannot create value until the founder approves, edits, or rejects them.",
                    recommended_improvement="Review top 3 approvals first, then log decisions so the learning loop can improve targeting.",
                    autonomy_bucket="auto_learn",
                )
            )
        if any(item.risk_level == "medium" for item in opportunities):
            improvements.append(
                ImprovementItem(
                    area="compliance",
                    failure_type="medium_risk_targets_present",
                    root_cause_hypothesis="Some targets require stronger proof or clearer consent/channel fit before outreach.",
                    recommended_improvement="Attach a one-page snapshot or warm-intro source before manual outreach.",
                    autonomy_bucket="approval_required",
                )
            )
        return improvements

    def _write_outputs(
        self,
        brain: CompanyBrain,
        opportunities: list[Opportunity],
        drafts: list[DraftMessage],
        approvals: list[ApprovalItem],
        proof: list[ProofEvent],
        improvements: list[ImprovementItem],
    ) -> dict[str, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        latest_dir = Path(self.config.output_root)
        latest_dir.mkdir(parents=True, exist_ok=True)

        bundle = {
            "generated_at": self.generated_at,
            "config": asdict(self.config),
            "company_brain": asdict(brain),
            "opportunities": [asdict(item) for item in opportunities],
            "drafts": [asdict(item) for item in drafts],
            "approvals": [asdict(item) for item in approvals],
            "proof_log": [asdict(item) for item in proof],
            "improvements": [asdict(item) for item in improvements],
            "blocked_actions": self.blocked_actions,
        }
        files = {
            "bundle": self.output_dir / "bundle.json",
            "opportunities": self.output_dir / "opportunities.json",
            "drafts": self.output_dir / "drafts.json",
            "approvals": self.output_dir / "approvals.json",
            "proof": self.output_dir / "proof.json",
            "improvements": self.output_dir / "improvements.json",
            "report": self.output_dir / "daily.md",
            "latest_bundle": latest_dir / "latest.json",
            "latest_report": latest_dir / "latest.md",
        }
        files["bundle"].write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["opportunities"].write_text(json.dumps(bundle["opportunities"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["drafts"].write_text(json.dumps(bundle["drafts"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["approvals"].write_text(json.dumps(bundle["approvals"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["proof"].write_text(json.dumps(bundle["proof_log"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["improvements"].write_text(json.dumps(bundle["improvements"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = self._render_markdown(brain, opportunities, drafts, approvals, proof, improvements)
        files["report"].write_text(report, encoding="utf-8")
        files["latest_bundle"].write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files["latest_report"].write_text(report, encoding="utf-8")
        return files

    def _render_markdown(
        self,
        brain: CompanyBrain,
        opportunities: list[Opportunity],
        drafts: list[DraftMessage],
        approvals: list[ApprovalItem],
        proof: list[ProofEvent],
        improvements: list[ImprovementItem],
    ) -> str:
        lines = [
            "# Dealix Full Company OS Daily Command",
            "",
            f"Generated: {self.generated_at}",
            f"Client: {brain.client}",
            f"Mode: {self.config.mode}",
            f"Autonomy: L{self.config.autonomy_level} - {AUTONOMY_LEVELS.get(self.config.autonomy_level)}",
            "",
            "## Positioning",
            brain.positioning,
            "",
            "## Top opportunities",
        ]
        for index, item in enumerate(opportunities[:10], start=1):
            lines.extend(
                [
                    f"{index}. **{item.company}** — score {item.score} ({item.bucket})",
                    f"   - Segment: {item.segment}",
                    f"   - Offer: {item.offer_match}",
                    f"   - Reason: {item.reason}",
                    f"   - Next action: {item.next_action}",
                    f"   - Risk: {item.risk_level}",
                ]
            )
        lines.extend(["", "## Drafts created"])
        for draft in drafts:
            lines.extend([f"- **{draft.company}** via {draft.channel}: {draft.subject}"])
        lines.extend(["", "## Approval queue"])
        for item in approvals:
            lines.extend([f"- **{item.company}**: {item.summary} Options: {', '.join(item.decision_options)}"])
        lines.extend(["", "## Proof log"])
        for event in proof:
            lines.extend([f"- {event.event_type}: {event.evidence}"])
        lines.extend(["", "## Self-improvement"])
        for item in improvements:
            lines.extend([f"- {item.area}/{item.failure_type}: {item.recommended_improvement} ({item.autonomy_bucket})"])
        lines.extend(
            [
                "",
                "## Safety status",
                "- No external send adapter exists in this kernel.",
                "- No payment capture exists in this kernel.",
                "- No production mutation exists in this kernel.",
                "- Generated messages are drafts that require founder approval.",
                "",
            ]
        )
        return "\n".join(lines)

    def _assert_no_forbidden_claims(self, text: str) -> None:
        lowered = text.lower()
        hits = [pattern for pattern in FORBIDDEN_CLAIM_PATTERNS if pattern in lowered]
        if hits:
            raise RuntimeError(f"Forbidden claim pattern detected: {', '.join(hits)}")


def run_daily_cycle(config: RunConfig | None = None) -> CycleResult:
    """Run one safe draft-only Dealix Company OS cycle."""

    return FullCompanyOS(config or RunConfig()).run()
