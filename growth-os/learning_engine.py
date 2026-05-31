"""
learning_engine.py — Dealix Growth OS
Analyzes daily results, updates experiments, and generates weekly reviews.

Reads from:
  memory/replies.jsonl
  memory/execution_logs.jsonl
  memory/channel_jobs.jsonl
  memory/company_briefs.jsonl
  memory/learning_log.jsonl

Writes to:
  memory/learning_log.jsonl (appends new entry)
  config/experiments.yml (updates experiment statuses)
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_BASE = Path(__file__).parent
_MEMORY = _BASE / "memory"
_EXPERIMENTS_CONFIG = _BASE / "config" / "experiments.yml"


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


def _append_jsonl(filename: str, record: dict) -> None:
    path = _MEMORY / filename
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


class LearningEngine:
    """
    Analyzes daily performance and generates learning updates.
    All outputs include a governance_decision field.
    """

    def analyze_daily(self, date: Optional[str] = None) -> dict:
        """
        Analyzes daily performance.

        Args:
            date: YYYY-MM-DD string, defaults to today

        Returns:
            {
                date, best_segment, worst_segment,
                reply_rate_overall, positive_reply_rate,
                channel_breakdown, experiment_updates,
                recommendations, governance_decision
            }
        """
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        jobs = _load_jsonl("channel_jobs.jsonl")
        replies = _load_jsonl("replies.jsonl")
        briefs = _load_jsonl("company_briefs.jsonl")

        brief_by_company: dict[str, dict] = {b.get("company_id"): b for b in briefs}

        # Segment analysis
        segment_stats: dict[str, dict] = {}
        for job in jobs:
            co_id = job.get("company_id", "")
            brief = brief_by_company.get(co_id, {})
            sector = brief.get("sector", "unknown")
            country = brief.get("country", "unknown")
            key = f"{sector}:{country}"
            if key not in segment_stats:
                segment_stats[key] = {
                    "sector": sector,
                    "country": country,
                    "jobs": 0,
                    "replies": 0,
                    "positive_replies": 0,
                }
            segment_stats[key]["jobs"] += 1

        for reply in replies:
            co_id = reply.get("company_id", "")
            brief = brief_by_company.get(co_id, {})
            sector = brief.get("sector", "unknown")
            country = brief.get("country", "unknown")
            key = f"{sector}:{country}"
            if key in segment_stats:
                segment_stats[key]["replies"] += 1
                if reply.get("classification") in (
                    "interested", "details_requested", "pricing_requested"
                ):
                    segment_stats[key]["positive_replies"] += 1

        # Compute rates
        for key, stats in segment_stats.items():
            j = stats["jobs"]
            stats["reply_rate"] = round(stats["replies"] / j if j else 0.0, 4)
            stats["positive_reply_rate"] = round(
                stats["positive_replies"] / j if j else 0.0, 4
            )

        sorted_segs = sorted(
            segment_stats.values(),
            key=lambda x: x["positive_reply_rate"],
            reverse=True,
        )

        total_jobs = len(jobs)
        total_replies = len(replies)
        positive_replies = [
            r for r in replies
            if r.get("classification") in (
                "interested", "details_requested", "pricing_requested"
            )
        ]

        reply_rate = round(total_replies / total_jobs if total_jobs else 0.0, 4)
        positive_reply_rate = round(
            len(positive_replies) / total_jobs if total_jobs else 0.0, 4
        )

        recommendations = self._generate_recommendations(
            reply_rate, positive_reply_rate, sorted_segs
        )

        analysis = {
            "date": date,
            "best_segment": sorted_segs[0] if sorted_segs else None,
            "worst_segment": sorted_segs[-1] if sorted_segs else None,
            "reply_rate_overall": reply_rate,
            "positive_reply_rate": positive_reply_rate,
            "total_jobs": total_jobs,
            "total_replies": total_replies,
            "total_positive_replies": len(positive_replies),
            "segment_breakdown": sorted_segs,
            "recommendations": recommendations,
            "governance_decision": "learning_engine_daily_analysis",
        }

        # Generate learning log id and append
        learning_id = f"learn_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        log_entry = {
            "learning_id": learning_id,
            "date": date,
            "best_segment": sorted_segs[0] if sorted_segs else None,
            "worst_segment": sorted_segs[-1] if sorted_segs else None,
            "reply_rate_overall": reply_rate,
            "positive_reply_rate": positive_reply_rate,
            "experiment_updates": [],
            "recommendations": recommendations,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl("learning_log.jsonl", log_entry)

        analysis["learning_id"] = learning_id
        return analysis

    def _generate_recommendations(
        self,
        reply_rate: float,
        positive_reply_rate: float,
        segments: list,
    ) -> list:
        """
        Generates actionable recommendations based on performance metrics.
        """
        recs = []

        if reply_rate < 0.02:
            recs.append(
                "Overall reply rate below 2% threshold — test new subject lines or angles immediately"
            )
        elif reply_rate >= 0.05:
            recs.append(
                "Strong overall reply rate — double outreach volume in best performing segments"
            )

        if positive_reply_rate < 0.005:
            recs.append(
                "Positive reply rate below 0.5% — revisit pain framing and offer relevance"
            )

        if segments:
            best = segments[0]
            worst = segments[-1]
            if best.get("positive_reply_rate", 0) > 0.02:
                recs.append(
                    f"Prioritize {best.get('sector')} in {best.get('country')} — "
                    f"strong positive reply rate of {best.get('positive_reply_rate')}"
                )
            if (
                worst.get("jobs", 0) > 5
                and worst.get("positive_reply_rate", 0) < 0.005
            ):
                recs.append(
                    f"Pause outreach to {worst.get('sector')} in {worst.get('country')} "
                    f"— below 0.5% positive reply rate after {worst.get('jobs')} sends"
                )

        if not recs:
            recs.append("Performance within acceptable range — continue current strategy")

        return recs

    def update_experiments(self, findings: dict) -> list:
        """
        Reviews active experiments and proposes updates based on findings.

        Args:
            findings: dict with segment analysis from analyze_daily()

        Returns:
            list of experiment update dicts
        """
        if not (_HAS_YAML and _EXPERIMENTS_CONFIG.exists()):
            return [{"update": "experiments.yml not available", "governance_decision": "no_update"}]

        with open(_EXPERIMENTS_CONFIG, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        active = config.get("experiments", {}).get("active_experiments", [])
        updates = []

        for exp in active:
            control_replies = exp.get("results", {}).get("control_replies", 0) or 0
            test_replies = exp.get("results", {}).get("test_replies", 0) or 0
            sample_min = exp.get("sample_size_min", 20)
            total_sample = control_replies + test_replies

            if total_sample < sample_min:
                updates.append({
                    "exp_id": exp.get("id"),
                    "update": f"Insufficient data ({total_sample}/{sample_min}) — continue running",
                    "action": "continue",
                    "governance_decision": f"experiment_continue_{exp.get('id')}",
                })
                continue

            # Simple comparison — in production this would use proper stats
            if control_replies > 0 and test_replies > 0:
                ratio = test_replies / control_replies
                if ratio > 1.2:
                    updates.append({
                        "exp_id": exp.get("id"),
                        "update": f"Test variant winning by {round((ratio - 1) * 100)}% — recommend declaring winner",
                        "action": "declare_winner_test",
                        "governance_decision": f"experiment_test_winner_{exp.get('id')}",
                    })
                elif ratio < 0.8:
                    updates.append({
                        "exp_id": exp.get("id"),
                        "update": f"Control variant winning — recommend reverting to control",
                        "action": "declare_winner_control",
                        "governance_decision": f"experiment_control_winner_{exp.get('id')}",
                    })
                else:
                    updates.append({
                        "exp_id": exp.get("id"),
                        "update": "No significant difference yet — extend by 7 days",
                        "action": "extend",
                        "governance_decision": f"experiment_extend_{exp.get('id')}",
                    })

        # Propose new experiments if reply rate is low
        reply_rate = findings.get("reply_rate_overall", 0)
        if reply_rate < 0.02:
            updates.append({
                "exp_id": "proposed_new",
                "update": "Reply rate below 2% — propose new subject line experiment",
                "action": "propose_experiment",
                "proposed_type": "subject_line",
                "governance_decision": "learning_engine_propose_new_experiment",
            })

        return updates

    def generate_weekly_review(self) -> dict:
        """
        Generates a weekly review with 7 reflective questions.

        Returns:
            {
                week_ending, questions_and_answers,
                key_learnings, next_week_priorities,
                governance_decision
            }
        """
        today = datetime.now(timezone.utc)
        week_ending = today.strftime("%Y-%m-%d")

        logs = _load_jsonl("learning_log.jsonl")
        # Last 7 days of logs
        seven_days_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        recent_logs = [
            l for l in logs
            if l.get("date", "") >= seven_days_ago
        ]

        # Aggregate weekly metrics
        total_recommendations = []
        avg_reply_rate = 0.0
        avg_positive_rate = 0.0
        if recent_logs:
            avg_reply_rate = round(
                sum(l.get("reply_rate_overall", 0) for l in recent_logs) / len(recent_logs), 4
            )
            avg_positive_rate = round(
                sum(l.get("positive_reply_rate", 0) for l in recent_logs) / len(recent_logs), 4
            )
            for log in recent_logs:
                total_recommendations.extend(log.get("recommendations", []))

        questions_and_answers = [
            {
                "q1": "What was the best performing segment this week?",
                "q1_ar": "ما كان أفضل شريحة أداءً هذا الأسبوع؟",
                "answer": (
                    recent_logs[-1].get("best_segment")
                    if recent_logs else "Insufficient data"
                ),
            },
            {
                "q2": "What is the current overall reply rate vs. 2% target?",
                "q2_ar": "ما معدل الرد الحالي مقارنةً بهدف 2%؟",
                "answer": f"{avg_reply_rate * 100:.1f}% (target: 2.0%)",
            },
            {
                "q3": "Which channel is producing the best positive replies?",
                "q3_ar": "أي قناة تُنتج أفضل ردود إيجابية؟",
                "answer": "See channel_execution screen for breakdown",
            },
            {
                "q4": "Are there any doctrine violations in the audit trail?",
                "q4_ar": "هل توجد انتهاكات للمبادئ في سجل التدقيق؟",
                "answer": "Review execution_logs.jsonl for governance_decision fields",
            },
            {
                "q5": "What experiments should we start next week?",
                "q5_ar": "ما التجارب التي يجب إطلاقها الأسبوع القادم؟",
                "answer": (
                    "Test Arabic subject lines for SA legal — proposed based on low reply rate"
                    if avg_reply_rate < 0.02
                    else "Continue current experiments — performance within range"
                ),
            },
            {
                "q6": "Which segments should we pause or double down on?",
                "q6_ar": "أي الشرائح يجب إيقافها أو مضاعفة الجهد فيها؟",
                "answer": "Based on segment_performance screen — pause if positive_reply < 0.5%",
            },
            {
                "q7": "Are we on track for 90-day revenue target?",
                "q7_ar": "هل نسير نحو هدف الإيرادات لـ 90 يوماً؟",
                "answer": "Review sales_pipeline screen — target: 8-15K SAR MRR + 30-40K SAR one-time by day 90",
            },
        ]

        key_learnings = list(set(total_recommendations))[:5]

        next_week_priorities = []
        if avg_reply_rate < 0.02:
            next_week_priorities.append("Test new subject lines — reply rate below 2% threshold")
        if avg_positive_rate < 0.005:
            next_week_priorities.append("Revise pain framing — positive reply rate too low")
        if not next_week_priorities:
            next_week_priorities.append("Increase outreach volume in best segments")
            next_week_priorities.append("Start one new A/B experiment")
            next_week_priorities.append("Review and follow up on all open opportunities")

        return {
            "week_ending": week_ending,
            "days_analyzed": len(recent_logs),
            "avg_reply_rate": avg_reply_rate,
            "avg_positive_reply_rate": avg_positive_rate,
            "questions_and_answers": questions_and_answers,
            "key_learnings": key_learnings,
            "next_week_priorities": next_week_priorities,
            "governance_decision": "learning_engine_weekly_review",
        }
