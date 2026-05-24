"""خادم التدريب — WorkshopBuilder."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WorkshopDraft(BaseModel):
    """A structured workshop outline."""

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(..., min_length=1, max_length=200)
    audience: str = Field(..., min_length=1, max_length=200)
    duration_hours: float = Field(..., gt=0.0, le=24.0)
    learning_objectives: list[str] = Field(..., min_length=1, max_length=10)
    agenda: list[dict[str, str]] = Field(..., min_length=1, max_length=12)
    materials: list[str] = Field(default_factory=list, max_length=20)
    success_metric: str = Field(..., min_length=1, max_length=300)


class WorkshopBuilder:
    """Draft a workshop outline from topic + audience + duration."""

    def draft(
        self,
        topic: str,
        audience: str,
        duration_hours: float,
    ) -> WorkshopDraft:
        if duration_hours <= 0:
            raise ValueError("duration_hours must be positive")
        objectives = self._objectives(topic)
        agenda = self._agenda(topic, duration_hours)
        materials = self._materials(topic)
        success_metric = (
            f"At least 80 % of attendees can articulate {objectives[0].lower()} "
            f"by the end of the session."
        )
        return WorkshopDraft(
            topic=topic,
            audience=audience,
            duration_hours=round(duration_hours, 2),
            learning_objectives=objectives,
            agenda=agenda,
            materials=materials,
            success_metric=success_metric,
        )

    @staticmethod
    def _objectives(topic: str) -> list[str]:
        topic_l = topic.lower()
        base = [f"Explain the core idea behind {topic}"]
        if "governance" in topic_l or "trust" in topic_l:
            base.append("Identify when an agent action needs Sami approval")
            base.append("Wire one evidence pack end-to-end")
        elif "sales" in topic_l or "revenue" in topic_l:
            base.append("Run one qualification call using the Dealix playbook")
            base.append("Draft one proposal that passes the §41 quality gate")
        elif "partner" in topic_l:
            base.append("Score one partner candidate via PartnerFitScorer")
            base.append("Move a partner from PROSPECT to QUALIFIED")
        else:
            base.append(f"Apply the {topic} playbook on a real case")
            base.append("Capture learnings into the asset registry")
        return base

    @staticmethod
    def _agenda(topic: str, duration_hours: float) -> list[dict[str, str]]:
        total_minutes = int(duration_hours * 60)
        slots = max(3, min(8, total_minutes // 30))
        per_slot_minutes = total_minutes // slots
        labels = [
            "Frame the problem",
            "Walk the playbook",
            "Live exercise",
            "Common failure modes",
            "Case study",
            "Q&A",
            "Action plan",
            "Wrap-up",
        ][:slots]
        agenda: list[dict[str, str]] = []
        for label in labels:
            agenda.append(
                {
                    "block": label,
                    "duration_minutes": str(per_slot_minutes),
                    "topic": f"{topic}: {label}",
                }
            )
        return agenda

    @staticmethod
    def _materials(topic: str) -> list[str]:
        return [
            f"Slide deck — {topic}",
            f"Workbook — {topic}",
            "Friction-log capture template",
        ]


__all__ = ["WorkshopBuilder", "WorkshopDraft"]
