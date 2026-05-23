import { ApprovalDecisionModal } from "../../components/approvals/ApprovalDecisionModal";
import { OversightQueue } from "../../components/approvals/OversightQueue";
import { FounderShell } from "../../components/founder-shell";

const queueItems = [
  {
    ticketId: "apt-100",
    actionType: "whatsapp.send_message",
    requestedBy: "sales_agent",
    state: "pending"
  }
];

export default function ApprovalsPage() {
  return (
    <FounderShell title="Approvals">
      <p className="lead">
        A1/A2/A3 actions awaiting founder review. Backed by the existing
        Trust Plane ApprovalCenter.
      </p>
      <div className="grid">
        <OversightQueue items={queueItems} />
        <ApprovalDecisionModal />
      </div>
    </FounderShell>
  );
}
