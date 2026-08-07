import type { Deliverable } from "@/lib/client/portal";

const COLORS: Record<string, string> = {
  done: "bg-emerald-100 text-emerald-700",
  in_progress: "bg-blue-100 text-blue-700",
  queued: "bg-neutral-100 text-neutral-700",
  blocked: "bg-red-100 text-red-700",
};

export function DeliverableList({ items }: { items: Deliverable[] }) {
  return (
    <ul className="space-y-2">
      {items.map((d) => (
        <li key={d.id} className="flex items-center justify-between rounded-xl border border-neutral-200 p-3 text-sm">
          <span className="font-medium">{d.title}</span>
          <span className={`rounded-full px-2 py-0.5 text-xs ${COLORS[d.status] ?? COLORS.queued}`}>
            {d.status} {d.completedAt ? `· ${d.completedAt}` : d.due ? `· due ${d.due}` : ""}
          </span>
        </li>
      ))}
    </ul>
  );
}
