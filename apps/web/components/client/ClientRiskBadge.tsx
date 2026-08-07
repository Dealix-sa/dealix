const COLORS: Record<string, string> = {
  low: "bg-emerald-100 text-emerald-700",
  med: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-700",
};
export function ClientRiskBadge({ severity }: { severity: string }) {
  return <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${COLORS[severity] ?? COLORS.med}`}>{severity}</span>;
}
