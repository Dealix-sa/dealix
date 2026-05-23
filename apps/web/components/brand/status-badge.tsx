type StatusTone = "neutral" | "success" | "warning" | "danger" | "info" | "accent";

const TONE_STYLE: Record<StatusTone, { bg: string; border: string; fg: string }> = {
  neutral: { bg: "#121C30", border: "#1B2740", fg: "#B2BBC6" },
  success: { bg: "rgba(0,209,161,0.10)", border: "rgba(0,209,161,0.35)", fg: "#00D1A1" },
  warning: { bg: "rgba(242,200,75,0.10)", border: "rgba(242,200,75,0.40)", fg: "#F2C84B" },
  danger:  { bg: "rgba(255,90,95,0.10)",  border: "rgba(255,90,95,0.40)",  fg: "#FF5A5F" },
  info:    { bg: "rgba(90,176,255,0.10)", border: "rgba(90,176,255,0.40)", fg: "#5AB0FF" },
  accent:  { bg: "rgba(0,209,161,0.15)",  border: "rgba(0,209,161,0.50)",  fg: "#00D1A1" },
};

export function StatusBadge({
  label,
  tone = "neutral",
}: {
  label: string;
  tone?: StatusTone;
}) {
  const t = TONE_STYLE[tone];
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "3px 10px",
        borderRadius: 999,
        background: t.bg,
        border: `1px solid ${t.border}`,
        color: t.fg,
        fontSize: 12,
        fontWeight: 600,
        lineHeight: 1.4,
      }}
    >
      <span style={{ width: 6, height: 6, borderRadius: "50%", background: t.fg }} aria-hidden />
      {label}
    </span>
  );
}
