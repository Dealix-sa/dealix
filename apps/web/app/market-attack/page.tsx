export const dynamic = "force-dynamic";

import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function MarketAttackPage() {
  const layer = await getLayer("market_attack");
  return (
    <FounderShell
      title="Market Attack System"
      subtitle="ICP, beachhead, wedge, qualification."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Verifier: <code>make market-attack-system</code>. Source:
        <code> docs/company/DEALIX_MARKET_ATTACK.md</code>.
      </p>
    </FounderShell>
  );
}
