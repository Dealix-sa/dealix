export const dynamic = "force-dynamic";

import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function CEOOSPage() {
  const layer = await getLayer("ceo_os");
  return (
    <FounderShell
      title="CEO Operating System"
      subtitle="Daily + weekly cadence, doctrine compliance hooks."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        See <code>docs/company/DEALIX_CEO_OS.md</code> for the full doctrine.
        Verifier: <code>make company-os</code>.
      </p>
    </FounderShell>
  );
}
