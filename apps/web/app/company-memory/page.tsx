import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function CompanyMemoryPage() {
  const layer = await getLayer("company_memory");
  return (
    <FounderShell
      title="Company Memory"
      subtitle="Decision log, value ledger, proof packs, capital assets."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Verifier: <code>make company-memory</code>. Source:
        <code> docs/company/DEALIX_COMPANY_MEMORY.md</code>.
      </p>
    </FounderShell>
  );
}
