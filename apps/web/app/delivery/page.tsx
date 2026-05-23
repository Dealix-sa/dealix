import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const data = await getDeliveryQueue();
  return (
    <FounderShell title={`Delivery Queue (${data.count})`} source={data.source}>
      <DataTable
        columns={["proposal_id", "lead_id", "stage", "value_sar", "expected_close", "owner", "updated_at"]}
        rows={data.items}
      />
    </FounderShell>
  );
}
