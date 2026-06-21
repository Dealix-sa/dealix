import type { Approval } from "@/lib/client/portal";

export function ApprovalQueue({ items }: { items: Approval[] }) {
  return (
    <ul className="space-y-2">
      {items.map((a) => (
        <li key={a.id} className="rounded-xl border border-neutral-200 p-3 text-sm">
          <div className="flex items-center justify-between">
            <span className="font-medium">{a.item}</span>
            <span className={`rounded-full px-2 py-0.5 text-xs ${
              a.status === "approved" ? "bg-emerald-100 text-emerald-700" :
              a.status === "rejected" ? "bg-red-100 text-red-700" :
              "bg-yellow-100 text-yellow-800"
            }`}>{a.status}</span>
          </div>
          {a.reviewer ? <p className="mt-1 text-xs text-neutral-500">by {a.reviewer} on {a.decidedAt}</p> : null}
        </li>
      ))}
      {items.length === 0 ? <p className="text-sm text-neutral-500">No pending approvals.</p> : null}
    </ul>
  );
}
