export function SourceBadge({ source }: { source: "api" | "fallback" }) {
  const label = source === "api" ? "source: api" : "source: fallback";
  const background = source === "api" ? "#e0f2fe" : "#fef3c7";
  const color = source === "api" ? "#075985" : "#92400e";
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 8px",
        borderRadius: 999,
        background,
        color,
        fontSize: 12,
        fontWeight: 600,
        marginInlineStart: 8
      }}
    >
      {label}
    </span>
  );
}
