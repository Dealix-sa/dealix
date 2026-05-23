import { ApprovalDecisionModal } from "../../components/approvals/ApprovalDecisionModal";
import { OversightQueue } from "../../components/approvals/OversightQueue";

type ApprovalItem = {
  id: string;
  type: string;
  company: string;
  approval_class: "A0" | "A1" | "A2" | "A3";
  risk_level: "Low" | "Medium" | "High" | "Critical";
  summary: string;
};

const approvals: ApprovalItem[] = [];

const queueItems = [
  {
    ticketId: "apt-100",
    actionType: "whatsapp.send_message",
    requestedBy: "sales_agent",
    state: "pending",
  },
];

export default function ApprovalCenterPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Approval Center</h1>
      <p className="mt-2 max-w-3xl">
        Approve, reject, edit, or escalate outreach, proposals, pricing, proof, and trust actions.
      </p>
      <section className="mt-8 rounded-2xl border p-6">
        {approvals.length === 0 ? (
          <p>No pending founder approvals. Connect API data source next.</p>
        ) : (
          approvals.map((item) => (
            <div key={item.id} className="border-b py-4">
              <p className="font-semibold">{item.company}</p>
              <p className="text-sm">Type: {item.type}</p>
              <p className="text-sm">Approval: {item.approval_class}</p>
              <p className="text-sm">Risk: {item.risk_level}</p>
              <p className="mt-2">{item.summary}</p>
            </div>
          ))
        )}
      </section>
      <section className="mt-8 grid gap-4">
        <OversightQueue items={queueItems} />
        <ApprovalDecisionModal />
      </section>
    </main>
  );
}
