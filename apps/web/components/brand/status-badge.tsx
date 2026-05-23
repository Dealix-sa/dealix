type Tone = "ok" | "warn" | "danger" | "info" | "neutral";

interface StatusBadgeProps {
  tone?: Tone;
  label: string;
}

export function StatusBadge({ tone = "ok", label }: StatusBadgeProps) {
  const cls =
    tone === "warn" ? "dx-badge dx-badge--warn" :
    tone === "danger" ? "dx-badge dx-badge--danger" :
    tone === "info" ? "dx-badge dx-badge--info" :
    "dx-badge";
  return <span className={cls}>{label}</span>;
}

export default StatusBadge;
