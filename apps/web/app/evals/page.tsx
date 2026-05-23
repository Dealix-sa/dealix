import { FounderShell, MetricGrid, DataTable } from "../../components/founder/founder-shell";
import { getEvalStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function EvalsPage() {
  const data = await getEvalStatus();
  return (
    <FounderShell title="Eval Gate" source={data.source}>
      <MetricGrid
        items={[
          { label: "Suites tracked", value: data.suites.length },
          { label: "Blocking failures", value: data.blocking_failures }
        ]}
      />
      <DataTable
        columns={["suite", "passed", "failed", "warn", "last_run", "blocking"]}
        rows={data.suites}
      />
    </FounderShell>
  );
}
