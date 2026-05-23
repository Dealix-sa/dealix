import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { ProofCard } from "../../components/brand/proof-card";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const res = await getProofLibrary();
  return (
    <FounderShell title="Proof Library">
      <BrandCard
        title="Proof, gated by approval"
        subtitle="No proof is published without explicit approval and PII redaction."
        source={res.source}
      >
        {res.data.items.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No proof artifacts yet.</p>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12 }}>
            {res.data.items.map((p) => (
              <ProofCard
                key={p.id}
                title={p.title}
                sector={p.sector}
                outcome={`Approval state: ${p.approval_state}`}
                approval_state={p.approval_state as "draft" | "queued" | "approved" | "redacted"}
              />
            ))}
          </div>
        )}
      </BrandCard>
    </FounderShell>
  );
}
