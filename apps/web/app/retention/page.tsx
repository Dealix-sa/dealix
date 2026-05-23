import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const data = await getRetentionQueue();
  return (
    <FounderShell title={`Retention (${data.count} won)`} source={data.source}>
      <DataTable
        columns={["proposal_id", "lead_id", "stage", "value_sar", "expected_close", "owner", "updated_at"]}
        rows={data.items}
      />
    </FounderShell>
  );
}
