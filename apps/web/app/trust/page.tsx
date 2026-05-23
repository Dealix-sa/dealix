import { FounderShell, MetricGrid, DataTable } from "../../components/founder/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const data = await getTrustFlags();
  return (
    <FounderShell title="Trust Plane" source={data.source}>
      <MetricGrid
        items={[
          { label: "Open trust flags", value: data.count },
          { label: "Suppression entries", value: data.suppression_count },
          { label: "A3 attempts", value: data.a3_attempts }
        ]}
      />
      <DataTable
        columns={["flag_id", "category", "severity", "summary", "status", "created_at"]}
        rows={data.flags}
      />
    </FounderShell>
  );
}
