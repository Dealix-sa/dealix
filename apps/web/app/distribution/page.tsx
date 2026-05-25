import { ChannelSectorMatrix } from "../../components/distribution/ChannelSectorMatrix";
import { KPIGrid } from "../../components/ceo/KPIGrid";
import type { ChannelSectorCell, Counter } from "../../lib/types";

// TODO: live wire — GET /api/v1/expansion-engine + /api/v1/growth (experiments)
const cells: ChannelSectorCell[] = [];

const totals: Counter[] = [
  { label: "Active Experiments", value: 0 },
  { label: "Double Down", value: 0 },
  { label: "Fix Needed", value: 0 },
  { label: "Killed", value: 0 },
  { label: "Best Channel", value: "—" },
  { label: "Best Sector", value: "—" },
];

export default function DistributionPage() {
  return (
    <main className="grid">
      <section>
        <h1>Distribution</h1>
        <p style={{ maxWidth: 720 }}>
          أي قناة وأي قطاع يعطيك أعلى ردود إيجابية. القرار بسيط: نُضاعف، نُصلح، أو نُلغي.
        </p>
      </section>
      <KPIGrid title="Distribution Verdict" counters={totals} />
      <ChannelSectorMatrix cells={cells} />
    </main>
  );
}
