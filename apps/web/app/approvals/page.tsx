import { ApprovalDecisionModal } from "../../components/approvals/ApprovalDecisionModal";
import { OversightQueue } from "../../components/approvals/OversightQueue";
import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";

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
    <PageShell currentPath="/approvals">
      <SectionHeading
        eyebrow="Approvals"
        title="Drafts in. Approvals out."
        description="Every external action is queued here. Nothing leaves Dealix without an explicit decision."
        action={<StatusBadge label="trust-gated" tone="accent" />}
      />
      <BrandCard title="Pending decisions">
        <OversightQueue items={queueItems} />
      </BrandCard>
      <ApprovalDecisionModal />
    </PageShell>
  );
}
