export function ReviewStatusBadge({ status }: { status: string }) {
  const isPending = status.toLowerCase().includes("pending");
  const isApproved = status.toLowerCase().includes("approved");
  const cls = isApproved
    ? "bg-emerald-100 text-emerald-700"
    : isPending
    ? "bg-yellow-100 text-yellow-800"
    : "bg-neutral-100 text-neutral-700";
  return <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${cls}`}>{status}</span>;
}
