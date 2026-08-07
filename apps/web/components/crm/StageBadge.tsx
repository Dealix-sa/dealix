const COLORS: Record<string, string> = {
  new: "bg-neutral-100 text-neutral-700",
  scored: "bg-blue-100 text-blue-700",
  drafted: "bg-yellow-100 text-yellow-800",
  outreach_sent: "bg-purple-100 text-purple-700",
  qualified: "bg-indigo-100 text-indigo-700",
  proposal_sent: "bg-orange-100 text-orange-700",
  won: "bg-emerald-100 text-emerald-700",
  lost: "bg-red-100 text-red-700",
};

export function StageBadge({ stage }: { stage: string }) {
  const cls = COLORS[stage] ?? "bg-neutral-100 text-neutral-700";
  return <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${cls}`}>{stage}</span>;
}
