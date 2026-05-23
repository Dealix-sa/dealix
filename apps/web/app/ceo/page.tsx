import { CEOTopAction } from "../../components/ceo/CEOTopAction";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import { WorkerHealthSummary } from "../../components/ceo/WorkerHealthSummary";
import type { Counter, TopAction, WorkerRow } from "../../lib/types";

// TODO: live wire — GET /api/v1/business-now/snapshot + /api/v1/command-center
const topAction: TopAction = {
  title: "Approve today's outreach batch",
  detail: "12 drafts waiting on founder review. SLA 2h.",
  cta: "Open Approval Center",
  href: "/approvals",
};

const revenueFunnel: Counter[] = [
  { label: "Lead Intelligence", value: 0, hint: "discovered today" },
  { label: "A Leads", value: 0 },
  { label: "Outreach Ready", value: 0 },
  { label: "Sent (24h)", value: 0 },
  { label: "Positive Replies", value: 0 },
  { label: "Samples Due", value: 0 },
  { label: "Proposals Due", value: 0 },
  { label: "Payment Capture", value: "0 SAR" },
];

const oversight: Counter[] = [
  { label: "Approval Inbox", value: 12, hint: "pending action" },
  { label: "Follow-ups Due", value: 0 },
  { label: "Delivery Queue", value: 0 },
  { label: "Trust Flags", value: 0 },
  { label: "Cash", value: "0 SAR" },
  { label: "MRR", value: "0 SAR" },
  { label: "Pipeline (weighted)", value: "0 SAR" },
];

// TODO: live wire — GET /api/v1/observability/workers
const workers: WorkerRow[] = [];

export default function CEOCommandCenterPage() {
  return (
    <main className="grid">
      <section>
        <p style={{ margin: 0, fontSize: 12, textTransform: "uppercase", letterSpacing: "0.06em", opacity: 0.6 }}>
          Dealix CEO Command Center
        </p>
        <h1 style={{ marginTop: 4 }}>Control the Revenue Factory</h1>
        <p style={{ marginTop: 0, maxWidth: 720 }}>
          The CEO approves and decides. The system prepares and routes. Every external-impact action goes through Approval Center.
        </p>
      </section>
      <CEOTopAction action={topAction} />
      <KPIGrid title="Revenue Funnel" counters={revenueFunnel} />
      <KPIGrid title="Oversight & Cash" counters={oversight} />
      <WorkerHealthSummary workers={workers} />
    </main>
  );
}
