"""
founder_dashboard.py — Dealix Growth OS
Six dashboard screens + daily brief generator for the founder.

Screens:
  1. Growth Production
  2. Channel Execution
  3. Health & Risk
  4. Sales Pipeline
  5. Segment Performance
  6. Founder Actions Today

All data is read from memory/ JSONL files. No external API calls.
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

_BASE = Path(__file__).parent
_MEMORY = _BASE / "memory"


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


def _today_str(date: Optional[str] = None) -> str:
    if date:
        return date
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class FounderDashboard:
    """
    Aggregates data from memory/ JSONL files and presents
    founder-ready views of the Growth OS pipeline.
    """

    def get_growth_production(self, date: Optional[str] = None) -> dict:
        """
        Screen 1: Growth Production
        Shows what the system produced today — companies researched,
        drafts created, jobs queued.
        """
        d = _today_str(date)
        briefs = _load_jsonl("company_briefs.jsonl")
        assets = _load_jsonl("channel_assets.jsonl")
        jobs = _load_jsonl("channel_jobs.jsonl")
        leads = _load_jsonl("raw_leads.jsonl")

        today_briefs = [b for b in briefs if b.get("created_at", "").startswith(d)]
        today_assets = [a for a in assets if a.get("created_at", "").startswith(d)]
        today_jobs = [j for j in jobs if j.get("scheduled_at", "").startswith(d)]
        today_leads = [l for l in leads if l.get("discovered_at", "").startswith(d)]

        ready_assets = [a for a in today_assets if a.get("decision") == "ready"]
        review_assets = [a for a in today_assets if a.get("decision") == "founder_review"]

        return {
            "screen": "growth_production",
            "date": d,
            "new_leads_discovered": len(today_leads),
            "company_briefs_completed": len(today_briefs),
            "drafts_created": len(today_assets),
            "drafts_ready_auto_send": len(ready_assets),
            "drafts_pending_founder_review": len(review_assets),
            "jobs_queued": len(today_jobs),
            "governance_decision": "growth_production_dashboard_read_only",
        }

    def get_channel_execution(self, date: Optional[str] = None) -> dict:
        """
        Screen 2: Channel Execution
        Shows what was actually sent, by channel, and current mode.
        """
        d = _today_str(date)
        logs = _load_jsonl("execution_logs.jsonl")
        jobs = _load_jsonl("channel_jobs.jsonl")

        today_logs = [l for l in logs if l.get("event_at", "").startswith(d)]

        by_channel: dict[str, dict] = {}
        for log in today_logs:
            ch = log.get("channel", "unknown")
            if ch not in by_channel:
                by_channel[ch] = {"sent": 0, "queued": 0, "paused": 0, "rejected": 0}
            event = log.get("event_type", "")
            if "sent" in event:
                by_channel[ch]["sent"] += 1
            elif "queued" in event:
                by_channel[ch]["queued"] += 1
            elif "paused" in event:
                by_channel[ch]["paused"] += 1
            elif "rejected" in event:
                by_channel[ch]["rejected"] += 1

        pending_approval = [
            j for j in jobs
            if j.get("status") == "pending_founder_approval"
        ]

        return {
            "screen": "channel_execution",
            "date": d,
            "by_channel": by_channel,
            "pending_founder_approval": len(pending_approval),
            "pending_items": [
                {
                    "job_id": j.get("job_id"),
                    "channel": j.get("channel"),
                    "company_id": j.get("company_id"),
                    "mode": j.get("execution_mode"),
                }
                for j in pending_approval[:10]
            ],
            "governance_decision": "channel_execution_dashboard_read_only",
        }

    def get_health_risk(self, date: Optional[str] = None) -> dict:
        """
        Screen 3: Health and Risk
        Shows current channel health signals and active warnings.
        """
        d = _today_str(date)
        warnings = _load_jsonl("warnings.jsonl")

        active_warnings = [w for w in warnings if w.get("resolved_at") is None]
        high_severity = [w for w in active_warnings if w.get("severity") == "high"]
        medium_severity = [w for w in active_warnings if w.get("severity") == "medium"]

        risk_level = "green"
        if high_severity:
            risk_level = "red"
        elif medium_severity:
            risk_level = "yellow"

        return {
            "screen": "health_risk",
            "date": d,
            "overall_risk_level": risk_level,
            "active_warnings": len(active_warnings),
            "high_severity_warnings": len(high_severity),
            "medium_severity_warnings": len(medium_severity),
            "warnings": active_warnings[:10],
            "recommended_action": (
                "PAUSE and review immediately"
                if risk_level == "red"
                else "Monitor closely"
                if risk_level == "yellow"
                else "All systems normal"
            ),
            "governance_decision": "health_risk_dashboard_read_only",
        }

    def get_sales_pipeline(self, date: Optional[str] = None) -> dict:
        """
        Screen 4: Sales Pipeline
        Shows opportunities by stage and estimated pipeline value.
        """
        d = _today_str(date)
        opps = _load_jsonl("opportunities.jsonl")
        replies = _load_jsonl("replies.jsonl")

        stages: dict[str, list] = {}
        total_pipeline_sar = 0.0
        for opp in opps:
            stage = opp.get("stage", "unknown")
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(opp)
            est = opp.get("estimated_value_sar", 0)
            prob = opp.get("probability", 0.0)
            total_pipeline_sar += est * prob

        recent_replies = [
            r for r in replies
            if r.get("received_at", "").startswith(d[:7])
        ]
        positive_replies = [
            r for r in recent_replies
            if r.get("classification") in ("interested", "details_requested", "pricing_requested")
        ]

        return {
            "screen": "sales_pipeline",
            "date": d,
            "total_opportunities": len(opps),
            "total_pipeline_value_sar_weighted": round(total_pipeline_sar, 2),
            "by_stage": {
                stage: len(items) for stage, items in stages.items()
            },
            "recent_positive_replies": len(positive_replies),
            "opportunities_needing_action": [
                {
                    "opp_id": o.get("opp_id"),
                    "company_id": o.get("company_id"),
                    "stage": o.get("stage"),
                    "next_action": o.get("next_action"),
                    "last_activity": o.get("last_activity"),
                }
                for o in opps
                if o.get("next_action")
            ][:10],
            "governance_decision": "sales_pipeline_dashboard_read_only",
        }

    def get_segment_performance(self, date: Optional[str] = None) -> dict:
        """
        Screen 5: Segment Performance
        Shows reply rates and pipeline by sector and country.
        """
        d = _today_str(date)
        briefs = _load_jsonl("company_briefs.jsonl")
        replies = _load_jsonl("replies.jsonl")
        jobs = _load_jsonl("channel_jobs.jsonl")

        # Group jobs by sector (via company brief lookup)
        brief_by_company: dict[str, dict] = {b.get("company_id"): b for b in briefs}

        sector_stats: dict[str, dict] = {}
        for job in jobs:
            co_id = job.get("company_id", "")
            brief = brief_by_company.get(co_id, {})
            sector = brief.get("sector", "unknown")
            country = brief.get("country", "unknown")
            key = f"{sector}:{country}"
            if key not in sector_stats:
                sector_stats[key] = {
                    "sector": sector,
                    "country": country,
                    "jobs": 0,
                    "replies": 0,
                    "positive_replies": 0,
                }
            sector_stats[key]["jobs"] += 1

        for reply in replies:
            co_id = reply.get("company_id", "")
            brief = brief_by_company.get(co_id, {})
            sector = brief.get("sector", "unknown")
            country = brief.get("country", "unknown")
            key = f"{sector}:{country}"
            if key in sector_stats:
                sector_stats[key]["replies"] += 1
                if reply.get("classification") in ("interested", "details_requested"):
                    sector_stats[key]["positive_replies"] += 1

        # Compute reply rates
        for key, stats in sector_stats.items():
            jobs_count = stats["jobs"]
            stats["reply_rate"] = round(
                stats["replies"] / jobs_count if jobs_count > 0 else 0.0, 3
            )
            stats["positive_reply_rate"] = round(
                stats["positive_replies"] / jobs_count if jobs_count > 0 else 0.0, 3
            )

        # Sort by positive reply rate
        sorted_segments = sorted(
            sector_stats.values(),
            key=lambda x: x["positive_reply_rate"],
            reverse=True,
        )

        return {
            "screen": "segment_performance",
            "date": d,
            "segments": sorted_segments,
            "best_segment": sorted_segments[0] if sorted_segments else None,
            "worst_segment": sorted_segments[-1] if sorted_segments else None,
            "governance_decision": "segment_performance_dashboard_read_only",
        }

    def get_founder_actions_today(self, date: Optional[str] = None) -> list:
        """
        Screen 6: Founder Actions Today
        Returns a prioritized list of actions the founder must take.
        """
        d = _today_str(date)
        jobs = _load_jsonl("channel_jobs.jsonl")
        warnings = _load_jsonl("warnings.jsonl")
        opps = _load_jsonl("opportunities.jsonl")

        actions = []

        # High severity warnings
        active_warnings = [w for w in warnings if w.get("resolved_at") is None]
        high_warnings = [w for w in active_warnings if w.get("severity") == "high"]
        for w in high_warnings:
            actions.append({
                "priority": 1,
                "action": f"RESOLVE warning: {w.get('channel')} {w.get('metric')} at {w.get('actual_value')}",
                "type": "warning",
                "urgency": "critical",
                "ref": w.get("warning_id"),
            })

        # Pending founder approval jobs
        pending = [j for j in jobs if j.get("status") == "pending_founder_approval"]
        if pending:
            actions.append({
                "priority": 2,
                "action": f"Review and approve {len(pending)} outreach draft(s) in outputs/founder_review/",
                "type": "approval",
                "urgency": "high",
                "count": len(pending),
            })

        # Opportunities with next_action
        hot_opps = [
            o for o in opps
            if o.get("stage") in (
                "discovery_call_requested", "pricing_shared", "founder_escalation_required"
            )
        ]
        for opp in hot_opps[:5]:
            actions.append({
                "priority": 3,
                "action": f"Follow up on opportunity {opp.get('opp_id')}: {opp.get('next_action')}",
                "type": "sales_follow_up",
                "urgency": "high",
                "ref": opp.get("opp_id"),
            })

        # Default: check learning log
        if not actions:
            actions.append({
                "priority": 5,
                "action": "Review today's learning log and approve tomorrow's outreach plan",
                "type": "review",
                "urgency": "medium",
            })

        # Sort by priority
        actions.sort(key=lambda x: x["priority"])
        return actions

    def generate_daily_brief(self, date: Optional[str] = None) -> str:
        """
        Generates a bilingual (Arabic + English) daily brief.
        Returns a markdown string — NOT written to file.
        """
        d = _today_str(date)
        prod = self.get_growth_production(d)
        exec_ = self.get_channel_execution(d)
        health = self.get_health_risk(d)
        pipeline = self.get_sales_pipeline(d)
        actions = self.get_founder_actions_today(d)

        risk_ar = {
            "green": "جيد — لا تحذيرات نشطة",
            "yellow": "تحذير — مراقبة مستمرة",
            "red": "خطر — إجراء فوري مطلوب",
        }.get(health.get("overall_risk_level", "green"), "")

        risk_en = health.get("recommended_action", "All systems normal")

        brief = f"""# Dealix Daily Brief — {d}
# ملخص ديليكس اليومي — {d}

---

## Growth Production / الإنتاج اليومي

| Metric | Value |
|--------|-------|
| New Leads / عملاء محتملون جدد | {prod.get('new_leads_discovered', 0)} |
| Briefs Completed / ملخصات مكتملة | {prod.get('company_briefs_completed', 0)} |
| Drafts Created / مسودات أُنشئت | {prod.get('drafts_created', 0)} |
| Ready to Send / جاهزة للإرسال | {prod.get('drafts_ready_auto_send', 0)} |
| Pending Founder Review / تنتظر موافقة المؤسس | {prod.get('drafts_pending_founder_review', 0)} |

---

## Channel Health / صحة القنوات

**Risk Level / مستوى الخطر:** {health.get('overall_risk_level', 'green').upper()}

EN: {risk_en}
AR: {risk_ar}

Active Warnings / تحذيرات نشطة: {health.get('active_warnings', 0)}

---

## Sales Pipeline / خط المبيعات

| Metric | Value |
|--------|-------|
| Open Opportunities / الفرص المفتوحة | {pipeline.get('total_opportunities', 0)} |
| Weighted Pipeline (SAR) / القيمة المرجحة (ريال) | {pipeline.get('total_pipeline_value_sar_weighted', 0.0)} |
| Positive Replies This Month / ردود إيجابية هذا الشهر | {pipeline.get('recent_positive_replies', 0)} |
| Pending Founder Approval / تنتظر موافقة المؤسس | {exec_.get('pending_founder_approval', 0)} |

---

## Founder Actions Today / إجراءات المؤسس اليوم

"""
        for i, action in enumerate(actions, 1):
            brief += f"{i}. [{action.get('urgency', '').upper()}] {action.get('action')}\n"

        brief += """
---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""
        return brief
