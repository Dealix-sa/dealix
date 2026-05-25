import { TrustFlagList } from "../../components/trust/TrustFlagList";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import type { Counter, TrustFlag } from "../../lib/types";

// TODO: live wire — GET /api/v1/safety + /api/v1/agent-governance + audit sink
const flags: TrustFlag[] = [];

const totals: Counter[] = [
  { label: "ALLOW (24h)", value: flags.filter((f) => f.decision === "ALLOW").length },
  { label: "DENY (24h)", value: flags.filter((f) => f.decision === "DENY").length },
  { label: "ESCALATE (24h)", value: flags.filter((f) => f.decision === "ESCALATE").length },
  { label: "Suppression Violations", value: 0 },
  { label: "Overclaim Hits", value: 0 },
  { label: "Open Incidents", value: 0 },
];

export default function TrustPage() {
  return (
    <main className="grid">
      <section>
        <h1>Trust</h1>
        <p style={{ maxWidth: 720 }}>
          PolicyEvaluator يرجع ALLOW · DENY · ESCALATE. كل قرار خارجي عبر هذه البوابة.
        </p>
      </section>
      <KPIGrid title="Last 24h" counters={totals} />
      <TrustFlagList flags={flags} />
    </main>
  );
}
