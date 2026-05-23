import { getMarketAttackSummary } from "../../components/marketAttack/runtimeClient";
import { MetricGrid } from "../../components/marketAttack/MetricGrid";
import { SourceBadge } from "../../components/marketAttack/SourceBadge";

export const dynamic = "force-static";

export default async function MarketAttackPage() {
  const summary = await getMarketAttackSummary();
  return (
    <main className="grid">
      <h1>
        Market Attack
        <SourceBadge source={summary.source} />
      </h1>
      <div className="card">
        <p>
          نقطة القيادة لطبقة Market Attack &amp; Scaling. لا يصدر هذا
          الواجهة أي رسائل خارجية ولا ينشر أي إثبات. كل اتخاذ قرار يلزم
          مراجعة المؤسس.
        </p>
        <p style={{ color: "#475569" }}>
          Source of truth: <code>scripts/verify_market_attack_system.py</code>.
        </p>
      </div>
      <MetricGrid
        metrics={[
          {
            label: "Locked beachhead",
            value: summary.beachhead?.sector ?? "—",
            hint:
              summary.beachhead != null
                ? `priority ${summary.beachhead.priority}, score ${summary.beachhead.totalScore}`
                : "no P0 sector"
          },
          { label: "P0 sectors", value: summary.p0Count },
          { label: "P1 sectors", value: summary.p1Count },
          { label: "Open objections", value: summary.openObjections },
          {
            label: "High-frequency objections",
            value: summary.highFrequencyObjections,
            hint: "frequency >= 3"
          },
          {
            label: "Active T0+T1 accounts",
            value: summary.activeT0AndT1Accounts,
            hint: "ceiling 25"
          }
        ]}
      />
      <div className="card">
        <h2>Daily / weekly cadence</h2>
        <ul>
          <li>
            <code>make beachhead-scorecard PRIVATE_OPS=…</code> — daily refresh
            of the sector scorecard.
          </li>
          <li>
            <code>make offer-market-fit PRIVATE_OPS=…</code> — weekly review of
            test outcomes.
          </li>
          <li>
            <code>make objection-intel PRIVATE_OPS=…</code> — weekly recap of
            objections.
          </li>
          <li>
            <code>make market-attack-system</code> — master verifier.
          </li>
        </ul>
      </div>
      <div className="card">
        <h2>Non-negotiables</h2>
        <ol>
          <li>No external sending.</li>
          <li>No proof publishing without proof-pack validation.</li>
          <li>No off-ladder pricing or contracts.</li>
          <li>No guaranteed revenue / sales / meetings claims.</li>
        </ol>
      </div>
    </main>
  );
}
