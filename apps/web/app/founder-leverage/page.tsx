export const dynamic = "force-dynamic";

import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function FounderLeveragePage() {
  const layer = await getLayer("hypergrowth_ceo");
  return (
    <FounderShell
      title="Founder Leverage"
      subtitle="Where the founder's hours go, this week."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Sourced from <code>docs/company/DEALIX_HYPERGROWTH_CEO.md</code>.
        Verifier: <code>make founder-ceo-hypergrowth-layer</code>.
      </p>
    </FounderShell>
  );
}
