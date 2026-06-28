import { AgentRegistryTable } from "@/components/agents/AgentRegistryTable";
import { AgentTrustBoundaryEditor } from "@/components/agents/AgentTrustBoundaryEditor";

export const metadata = { title: "Agents — Dealix" };

const agents = [
  { agentId: "sales_agent", tenantId: "tenant-enterprise", capability: "outbound_sales", status: "active" },
  { agentId: "ops_agent", tenantId: "tenant-enterprise", capability: "approval_routing", status: "active" },
];

export default function AgentsPage() {
  return (
    <main>
      <section>
        <p className="eyebrow">Agent Workforce</p>
        <h1>الوكلاء · Agents <span className="badge badge-amber">بيانات تجريبية · Demo data</span></h1>
        <p className="stat-label">سجل الوكلاء وحدود الثقة — كل وكيل محكوم بموافقة بشرية ولا يرسل خارجياً تلقائياً.</p>
      </section>
      <section className="card"><AgentRegistryTable agents={agents} /></section>
      <section className="card"><AgentTrustBoundaryEditor /></section>
    </main>
  );
}
