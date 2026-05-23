import { RunActions } from "../../components/control-plane/RunActions";
import { RunTable } from "../../components/control-plane/RunTable";
import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";

const runs = [
  { runId: "run-001", tenantId: "tenant-enterprise", workflowId: "revenue_os", state: "running" },
  { runId: "run-002", tenantId: "tenant-enterprise", workflowId: "approval_flow", state: "paused" }
];

export default function ControlPlanePage() {
  return (
    <PageShell currentPath="/control-plane">
      <SectionHeading
        eyebrow="Control Plane"
        title="Workflow runs and traces."
        description="Every run is durable. Every state change is auditable. Every external commitment goes through the trust gate."
      />
      <BrandCard title="Active runs">
        <RunTable runs={runs} />
        <RunActions runId="run-001" />
      </BrandCard>
    </PageShell>
  );
}
