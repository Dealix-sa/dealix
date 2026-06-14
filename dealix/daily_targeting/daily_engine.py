"""Daily targeting engine — runs every morning.

Scores accounts → picks top 10 → composes personalised Arabic emails →
queues as Gmail drafts (or prints in dry-run mode).

Usage:
    engine = DailyTargetingEngine(dry_run=True)
    report = engine.run()
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from dealix.daily_targeting.email_composer import EmailComposer
from dealix.launch_os.icp_scorer import ICPScore, batch_score

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sample accounts — 20 realistic Saudi businesses across 4 sectors
# ---------------------------------------------------------------------------

SAMPLE_ACCOUNTS: list[dict[str, Any]] = [
    # --- Real estate (5) ---
    {
        "account_id": "re_001",
        "company_name": "الحلول العقارية الرائدة",
        "company_name_en": "Leading Real Estate Solutions",
        "contact_name": "محمد العتيبي",
        "email": "m.otaibi@leading-re.sa",
        "sector": "real_estate",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 15000,
        "pain_signals": ["slow_lead_response", "no_crm", "agent_tracking_manual"],
        "urgency": "high",
        "revenue_leak_sar": 250000,
        "process_chaos_score": 12,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 7,
        "budget_signal": "likely",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "re_002",
        "company_name": "بيوت جدة للعقارات",
        "company_name_en": "Jeddah Homes Real Estate",
        "contact_name": "خالد الزهراني",
        "email": "k.zahrani@byootjeddah.sa",
        "sector": "real_estate",
        "region": "جدة",
        "size": "smb",
        "estimated_budget_sar": 8000,
        "pain_signals": ["data_silos", "manual_follow_up"],
        "urgency": "medium",
        "revenue_leak_sar": 120000,
        "process_chaos_score": 9,
        "decision_maker_access": "champion",
        "start_small_score": 9,
        "proof_speed_score": 8,
        "budget_signal": "possible",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "re_003",
        "company_name": "الشرقية للتطوير العقاري",
        "company_name_en": "Eastern Province Real Estate Development",
        "contact_name": "فيصل الدوسري",
        "email": "f.dosari@sharqiya-dev.sa",
        "sector": "real_estate",
        "region": "الدمام",
        "size": "mid_market",
        "estimated_budget_sar": 25000,
        "pain_signals": ["agent_tracking", "reporting_manual", "lead_loss"],
        "urgency": "high",
        "revenue_leak_sar": 400000,
        "process_chaos_score": 14,
        "decision_maker_access": "direct",
        "start_small_score": 7,
        "proof_speed_score": 8,
        "budget_signal": "confirmed",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "re_004",
        "company_name": "نخيل الرياض العقارية",
        "company_name_en": "Riyadh Palms Properties",
        "contact_name": "عبدالله السبيعي",
        "email": "a.subai@nakheel-riyadh.sa",
        "sector": "real_estate",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 6000,
        "pain_signals": ["slow_lead_response", "data_silos"],
        "urgency": "medium",
        "revenue_leak_sar": 80000,
        "process_chaos_score": 7,
        "decision_maker_access": "gatekeeper",
        "start_small_score": 9,
        "proof_speed_score": 9,
        "budget_signal": "possible",
        "referral_potential_score": 2,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "re_005",
        "company_name": "واحة الخليج للعقارات",
        "company_name_en": "Gulf Oasis Real Estate",
        "contact_name": "نورة الشمري",
        "email": "n.shamri@gulf-oasis.sa",
        "sector": "real_estate",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 10000,
        "pain_signals": ["no_crm", "manual_follow_up", "agent_tracking"],
        "urgency": "high",
        "revenue_leak_sar": 180000,
        "process_chaos_score": 11,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 7,
        "budget_signal": "likely",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    # --- Medical (5) ---
    {
        "account_id": "med_001",
        "company_name": "مركز نبض الصحة الطبي",
        "company_name_en": "Pulse Health Medical Center",
        "contact_name": "أحمد القحطاني",
        "email": "a.qahtani@pulse-health.sa",
        "sector": "medical",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 12000,
        "pain_signals": ["appointment_noshows", "manual_reminders", "patient_data_chaos"],
        "urgency": "high",
        "revenue_leak_sar": 200000,
        "process_chaos_score": 13,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 9,
        "budget_signal": "likely",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "med_002",
        "company_name": "عيادات الشفاء التخصصية",
        "company_name_en": "Al-Shifa Specialty Clinics",
        "contact_name": "سارة المالكي",
        "email": "s.maliki@shifa-clinics.sa",
        "sector": "medical",
        "region": "جدة",
        "size": "mid_market",
        "estimated_budget_sar": 20000,
        "pain_signals": ["no_patient_followup_system", "paper_records", "noshows"],
        "urgency": "critical",
        "revenue_leak_sar": 350000,
        "process_chaos_score": 15,
        "decision_maker_access": "direct",
        "start_small_score": 7,
        "proof_speed_score": 8,
        "budget_signal": "confirmed",
        "referral_potential_score": 5,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "med_003",
        "company_name": "مجمع الراحة الطبي",
        "company_name_en": "Al-Raha Medical Complex",
        "contact_name": "عمر البلوي",
        "email": "o.balawi@raha-medical.sa",
        "sector": "medical",
        "region": "الدمام",
        "size": "smb",
        "estimated_budget_sar": 8000,
        "pain_signals": ["appointment_noshows", "manual_reminders"],
        "urgency": "medium",
        "revenue_leak_sar": 100000,
        "process_chaos_score": 8,
        "decision_maker_access": "champion",
        "start_small_score": 9,
        "proof_speed_score": 8,
        "budget_signal": "possible",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "med_004",
        "company_name": "عيادة الأمل للأسنان",
        "company_name_en": "Amal Dental Clinic",
        "contact_name": "ريم العصيمي",
        "email": "r.osaimi@amal-dental.sa",
        "sector": "medical",
        "region": "الرياض",
        "size": "micro",
        "estimated_budget_sar": 3000,
        "pain_signals": ["manual_appointment_booking", "noshows"],
        "urgency": "low",
        "revenue_leak_sar": 40000,
        "process_chaos_score": 5,
        "decision_maker_access": "direct",
        "start_small_score": 10,
        "proof_speed_score": 9,
        "budget_signal": "unlikely",
        "referral_potential_score": 2,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "med_005",
        "company_name": "مركز الحياة للطب الباطني",
        "company_name_en": "Al-Hayat Internal Medicine Center",
        "contact_name": "يوسف الحربي",
        "email": "y.harbi@hayat-med.sa",
        "sector": "medical",
        "region": "جدة",
        "size": "smb",
        "estimated_budget_sar": 10000,
        "pain_signals": ["patient_data_chaos", "manual_follow_up", "noshows"],
        "urgency": "high",
        "revenue_leak_sar": 160000,
        "process_chaos_score": 11,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 7,
        "budget_signal": "likely",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    # --- Training institutes (5) ---
    {
        "account_id": "trn_001",
        "company_name": "أكاديمية المهارات المتقدمة",
        "company_name_en": "Advanced Skills Academy",
        "contact_name": "سلطان الغامدي",
        "email": "s.ghamdi@advanced-skills.sa",
        "sector": "training",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 12000,
        "pain_signals": ["enrollment_dropoff", "manual_reporting", "trainee_dropout"],
        "urgency": "high",
        "revenue_leak_sar": 220000,
        "process_chaos_score": 12,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 7,
        "budget_signal": "likely",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "trn_002",
        "company_name": "معهد القيادة الاحترافية",
        "company_name_en": "Professional Leadership Institute",
        "contact_name": "منى العمري",
        "email": "m.omari@pl-institute.sa",
        "sector": "training",
        "region": "جدة",
        "size": "mid_market",
        "estimated_budget_sar": 18000,
        "pain_signals": ["reporting_gaps", "no_attendance_tracking", "dropout_rate"],
        "urgency": "high",
        "revenue_leak_sar": 300000,
        "process_chaos_score": 13,
        "decision_maker_access": "direct",
        "start_small_score": 7,
        "proof_speed_score": 8,
        "budget_signal": "confirmed",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "trn_003",
        "company_name": "مركز التميز للتدريب التقني",
        "company_name_en": "Excellence Center for Technical Training",
        "contact_name": "بندر الرشيدي",
        "email": "b.rashidi@excellence-tech.sa",
        "sector": "training",
        "region": "الدمام",
        "size": "smb",
        "estimated_budget_sar": 7000,
        "pain_signals": ["manual_reporting", "enrollment_dropoff"],
        "urgency": "medium",
        "revenue_leak_sar": 90000,
        "process_chaos_score": 8,
        "decision_maker_access": "champion",
        "start_small_score": 9,
        "proof_speed_score": 8,
        "budget_signal": "possible",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
        "notes": "",
    },
    {
        "account_id": "trn_004",
        "company_name": "أكاديمية الريادة الرقمية",
        "company_name_en": "Digital Leadership Academy",
        "contact_name": "لمياء الحمدان",
        "email": "l.hamdan@digital-lead-academy.sa",
        "sector": "training",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 9000,
        "pain_signals": ["reporting_gaps", "trainee_followup_manual"],
        "urgency": "medium",
        "revenue_leak_sar": 70000,
        "process_chaos_score": 7,
        "decision_maker_access": "direct",
        "start_small_score": 9,
        "proof_speed_score": 9,
        "budget_signal": "possible",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "trn_005",
        "company_name": "كلية الإدارة والأعمال الخاصة",
        "company_name_en": "Private College of Management and Business",
        "contact_name": "عادل الشهري",
        "email": "a.shahri@pcmb.sa",
        "sector": "training",
        "region": "الرياض",
        "size": "mid_market",
        "estimated_budget_sar": 22000,
        "pain_signals": ["enrollment_dropoff", "reporting_gaps", "no_early_warning"],
        "urgency": "high",
        "revenue_leak_sar": 380000,
        "process_chaos_score": 14,
        "decision_maker_access": "direct",
        "start_small_score": 7,
        "proof_speed_score": 7,
        "budget_signal": "confirmed",
        "referral_potential_score": 5,
        "compliance_risk_penalty": 0,
    },
    # --- Marketing agencies (5) ---
    {
        "account_id": "mkt_001",
        "company_name": "وكالة الإبداع الرقمي",
        "company_name_en": "Digital Creativity Agency",
        "contact_name": "تركي الفهد",
        "email": "t.fahad@digital-creativity.sa",
        "sector": "marketing_agency",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 15000,
        "pain_signals": ["manual_client_reporting", "roi_unclear", "campaign_tracking_silos"],
        "urgency": "high",
        "revenue_leak_sar": 180000,
        "process_chaos_score": 12,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 9,
        "budget_signal": "likely",
        "referral_potential_score": 4,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "mkt_002",
        "company_name": "ميديا بلص للتسويق",
        "company_name_en": "Media Plus Marketing",
        "contact_name": "رانيا البكري",
        "email": "r.bakri@mediaplus.sa",
        "sector": "marketing_agency",
        "region": "جدة",
        "size": "mid_market",
        "estimated_budget_sar": 25000,
        "pain_signals": ["reporting_manual_12h_weekly", "roi_proof_hard", "multi_platform_chaos"],
        "urgency": "critical",
        "revenue_leak_sar": 320000,
        "process_chaos_score": 15,
        "decision_maker_access": "direct",
        "start_small_score": 7,
        "proof_speed_score": 8,
        "budget_signal": "confirmed",
        "referral_potential_score": 5,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "mkt_003",
        "company_name": "ستراتيجي هب للتسويق",
        "company_name_en": "Strategy Hub Marketing",
        "contact_name": "وليد السلمي",
        "email": "w.salmi@strat-hub.sa",
        "sector": "marketing_agency",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 8000,
        "pain_signals": ["campaign_roi_unclear", "manual_reporting"],
        "urgency": "medium",
        "revenue_leak_sar": 90000,
        "process_chaos_score": 8,
        "decision_maker_access": "champion",
        "start_small_score": 9,
        "proof_speed_score": 9,
        "budget_signal": "possible",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "mkt_004",
        "company_name": "كونتنت لاب للتسويق الرقمي",
        "company_name_en": "Content Lab Digital Marketing",
        "contact_name": "هند الأحمدي",
        "email": "h.ahmadi@contentlab.sa",
        "sector": "marketing_agency",
        "region": "الدمام",
        "size": "smb",
        "estimated_budget_sar": 6000,
        "pain_signals": ["manual_client_reporting", "data_silos"],
        "urgency": "medium",
        "revenue_leak_sar": 60000,
        "process_chaos_score": 7,
        "decision_maker_access": "direct",
        "start_small_score": 9,
        "proof_speed_score": 9,
        "budget_signal": "possible",
        "referral_potential_score": 2,
        "compliance_risk_penalty": 0,
    },
    {
        "account_id": "mkt_005",
        "company_name": "بيرفورمنس بروز للتسويق",
        "company_name_en": "Performance Bros Marketing",
        "contact_name": "كريم الجهني",
        "email": "k.juhani@perfbros.sa",
        "sector": "marketing_agency",
        "region": "الرياض",
        "size": "smb",
        "estimated_budget_sar": 10000,
        "pain_signals": ["roi_reporting_manual", "campaign_tracking_silos", "client_churn"],
        "urgency": "high",
        "revenue_leak_sar": 140000,
        "process_chaos_score": 10,
        "decision_maker_access": "direct",
        "start_small_score": 8,
        "proof_speed_score": 8,
        "budget_signal": "likely",
        "referral_potential_score": 3,
        "compliance_risk_penalty": 0,
    },
]


@dataclass
class TargetEntry:
    """Enriched target with ICP score + composed email."""

    account: dict[str, Any]
    icp_score: int
    tier: str
    action: str
    email: dict[str, Any]
    draft_id: str = ""


@dataclass
class DailyReport:
    """Output of one DailyTargetingEngine run."""

    date: str
    run_at: str
    dry_run: bool
    total_accounts_loaded: int
    total_accounts_scored: int
    top_targets: list[TargetEntry]
    tier_counts: dict[str, int]
    drafts_created: int
    drafts_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "run_at": self.run_at,
            "dry_run": self.dry_run,
            "total_accounts_loaded": self.total_accounts_loaded,
            "total_accounts_scored": self.total_accounts_scored,
            "tier_counts": self.tier_counts,
            "drafts_created": self.drafts_created,
            "drafts_ids": self.drafts_ids,
            "top_targets": [
                {
                    "account_id": t.account["account_id"],
                    "company_name": t.account.get("company_name", ""),
                    "sector": t.account.get("sector", ""),
                    "region": t.account.get("region", ""),
                    "icp_score": t.icp_score,
                    "tier": t.tier,
                    "action": t.action,
                    "email": {
                        "subject": t.email.get("subject", ""),
                        "to_email": t.email.get("to_email", ""),
                        "offer_matched": t.email.get("offer_matched", ""),
                        "pain_points_used": t.email.get("pain_points_used", []),
                    },
                    "draft_id": t.draft_id,
                }
                for t in self.top_targets
            ],
        }


class DailyTargetingEngine:
    """Run every morning: score accounts, pick top 10, compose emails, queue drafts."""

    _REPORTS_DIR = Path(__file__).resolve().parents[3] / "reports" / "daily"
    _MIN_SCORE = 35
    _MAX_DAILY = 10

    def __init__(self, dry_run: bool = True, founder_name: str = "سامي") -> None:
        self.dry_run = dry_run
        self.founder_name = founder_name
        self.date = date.today().isoformat()
        self._composer = EmailComposer()

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> DailyReport:
        """Execute the full daily targeting pipeline."""
        accounts = self._load_accounts()
        scored: list[ICPScore] = self._score_all(accounts)
        account_map = {a["account_id"]: a for a in accounts}
        top10 = self._pick_daily_targets(scored)

        emails = self._compose_emails(top10, account_map)
        draft_ids = self._create_drafts(emails, top10, account_map)

        report = self._build_report(accounts, scored, top10, emails, draft_ids, account_map)
        self._save_report(report)
        return report

    # ------------------------------------------------------------------
    # Step helpers
    # ------------------------------------------------------------------

    def _load_accounts(self) -> list[dict[str, Any]]:
        """Load accounts from targeting CSV; fall back to SAMPLE_ACCOUNTS.

        CSV rows are only included if they have a real company name (not a
        placeholder starting with "REPLACE:") and a contact email field set.
        """
        try:
            from dealix.commercial_ops.targeting_csv import load_targets
            rows = load_targets()
            # Filter out placeholder / template rows
            real_rows = [
                r for r in rows
                if r.get("company", "").strip()
                and not r.get("company", "").startswith("REPLACE:")
                and r.get("contact", "").strip()
                and not r.get("contact", "").startswith("REPLACE:")
            ]
            if real_rows:
                adapted: list[dict[str, Any]] = []
                priority_urgency_map = {"high": "high", "medium": "medium", "low": "low"}
                for i, r in enumerate(real_rows):
                    priority = r.get("priority", "medium").strip().lower()
                    adapted.append({
                        "account_id": f"csv_{i:04d}",
                        "company_name": r.get("company", ""),
                        "contact_name": r.get("contact", ""),
                        "email": "",
                        "sector": r.get("segment", "default"),
                        "region": "",
                        "size": "smb",
                        "estimated_budget_sar": 0,
                        "pain_signals": [r.get("pain_hypothesis", "")],
                        "urgency": priority_urgency_map.get(priority, "medium"),
                        "revenue_leak_sar": 0,
                        "process_chaos_score": 5,
                        "decision_maker_access": "unknown",
                        "start_small_score": 5,
                        "proof_speed_score": 5,
                        "budget_signal": "unknown",
                        "referral_potential_score": 2,
                        "compliance_risk_penalty": 0,
                    })
                log.info("daily_engine: loaded %d real accounts from CSV", len(adapted))
                # Merge with SAMPLE_ACCOUNTS so scoring signals are rich
                return list(SAMPLE_ACCOUNTS) + adapted
        except Exception as exc:
            log.warning("daily_engine: CSV load failed (%s) — using sample accounts", exc)
        return list(SAMPLE_ACCOUNTS)

    def _score_all(self, accounts: list[dict[str, Any]]) -> list[ICPScore]:
        """Batch-score all accounts, sorted descending by total."""
        return batch_score(accounts)

    def _pick_daily_targets(self, scored: list[ICPScore]) -> list[ICPScore]:
        """Return up to MAX_DAILY targets: skip DQ, prefer Tier A then B then C."""
        already_contacted = self._load_contacted_ids()

        tier_order = {"A": 0, "B": 1, "C": 2, "DQ": 3}
        eligible = [
            s for s in scored
            if s.total >= self._MIN_SCORE and s.account_id not in already_contacted
        ]
        eligible.sort(key=lambda s: (tier_order.get(s.tier, 9), -s.total))
        return eligible[: self._MAX_DAILY]

    def _compose_emails(
        self,
        targets: list[ICPScore],
        account_map: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Compose an email dict for each target."""
        emails = []
        for t in targets:
            account = account_map.get(t.account_id, {"account_id": t.account_id})
            email = self._composer.compose(account, t.total, self.founder_name)
            emails.append(email)
        return emails

    def _create_drafts(
        self,
        emails: list[dict[str, Any]],
        targets: list[ICPScore],
        account_map: dict[str, dict[str, Any]],
    ) -> list[str]:
        """Create Gmail drafts (or print in dry-run). Returns list of draft IDs."""
        from auto_client_acquisition.email.gmail_send import is_configured

        if self.dry_run or not is_configured():
            for i, (email, target) in enumerate(zip(emails, targets)):
                account = account_map.get(target.account_id, {})
                company = account.get("company_name", target.account_id)
                print(f"\n--- Draft {i + 1}: {company} (Score {target.total} / Tier {target.tier}) ---")
                print(f"To:      {email.get('to_email', 'N/A')}")
                print(f"Subject: {email.get('subject', '')}")
                print(f"Offer:   {email.get('offer_matched', '')} — {email.get('offer_price', '')}")
                body_preview = email.get("body_ar", "")[:300]
                print(f"Body preview:\n{body_preview}")
                print("---")
            return ["DRY_RUN"] * len(emails)

        # Real draft creation via Gmail API
        draft_ids: list[str] = []
        for email in emails:
            draft_id = asyncio.run(self._create_single_draft(email))
            draft_ids.append(draft_id)
        return draft_ids

    async def _create_single_draft(self, email: dict[str, Any]) -> str:
        from auto_client_acquisition.email.gmail_send import create_draft

        result = await create_draft(
            to_email=email.get("to_email", ""),
            subject=email.get("subject", ""),
            body_plain=email.get("body_ar", ""),
            sender_name=f"{self.founder_name} | Dealix",
        )
        if result.status == "ok":
            log.info("draft_created draft_id=%s", result.draft_id)
            return result.draft_id or "unknown"
        log.warning("draft_failed status=%s error=%s", result.status, result.error)
        return f"ERROR:{result.status}"

    def _build_report(
        self,
        accounts: list[dict[str, Any]],
        scored: list[ICPScore],
        top10: list[ICPScore],
        emails: list[dict[str, Any]],
        draft_ids: list[str],
        account_map: dict[str, dict[str, Any]],
    ) -> DailyReport:
        tier_counts: dict[str, int] = {"A": 0, "B": 0, "C": 0, "DQ": 0}
        for s in scored:
            tier_counts[s.tier] = tier_counts.get(s.tier, 0) + 1

        target_entries: list[TargetEntry] = []
        for i, (t, email) in enumerate(zip(top10, emails)):
            target_entries.append(
                TargetEntry(
                    account=account_map.get(t.account_id, {"account_id": t.account_id}),
                    icp_score=t.total,
                    tier=t.tier,
                    action=t.action,
                    email=email,
                    draft_id=draft_ids[i] if i < len(draft_ids) else "",
                )
            )

        drafts_created = sum(1 for d in draft_ids if d and not d.startswith("ERROR") and d != "DRY_RUN")

        return DailyReport(
            date=self.date,
            run_at=datetime.now(timezone.utc).isoformat(),
            dry_run=self.dry_run,
            total_accounts_loaded=len(accounts),
            total_accounts_scored=len(scored),
            top_targets=target_entries,
            tier_counts=tier_counts,
            drafts_created=drafts_created,
            drafts_ids=draft_ids,
        )

    def _save_report(self, report: DailyReport) -> None:
        """Persist daily report to reports/daily/YYYY-MM-DD.json."""
        self._REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        path = self._REPORTS_DIR / f"{report.date}.json"
        try:
            with path.open("w", encoding="utf-8") as fh:
                json.dump(report.to_dict(), fh, ensure_ascii=False, indent=2)
            log.info("daily_report_saved path=%s", path)
        except Exception as exc:
            log.warning("daily_report_save_failed error=%s", exc)

    def _load_contacted_ids(self) -> set[str]:
        """Return account_ids contacted in the last 7 days (from saved reports)."""
        contacted: set[str] = set()
        if not self._REPORTS_DIR.is_dir():
            return contacted
        try:
            today = date.today()
            for report_file in self._REPORTS_DIR.glob("*.json"):
                try:
                    report_date = date.fromisoformat(report_file.stem)
                except ValueError:
                    continue
                delta = (today - report_date).days
                if 0 < delta <= 7:
                    with report_file.open(encoding="utf-8") as fh:
                        data = json.load(fh)
                    for entry in data.get("top_targets", []):
                        aid = entry.get("account_id", "")
                        if aid:
                            contacted.add(aid)
        except Exception as exc:
            log.warning("load_contacted_ids_failed error=%s", exc)
        return contacted

    # ------------------------------------------------------------------
    # Terminal output helpers
    # ------------------------------------------------------------------

    def print_war_room(self) -> None:
        """Print today's war room briefing to stdout."""
        report = self.run()
        _print_war_room_banner(report)


def _print_war_room_banner(report: DailyReport) -> None:
    """Render the war room banner to stdout."""
    n = len(report.top_targets)
    print("\n" + "=" * 66)
    print("  DEALIX - غرفة القيادة اليومية")
    print(f"  {report.date} | التارجت اليوم: {n} حساب")
    print("=" * 66)

    print("\nTOP TARGETS اليوم:")
    print("-" * 40)

    for i, target in enumerate(report.top_targets, 1):
        company = target.account.get("company_name", target.account.get("account_id", ""))
        sector = target.account.get("sector", "")
        region = target.account.get("region", "")
        pains = target.email.get("pain_points_used", [])
        subject = target.email.get("subject", "")
        draft_note = "مسودة جاهزة في Gmail" if target.draft_id and target.draft_id != "DRY_RUN" else "DRY_RUN"

        print(f"\n{i}. [{company}] - Tier {target.tier} ({target.icp_score}/100) - {sector} - {region}")
        for pain in pains[:1]:
            print(f"   Pain: {pain}")
        print(f"   Subject: {subject}")
        print(f"   {draft_note}")

    tc = report.tier_counts
    print(f"\nملخص اليوم:")
    print(f"   Tier A: {tc.get('A', 0)} | Tier B: {tc.get('B', 0)} | Tier C: {tc.get('C', 0)}")
    print(f"   مسودات Gmail: {report.drafts_created}")

    if report.dry_run:
        print("\n[DRY-RUN] لم يتم إرسال أي رسائل. استخدم --send لإنشاء مسودات Gmail فعلية.")
    else:
        print("\nالخطوة التالية: افتح Gmail -> Drafts -> راجع وأرسل")
    print("=" * 66 + "\n")
