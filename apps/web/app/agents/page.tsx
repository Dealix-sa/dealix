import {
  ConsolePage,
  PlaceholderTable,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { StatusBadge } from "../../components/brand/StatusBadge";
import { loadInternal } from "../../lib/runtime-client";

type AgentRow = {
  id: string;
  name: string;
  approval_class_max: string;
  external_action_allowed: boolean;
  eval_required: boolean;
  owner: string;
};

const fallback: AgentRow[] = [
  { id: "ceo_copilot", name: "CEO Copilot", approval_class_max: "A2", external_action_allowed: false, eval_required: true, owner: "founder" },
  { id: "brand_guardian", name: "Brand Guardian", approval_class_max: "A2", external_action_allowed: false, eval_required: true, owner: "brand" },
  { id: "growth_strategist", name: "Growth Strategist", approval_class_max: "A2", external_action_allowed: false, eval_required: true, owner: "growth" },
  { id: "distribution_operator", name: "Distribution Operator", approval_class_max: "A2", external_action_allowed: false, eval_required: true, owner: "growth" },
  { id: "trust_guardian", name: "Trust Guardian", approval_class_max: "A1", external_action_allowed: false, eval_required: true, owner: "trust" },
  { id: "eval_guardian", name: "Eval Guardian", approval_class_max: "A1", external_action_allowed: false, eval_required: true, owner: "trust" },
];

export default async function AgentsPage() {
  const payload = await loadInternal<AgentRow[]>(
    "/api/v1/internal/control/agents",
    fallback
  );

  return (
    <ConsolePage
      active="/agents"
      title="Agents"
      subtitle="Registry — scope, approval class, external-action policy"
      source={payload.source}
      intro={
        <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
          Source of truth: <code>registries/agent_registry.yaml</code>. No agent
          may exceed its approval_class_max. Agents with
          external_action_allowed = false cannot send, post, or publish — only
          draft, queue, and recommend.
        </p>
      }
    >
      <SectionHeading title="Registered agents" />
      <BrandCard>
        <table className="dx-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Max class</th>
              <th>External action</th>
              <th>Eval required</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {payload.data.map((a) => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.name}</td>
                <td>
                  <StatusBadge tone={a.approval_class_max === "A1" ? "a1" : a.approval_class_max === "A2" ? "a2" : "a3"}>
                    {a.approval_class_max}
                  </StatusBadge>
                </td>
                <td>{a.external_action_allowed ? "yes" : "no"}</td>
                <td>{a.eval_required ? "yes" : "no"}</td>
                <td>{a.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>

      <SectionHeading title="Kill-switch / quarantine" />
      <BrandCard>
        <PlaceholderTable columns={["Agent", "State", "Reason", "Since"]} />
      </BrandCard>
    </ConsolePage>
  );
}
