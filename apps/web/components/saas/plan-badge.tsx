export function PlanBadge({ plan = "Founder-led Beta" }: { plan?: string }) {
  return <span className="rounded-full border px-3 py-1 text-sm">{plan}</span>;
}
