import { RunActions } from "@/components/control-plane/RunActions";
import { RunTable } from "@/components/control-plane/RunTable";

export const metadata = { title: "Control Plane — Dealix" };

const runs = [
  { runId: "run-001", tenantId: "tenant-enterprise", workflowId: "revenue_os", state: "running" },
  { runId: "run-002", tenantId: "tenant-enterprise", workflowId: "approval_flow", state: "paused" },
];

export default function ControlPlanePage() {
  return (
    <main>
      <section>
        <p className="eyebrow">Control Plane</p>
        <h1>لوحة التحكم · Control Plane <span className="badge badge-amber">بيانات تجريبية · Demo data</span></h1>
        <p className="stat-label">تشغيلات سير العمل وحالتها — كل تشغيل يحترم بوابات الموافقة البشرية.</p>
      </section>
      <section className="card"><RunTable runs={runs} /></section>
      <section className="card"><RunActions runId="run-001" /></section>
    </main>
  );
}
