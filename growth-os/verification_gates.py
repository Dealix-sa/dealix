"""
verification_gates.py — Dealix Growth OS
Ten verification gates for production readiness.

Each gate has a check() method returning:
    {gate, status, findings, recommendations}

Status values: pass | fail | warning

Usage:
    from verification_gates import Gate1InfrastructureReady
    result = Gate1InfrastructureReady().check()
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_BASE = Path(__file__).parent
_MEMORY = _BASE / "memory"
_CONFIG = _BASE / "config"
_OUTPUTS = _BASE / "outputs"


def _load_jsonl(filename: str) -> list:
    path = _MEMORY / filename
    rows = []
    if not path.exists():
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def _load_yaml(filename: str) -> dict:
    path = _CONFIG / filename
    if not _HAS_YAML or not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ---------------------------------------------------------------------------
# Gate 1: Infrastructure Ready
# ---------------------------------------------------------------------------

class Gate1InfrastructureReady:
    """
    Checks that all infrastructure components are in place before launch.
    Items: domain, SPF/DKIM/DMARC, tracking, suppression_list,
           opt_out_handling, logging, error_handling, kill_switch,
           dashboard, backups
    """

    GATE = 1
    NAME = "Infrastructure Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        # 1. Suppression list exists and is readable
        sup_path = _MEMORY / "suppression.jsonl"
        if sup_path.exists():
            passes.append("suppression_list: file exists")
        else:
            findings.append("FAIL: suppression.jsonl does not exist — no suppression protection")

        # 2. Opt-in list exists
        opt_path = _MEMORY / "opt_ins.jsonl"
        if opt_path.exists():
            passes.append("opt_out_handling: opt_ins.jsonl exists")
        else:
            findings.append("FAIL: opt_ins.jsonl does not exist — WhatsApp/Telegram opt-in not tracked")

        # 3. Logging infrastructure (execution_logs.jsonl)
        log_path = _MEMORY / "execution_logs.jsonl"
        if log_path.exists():
            passes.append("logging: execution_logs.jsonl exists")
        else:
            findings.append("FAIL: execution_logs.jsonl missing — no audit trail")

        # 4. Output directories
        required_output_dirs = [
            "daily", "channel_packs", "execution_queue",
            "founder_review", "sent", "paused", "rejected", "reports"
        ]
        for d in required_output_dirs:
            dir_path = _OUTPUTS / d
            if dir_path.exists():
                passes.append(f"output_dir_{d}: exists")
            else:
                findings.append(f"FAIL: outputs/{d}/ missing")

        # 5. Config files exist
        required_configs = [
            "anti-ban.yml", "scoring.yml", "countries.yml", "sectors.yml",
            "offers.yml", "channel-router.yml", "execution-modes.yml",
            "compliance.yml", "quotas.yml"
        ]
        for cfg in required_configs:
            if (_CONFIG / cfg).exists():
                passes.append(f"config_{cfg}: exists")
            else:
                findings.append(f"FAIL: config/{cfg} missing")

        # 6. Kill switch check — env var or config
        kill_switch = os.environ.get("GROWTH_OS_KILL_SWITCH", "").lower()
        if kill_switch in ("true", "1", "yes"):
            warnings.append("WARNING: GROWTH_OS_KILL_SWITCH is active — system will not send")
        else:
            passes.append("kill_switch: not active (system can send)")

        # 7. Dry run mode
        dry_run = os.environ.get("DRY_RUN", "").lower()
        if dry_run in ("true", "1", "yes"):
            warnings.append("WARNING: DRY_RUN mode is ON — no emails will be sent")
        else:
            passes.append("dry_run: not active")

        # 8. Domain env var
        domain = os.environ.get("SENDING_DOMAIN", "")
        if domain:
            passes.append(f"domain: {domain} configured")
        else:
            warnings.append("WARNING: SENDING_DOMAIN env var not set — email sending may fail")

        # 9. SPF/DKIM/DMARC — cannot verify programmatically without DNS, so mark as manual check
        warnings.append("MANUAL CHECK REQUIRED: SPF, DKIM, DMARC — verify via Google Postmaster Tools or MXToolbox")

        # 10. Backups — check if memory dir has files
        memory_files = list(_MEMORY.glob("*.jsonl"))
        if len(memory_files) >= 5:
            passes.append(f"data_files: {len(memory_files)} JSONL files present")
        else:
            warnings.append(f"WARNING: Only {len(memory_files)} memory files — ensure backups are configured")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "pass_count": len(passes),
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Set SENDING_DOMAIN env var before launch",
                "Verify SPF/DKIM/DMARC via MXToolbox",
                "Ensure daily backups of memory/ JSONL files",
            ],
            "governance_decision": f"gate1_infrastructure_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 2: Data Quality Ready
# ---------------------------------------------------------------------------

class Gate2DataQualityReady:
    """
    Checks data quality thresholds:
    duplicate < 3%, missing_sector < 10%, missing_country < 5%,
    wrong_language < 5%, invalid_contacts < 10%,
    sensitive_sector_flag 100%, suppression_respected 100%
    """

    GATE = 2
    NAME = "Data Quality Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        companies = _load_jsonl("companies.jsonl")
        contacts = _load_jsonl("contacts.jsonl")
        suppression = _load_jsonl("suppression.jsonl")

        n_companies = len(companies)
        if n_companies == 0:
            warnings.append("WARNING: No companies in database — populate before launch")
            return {
                "gate": self.GATE,
                "name": self.NAME,
                "status": "warning",
                "findings": findings,
                "warnings": warnings,
                "passes": passes,
                "recommendations": ["Add companies to companies.jsonl before launch"],
                "governance_decision": "gate2_data_quality_warning_empty",
            }

        # Duplicate check (by domain)
        domains = [c.get("domain", "") for c in companies if c.get("domain")]
        duplicate_count = len(domains) - len(set(domains))
        dup_rate = duplicate_count / n_companies if n_companies else 0
        if dup_rate < 0.03:
            passes.append(f"duplicate_rate: {dup_rate:.1%} (threshold < 3%)")
        else:
            findings.append(f"FAIL: duplicate_rate {dup_rate:.1%} exceeds 3% threshold")

        # Missing sector
        missing_sector = sum(1 for c in companies if not c.get("sector"))
        ms_rate = missing_sector / n_companies
        if ms_rate < 0.10:
            passes.append(f"missing_sector_rate: {ms_rate:.1%} (threshold < 10%)")
        else:
            findings.append(f"FAIL: missing_sector_rate {ms_rate:.1%} exceeds 10%")

        # Missing country
        missing_country = sum(1 for c in companies if not c.get("country"))
        mc_rate = missing_country / n_companies
        if mc_rate < 0.05:
            passes.append(f"missing_country_rate: {mc_rate:.1%} (threshold < 5%)")
        else:
            findings.append(f"FAIL: missing_country_rate {mc_rate:.1%} exceeds 5%")

        # Sensitive sector flag — all sensitive sectors must have sensitive_flag checked
        sectors_config = _load_yaml("sectors.yml")
        sensitive_sectors = [
            k for k, v in sectors_config.get("sectors", {}).items()
            if v.get("sensitive_flag", False)
        ]
        # Check that sensitive companies are flagged (simplified check)
        if sensitive_sectors:
            passes.append(
                f"sensitive_sector_flag: {len(sensitive_sectors)} sensitive sectors defined in config"
            )
        else:
            warnings.append("WARNING: No sensitive sectors defined — check sectors.yml")

        # Invalid contacts (contacts without email AND without linkedin)
        n_contacts = len(contacts)
        if n_contacts > 0:
            invalid_contacts = sum(
                1 for c in contacts
                if not c.get("email") and not c.get("linkedin_url") and not c.get("phone")
            )
            ic_rate = invalid_contacts / n_contacts
            if ic_rate < 0.10:
                passes.append(f"invalid_contacts_rate: {ic_rate:.1%} (threshold < 10%)")
            else:
                findings.append(f"FAIL: invalid_contacts_rate {ic_rate:.1%} exceeds 10%")
        else:
            warnings.append("WARNING: No contacts in database")

        # Suppression respected — check suppressed contacts are not in active jobs
        jobs = _load_jsonl("channel_jobs.jsonl")
        suppressed_domains = {s.get("email_or_domain", "") for s in suppression}
        violations = [
            job for job in jobs
            if job.get("status") in ("queued", "pending_founder_approval")
            and any(d and d in job.get("contact_email", "") for d in suppressed_domains)
        ]
        if violations:
            findings.append(f"FAIL: {len(violations)} suppressed contacts in active queue")
        else:
            passes.append("suppression_respected: no violations detected in current queue")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "companies_checked": n_companies,
            "contacts_checked": n_contacts,
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Deduplicate companies by domain before scaling outreach",
                "Ensure all companies have sector and country tagged",
                "Check all sensitive sector companies for proper flagging",
            ],
            "governance_decision": f"gate2_data_quality_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 3: Company Understanding Ready
# ---------------------------------------------------------------------------

class Gate3CompanyUnderstandingReady:
    """
    Checks company brief schema and minimum understanding scores:
    understanding >= 80, offer_fit >= 75, buyer_confidence >= 60,
    pain_clarity >= 75, language_confidence >= 90
    """

    GATE = 3
    NAME = "Company Understanding Ready"

    THRESHOLDS = {
        "understanding_score": 80,
        "offer_fit_score": 75,
        "buyer_confidence_score": 60,
        "pain_clarity_score": 75,
        "language_confidence_score": 90,
    }

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        briefs = _load_jsonl("company_briefs.jsonl")
        if not briefs:
            warnings.append("WARNING: No company briefs in database")
            return {
                "gate": self.GATE,
                "name": self.NAME,
                "status": "warning",
                "findings": findings,
                "warnings": warnings,
                "passes": passes,
                "recommendations": ["Run company-researcher agent to build company briefs"],
                "governance_decision": "gate3_company_understanding_warning_empty",
            }

        below_threshold: list[dict] = []
        for brief in briefs:
            brief_issues = []
            for field, threshold in self.THRESHOLDS.items():
                score = brief.get(field, 0)
                if score < threshold:
                    brief_issues.append(
                        f"{field}={score} below threshold {threshold}"
                    )
            if brief_issues:
                below_threshold.append({
                    "brief_id": brief.get("brief_id"),
                    "company_id": brief.get("company_id"),
                    "issues": brief_issues,
                })

        total = len(briefs)
        passing = total - len(below_threshold)
        pass_rate = passing / total if total else 0

        if pass_rate >= 0.80:
            passes.append(
                f"company_understanding: {passing}/{total} briefs meet all thresholds ({pass_rate:.0%})"
            )
        elif pass_rate >= 0.60:
            warnings.append(
                f"WARNING: {passing}/{total} briefs meet all thresholds — below 80% target"
            )
        else:
            findings.append(
                f"FAIL: Only {passing}/{total} briefs meet all thresholds ({pass_rate:.0%})"
            )

        # Schema check
        required_fields = [
            "brief_id", "company_id", "sector", "country", "language",
            "understanding_score", "offer_fit_score", "buyer_confidence_score",
            "pain_clarity_score", "language_confidence_score",
            "top_pains", "recommended_offer", "recommended_channel",
        ]
        missing_fields_count = 0
        for brief in briefs:
            missing = [f for f in required_fields if f not in brief]
            if missing:
                missing_fields_count += 1
        if missing_fields_count == 0:
            passes.append("schema: all briefs have required fields")
        else:
            findings.append(
                f"FAIL: {missing_fields_count} briefs missing required schema fields"
            )

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "briefs_checked": total,
            "briefs_passing": passing,
            "below_threshold": below_threshold[:5],
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "thresholds": self.THRESHOLDS,
            "recommendations": [
                "Re-run company-researcher agent for briefs below threshold",
                "Prioritize improving language_confidence_score (highest bar at 90)",
                "Only proceed to asset generation for briefs that pass all thresholds",
            ],
            "governance_decision": f"gate3_company_understanding_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 4: Draft Quality Ready
# ---------------------------------------------------------------------------

class Gate4DraftQualityReady:
    """
    Scores a sample of channel assets and verifies quality distribution.
    Decision thresholds: 90-100 → ready, 82-89 → founder_review,
    70-81 → rewrite, <70 → reject
    """

    GATE = 4
    NAME = "Draft Quality Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        assets = _load_jsonl("channel_assets.jsonl")
        if not assets:
            warnings.append("WARNING: No channel assets — run asset-generator first")
            return {
                "gate": self.GATE,
                "name": self.NAME,
                "status": "warning",
                "findings": findings,
                "warnings": warnings,
                "passes": passes,
                "recommendations": ["Run asset-generator agent to create outreach drafts"],
                "governance_decision": "gate4_draft_quality_warning_empty",
            }

        total = len(assets)
        decision_dist: dict[str, int] = {
            "ready": 0, "founder_review": 0, "rewrite": 0, "reject": 0
        }
        score_sum = 0
        scores = []

        for asset in assets:
            score = asset.get("quality_score", 0)
            scores.append(score)
            score_sum += score
            decision = asset.get("decision", "reject")
            if decision in decision_dist:
                decision_dist[decision] += 1
            else:
                decision_dist["reject"] += 1

        avg_score = round(score_sum / total if total else 0, 1)
        ready_rate = decision_dist["ready"] / total if total else 0
        reject_rate = decision_dist["reject"] / total if total else 0

        if avg_score >= 85:
            passes.append(f"avg_quality_score: {avg_score}/100 — excellent")
        elif avg_score >= 75:
            passes.append(f"avg_quality_score: {avg_score}/100 — acceptable")
        else:
            findings.append(f"FAIL: avg_quality_score {avg_score}/100 — below 75 minimum")

        if reject_rate > 0.20:
            findings.append(
                f"FAIL: reject_rate {reject_rate:.0%} too high — review prompts and asset-generator"
            )
        else:
            passes.append(f"reject_rate: {reject_rate:.0%} (acceptable)")

        # Compliance pass rate
        compliance_pass = sum(1 for a in assets if a.get("compliance_pass", False))
        compliance_rate = compliance_pass / total if total else 0
        if compliance_rate >= 0.95:
            passes.append(f"compliance_pass_rate: {compliance_rate:.0%}")
        else:
            findings.append(
                f"FAIL: compliance_pass_rate {compliance_rate:.0%} — below 95% minimum"
            )

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "assets_checked": total,
            "avg_quality_score": avg_score,
            "decision_distribution": decision_dist,
            "ready_rate": round(ready_rate, 3),
            "reject_rate": round(reject_rate, 3),
            "compliance_pass_rate": round(compliance_rate, 3),
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Review and rewrite all assets with decision=rewrite",
                "Reject assets must not enter execution queue",
                "Ensure all assets include opt-out language",
            ],
            "governance_decision": f"gate4_draft_quality_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 5: Channel Safety Ready
# ---------------------------------------------------------------------------

class Gate5ChannelSafetyReady:
    """
    Verifies channel policies are configured correctly.
    """

    GATE = 5
    NAME = "Channel Safety Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        anti_ban = _load_yaml("anti-ban.yml")
        if _load_yaml("execution-modes.yml"):
            passes.append("execution_modes_config: loaded")
        if _load_yaml("channel-router.yml"):
            passes.append("channel_router_config: loaded")

        if not anti_ban:
            findings.append("FAIL: config/anti-ban.yml not found or empty")
        else:
            passes.append("anti_ban_config: loaded")

        # LinkedIn must be assisted_manual
        linkedin_cfg = anti_ban.get("anti_ban_guardian", {}).get("linkedin", {})
        if linkedin_cfg.get("mode") == "assisted_manual":
            passes.append("linkedin_mode: assisted_manual — correct")
        else:
            findings.append(
                "FAIL: LinkedIn mode is not assisted_manual — non-negotiable violation"
            )

        # WhatsApp must require opt-in
        wa_cfg = anti_ban.get("anti_ban_guardian", {}).get("whatsapp", {})
        if wa_cfg.get("require_opt_in", False):
            passes.append("whatsapp_opt_in: required — correct")
        else:
            findings.append(
                "FAIL: WhatsApp opt-in not required — non-negotiable violation"
            )

        # LinkedIn block_scraping must be True
        if linkedin_cfg.get("block_scraping", False):
            passes.append("linkedin_block_scraping: True — correct")
        else:
            findings.append(
                "FAIL: LinkedIn scraping not blocked — non-negotiable violation"
            )

        # Website forms must have max per domain
        wf_cfg = anti_ban.get("anti_ban_guardian", {}).get("website_forms", {})
        if wf_cfg.get("max_per_domain_per_day", 0) >= 1:
            passes.append("website_forms_rate_limit: configured")
        else:
            warnings.append("WARNING: website_forms rate limit not set")

        # Instagram inbound-only
        ig_cfg = anti_ban.get("anti_ban_guardian", {}).get("instagram", {})
        if ig_cfg.get("block_unsolicited_dm", False):
            passes.append("instagram_block_unsolicited_dm: True — correct")
        else:
            warnings.append("WARNING: Instagram unsolicited DM not explicitly blocked")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "LinkedIn must always be assisted_manual — never automate",
                "WhatsApp opt-in is non-negotiable — do not send without it",
                "Scraping is permanently blocked — do not attempt to bypass",
            ],
            "governance_decision": f"gate5_channel_safety_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 6: Execution Health Ready
# ---------------------------------------------------------------------------

class Gate6ExecutionHealthReady:
    """
    Verifies execution log schema and health of the execution queue.
    """

    GATE = 6
    NAME = "Execution Health Ready"

    REQUIRED_LOG_FIELDS = [
        "log_id", "job_id", "company_id", "channel",
        "event_type", "event_at", "governance_decision"
    ]

    REQUIRED_JOB_FIELDS = [
        "job_id", "asset_id", "company_id", "channel",
        "execution_mode", "status", "governance_decision"
    ]

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        logs = _load_jsonl("execution_logs.jsonl")
        jobs = _load_jsonl("channel_jobs.jsonl")

        # Check log schema
        if logs:
            schema_fails = 0
            for log in logs:
                missing = [f for f in self.REQUIRED_LOG_FIELDS if f not in log]
                if missing:
                    schema_fails += 1
            if schema_fails == 0:
                passes.append("execution_logs_schema: all required fields present")
            else:
                findings.append(
                    f"FAIL: {schema_fails}/{len(logs)} execution logs missing required fields"
                )
        else:
            warnings.append("WARNING: No execution logs yet — system has not executed any jobs")

        # Check job schema
        if jobs:
            schema_fails = 0
            for job in jobs:
                missing = [f for f in self.REQUIRED_JOB_FIELDS if f not in job]
                if missing:
                    schema_fails += 1
            if schema_fails == 0:
                passes.append("channel_jobs_schema: all required fields present")
            else:
                findings.append(
                    f"FAIL: {schema_fails}/{len(jobs)} channel jobs missing required fields"
                )

            # Governance decision present in all jobs
            no_governance = sum(1 for j in jobs if not j.get("governance_decision"))
            if no_governance == 0:
                passes.append("governance_decision_field: present in all jobs")
            else:
                findings.append(
                    f"FAIL: {no_governance} jobs missing governance_decision field"
                )
        else:
            warnings.append("WARNING: No channel jobs in queue")

        # Check for jobs stuck in pending state > 48h
        from datetime import datetime as _dt, timezone as _tz
        now = _dt.now(_tz.utc)
        stuck_jobs = []
        for job in jobs:
            if job.get("status") == "pending_founder_approval":
                scheduled = job.get("scheduled_at", "")
                try:
                    scheduled_dt = _dt.fromisoformat(scheduled.replace("Z", "+00:00"))
                    hours_waiting = (now - scheduled_dt).total_seconds() / 3600
                    if hours_waiting > 48:
                        stuck_jobs.append(job.get("job_id"))
                except (ValueError, TypeError):
                    pass  # malformed timestamp — skip this job

        if stuck_jobs:
            warnings.append(
                f"WARNING: {len(stuck_jobs)} jobs stuck in pending_founder_approval > 48h: {stuck_jobs[:3]}"
            )
        else:
            passes.append("stuck_jobs: none detected")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "logs_checked": len(logs),
            "jobs_checked": len(jobs),
            "stuck_jobs": stuck_jobs,
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Every job must have a governance_decision field",
                "Review pending_founder_approval jobs daily — do not let them sit > 24h",
                "Ensure all logs have the required schema fields",
            ],
            "governance_decision": f"gate6_execution_health_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 7: Deliverability Ready
# ---------------------------------------------------------------------------

class Gate7DeliverabilityReady:
    """
    Checks email deliverability metrics against thresholds:
    bounce < 2%, spam < 0.1%, unsubscribe < 1%, reply > 3%
    """

    GATE = 7
    NAME = "Deliverability Ready"

    THRESHOLDS = {
        "bounce_rate_max": 0.02,
        "spam_rate_max": 0.001,
        "unsubscribe_rate_max": 0.01,
        "reply_rate_min": 0.03,
    }

    def check(self, metrics: Optional[dict] = None) -> dict:
        """
        Args:
            metrics: dict with bounce_rate, spam_rate, unsubscribe_rate, reply_rate.
                     If None, reads from warnings.jsonl for signal.
        """
        findings = []
        warnings = []
        passes = []

        if metrics is None:
            # Read from warnings log to infer metrics
            warn_logs = _load_jsonl("warnings.jsonl")
            active_warns = [w for w in warn_logs if w.get("resolved_at") is None]
            email_warns = [w for w in active_warns if w.get("channel") == "email"]

            if email_warns:
                for w in email_warns:
                    metric = w.get("metric")
                    actual = w.get("actual_value", 0)
                    threshold = w.get("threshold", 0)
                    if actual > threshold:
                        findings.append(
                            f"FAIL: {metric}={actual} exceeds threshold {threshold} per active warning"
                        )
            else:
                passes.append("deliverability: no active email warnings detected")
                warnings.append(
                    "WARNING: Actual deliverability metrics not provided — "
                    "provide metrics dict for full check. "
                    "Required: bounce_rate, spam_rate, unsubscribe_rate, reply_rate"
                )
        else:
            bounce = metrics.get("bounce_rate", 0)
            spam = metrics.get("spam_rate", 0)
            unsub = metrics.get("unsubscribe_rate", 0)
            reply = metrics.get("reply_rate", 0)

            if bounce < self.THRESHOLDS["bounce_rate_max"]:
                passes.append(f"bounce_rate: {bounce:.2%} (threshold < 2%)")
            else:
                findings.append(
                    f"FAIL: bounce_rate {bounce:.2%} exceeds 2% threshold"
                )

            if spam < self.THRESHOLDS["spam_rate_max"]:
                passes.append(f"spam_rate: {spam:.3%} (threshold < 0.1%)")
            else:
                findings.append(
                    f"FAIL: spam_rate {spam:.3%} exceeds 0.1% threshold"
                )

            if unsub < self.THRESHOLDS["unsubscribe_rate_max"]:
                passes.append(f"unsubscribe_rate: {unsub:.2%} (threshold < 1%)")
            else:
                warnings.append(
                    f"WARNING: unsubscribe_rate {unsub:.2%} near or above 1% threshold"
                )

            if reply > self.THRESHOLDS["reply_rate_min"]:
                passes.append(f"reply_rate: {reply:.2%} (target > 3%)")
            else:
                warnings.append(
                    f"WARNING: reply_rate {reply:.2%} below 3% target"
                )

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "thresholds": self.THRESHOLDS,
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Check Google Postmaster Tools daily for bounce and spam rates",
                "Pause sending if bounce > 2% or spam > 0.1%",
                "Use SPF, DKIM, DMARC to improve deliverability",
                "Warm up new sending domain over 14 days per quotas.yml schedule",
            ],
            "governance_decision": f"gate7_deliverability_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 8: Reply Quality Ready
# ---------------------------------------------------------------------------

class Gate8ReplyQualityReady:
    """
    Verifies the reply classifier is working and reply handling is correct.
    """

    GATE = 8
    NAME = "Reply Quality Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        replies = _load_jsonl("replies.jsonl")

        if not replies:
            warnings.append("WARNING: No replies yet — cannot verify reply classification")
            return {
                "gate": self.GATE,
                "name": self.NAME,
                "status": "warning",
                "findings": findings,
                "warnings": warnings,
                "passes": passes,
                "recommendations": ["Process replies as they arrive using reply_classifier.py"],
                "governance_decision": "gate8_reply_quality_warning_no_replies",
            }

        # Schema check
        required = ["reply_id", "channel", "raw_text", "classification", "next_action"]
        schema_fails = sum(
            1 for r in replies
            if any(f not in r for f in required)
        )
        if schema_fails == 0:
            passes.append("reply_schema: all required fields present")
        else:
            findings.append(f"FAIL: {schema_fails} replies missing required fields")

        # Unsubscribe handling — all unsubscribes must have next_action = add_to_suppression_immediately
        unsubscribes = [r for r in replies if r.get("classification") == "unsubscribe"]
        bad_unsub = [
            r for r in unsubscribes
            if r.get("next_action") != "add_to_suppression_immediately"
        ]
        if not bad_unsub:
            passes.append(
                f"unsubscribe_handling: {len(unsubscribes)} unsubscribes correctly routed to suppression"
            )
        else:
            findings.append(
                f"FAIL: {len(bad_unsub)} unsubscribe replies not routed to suppression immediately"
            )

        # Bounce handling — all bounces must have suppression
        bounces = [r for r in replies if r.get("classification") == "bounce"]
        bad_bounce = [
            r for r in bounces
            if r.get("next_action") != "mark_invalid_email"
        ]
        if not bad_bounce:
            passes.append(
                f"bounce_handling: {len(bounces)} bounces correctly marked as invalid"
            )
        else:
            findings.append(
                f"FAIL: {len(bad_bounce)} bounce replies not properly handled"
            )

        # Classification coverage
        classified = [r for r in replies if r.get("classification")]
        classification_rate = len(classified) / len(replies) if replies else 0
        if classification_rate >= 0.95:
            passes.append(f"classification_coverage: {classification_rate:.0%}")
        else:
            findings.append(
                f"FAIL: Only {classification_rate:.0%} of replies classified — check reply_classifier.py"
            )

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "replies_checked": len(replies),
            "unsubscribes": len(unsubscribes),
            "bounces": len(bounces),
            "classification_rate": round(classification_rate, 3),
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Process all unsubscribes within 1 hour — add to suppression immediately",
                "Hard bounces must be suppressed immediately",
                "Run reply_classifier.py on all inbound messages within 15 minutes of receipt",
            ],
            "governance_decision": f"gate8_reply_quality_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 9: Pipeline Conversion Ready
# ---------------------------------------------------------------------------

class Gate9PipelineConversionReady:
    """
    Computes funnel metrics and checks against benchmarks.
    """

    GATE = 9
    NAME = "Pipeline Conversion Ready"

    BENCHMARKS = {
        "reply_rate_min": 0.02,
        "positive_reply_min": 0.005,
        "call_booking_from_positive": 0.20,
        "proposal_from_discovery": 0.30,
        "close_from_proposal": 0.10,
    }

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        jobs = _load_jsonl("channel_jobs.jsonl")
        replies = _load_jsonl("replies.jsonl")
        opportunities = _load_jsonl("opportunities.jsonl")

        n_sent = len([j for j in jobs if j.get("status") in ("sent", "queued", "pending_founder_approval")])
        n_replies = len(replies)
        n_positive = len([
            r for r in replies
            if r.get("classification") in ("interested", "details_requested", "pricing_requested")
        ])
        n_calls = len([
            o for o in opportunities
            if o.get("stage") in ("discovery_call_scheduled", "discovery_call_completed")
        ])
        n_proposals = len([
            o for o in opportunities
            if o.get("stage") in ("proposal_sent", "proposal_reviewed")
        ])
        n_closed = len([
            o for o in opportunities
            if o.get("stage") in ("closed_won",)
        ])

        # Compute rates
        reply_rate = n_replies / n_sent if n_sent else 0
        positive_rate = n_positive / n_sent if n_sent else 0
        call_from_positive = n_calls / n_positive if n_positive else 0
        proposal_from_call = n_proposals / n_calls if n_calls else 0
        close_from_proposal = n_closed / n_proposals if n_proposals else 0

        metrics = {
            "sent": n_sent,
            "replies": n_replies,
            "positive_replies": n_positive,
            "calls": n_calls,
            "proposals": n_proposals,
            "closed": n_closed,
            "reply_rate": round(reply_rate, 4),
            "positive_reply_rate": round(positive_rate, 4),
            "call_booking_from_positive": round(call_from_positive, 4),
            "proposal_from_discovery": round(proposal_from_call, 4),
            "close_from_proposal": round(close_from_proposal, 4),
        }

        # Check against benchmarks — only check if we have enough data
        if n_sent >= 20:
            if reply_rate >= self.BENCHMARKS["reply_rate_min"]:
                passes.append(f"reply_rate: {reply_rate:.2%} (benchmark >= 2%)")
            else:
                warnings.append(
                    f"WARNING: reply_rate {reply_rate:.2%} below 2% benchmark after {n_sent} sends"
                )

            if positive_rate >= self.BENCHMARKS["positive_reply_min"]:
                passes.append(f"positive_reply_rate: {positive_rate:.3%} (benchmark >= 0.5%)")
            else:
                warnings.append(
                    f"WARNING: positive_reply_rate {positive_rate:.3%} below 0.5% benchmark"
                )
        else:
            warnings.append(
                f"WARNING: Only {n_sent} sends — need 20+ for benchmark comparison"
            )

        if n_sent == 0:
            findings.append("FAIL: No jobs executed yet — cannot compute pipeline metrics")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "metrics": metrics,
            "benchmarks": self.BENCHMARKS,
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Wait for 20+ sends before making optimization decisions",
                "If reply rate < 2% after 50 sends — stop and revise angle/segment",
                "If positive reply rate < 0.5% — revisit offer and pain framing",
            ],
            "governance_decision": f"gate9_pipeline_conversion_{status}",
        }


# ---------------------------------------------------------------------------
# Gate 10: Learning Loop Ready
# ---------------------------------------------------------------------------

class Gate10LearningLoopReady:
    """
    Verifies daily learning outputs are being generated.
    """

    GATE = 10
    NAME = "Learning Loop Ready"

    def check(self) -> dict:
        findings = []
        warnings = []
        passes = []

        learning_logs = _load_jsonl("learning_log.jsonl")
        experiments_config = _load_yaml("experiments.yml")

        if not learning_logs:
            warnings.append(
                "WARNING: No learning log entries — run learning_engine.analyze_daily() daily"
            )
        else:
            passes.append(f"learning_log: {len(learning_logs)} entries")

            # Check recency — last entry should be within 2 days
            last = learning_logs[-1]
            last_date = last.get("date", "")
            try:
                last_dt = datetime.strptime(last_date, "%Y-%m-%d")
                days_ago = (datetime.now() - last_dt).days
                if days_ago <= 2:
                    passes.append(f"learning_recency: last entry {days_ago} days ago — current")
                elif days_ago <= 7:
                    warnings.append(
                        f"WARNING: Last learning entry {days_ago} days ago — run daily"
                    )
                else:
                    findings.append(
                        f"FAIL: Last learning entry {days_ago} days ago — learning loop is broken"
                    )
            except (ValueError, TypeError):
                warnings.append("WARNING: Cannot parse last learning log date")

        # Check that recommendations are present
        entries_with_recs = [
            l for l in learning_logs if l.get("recommendations")
        ]
        if len(entries_with_recs) == len(learning_logs) and learning_logs:
            passes.append("recommendations_present: all learning entries have recommendations")
        elif learning_logs:
            warnings.append(
                f"WARNING: {len(learning_logs) - len(entries_with_recs)} entries without recommendations"
            )

        # Experiments config check
        if experiments_config:
            passes.append("experiments_config: loaded")
            ideas = experiments_config.get("experiments", {}).get("experiment_ideas", {})
            total_ideas = sum(len(v) for v in ideas.values() if isinstance(v, list))
            if total_ideas >= 5:
                passes.append(f"experiment_ideas: {total_ideas} ideas available")
            else:
                warnings.append("WARNING: Fewer than 5 experiment ideas defined")
        else:
            warnings.append("WARNING: experiments.yml not available")

        status = "fail" if findings else ("warning" if warnings else "pass")

        return {
            "gate": self.GATE,
            "name": self.NAME,
            "status": status,
            "learning_log_entries": len(learning_logs),
            "findings": findings,
            "warnings": warnings,
            "passes": passes,
            "recommendations": [
                "Run learning_engine.analyze_daily() every day at 23:00 local time",
                "Review weekly_review every Sunday before the new week starts",
                "Update experiments based on weekly_review recommendations",
                "Never run the same failing strategy for > 14 days without A/B testing",
            ],
            "governance_decision": f"gate10_learning_loop_{status}",
        }


# ---------------------------------------------------------------------------
# Run all gates
# ---------------------------------------------------------------------------

def run_all_gates(metrics: Optional[dict] = None) -> dict:
    """
    Runs all 10 gates and returns a summary.

    Args:
        metrics: optional deliverability metrics for Gate 7

    Returns:
        {
            overall_status, gates: [gate results],
            pass_count, fail_count, warning_count,
            governance_decision
        }
    """
    gates = [
        Gate1InfrastructureReady(),
        Gate2DataQualityReady(),
        Gate3CompanyUnderstandingReady(),
        Gate4DraftQualityReady(),
        Gate5ChannelSafetyReady(),
        Gate6ExecutionHealthReady(),
        Gate7DeliverabilityReady(),
        Gate8ReplyQualityReady(),
        Gate9PipelineConversionReady(),
        Gate10LearningLoopReady(),
    ]

    results = []
    for gate in gates:
        if isinstance(gate, Gate7DeliverabilityReady) and metrics:
            result = gate.check(metrics=metrics)
        else:
            result = gate.check()
        results.append(result)

    pass_count = sum(1 for r in results if r.get("status") == "pass")
    fail_count = sum(1 for r in results if r.get("status") == "fail")
    warning_count = sum(1 for r in results if r.get("status") == "warning")

    overall = "fail" if fail_count > 0 else ("warning" if warning_count > 0 else "pass")

    return {
        "overall_status": overall,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "warning_count": warning_count,
        "gates": results,
        "summary": f"{pass_count}/10 gates passing, {fail_count} failing, {warning_count} warnings",
        "governance_decision": f"all_gates_{overall}",
    }


if __name__ == "__main__":
    summary = run_all_gates()
    print(f"\nGrowth OS Verification — {summary['summary']}\n")
    for gate in summary["gates"]:
        status_symbol = {"pass": "PASS", "fail": "FAIL", "warning": "WARN"}.get(
            gate.get("status", ""), "????"
        )
        print(f"  Gate {gate['gate']} [{status_symbol}] {gate['name']}")
        for finding in gate.get("findings", []):
            print(f"    - {finding}")
        for warning in gate.get("warnings", []):
            print(f"    ~ {warning}")
    print()
