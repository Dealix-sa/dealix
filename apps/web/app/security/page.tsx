import { FounderShell, MetricGrid, DataTable } from "../../components/founder/founder-shell";
import { getSecurityStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SecurityPage() {
  const data = await getSecurityStatus();
  const tokenSet = data.production_token_set ?? false;
  return (
    <FounderShell
      title="Security & Governance"
      subtitle={tokenSet ? "Internal API token is set." : "Set DEALIX_INTERNAL_TOKEN before promoting to production."}
      source={data.source}
    >
      <MetricGrid
        items={[
          { label: "Controls tracked", value: data.count },
          { label: "Production token", value: tokenSet ? "set" : "unset" }
        ]}
      />
      <DataTable
        columns={["control", "status", "last_checked", "owner", "evidence"]}
        rows={data.controls}
      />
    </FounderShell>
  );
}
