import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function CapitalAllocationPage() {
  const layer = await getLayer("capital_allocation");
  return (
    <FounderShell
      title="Capital Allocation"
      subtitle="Budget pools, decision rules, compute caps."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Generate report: <code>make capital-allocation</code>. Source:
        <code> docs/company/DEALIX_CAPITAL_ALLOCATION.md</code>.
      </p>
    </FounderShell>
  );
}
