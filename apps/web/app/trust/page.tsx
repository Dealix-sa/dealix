import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const res = await getTrustFlags();
  return (
    <FounderShell title="Trust">
      <BrandCard title="Trust flags" subtitle="From trust/trust_flags.csv" source={res.source}>
        {res.data.flags.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No open trust flags. Stay vigilant.</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {res.data.flags.map((f) => (
              <li
                key={f.id}
                style={{ padding: "10px 0", borderBottom: "1px solid var(--dealix-border)", display: "flex", justifyContent: "space-between" }}
              >
                <span>{f.description}</span>
                <StatusBadge tone={f.severity === "high" ? "danger" : f.severity === "medium" ? "warn" : "neutral"}>
                  {f.severity}
                </StatusBadge>
              </li>
            ))}
          </ul>
        )}
      </BrandCard>
    </FounderShell>
  );
}
