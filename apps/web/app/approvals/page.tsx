import { ApprovalDecisionModal } from "../../components/approvals/ApprovalDecisionModal";
import { ApprovalsList } from "../../components/approvals/ApprovalsList";
import { OversightQueue } from "../../components/approvals/OversightQueue";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import type { ApprovalItem, Counter } from "../../lib/types";

// TODO: live wire — GET /api/v1/approvals
const items: ApprovalItem[] = [
  {
    ticketId: "apt-100",
    actionType: "whatsapp.send_message",
    requestedBy: "sales_agent",
    riskClass: "A2/R2/S2",
    state: "pending",
  },
];

const totals: Counter[] = [
  { label: "Pending", value: items.filter((i) => i.state === "pending").length },
  { label: "Approved (today)", value: 0 },
  { label: "Rejected (today)", value: 0 },
  { label: "Escalated", value: 0 },
  { label: "SLA Breaches", value: 0 },
];

export default function ApprovalCenterPage() {
  return (
    <main className="grid">
      <section>
        <h1>Approval Center</h1>
        <p style={{ maxWidth: 720 }}>
          Review outreach, proposals, pricing, delivery, proof, and trust escalations before any external action.
        </p>
      </section>
      <KPIGrid title="Today" counters={totals} />
      <ApprovalsList items={items} />
      <OversightQueue
        items={items.map((i) => ({
          ticketId: i.ticketId,
          actionType: i.actionType,
          requestedBy: i.requestedBy,
          state: i.state,
        }))}
      />
      <ApprovalDecisionModal />
    </main>
  );
}
