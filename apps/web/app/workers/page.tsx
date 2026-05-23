import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const data = await getWorkerHealth();
  return (
    <FounderShell title={`Worker Health (${data.count})`} source={data.source}>
      <DataTable
        columns={["worker", "last_run", "status", "failures_24h", "next_run", "notes"]}
        rows={data.workers}
      />
    </FounderShell>
  );
}
