import { BrandCard } from "./brand-card";
import { StatusBadge } from "./status-badge";

export function ProofCard({
  title,
  sector,
  outcome,
  approval_state,
}: {
  title: string;
  sector: string;
  outcome: string;
  approval_state: "draft" | "queued" | "approved" | "redacted";
}) {
  const tone = approval_state === "approved" ? "ok" : approval_state === "redacted" ? "danger" : "warn";
  return (
    <BrandCard title={title} subtitle={sector}>
      <p style={{ color: "var(--dealix-soft-silver)", margin: "0 0 12px" }}>{outcome}</p>
      <StatusBadge tone={tone}>{approval_state}</StatusBadge>
    </BrandCard>
  );
}
