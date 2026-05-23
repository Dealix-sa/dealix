import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getProductization } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProductPage() {
  const data = await getProductization();
  return (
    <FounderShell title={`Productization (${data.count})`} source={data.source}>
      <DataTable
        columns={["candidate_id", "name", "stage", "evidence", "next_step", "updated_at"]}
        rows={data.candidates}
      />
    </FounderShell>
  );
}
