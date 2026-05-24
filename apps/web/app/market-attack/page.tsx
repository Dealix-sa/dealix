import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function MarketAttackPage() {
  const env = await dealixActions.marketAttack();
  return (
    <FounderShell
      titleEn="Market Attack — Beachhead Scorecard"
      titleAr="ساحة الاقتحام — لوحة قطّاع البداية"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Backed by <code>$PRIVATE_OPS/market_attack/beachhead_sector_scorecard.csv</code>.
        Scaling beyond Phase G of Article 13 is forbidden until 3 paid
        pilots are recorded in the canonical Proof Ledger.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
