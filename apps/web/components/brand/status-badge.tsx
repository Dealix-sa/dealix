export type StatusBadgeTone = "ok" | "warn" | "danger" | "neutral";

export function StatusBadge({ tone = "neutral", children }: { tone?: StatusBadgeTone; children: React.ReactNode }) {
  const cls = `dealix-badge ${tone === "neutral" ? "" : tone}`.trim();
  return <span className={cls}>{children}</span>;
}
