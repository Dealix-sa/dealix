import {
  ConsolePage,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { StatusBadge } from "../../components/brand/StatusBadge";
import { loadInternal } from "../../lib/runtime-client";

type Sovereign = {
  layers_total: number | null;
  layers_pass: number | null;
  layers_blocked: number | null;
  last_run: string | null;
};

const layers = [
  "Brand Authority",
  "Category & Positioning",
  "Market Intelligence",
  "ICP & Account Scoring",
  "Distribution War Machine",
  "Revenue Factory",
  "Product Marketing OS",
  "Founder Console",
  "Control Plane",
  "AI Agent OS",
  "Policy-as-Code",
  "Eval / Red Team Gate",
  "Trust + Audit Layer",
  "Worker Orchestrator",
  "Data Platform / Postgres",
  "Delivery + Retention OS",
  "Finance + Unit Economics OS",
  "Observability + Security + Production Gates",
];

export default async function SovereignPage() {
  const payload = await loadInternal<Sovereign>(
    "/api/v1/internal/founder/sovereign",
    { layers_total: layers.length, layers_pass: null, layers_blocked: null, last_run: null }
  );

  return (
    <ConsolePage
      active="/sovereign"
      title="Sovereign Operating Stack"
      subtitle="18-layer readiness for Dealix as a market-ready operating company"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Layers tracked" value={payload.data.layers_total ?? layers.length} />
        <MetricCard label="Passing" value={payload.data.layers_pass ?? "—"} />
        <MetricCard label="Blocked" value={payload.data.layers_blocked ?? "—"} />
      </div>

      <SectionHeading title="Layers" />
      <BrandCard>
        <table className="dx-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Layer</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {layers.map((layer, idx) => (
              <tr key={layer}>
                <td>{(idx + 1).toString().padStart(2, "0")}</td>
                <td>{layer}</td>
                <td>
                  <StatusBadge tone="neutral">pending verifier</StatusBadge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>

      <SectionHeading title="Verifier commands" />
      <BrandCard>
        <SafeList
          items={[
            "make brand-system",
            "make growth-system",
            "make marketing-system",
            "make product-distribution",
            "make policy-check",
            "make agent-registry",
            "make eval-gate",
            "make brand-growth-operating-layer",
            "make ultimate-operating-layer",
            "make sovereign-operating-stack",
            "make smoke-internal-api",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
