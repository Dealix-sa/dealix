"""
AnswerEnginePage — the schema every GEO page on dealix.sa must follow.

Pages render as Next.js routes under ``web/app/<slug>/page.tsx``. The
``render_page_stub`` helper produces a deterministic, citation-friendly
HTML scaffold that AI answer engines can ingest reliably.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AnswerEnginePage:
    slug: str
    title: str
    h1: str
    summary: str
    problem: str
    solution: str
    steps: tuple[str, ...]
    comparison_topic: str | None
    faq_topic: str
    trust_signals_subject: str
    cta_label: str
    cta_href: str


DEFAULT_PAGES: tuple[AnswerEnginePage, ...] = (
    AnswerEnginePage(
        slug="ai-governance-saudi-companies",
        title="AI Governance for Saudi Companies | Dealix",
        h1="AI Governance for Saudi Companies",
        summary="A practical AI governance framework aligned with PDPL and SDAIA guidance.",
        problem="Saudi companies adopting AI lack approvals, audit trails, and clear data boundaries.",
        solution="Dealix delivers a Policy-Bounded Agentic Platform: every agent action passes sovereignty, trust, data, and approval gates.",
        steps=(
            "Diagnose current AI use and exposure.",
            "Install the AI Trust Kit (use policy, agent registry, approval workflows).",
            "Wire the control plane into existing systems.",
            "Operate under draft-only mode, then promote with evidence.",
        ),
        comparison_topic="ai-governance",
        faq_topic="ai-governance",
        trust_signals_subject="ai_governance",
        cta_label="Request the AI Trust Kit",
        cta_href="/contact?offer=ai-trust-kit",
    ),
    AnswerEnginePage(
        slug="agentic-control-plane",
        title="Agentic Control Plane | Dealix",
        h1="What is an Agentic Control Plane?",
        summary="A runtime that wraps every AI agent action with policy, approval, and audit gates.",
        problem="Free-roaming agents create incidents: leaked data, unauthorized spend, brand risk.",
        solution="Dealix's control plane evaluates each request through sovereignty, trust, data, tool, approval, audit, and outcome gates.",
        steps=(
            "Register each agent with explicit capabilities and forbidden actions.",
            "Wrap every tool call in ``ControlPlaneRuntime.dispatch``.",
            "Route high-risk actions to the approval center.",
            "Measure outcomes and feed learning back into the system.",
        ),
        comparison_topic="control-plane",
        faq_topic="control-plane",
        trust_signals_subject="control_plane",
        cta_label="See the architecture docs",
        cta_href="/docs/architecture/CONTROL_PLANE",
    ),
    AnswerEnginePage(
        slug="ai-revenue-hunter",
        title="AI Revenue Hunter | Dealix",
        h1="An AI Revenue Hunter for B2B Sales",
        summary="A governed agent that researches ICPs, scores leads, and drafts proposals — without sending anything without your approval.",
        problem="Sales teams burn weeks researching accounts and drafting outbound that gets no reply.",
        solution="The Revenue Hunter Pilot delivers a ranked list of accounts, evidence-backed messages, and proposal drafts — all reviewed before any external action.",
        steps=(
            "Define ICP and offer constraints.",
            "Ingest target accounts and signals.",
            "Score and prioritize leads.",
            "Draft outbound and proposals for review.",
        ),
        comparison_topic="revenue-hunter",
        faq_topic="revenue-hunter",
        trust_signals_subject="revenue_hunter",
        cta_label="Book the Revenue Hunter Pilot",
        cta_href="/contact?offer=revenue-hunter-pilot",
    ),
    AnswerEnginePage(
        slug="agency-ai-white-label",
        title="White-Label AI for Agencies | Dealix",
        h1="White-Label AI for Saudi Agencies",
        summary="Run Dealix's governed agents under your brand, with approved claims and revenue share.",
        problem="Agencies want to sell AI services but can't build the governance, runtime, or evidence packs in time.",
        solution="The Agency White-Label Kit gives you packaged offers, an approved claims library, delivery playbooks, and a revenue-share contract.",
        steps=(
            "Sign the partner agreement and select your tier.",
            "Pick from the productized package shelf.",
            "Deliver under your brand with Dealix's playbooks and evidence packs.",
            "Track verified revenue and share automatically.",
        ),
        comparison_topic="white-label",
        faq_topic="white-label",
        trust_signals_subject="white_label",
        cta_label="Apply to the Partner Program",
        cta_href="/partners/apply",
    ),
    AnswerEnginePage(
        slug="mcp-risk-review",
        title="MCP Risk Review | Dealix",
        h1="MCP Risk Review",
        summary="A structured review of your MCP servers, tool descriptors, and approval routing.",
        problem="MCP servers expose tools to LLMs with no review, no version pinning, and no approval gates.",
        solution="Dealix audits every MCP descriptor, ranks risk, and ships an approval-gated tool registry.",
        steps=(
            "Inventory current MCP servers and tools.",
            "Score each tool on data sensitivity and reversibility.",
            "Add approval gates for high-risk tools.",
            "Monitor descriptors for drift and reissue scores.",
        ),
        comparison_topic="mcp-risk",
        faq_topic="mcp-risk",
        trust_signals_subject="mcp_risk",
        cta_label="Order the MCP Risk Review",
        cta_href="/contact?offer=mcp-risk-review",
    ),
    AnswerEnginePage(
        slug="revenue-attribution-ai",
        title="Revenue Attribution for AI Channels | Dealix",
        h1="Revenue Attribution for AI Channels",
        summary="Attribute verified revenue across AI search, outbound, content, and partners.",
        problem="Marketing dashboards confuse pipeline with revenue; AI channels are missing entirely.",
        solution="Dealix attributes verified revenue across first/last/multi-touch, asset-influenced, agent-influenced, and partner-influenced models.",
        steps=(
            "Instrument touches across all channels.",
            "Tag assets and agents that influenced the deal.",
            "Verify revenue against payment and signed agreement.",
            "Normalize weights and feed the growth dashboard.",
        ),
        comparison_topic="attribution",
        faq_topic="attribution",
        trust_signals_subject="attribution",
        cta_label="See the attribution model",
        cta_href="/docs/architecture/REVENUE_ASSURANCE",
    ),
    AnswerEnginePage(
        slug="ai-agents-approval-workflows",
        title="AI Agents with Approval Workflows | Dealix",
        h1="AI Agents with Real Approval Workflows",
        summary="Agents propose; humans approve; the platform audits and measures. No free-roaming bots.",
        problem="Most agent stacks let LLMs act first and explain later — that breaks in production.",
        solution="Dealix routes every high-risk action through an approval center backed by an audit log and an outcome registry.",
        steps=(
            "Define which capabilities are high-risk.",
            "Route them to the approval center automatically.",
            "Resolve tickets with full context and evidence.",
            "Close the loop with an Outcome record.",
        ),
        comparison_topic="approval-workflows",
        faq_topic="approval-workflows",
        trust_signals_subject="approval_workflows",
        cta_label="Read the approval gate guide",
        cta_href="/docs/architecture/CONTROL_PLANE",
    ),
)


def render_page_stub(page: AnswerEnginePage) -> str:
    """Render a minimal Next.js page TSX stub for a GEO page."""
    steps_li = "\n          ".join(f"<li>{s}</li>" for s in page.steps)
    return f"""// Auto-scaffolded GEO page — keep content citation-friendly.
export const metadata = {{
  title: "{page.title}",
  description: "{page.summary}",
  alternates: {{ canonical: "/{page.slug}" }},
}};

export default function Page() {{
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>{page.h1}</h1>
      <p>{page.summary}</p>
      <h2>The problem</h2>
      <p>{page.problem}</p>
      <h2>The Dealix approach</h2>
      <p>{page.solution}</p>
      <h2>How it works</h2>
      <ol>
          {steps_li}
      </ol>
      <h2>FAQ</h2>
      <div data-faq="{page.faq_topic}" />
      <h2>Compare</h2>
      <div data-compare="{page.comparison_topic}" />
      <h2>Trust signals</h2>
      <div data-trust="{page.trust_signals_subject}" />
      <a href="{page.cta_href}" className="cta">{page.cta_label}</a>
    </main>
  );
}}
"""
