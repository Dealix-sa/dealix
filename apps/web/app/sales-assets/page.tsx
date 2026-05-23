import { getSalesAssetSummary } from "../../components/marketAttack/runtimeClient";
import { MetricGrid } from "../../components/marketAttack/MetricGrid";
import { SourceBadge } from "../../components/marketAttack/SourceBadge";

export const dynamic = "force-static";

export default async function SalesAssetsPage() {
  const s = await getSalesAssetSummary();
  return (
    <main className="grid">
      <h1>
        Sales Assets
        <SourceBadge source={s.source} />
      </h1>
      <div className="card">
        <p>
          مكان واحد لجميع الأصول البيعية: one-pagers، proposal templates،
          samples، objection responses، وفهرس proof-safe. كل أصل يخضع
          لـ <code>PROOF_SAFE_ASSET_POLICY.md</code>.
        </p>
      </div>
      <MetricGrid
        metrics={[
          { label: "Total assets", value: s.total },
          { label: "One-pagers", value: s.byType.one_pager ?? 0 },
          { label: "Proposals", value: s.byType.proposal ?? 0 },
          { label: "Samples", value: s.byType.sample ?? 0 },
          { label: "Objection sheets", value: s.byType.objection ?? 0 },
          { label: "Proof-safe", value: s.byType.proof_safe ?? 0 }
        ]}
      />
      <h2>Approval status</h2>
      <MetricGrid
        metrics={[
          { label: "Pending", value: s.byApprovalStatus.pending ?? 0 },
          { label: "Approved", value: s.byApprovalStatus.approved ?? 0 },
          { label: "Held", value: s.byApprovalStatus.held ?? 0 },
          { label: "Rejected", value: s.byApprovalStatus.rejected ?? 0 },
          {
            label: "Champion",
            value: s.championAssets,
            hint: "≥ 3 positive replies cited"
          }
        ]}
      />
      <div className="card">
        <h2>Proof-safe rules</h2>
        <ol>
          <li>No claim without a source.</li>
          <li>No promise without an upstream activity required.</li>
          <li>No customer data or logos without a permission row.</li>
          <li>No off-ladder pricing or contract terms.</li>
          <li>No automation that bypasses approval.</li>
        </ol>
      </div>
    </main>
  );
}
