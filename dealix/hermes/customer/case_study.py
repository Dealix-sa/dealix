"""Case study library — assets generated from successful outcomes."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class CaseStudy:
    id: str
    customer_id: str
    headline: str
    problem: str
    solution: str
    outcome_metric: str
    outcome_value: float
    approved_to_publish: bool = False


@dataclass
class CaseStudyLibrary:
    _by_id: dict[str, CaseStudy] = field(default_factory=dict)

    def draft(
        self,
        *,
        customer_id: str,
        headline: str,
        problem: str,
        solution: str,
        outcome_metric: str,
        outcome_value: float,
    ) -> CaseStudy:
        cs = CaseStudy(
            id=f"cs_{uuid.uuid4().hex[:10]}",
            customer_id=customer_id,
            headline=headline,
            problem=problem,
            solution=solution,
            outcome_metric=outcome_metric,
            outcome_value=outcome_value,
        )
        self._by_id[cs.id] = cs
        return cs

    def approve(self, case_study_id: str, *, by: str = "sami") -> CaseStudy:
        if by != "sami":
            raise PermissionError("Only Sami may approve case studies for publication.")
        cs = self._by_id[case_study_id]
        cs.approved_to_publish = True
        return cs

    def all(self) -> list[CaseStudy]:
        return list(self._by_id.values())


__all__ = ["CaseStudy", "CaseStudyLibrary"]
