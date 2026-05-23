import { LiveApprovalsQueue } from "../../components/approvals/LiveApprovalsQueue";
import { FounderShell } from "../../components/founder-shell";
import { loadApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalsPage() {
  const result = await loadApprovals();

  if (!result.ok) {
    return (
      <FounderShell
        title="Approvals"
        subtitle="CEO approval queue · every decision is audited"
        error={result.error}
      >
        <div className="card">
          <p style={{ margin: 0 }}>
            Approval queue runtime is unreachable. Start the API and bootstrap
            Private Ops to see pending approvals.
          </p>
        </div>
      </FounderShell>
    );
  }

  return (
    <FounderShell
      title="Approvals"
      subtitle="CEO approval queue · every decision is audited"
      source="private_ops_csv"
      lastUpdated={new Date().toISOString()}
    >
      <LiveApprovalsQueue initialItems={result.data} />
    </FounderShell>
  );
}
