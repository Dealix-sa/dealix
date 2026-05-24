"""Workshop Builder — every workshop must produce slides, worksheet, policy, prompt pack, follow-up offer, upsell."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkshopPlan:
    title: str
    audience: str
    modules: list[str]
    upsell: str
    assets_created: list[str] = field(default_factory=list)


class WorkshopBuilder:
    REQUIRED_ASSETS = ("slides", "worksheet", "policy_template", "prompt_pack", "follow_up_offer", "upsell_path")

    def build(self, *, title: str, audience: str, modules: list[str], upsell: str) -> WorkshopPlan:
        return WorkshopPlan(
            title=title,
            audience=audience,
            modules=list(modules),
            upsell=upsell,
            assets_created=list(self.REQUIRED_ASSETS),
        )
