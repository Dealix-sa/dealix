import { FollowUpsDue } from "../../components/sales/FollowUpsDue";
import { SalesFunnel } from "../../components/sales/SalesFunnel";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import type { Counter, FollowUp, FunnelStage } from "../../lib/types";

// TODO: live wire — GET /api/v1/sales + /api/v1/revenue-pipeline
const stages: FunnelStage[] = [
  { stage: "Lead Intelligence", count: 0 },
  { stage: "A Leads", count: 0 },
  { stage: "Pending Approval", count: 0 },
  { stage: "Ready Drafts", count: 0 },
  { stage: "Sent", count: 0 },
  { stage: "Replies", count: 0 },
  { stage: "Positive", count: 0 },
  { stage: "Samples", count: 0 },
  { stage: "Proposals", count: 0 },
  { stage: "Payment Queue", count: 0 },
];

const captureMetrics: Counter[] = [
  { label: "Payment Capture", value: "0 SAR", hint: "owed by customers" },
  { label: "Avg Days to Pay", value: "—" },
  { label: "Sample Conversion", value: "0%" },
];

// TODO: live wire — GET /api/v1/follow-ups (or /api/v1/sales/follow-ups)
const followUps: FollowUp[] = [];

export default function SalesCockpitPage() {
  return (
    <main className="grid">
      <section>
        <h1>Sales Cockpit</h1>
        <p style={{ maxWidth: 720 }}>
          Track the Dealix revenue factory from market intelligence to payment capture.
        </p>
      </section>
      <SalesFunnel stages={stages} />
      <KPIGrid title="Payment Capture" counters={captureMetrics} />
      <FollowUpsDue items={followUps} />
    </main>
  );
}
