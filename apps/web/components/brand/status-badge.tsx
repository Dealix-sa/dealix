type Tone = "ok" | "warn" | "danger" | "neutral";

export function StatusBadge({ tone = "neutral", children }: { tone?: Tone; children: React.ReactNode }) {
  return <span className={`dlx-badge ${tone}`}>{children}</span>;
}
