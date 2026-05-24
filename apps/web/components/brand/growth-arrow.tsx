export function GrowthArrow({ direction = "up" }: { direction?: "up" | "down" | "flat" }) {
  const map = { up: "▲", down: "▼", flat: "→" } as const;
  const color = direction === "up" ? "#16A34A" : direction === "down" ? "#DC2626" : "#475569";
  return <span style={{ color, fontWeight: 700 }}>{map[direction]}</span>;
}
