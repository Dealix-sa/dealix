export const dynamic = "force-dynamic";

import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function MoatPage() {
  const layer = await getLayer("scale_moat");
  return (
    <FounderShell
      title="Scale / Moat"
      subtitle="Data moat, governance moat, distribution moat, switching cost."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Verifier: <code>make scale-moat-system</code>. Source:
        <code> docs/company/DEALIX_SCALE_MOAT.md</code>.
      </p>
    </FounderShell>
  );
}
