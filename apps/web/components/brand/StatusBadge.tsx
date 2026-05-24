export type StatusTone =
  | "neutral"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "a1"
  | "a2"
  | "a3";

export function StatusBadge({
  tone = "neutral",
  children,
}: {
  tone?: StatusTone;
  children: React.ReactNode;
}) {
  return <span className={`dx-badge dx-badge--${tone}`}>{children}</span>;
}
