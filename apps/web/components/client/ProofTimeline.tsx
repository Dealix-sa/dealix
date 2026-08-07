import type { ProofItem } from "@/lib/client/portal";

export function ProofTimeline({ items }: { items: ProofItem[] }) {
  return (
    <ol className="space-y-3">
      {items.map((p) => (
        <li key={p.id} className="rounded-xl border border-neutral-200 p-3 text-sm">
          <p className="font-medium">{p.title}</p>
          <p className="mt-1 text-xs text-neutral-500">{p.evidence} · {p.date}</p>
        </li>
      ))}
      {items.length === 0 ? <p className="text-sm text-neutral-500">No proof items yet.</p> : null}
    </ol>
  );
}
